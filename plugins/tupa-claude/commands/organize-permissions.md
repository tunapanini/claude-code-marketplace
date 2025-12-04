# /organize-permissions

프로젝트의 로컬 Claude settings.json 파일을 분석하여 글로벌 설정으로 이동할 권한들을 자동으로 분류하고 추천하는 명령어입니다.

## Command Usage

```
/organize-permissions [path-to-local-settings]
```

## Description

로컬 `.claude/settings.local.json` 파일의 permissions를 분석하여:
- 안전한 읽기 전용 명령어는 `allow`로
- 위험하거나 수정이 필요한 명령어는 `ask`로
- 보안상 위험한 명령어는 `deny`로
자동 분류하여 글로벌 설정에 추가할 것을 추천합니다.

## Implementation Steps

1. **현재 설정 파일 확인**
   - 로컬 settings.local.json 읽기
   - 글로벌 ~/.claude/settings.json 읽기
   - 중복 항목 식별

2. **명령어 분석 및 분류**
   ```
   Allow (안전한 읽기 전용):
   - Bash(ls:*), Bash(cat:*), Bash(pwd:*), Bash(which:*)
   - Bash(git status:*), Bash(git log:*), Bash(git diff:*)
   - Read() 명령어들 (민감한 경로 제외)

   Ask (확인 필요):
   - Bash(git clone:*), Bash(git add:*), Bash(git commit:*)
   - Bash(npm install:*), Bash(pnpm install:*)
   - Bash(chmod:*), Bash(mv:*), Bash(cp:*)
   - Bash(./*.sh:*) - 스크립트 실행

   Deny (위험한 명령어):
   - Bash(rm -rf:*), Bash(sudo:*)
   - Bash(eval:*), Bash(exec:*)
   - Read(/etc/passwd), Read(~/.ssh/*)
   ```

3. **글로벌 설정 업데이트**
   - 기존 설정과 병합
   - 중복 제거
   - 카테고리별 정렬

## Expected Output

```
📋 로컬 설정 분석 완료

✅ Allow로 이동 추천:
- Bash(readlink:*) - 안전한 읽기 명령어
- Bash(cat:*) - 파일 내용 확인용

⚠️ Ask로 이동 추천:
- Bash(git clone:*) - 저장소 복제
- Bash(chmod:*) - 권한 변경
- Bash(./*.sh:*) - 스크립트 실행

🚫 Deny로 이동 추천:
- Read(//Users/tunapanini/**) - 너무 광범위한 접근

💡 이미 글로벌에 존재:
- Read(~/.claude/**)
- Bash(git clone:*)

글로벌 설정을 업데이트하시겠습니까?
```

## Parameters

- `path-to-local-settings` (optional): 분석할 로컬 설정 파일 경로. 기본값은 현재 디렉토리의 `.claude/settings.local.json`
