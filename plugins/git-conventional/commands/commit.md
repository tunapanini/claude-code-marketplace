# /commit

staged 변경사항을 분석하여 Conventional Commits 형식의 커밋 메시지를 생성합니다.

## Usage

```
/commit [type]
```

## Parameters

- `type` (optional): feat, fix, docs, style, refactor, test, chore

## Commit Types

| Type | Description |
|------|-------------|
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서 변경 |
| `style` | 코드 포맷팅 (기능 변경 없음) |
| `refactor` | 리팩토링 |
| `test` | 테스트 추가/수정 |
| `chore` | 빌드, 설정 등 기타 변경 |

## Process

1. `git diff --staged` 분석
2. 변경 내용 기반 타입 추론
3. 커밋 메시지 생성
4. 사용자 확인 후 커밋

## Output Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Example

```bash
/commit
/commit feat
/commit fix
```
