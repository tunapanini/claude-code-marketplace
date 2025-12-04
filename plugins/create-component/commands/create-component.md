# /create-component

React/Vue/Svelte 컴포넌트를 테스트와 스토리와 함께 생성합니다.

## Usage

```
/create-component <name> [framework]
```

## Parameters

- `name` (required): 컴포넌트 이름 (PascalCase)
- `framework` (optional): react, vue, svelte (자동 감지됨)

## Generated Files

### React
```
src/components/Button/
├── Button.tsx
├── Button.test.tsx
├── Button.stories.tsx
├── Button.module.css
└── index.ts
```

### Vue
```
src/components/Button/
├── Button.vue
├── Button.test.ts
├── Button.stories.ts
└── index.ts
```

## Features

- 프로젝트 구조 자동 감지
- TypeScript 지원
- 테스트 파일 생성 (Jest/Vitest)
- Storybook 스토리 생성
- CSS Modules / Tailwind 지원
- 접근성 기본 속성 포함

## Example

```bash
/create-component Button
/create-component UserCard react
/create-component Modal vue
```
