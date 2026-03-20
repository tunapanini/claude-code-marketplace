# /slack:daily-digest

Slack에서 특정 기간의 나의 활동을 수집/요약하여 Obsidian daily note에 저장하는 커맨드입니다.

## Usage

```
/slack:daily-digest [period]
```

## Parameters

- `period` (optional): 검색 기간. 기본값은 오늘
  - `today` (기본값): 오늘 활동
  - `yesterday`: 어제 활동
  - `this week`: 이번 주 활동
  - `YYYY-MM-DD~YYYY-MM-DD`: 날짜 범위 지정 (예: 2026-03-19~2026-03-20)

## Implementation

### 1. 기간 파싱

- `today` → 오늘 날짜 기준 `after:YYYY-MM-DD before:YYYY-MM-DD+1`
- `yesterday` → 어제 날짜 기준
- `this week` → 이번 주 월요일~오늘
- `YYYY-MM-DD~YYYY-MM-DD` → 해당 범위

### 2. Slack 메시지 검색

Slack MCP `slack_search_public_and_private` 도구를 사용하여 내 메시지를 검색합니다.

```
검색 쿼리: from:<@현재유저ID> after:YYYY-MM-DD before:YYYY-MM-DD
```

**주의사항:**
- 현재 유저 ID는 `slack_read_user_profile` 등으로 먼저 확인
- 검색 결과가 많을 경우 페이지네이션 처리

### 3. 채널별 그룹핑 및 요약

검색된 메시지를 채널별로 그룹핑한 뒤, 각 채널에서의 활동을 간결하게 요약합니다.

**규칙:**
- 원문을 그대로 복사하지 않고, 활동 내용만 요약
- PII(개인식별정보) 및 민감정보는 마스킹 처리
- 이메일 주소, 전화번호, API 키 등은 `***` 로 대체

### 4. 중복 확인

Obsidian CLI로 기존 daily note를 확인하여 동일 섹션이 이미 있는지 체크합니다.

```bash
obsidian daily:read
```

- `## Slack Activity` 또는 동일 날짜의 Slack 다이제스트 섹션이 이미 존재하면 중복 추가하지 않음
- 이미 존재할 경우 사용자에게 알리고 덮어쓸지 확인

### 5. Obsidian daily note에 저장

```bash
obsidian daily:append
```

## Output Format

```markdown
## 🗣️ Slack Activity (YYYY-MM-DD)

### #channel-name-1
- 프로젝트 배포 관련 논의 참여, 롤백 절차 공유
- 모니터링 대시보드 링크 공유 및 알림 설정 논의

### #channel-name-2
- 코드 리뷰 피드백 제공 (PR #234)
- API 스키마 변경사항 공유

### DM / 그룹 DM
- 1:1 미팅 일정 조율
```

## Examples

```bash
# 오늘 활동 요약 (기본값)
/slack:daily-digest

# 어제 활동 요약
/slack:daily-digest yesterday

# 이번 주 활동 요약
/slack:daily-digest this week

# 특정 날짜 범위
/slack:daily-digest 2026-03-19~2026-03-20
```

## Dependencies

- **Slack MCP**: `slack_search_public_and_private`, `slack_read_user_profile`
- **Obsidian CLI**: `obsidian daily:read`, `obsidian daily:append`

## Notes

- DM 내용은 프라이버시를 위해 상세 내용 대신 간략한 주제만 기록합니다
- 검색 결과가 없을 경우 "활동 없음"으로 기록합니다
- 봇 메시지나 자동 알림은 제외합니다
