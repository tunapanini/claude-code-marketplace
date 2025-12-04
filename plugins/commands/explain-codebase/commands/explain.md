# /explain

코드베이스의 구조와 아키텍처를 분석하여 문서화합니다.

## Usage

```
/explain [scope]
```

## Parameters

- `scope` (optional): full, 디렉토리 경로, 파일 경로

## Output

### 프로젝트 개요
- 기술 스택
- 주요 의존성
- 프로젝트 구조

### 아키텍처
- 디렉토리 구조 설명
- 주요 모듈 관계
- 데이터 흐름

### 핵심 파일
- 진입점
- 설정 파일
- 핵심 비즈니스 로직

### 개발 가이드
- 로컬 실행 방법
- 테스트 실행 방법
- 빌드 방법

## Example

```bash
/explain
/explain src/api
/explain src/components/Button.tsx
```
