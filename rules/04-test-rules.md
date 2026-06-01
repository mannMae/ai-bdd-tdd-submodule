---
description: 테스트 코드 작성 및 시나리오 맵핑 원칙
glob: "**/*.test.*, **/*.spec.*"
---
# 4. 테스트(Test) 작성 원칙

테스트 코드는 설계된 시나리오와 개별 유닛들의 세부 동작 규격을 코드로 검증하는 수단입니다. 모든 테스트는 엄격한 개발 흐름을 준수하며 작성되어야 합니다.

## 1) 🛑 BDD-TDD 개발 프로세스 흐름
모든 기능 및 비즈니스 로직 개발은 아래의 단방향 프로세스 흐름을 철저히 준수하여 진행합니다.
`유저플로우 (User Flow) ➔ 시나리오 (Scenario) ➔ 통합테스트 (Integration Test) ➔ 유닛테스트 (Unit Test) ➔ 유닛 코드 (Unit Code)`

---

## 2) 통합 테스트 (Integration Test) 작성 원칙
통합 테스트는 사용자 시나리오의 전체 흐름이 실제 비즈니스 가치를 충족하는지 검증합니다.

1. **시나리오 1:1 매핑**: 각 테스트 코드 블록은 시나리오 구문(`Given`, `When`, `Then`)과 1:1로 매핑되어야 하며, 검증하는 테스트 코드 바로 상단에 **시나리오 구문을 토씨 하나 틀리지 않고 그대로 주석으로 포함**해야 합니다.
2. **협력 유닛 및 규칙 명시**: 통합 테스트 파일 또는 테스트 스위트 최상단에 **(1) 해당 시나리오 수행을 위해 협력하는 개별 유닛들의 목록**과 **(2) 각 유닛이 시나리오 상에서 만족해야 하는 동작 규칙(제약 조건)**을 반드시 상세히 명시해야 합니다.

### [통합 테스트 상단 명세 예시]
```typescript
/**
 * @file core.schema.test.tsx
 * @description Zustand 기반 악보 Core 데이터 구조 정의 및 파일 로드/닫기 통합 테스트
 * 
 * [1. 통합 테스트 구동을 위해 요구되는 각 유닛별 SUT 동작 규칙 (SUT Operational Rules)]
 * 
 * 1) 글로벌 스토어: src/stores/score-store.ts (useScoreStore)
 *    1. 성공 세팅: 검증 성공 시 score 상태를 주입된 곡 데이터(title, composer, parts)로 업데이트하고, error는 null로 초기화해야 한다.
 *    2. 실패 상태 유지: 검증 실패 시 기존 score 상태를 유지해야 한다.
 *    3. 초기화: clearScore 호출 시 score와 error 상태를 모두 null로 초기화해야 한다.
 * 
 * 2) 대시보드 컴포넌트: src/features/dashboard/components/DashboardPage.tsx (DashboardPage)
 *    1. 대시보드 식별: 컴포넌트 최상위 엘리먼트는 data-testid="dashboard"를 제공해야 한다.
 *    2. 업로드 인풋: 악보를 업로드할 수 있는 파일 인풋(type="file", accept=".json")을 제공해야 한다.
 *    3. 에러 노출: 스토어의 error 상태가 존재할 때에만 에러 메시지(data-testid="score-load-error-message") 엘리먼트를 렌더링해야 한다.
 *    4. 업로드 트리거: 파일 선택 이벤트 발생 시 FileReader를 사용하여 JSON 파일을 파싱하고 스토어의 setScore를 트리거해야 한다.
 * 
 * 3) 악보 에디터 컴포넌트: src/features/editor/components/ScoreEditorPage.tsx (ScoreEditorPage)
 *    1. 에디터 식별: 컴포넌트 최상위 엘리먼트는 data-testid="score-editor"를 제공해야 한다.
 *    2. 악보 정보 렌더링: 화면에 스토어의 score 데이터 중 곡 제목(title)과 작곡가(composer)를 텍스트로 렌더링해야 한다.
 *    3. 닫기 버튼: 악보를 닫을 수 있는 버튼(data-testid="close-score-button")을 제공해야 한다.
 *    4. 닫기 트리거: 닫기 버튼 클릭 시 스토어의 clearScore 액션을 트리거해야 한다.
 * 
 * [2. 활용된 외부 라이브러리 및 도구 (Dependencies)]
 * - 상태 관리: Zustand (create) - 전역 상태 제어
 * - 스키마 검증: Zod (z) - 악보 데이터 유효성 검사
 */
```

---

## 3) 유닛 테스트 (Unit Test) 작성 원칙
단위 테스트는 통합 테스트 단계에서 도출된 개별 유닛들의 세부 규격(Specification)을 격리 검증하는 단계입니다.

1. **규칙 격리 테스트**: 단위 테스트는 이전 단계인 통합 테스트 상단 주석에 정의된 **개별 유닛의 구체적인 규칙 항목에 대해서만 테스트 케이스를 추가**하며, 규칙 문서에 없는 임의의 비즈니스 로직이나 단순 구현 세부 사항을 테스트하지 않습니다.
2. **1:1 매핑 및 출처 표기**: 테스트 케이스와 SUT 동작 규칙(Business Rules)을 1:1로 매핑하고, `test` 또는 `it` 메서드의 설명 문자열에 검증 규칙 내용을 그대로 적고, **해당 규칙이 정의된 통합 테스트 파일명을 출처로 표시(예: `(요구처: {통합테스트파일명})`)**합니다.

### [유닛 테스트 상단 명세 예시]
```typescript
/**
 * @file score-store.test.ts
 * @description Zustand 악보 상태 스토어(score-store) 단위 테스트
 * 
 * [1. 테스트 대상 유닛 (SUT)]
 * - 스토어: src/stores/score-store.ts (useScoreStore)
 *   - State: score (ScoreData | null), error (string | null)
 *   - Actions: setScore(data: unknown) => void, clearScore() => void
 * 
 * [2. 호출/의존하는 유닛 (Dependencies)]
 * - 스키마: src/stores/score-store.ts (ScoreSchema - Zod)
 * 
 * [3. SUT 동작 규칙 (Business Rules)]
 *   1. 성공 세팅: 검증 성공 시 score 상태를 주입된 곡 데이터(title, composer, parts)로 업데이트하고, error는 null로 초기화해야 한다. (요구처: core.schema.test.tsx)
 *   2. 실패 상태 유지: 검증 실패 시 기존 score 상태를 유지하고, error 필드를 "올바르지 않은 악보 파일 형식입니다"로 설정해야 한다. (요구처: core.schema.test.tsx)
 *   3. 초기화: clearScore 호출 시 score와 error 상태를 모두 null로 초기화해야 한다. (요구처: core.schema.test.tsx)
 */
```

---

## 4) 완전한 검증 및 업데이트
1. **완전한 검증**: 시나리오 및 통합 테스트 단계에서 도출된 개별 유닛 규칙들은 단 하나도 유실되지 않고 유닛 테스트로 검증되어야 합니다.
2. **동시 업데이트**: 기획/시나리오나 통합 테스트의 규칙 명세가 업데이트되면, 이에 매핑되는 모든 단위 테스트 코드와 그 내용도 즉시 동기화되어 수정되어야 합니다.

