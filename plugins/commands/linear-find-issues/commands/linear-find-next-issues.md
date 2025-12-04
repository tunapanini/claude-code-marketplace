# /linear:find-next-issues

Linear에서 현재 프로젝트의 다음 진행할 이슈를 우선순위별로 분석하여 추천하는 커맨드입니다.

## Command Usage

```
/linear:find-next-issues [project-name]
```

## Description

현재 작업중인 프로젝트의 Linear 이슈들을 분석하여 다음에 진행해야 할 작업을 우선순위와 함께 추천합니다.

## Implementation

1. Linear MCP를 통해 프로젝트 이슈 조회
2. 상태별 필터링 (Todo, Backlog)
3. 우선순위별 정렬 (Urgent > High > Medium > Low)
4. 의존성 및 블로커 분석
5. 추천 실행 순서 제공

## Expected Output

### 🎯 높은 우선순위 (Todo 상태)
- 즉시 시작 가능한 이슈들
- 예상 소요 시간
- 이슈 요약 및 주요 작업 내용

### 🔥 긴급/중요 이슈들 (Backlog)
- Urgent/High 우선순위 이슈
- 선행 작업 의존성 분석
- 비즈니스 임팩트 평가

### 💡 추천 진행 순서
1. 우선순위 및 의존성 기반 순서
2. 각 이슈별 시작 조건 및 필요 리소스
3. 병렬 처리 가능한 작업들

## Parameters

- `project-name` (optional): 특정 프로젝트 필터링. 생략 시 현재 작업 디렉토리 기반으로 추론

## Examples

```bash
/linear:find-next-issues
/linear:find-next-issues one-move
/linear:find-next-issues moo3
```

## Integration

이 커맨드는 Linear MCP 서버를 활용하여 실시간 이슈 정보를 조회하고 분석합니다.
