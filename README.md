# Claude Code Plugins Marketplace

Claude Code plugins and portable agent skills by tunapanini.

> 이 저장소는 공개 저장소입니다. 민감정보, 내부 시스템 정보, 실제 업무 데이터,
> 개인 경로가 포함된 예시는 추가하지 마세요.

## Claude Code Marketplace

### Marketplace 추가

```text
/plugin marketplace add tunapanini/claude-code-marketplace
```

### 플러그인 설치

```text
/plugin
```

`/plugin` 화면에서 `cc-market` Marketplace를 선택하고 원하는 플러그인을
설치합니다.

## Agent Skills CLI

[`skills`](https://github.com/vercel-labs/skills) CLI를 사용하면 이 저장소의
`SKILL.md` 기반 스킬을 Claude Code와 Codex에 함께 설치할 수 있습니다.

### 설치 가능한 스킬 확인

```bash
npx skills add tunapanini/claude-code-marketplace --list
```

### 프로젝트에 설치

현재 프로젝트에서만 사용할 스킬을 설치합니다.

```bash
npx skills add tunapanini/claude-code-marketplace \
  --skill <skill-name> \
  --agent claude-code \
  --agent codex
```

### 사용자 전역에 설치

모든 프로젝트에서 사용할 스킬을 비대화식으로 설치합니다.

```bash
DISABLE_TELEMETRY=1 npx skills add tunapanini/claude-code-marketplace \
  --skill <skill-name> \
  --global \
  --agent claude-code \
  --agent codex \
  --yes
```

`skills` CLI는 기본적으로 익명 텔레메트리를 전송합니다. 전송을 원하지 않으면
예시처럼 `DISABLE_TELEMETRY=1`을 설정합니다.

### 관리 명령

```bash
npx skills list
npx skills update
npx skills remove <skill-name>
```

## Public Repository Policy

이 저장소의 모든 파일과 Git 기록은 누구나 볼 수 있다고 가정합니다. 기여하기
전에 [AGENTS.md](./AGENTS.md)의 공개 저장소 안전 지침을 확인하세요.

## License

MIT
