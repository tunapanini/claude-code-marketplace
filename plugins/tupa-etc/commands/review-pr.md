# /review-pr

Pull Request를 종합적으로 리뷰하는 커맨드입니다.

## Usage

```
/review-pr <pr_number> [focus]
```

## Parameters

- `pr_number` (required): 리뷰할 PR 번호
- `focus` (optional): 집중 영역 - security, performance, style, all (기본값: all)

## Review Process

### 1. PR 정보 수집
- PR diff 확인
- 변경된 파일 목록
- 커밋 히스토리

### 2. 코드 품질 검토
- 코드 스타일 및 컨벤션
- 잠재적 버그
- 성능 이슈
- 보안 취약점

### 3. 리뷰 결과 출력
```
## 📋 PR Review: #123

### ✅ 좋은 점
- 명확한 함수 네이밍
- 적절한 에러 핸들링

### ⚠️ 개선 필요
- src/utils.ts:45 - 잠재적 null 참조
- src/api.ts:102 - SQL 인젝션 가능성

### 💡 제안사항
- 테스트 커버리지 추가 권장
- 타입 정의 분리 고려

### 📊 요약
- 변경 파일: 5개
- 추가: +234줄
- 삭제: -56줄
- 리스크 레벨: Medium
```

## Focus Areas

- **security**: OWASP Top 10, 인증/인가, 데이터 검증
- **performance**: N+1 쿼리, 불필요한 렌더링, 메모리 누수
- **style**: 네이밍 컨벤션, 코드 구조, 주석
- **all**: 모든 영역 종합 리뷰
