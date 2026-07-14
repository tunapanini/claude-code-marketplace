---
name: create-verified-encrypted-zip
description: 파일이나 폴더를 ZIP 또는 tar.gz로 압축하고 실제로 다시 해제하여 원본 무결성을 검증한 결과물만 남긴다. 사용자가 압축, ZIP 생성, tar.gz 생성, 암호 압축, 비밀번호 압축, 압축 해제 검증 또는 원본 비교를 요청할 때 사용한다. 형식이 없으면 암호 없는 ZIP을 기본으로 선택하고, Unix 메타데이터 보존이나 명시된 보안 요구가 있으면 상황에 맞는 형식을 질문 없이 선택한다.
---

# 검증된 압축 파일 생성

한 개의 파일 또는 폴더를 압축하고 실제 해제 결과를 원본과 비교한다. 모든 검증이 성공하기 전에는 요청한 출력 경로에 결과물을 만들지 않는다.

## 형식 선택

사용자가 형식을 지정하면 우선한다. 지정하지 않으면 다음 표를 적용하고 형식을 되묻지 않는다.

| 요구사항 | 형식 | 처리 |
|---|---|---|
| 범용 공유, 암호 사용 | `.zip` | `zip -er`로 생성하고 암호 및 무결성 검증 |
| 범용 공유, 암호 없음 | `.zip` | 일반 ZIP으로 생성하고 무결성 검증 |
| Unix 권한·심볼릭 링크 보존, 암호 없음 | `.tar.gz` | tar+gzip으로 생성하고 무결성 검증 |
| 강한 암호화 | `.7z` AES-256 | `7z` 또는 `7zz`가 필요함을 알리고 설치 여부 확인 |
| tar 계열과 강한 암호화 | `.tar.gz.gpg` | `gpg`가 필요함을 알리고 수신자도 GPG가 필요한지 확인 |

다음 순서로 자동 결정한다.

1. 형식과 암호 요구가 모두 없으면 암호 없는 `.zip`을 선택한다.
2. 사용자가 형식이나 암호 여부를 명시하면 그대로 따르고 되묻지 않는다.
3. 소스 코드, Unix 권한, 심볼릭 링크 보존이나 Linux/macOS 전달을 강조하면 암호 없는 `.tar.gz`를 선택한다.
4. 강한 암호화를 요구하면 기존 ZipCrypto를 사용하지 않는다. 7z/GPG 도구가 없으면 형식을 묻지 말고 필요한 도구와 호환성 차이를 알린다.
5. 호환성만 언급하면 `.zip`을 선택한다.

## 실행

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export VERIFIED_ARCHIVE="$CODEX_HOME/skills/create-verified-encrypted-zip/scripts/create_verified_encrypted_zip.py"
```

암호 ZIP:

```bash
python3 "$VERIFIED_ARCHIVE" "/path/to/source" --output "/path/to/result.zip" --password
```

암호 없는 ZIP:

```bash
python3 "$VERIFIED_ARCHIVE" "/path/to/source" --output "/path/to/result.zip"
```

tar.gz:

```bash
python3 "$VERIFIED_ARCHIVE" "/path/to/source" --output "/path/to/result.tar.gz"
```

`--password`를 지정한 암호 ZIP 명령만 비밀번호를 두 번 묻는다. 비밀번호를 채팅, 명령 인자, 추적 파일에 기록하지 않는다. 대화형 실행에는 TTY를 할당한다. 사용자가 이미 자신의 셸에서 `VERIFIED_ZIP_PASSWORD`를 내보낸 경우에는 그 값을 사용할 수 있지만, 값을 포함한 `export` 명령을 대신 실행하거나 출력하지 않는다.

## 검증

번들 스크립트가 다음을 모두 수행하게 한다.

1. 원본의 경로, 파일 형식, 일반 권한, 심볼릭 링크 대상, 파일 크기와 SHA-256 매니페스트를 만든다.
2. 선택한 형식으로 임시 압축 파일을 만든다.
3. 압축 도중 원본이 바뀌지 않았는지 확인한다.
4. 암호 ZIP이면 모든 파일 항목의 암호화 플래그와 잘못된 비밀번호 거부를 확인한다.
5. 임시 디렉터리에 실제로 압축 해제한다.
6. 해제 결과를 원본 매니페스트와 비교한다.
7. 모두 성공한 경우에만 결과물을 게시하고 SHA-256을 출력한다.

완료 응답에는 결과물의 절대 경로, 형식, 암호화 여부, 크기, SHA-256과 검증 결과를 적는다. 비밀번호는 되풀이하지 않는다.

## 안전 규칙

- 출력 파일이 이미 있으면 덮어쓰지 않고 다른 이름을 사용한다.
- FIFO, 소켓, 장치 파일처럼 안전하게 재현할 수 없는 항목이 있으면 실패시킨다.
- 결과물 외에 해제본, 비밀번호 파일, 검증용 임시 파일을 남기지 않는다.
- 암호 ZIP은 호환성을 위해 Info-ZIP ZipCrypto를 사용하며 강한 암호화가 아님을 구분한다.
- 검증 범위에는 내용, 경로, 형식, 일반 권한과 심볼릭 링크가 포함된다. 소유자, ACL, 확장 속성과 정밀 타임스탬프는 제외한다.

## 리소스

- `scripts/create_verified_encrypted_zip.py`: 암호 ZIP, 일반 ZIP, tar.gz의 생성·실제 해제·원본 무결성 검증을 수행한다.
