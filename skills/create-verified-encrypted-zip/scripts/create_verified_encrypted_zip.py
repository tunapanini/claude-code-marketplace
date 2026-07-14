#!/usr/bin/env python3
"""Create a ZIP or tar.gz and publish it only after round-trip verification."""

from __future__ import annotations

import argparse
import getpass
import hashlib
import os
import pty
import secrets
import select
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


PASSWORD_ENV = "VERIFIED_ZIP_PASSWORD"
TRANSCRIPT_LIMIT = 64 * 1024


class VerificationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Entry:
    kind: str
    mode: Optional[int] = None
    size: Optional[int] = None
    sha256: Optional[str] = None
    link_target: Optional[str] = None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path) -> dict[str, Entry]:
    manifest: dict[str, Entry] = {}

    def visit(path: Path, relative: str) -> None:
        info = path.lstat()
        mode = stat.S_IMODE(info.st_mode) & 0o777

        if stat.S_ISLNK(info.st_mode):
            manifest[relative] = Entry("symlink", link_target=os.readlink(path))
            return
        if stat.S_ISREG(info.st_mode):
            manifest[relative] = Entry(
                "file",
                mode=mode,
                size=info.st_size,
                sha256=sha256_file(path),
            )
            return
        if stat.S_ISDIR(info.st_mode):
            manifest[relative] = Entry("directory", mode=mode)
            for child in sorted(path.iterdir(), key=lambda item: os.fsencode(item.name)):
                child_relative = child.name if relative == "." else f"{relative}/{child.name}"
                visit(child, child_relative)
            return

        raise VerificationError(f"지원하지 않는 파일 형식입니다: {path}")

    visit(root, ".")
    return manifest


def describe_manifest_difference(
    expected: dict[str, Entry], actual: dict[str, Entry]
) -> Optional[str]:
    expected_paths = set(expected)
    actual_paths = set(actual)
    missing = sorted(expected_paths - actual_paths)
    extra = sorted(actual_paths - expected_paths)
    changed = sorted(
        path for path in expected_paths & actual_paths if expected[path] != actual[path]
    )

    parts: list[str] = []
    if missing:
        parts.append(f"누락: {', '.join(repr(path) for path in missing[:5])}")
    if extra:
        parts.append(f"추가: {', '.join(repr(path) for path in extra[:5])}")
    if changed:
        parts.append(f"변경: {', '.join(repr(path) for path in changed[:5])}")
    return "; ".join(parts) if parts else None


def read_password() -> str:
    password = os.environ.pop(PASSWORD_ENV, None)
    if password is None:
        password = getpass.getpass("ZIP 비밀번호: ")
        confirmation = getpass.getpass("ZIP 비밀번호 확인: ")
        if password != confirmation:
            raise VerificationError("입력한 비밀번호가 서로 다릅니다.")

    if not password:
        raise VerificationError("빈 비밀번호는 사용할 수 없습니다.")
    if "\n" in password or "\r" in password:
        raise VerificationError("비밀번호에는 줄바꿈 문자를 사용할 수 없습니다.")
    return password


def redact(data: bytes, password_bytes: bytes) -> str:
    if password_bytes:
        data = data.replace(password_bytes, b"[REDACTED]")
    return data.decode("utf-8", errors="replace").strip()


def run_with_password(
    command: list[str],
    password: str,
    prompts: tuple[bytes, ...],
    *,
    cwd: Optional[Path] = None,
    repeat_last_prompt: bool = False,
) -> tuple[int, int, str]:
    password_bytes = password.encode(sys.getfilesystemencoding(), errors="surrogateescape")
    pid, master_fd = pty.fork()

    if pid == 0:
        environment = os.environ.copy()
        environment["LC_ALL"] = "C"
        try:
            if cwd is not None:
                os.chdir(cwd)
            os.execvpe(command[0], command, environment)
        except OSError as error:
            print(f"명령 실행 실패: {error}", file=sys.stderr)
            os._exit(127)

    transcript = bytearray()
    prompt_window = bytearray()
    prompt_index = 0
    prompts_answered = 0
    child_status: Optional[int] = None

    try:
        while child_status is None:
            readable, _, _ = select.select([master_fd], [], [], 0.25)
            if readable:
                try:
                    chunk = os.read(master_fd, 4096)
                except OSError:
                    chunk = b""

                if chunk:
                    transcript.extend(chunk)
                    if len(transcript) > TRANSCRIPT_LIMIT:
                        del transcript[:-TRANSCRIPT_LIMIT]
                    prompt_window.extend(chunk.lower())
                    if len(prompt_window) > 4096:
                        del prompt_window[:-4096]

                    if prompt_index < len(prompts):
                        expected_prompt = prompts[prompt_index].lower()
                        if expected_prompt in prompt_window:
                            os.write(master_fd, password_bytes + b"\n")
                            prompts_answered += 1
                            prompt_window.clear()
                            if prompt_index < len(prompts) - 1:
                                prompt_index += 1
                            elif not repeat_last_prompt:
                                prompt_index += 1

            waited_pid, waited_status = os.waitpid(pid, os.WNOHANG)
            if waited_pid == pid:
                child_status = waited_status

        exit_code = os.waitstatus_to_exitcode(child_status)
    finally:
        os.close(master_fd)
        if child_status is None:
            try:
                os.kill(pid, 15)
            except ProcessLookupError:
                pass
            os.waitpid(pid, 0)

    return exit_code, prompts_answered, redact(bytes(transcript), password_bytes)


def run_checked(command: list[str], *, cwd: Optional[Path] = None) -> None:
    result = subprocess.run(
        command,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stdout.strip()
        suffix = f"\n{detail}" if detail else ""
        raise VerificationError(f"명령 실행에 실패했습니다: {' '.join(command[:2])}{suffix}")


def validate_zip_encryption(archive: Path, *, encrypted: bool) -> int:
    try:
        with zipfile.ZipFile(archive) as zipped:
            entries = [entry for entry in zipped.infolist() if not entry.is_dir()]
    except (OSError, zipfile.BadZipFile) as error:
        raise VerificationError(f"생성된 ZIP을 읽을 수 없습니다: {error}") from error

    if encrypted and not entries:
        raise VerificationError("암호화할 파일 항목이 없습니다. 빈 디렉터리만 암호 ZIP으로 만들 수 없습니다.")

    mismatched = [
        entry.filename
        for entry in entries
        if bool(entry.flag_bits & 0x1) is not encrypted
    ]
    if mismatched:
        expected = "암호화" if encrypted else "비암호화"
        shown = ", ".join(repr(name) for name in mismatched[:5])
        raise VerificationError(f"{expected} 상태가 예상과 다른 ZIP 항목이 있습니다: {shown}")
    return len(entries)


def ensure_wrong_password_is_rejected(unzip: str, archive: Path, password: str) -> None:
    wrong_password = secrets.token_urlsafe(24)
    while wrong_password == password:
        wrong_password = secrets.token_urlsafe(24)

    result = subprocess.run(
        [unzip, "-t", "-P", wrong_password, str(archive)],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode == 0:
        raise VerificationError("잘못된 비밀번호로 ZIP 검증이 성공해 암호 보호를 신뢰할 수 없습니다.")


def publish_archive(archive: Path, output: Path) -> None:
    file_descriptor, staged_name = tempfile.mkstemp(
        prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
    )
    os.close(file_descriptor)
    staged = Path(staged_name)
    try:
        shutil.copyfile(archive, staged)
        staged.chmod(0o600)
        try:
            os.link(staged, output)
        except FileExistsError:
            raise VerificationError(f"출력 파일이 이미 존재합니다: {output}")
        except OSError as error:
            raise VerificationError(
                f"검증된 압축 파일을 출력 경로에 게시하지 못했습니다: {error}"
            ) from error
    finally:
        if staged.exists() or staged.is_symlink():
            staged.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ZIP 또는 tar.gz를 만들고 실제 해제 결과를 원본과 비교합니다."
    )
    parser.add_argument("source", help="압축할 파일 또는 폴더")
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="생성할 .zip, .tar.gz 또는 .tgz 파일 경로",
    )
    encryption_group = parser.add_mutually_exclusive_group()
    encryption_group.add_argument(
        "--password",
        action="store_true",
        help="ZIP을 비밀번호로 보호합니다.",
    )
    encryption_group.add_argument(
        "--no-password",
        action="store_true",
        help="이전 호출과의 호환용입니다. ZIP의 기본값은 암호 없음입니다.",
    )
    return parser.parse_args()


def detect_archive_format(output: Path) -> str:
    lower_name = output.name.lower()
    if lower_name.endswith(".tar.gz") or lower_name.endswith(".tgz"):
        return "tar.gz"
    if lower_name.endswith(".zip"):
        return "zip"
    raise VerificationError("출력 파일명은 .zip, .tar.gz 또는 .tgz로 끝나야 합니다.")


def normalize_paths(args: argparse.Namespace) -> tuple[Path, Path, str]:
    source = Path(os.path.abspath(os.path.expanduser(args.source)))
    output = Path(os.path.abspath(os.path.expanduser(args.output)))

    if not os.path.lexists(source):
        raise VerificationError(f"원본 경로가 없습니다: {source}")
    if source == Path(source.anchor):
        raise VerificationError("파일시스템 루트 전체는 압축할 수 없습니다.")
    if not output.parent.is_dir():
        raise VerificationError(f"출력 디렉터리가 없습니다: {output.parent}")
    if output.exists() or output.is_symlink():
        raise VerificationError(f"출력 파일이 이미 존재합니다: {output}")
    return source, output, detect_archive_format(output)


def create_zip(
    zip_command: str,
    archive: Path,
    source: Path,
    *,
    encrypted: bool,
    password: Optional[str],
) -> None:
    command = [zip_command, "-q", "-r"]
    if encrypted:
        command.append("-e")
    command.extend(["-y", str(archive), "--", source.name])

    if encrypted:
        if password is None:
            raise VerificationError("암호 ZIP 비밀번호가 없습니다.")
        exit_code, prompt_count, transcript = run_with_password(
            command,
            password,
            (b"Enter password:", b"Verify password:"),
            cwd=source.parent,
        )
        if exit_code != 0 or prompt_count != 2:
            detail = f"\n{transcript}" if transcript else ""
            raise VerificationError(f"zip -er 실행에 실패했습니다.{detail}")
        return

    run_checked(command, cwd=source.parent)


def extract_zip(
    unzip_command: str,
    archive: Path,
    extracted_root: Path,
    *,
    encrypted: bool,
    password: Optional[str],
) -> None:
    command = [unzip_command, "-qq", str(archive), "-d", str(extracted_root)]
    if encrypted:
        if password is None:
            raise VerificationError("암호 ZIP 비밀번호가 없습니다.")
        exit_code, prompt_count, transcript = run_with_password(
            command,
            password,
            (b"password:",),
            repeat_last_prompt=True,
        )
        if exit_code != 0 or prompt_count < 1:
            detail = f"\n{transcript}" if transcript else ""
            raise VerificationError(f"올바른 비밀번호로 압축 해제하지 못했습니다.{detail}")
        return

    run_checked(command)


def verify_extracted_source(
    source: Path,
    extracted_root: Path,
    expected_manifest: dict[str, Entry],
) -> None:
    extracted_source = extracted_root / source.name
    if not os.path.lexists(extracted_source):
        raise VerificationError("압축 해제 결과에서 최상위 원본 항목을 찾을 수 없습니다.")
    extracted_manifest = build_manifest(extracted_source)
    difference = describe_manifest_difference(expected_manifest, extracted_manifest)
    if difference:
        raise VerificationError(f"압축 해제 결과가 원본과 다릅니다: {difference}")


def main() -> int:
    args = parse_args()
    source, output, archive_format = normalize_paths(args)
    if archive_format == "tar.gz" and args.password:
        raise VerificationError("tar.gz 자체는 비밀번호를 지원하지 않습니다. 7z 또는 GPG를 사용하세요.")
    encrypted = archive_format == "zip" and args.password
    password = read_password() if encrypted else None

    zip_command = shutil.which("zip") if archive_format == "zip" else None
    unzip_command = shutil.which("unzip") if archive_format == "zip" else None
    tar_command = shutil.which("tar") if archive_format == "tar.gz" else None
    if archive_format == "zip" and (not zip_command or not unzip_command):
        raise VerificationError("ZIP을 처리하려면 zip과 unzip 명령이 모두 필요합니다.")
    if archive_format == "tar.gz" and not tar_command:
        raise VerificationError("tar.gz를 처리하려면 tar 명령이 필요합니다.")

    started_at = time.monotonic()
    print(f"원본 검사 중: {source}")
    manifest_before = build_manifest(source)

    with tempfile.TemporaryDirectory(prefix="verified-archive-") as temporary:
        temporary_root = Path(temporary)
        archive_name = "candidate.zip" if archive_format == "zip" else "candidate.tar.gz"
        archive = temporary_root / archive_name
        extracted_root = temporary_root / "extracted"
        extracted_root.mkdir()

        if archive_format == "zip":
            label = "암호 ZIP" if encrypted else "일반 ZIP"
            print(f"{label} 생성 중...")
            create_zip(
                zip_command,
                archive,
                source,
                encrypted=encrypted,
                password=password,
            )
        else:
            print("tar.gz 생성 중...")
            run_checked(
                [tar_command, "-czf", str(archive), "--", source.name],
                cwd=source.parent,
            )

        manifest_after = build_manifest(source)
        source_difference = describe_manifest_difference(manifest_before, manifest_after)
        if source_difference:
            raise VerificationError(f"압축 도중 원본이 변경되었습니다: {source_difference}")

        if archive_format == "zip":
            validate_zip_encryption(archive, encrypted=encrypted)
            if encrypted:
                ensure_wrong_password_is_rejected(unzip_command, archive, password)
            print("ZIP 임시 압축 해제 중...")
            extract_zip(
                unzip_command,
                archive,
                extracted_root,
                encrypted=encrypted,
                password=password,
            )
        else:
            run_checked([tar_command, "-tzf", str(archive)])
            print("tar.gz 임시 압축 해제 중...")
            run_checked([tar_command, "-xzf", str(archive), "-C", str(extracted_root)])

        verify_extracted_source(source, extracted_root, manifest_after)
        publish_archive(archive, output)

    archive_sha256 = sha256_file(output)
    elapsed = time.monotonic() - started_at
    encryption_label = "ZipCrypto" if encrypted else "없음"
    print("검증 완료")
    print(f"결과: {output}")
    print(f"형식: {archive_format}")
    print(f"암호화: {encryption_label}")
    print(f"크기: {output.stat().st_size} bytes")
    print(f"SHA-256: {archive_sha256}")
    print(f"검증한 원본 항목: {len(manifest_after)}개")
    print(f"소요 시간: {elapsed:.2f}초")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (VerificationError, OSError) as error:
        print(f"오류: {error}", file=sys.stderr)
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\n취소되었습니다. 결과 압축 파일은 생성하지 않았습니다.", file=sys.stderr)
        raise SystemExit(130)
