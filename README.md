# Claude Code Plugins Marketplace

Community-driven marketplace for Claude Code plugins - commands, hooks, and agents.

## Installation

### Add Marketplace

```bash
# GitHub 저장소 추가
/plugin marketplace add tunapanini/claude-code-marketplace
```

### Install Plugin

```bash
# 마켓플레이스에서 플러그인 설치
/plugin install command-commit-and-pr@claude-code-marketplace
/plugin install hook-auto-lint@claude-code-marketplace
/plugin install agent-backend-architect@claude-code-marketplace
```

### Manage Marketplace

```bash
# 마켓플레이스 목록
/plugin marketplace list

# 메타데이터 새로고침
/plugin marketplace update claude-code-marketplace

# 마켓플레이스 제거
/plugin marketplace remove claude-code-marketplace
```

## Available Plugins

### Commands (8)

| Plugin | Description | Usage |
|--------|-------------|-------|
| `command-review-pr` | PR 코드 리뷰 | `/review-pr <number>` |
| `command-create-component` | 컴포넌트 스캐폴딩 | `/create-component <name>` |
| `command-git-conventional` | Conventional commits | `/commit` |
| `command-explain-codebase` | 코드베이스 문서화 | `/explain` |
| `command-linear-find-issues` | Linear 이슈 우선순위 분석 | `/linear:find-next-issues` |
| `command-organize-permissions` | 권한 설정 정리 | `/organize-permissions` |
| `command-commit-and-pr` | 커밋 → 테스트 → PR 생성 | `/commit-and-pr` |
| `command-commit-and-push` | 커밋 → 테스트 → 푸시 | `/commit-and-push` |

### Hooks (4)

| Plugin | Description | Event |
|--------|-------------|-------|
| `hook-auto-lint` | 파일 수정 후 자동 린트 | PostToolUse |
| `hook-auto-test` | 코드 변경 후 관련 테스트 실행 | PostToolUse |
| `hook-notify-slack` | 작업 완료 시 Slack 알림 | Stop |
| `hook-security-scan` | 위험한 bash 명령어 차단 | PreToolUse |

### Agents (4)

| Plugin | Description | Category |
|--------|-------------|----------|
| `agent-backend-architect` | 백엔드 시스템 설계 | engineering |
| `agent-frontend-architect` | 접근성, 성능 중심 UI 설계 | engineering |
| `agent-security-engineer` | 보안 취약점 분석 | quality |
| `agent-refactoring-expert` | 코드 품질 개선 및 리팩토링 | quality |

## Project Structure

```
claude-code-marketplace/
├── .claude-plugin/
│   └── marketplace.json    # 마켓플레이스 메타데이터
├── plugins/
│   ├── commands/           # 슬래시 커맨드
│   │   ├── commit-and-pr/
│   │   │   ├── plugin.json
│   │   │   └── commands/
│   │   │       └── commit-and-pr.md
│   │   └── ...
│   ├── hooks/              # 훅 플러그인
│   │   ├── auto-lint/
│   │   │   ├── plugin.json
│   │   │   └── hooks.json
│   │   └── ...
│   └── agents/             # 에이전트 페르소나
│       ├── backend-architect/
│       │   ├── plugin.json
│       │   └── agents/
│       │       └── backend-architect.md
│       └── ...
└── README.md
```

## Contributing

1. Fork this repository
2. Create plugin directory in appropriate location:
   - `plugins/commands/` - 슬래시 커맨드
   - `plugins/hooks/` - 훅 플러그인
   - `plugins/agents/` - 에이전트 페르소나
3. Add `plugin.json` with required fields
4. Submit pull request

### plugin.json Schema

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief description",
  "author": {
    "name": "Your Name",
    "url": "https://github.com/yourname"
  },
  "repository": "https://github.com/...",
  "license": "MIT",
  "keywords": ["tag1", "tag2"]
}
```

## License

MIT
