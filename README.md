# Claude Code Plugins Marketplace

Claude Code plugins - commands, hooks, and agents by tunapanini

## Installation

### Add Marketplace

```bash
# GitHub 저장소 추가
/plugin marketplace add tunapanini/claude-code-marketplace
```

### Install Plugin

```bash
/plugin  # interactive 방식으로 플러그인(마켓플레이스) 관리함
```

## Plugins

| Plugin | Description |
|--------|-------------|
| `tupa-claude` | Claude 코드베이스 분석 커맨드 |
| `tupa-etc` | 유틸리티 커맨드 (PR 리뷰, Linear 연동, Slack 다이제스트 등) |
| `tupa-frontend` | 프론트엔드 개발 커맨드 |
| `tupa-git` | Git 워크플로우 커맨드 |
| `tupa-makers` | 전문가 에이전트 |
| `tupa-quality` | 코드 품질 훅 |

### tupa-etc Commands

| Command | Description |
|---------|-------------|
| `/review-pr` | PR 종합 리뷰 |
| `/linear:find-next-issues` | Linear 이슈 우선순위 분석 및 추천 |
| `/slack:daily-digest` | Slack 활동 요약 → Obsidian daily note 저장 |

## License

MIT
