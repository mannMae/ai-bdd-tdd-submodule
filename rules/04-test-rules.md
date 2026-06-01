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
3. **데이터와 코드 구현의 상세화**: 단순히 상단 주석 명세만 달고 끝내는 것이 아니라, 해당 명세를 만족시키기 위한 **실제 테스트 코드(모킹, 렌더링, 액션 유저 플로우, Assertions 검증)의 구현체(데이터 및 동작 내용)**가 완벽히 구성되어야 합니다.

### [통합 테스트 메타데이터 템플릿 (Metadata Template)]
통합 테스트 파일 상단 주석 또는 문서로 기입하는 프레임워크 독립적인 메타데이터 설계 구조입니다. 각 프로젝트 환경의 언어/주석 규격에 맞게 변형하여 적용합니다.

```typescript
/**
 * @description {시나리오 기능명} 통합 테스트 메타데이터
 * 
 * [1. 통합 테스트 구동을 위해 요구되는 각 유닛별 SUT 동작 규칙 (SUT Operational Rules)]
 * 
 * 1) {유닛분류/명칭}: {물리 파일경로} ({심볼/클래스/함수명})
 *    - 하위 유닛 (Sub-units): {하위 구성 컴포넌트 또는 헬퍼 모듈 목록 (해당하는 경우만 기입)}
 *    - {동작규칙 1}: {구체적인 비즈니스 동작 설명 및 상태 변화 기술}
 *    - {동작규칙 2}: {구체적인 비즈니스 동작 설명 및 상태 변화 기술}
 * 
 * 2) {유닛분류/명칭}: {물리 파일경로} ({심볼/클래스/함수명})
 *    - {동작규칙 1}: {구체적인 비즈니스 동작 설명 및 상태 변화 기술}
 * 
 * [2. 활용된 외부 라이브러리 및 핵심 의존성 (Dependencies)]
 * - {라이브러리/프레임워크명}: {검증/구현 과정에서의 역할 및 목적}
 */
```

### [통합 테스트 구체적 예시 (Example)]
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

import { loadFeature, defineFeature } from 'jest-cucumber';
import { render, screen, act } from '@testing-library/react';
import App from '../App';
import { useScoreStore } from '../store/scoreStore';
import { expect, beforeEach } from 'vitest';
import * as path from 'path';

const feature = loadFeature(path.resolve(__dirname, '../../docs/user-flow/core_schema.feature'));

defineFeature(feature, (test) => {
  beforeEach(() => {
    useScoreStore.setState({ score: null, error: null });
  });

  test('새로운 악보 데이터를 스토어에 로드하면 상태가 올바르게 업데이트되어야 한다', ({ given, when, then, and }) => {
    let validScoreData: any;

    given('사용자가 업로드할 다음과 같은 단일 보표/성부 악보 데이터가 주어졌을 때:', (docString) => {
      // 큐컴버 DocString 데이터 로딩
      validScoreData = JSON.parse(docString);
    });

    when('사용자가 이 악보 데이터를 로드(setScore)할 때', () => {
      render(<App />);
      act(() => {
        useScoreStore.getState().setScore(validScoreData);
      });
    });

    then('스토어 상태의 곡 정보(곡 제목 및 작곡가)가 업로드된 데이터와 일치하도록 업데이트되어야 한다', () => {
      const state = useScoreStore.getState();
      expect(state.score?.title).toBe(validScoreData.title);
      expect(state.score?.composer).toBe(validScoreData.composer);
    });

    and('대시보드에서 악보 편집기 화면으로 전환되어야 한다', () => {
      expect(screen.getByTestId('score-editor')).toBeInTheDocument();
      expect(screen.queryByTestId('dashboard')).not.toBeInTheDocument();
    });
  });
});
```

---

## 3) 유닛 테스트 (Unit Test) 작성 원칙
단위 테스트는 통합 테스트 단계에서 도출된 개별 유닛들의 세부 규격(Specification)을 격리 검증하는 단계입니다.

1. **규칙 격리 테스트**: 단위 테스트는 이전 단계인 통합 테스트 상단 주석에 정의된 **개별 유닛의 구체적인 규칙 항목에 대해서만 테스트 케이스를 추가**하며, 규칙 문서에 없는 임의의 비즈니스 로직이나 단순 구현 세부 사항을 테스트하지 않습니다.
2. **1:1 매핑 및 출처 표기**: 테스트 케이스와 SUT 동작 규칙(Business Rules)을 1:1로 매핑하고, `test` 또는 `it` 메서드의 설명 문자열에 검증 규칙 내용을 그대로 적고, **해당 규칙이 정의된 통합 테스트 파일명을 출처로 표시(예: `(요구처: {통합테스트파일명})`)**합니다.
3. **실제 데이터와 어서션 코드로 완성**: 단위 테스트는 해당 규칙이 실제로 준수되고 있는지를 확실히 드러내기 위해 **구체적인 Mock/테스트 데이터와 세밀한 단언문(Assertions)**으로 코드가 작성되어야 합니다.

### [유닛 테스트 메타데이터 템플릿 (Metadata Template)]
개별 단위 테스트 파일 상단에 격리 대상(SUT)과 동작 규칙을 명시하는 프레임워크 독립적인 메타데이터 설계 구조입니다.

```typescript
/**
 * @description {유닛명} 단위 테스트 메타데이터
 * 
 * [1. 테스트 대상 유닛 (SUT - System Under Test)]
 * - {유닛분류}: {물리 파일경로} ({클래스/함수/훅/스토어액션 명칭})
 *   - 하위 유닛 (Sub-units): {유닛 내부에서 렌더링되거나 동작을 돕는 로컬 하위 유닛 목록 (해당하는 경우만 기입)}
 *   - State: {유닛 내부에서 관리 및 변형시키는 상태 속성 목록}
 *   - Actions/Methods: {동작 검증을 위해 외부로 제공하는 메서드 및 인터페이스}
 * 
 * [2. 호출/의존하는 유닛 (Dependencies)]
 * - {의존유닛분류}: {물리 파일경로} ({심볼명})
 * 
 * [3. SUT 동작 규칙 (Business Rules)]
 *   - {규칙 1}: {구체적인 동작 조건 및 결과 기술} (요구처: {통합테스트파일명})
 *   - {규칙 2}: {구체적인 동작 조건 및 결과 기술} (요구처: {통합테스트파일명})
 */
```

### [유닛 테스트 구체적 예시 (Example)]
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

import { describe, test, expect, beforeEach } from 'vitest';
import { useScoreStore } from '../store/scoreStore';

describe('useScoreStore', () => {
  beforeEach(() => {
    // 테스트 실행 전 스토어 상태 초기화
    useScoreStore.getState().clearScore();
  });

  test('[1] 성공 세팅: 검증 성공 시 score 상태를 주입된 곡 데이터(title, composer, parts)로 업데이트하고, error는 null로 초기화해야 한다', () => {
    const validData = {
      title: "Valid Score",
      composer: "Test Composer",
      parts: []
    };

    useScoreStore.getState().setScore(validData);
    
    const state = useScoreStore.getState();
    expect(state.score).not.toBeNull();
    expect(state.score?.title).toBe("Valid Score");
    expect(state.error).toBeNull();
  });

  test('[2] 실패 상태 유지: 검증 실패 시 기존 score 상태를 유지하고, error 필드를 "올바르지 않은 악보 파일 형식입니다"로 설정해야 한다', () => {
    const invalidData = {
      composer: "Unknown" // 필수 필드(title, parts)가 누락된 데이터
    };

    useScoreStore.getState().setScore(invalidData);

    const state = useScoreStore.getState();
    expect(state.score).toBeNull();
    expect(state.error).toBe("올바르지 않은 악보 파일 형식입니다");
  });
});
```

---

## 4) 하위 유닛(Sub-unit) 정의 및 계층 구조 관리 규칙

단일 유닛이 비대해지거나 복잡해질 때, 이를 보조하기 위해 여러 하위 유닛(Sub-unit)을 생성하여 의존 구조를 형성할 수 있습니다. AI 에이전트는 하위 유닛을 설계하고 테스트할 때 다음 규칙을 철저히 준수해야 합니다.

1. **의존성(Dependencies)과 하위 유닛(Sub-units)의 구분**:
   - **의존성**: SUT 외부의 독립된 모듈 또는 전역 리소스로서 SUT에 주입되거나 호출되는 연동 대상을 의미합니다 (예: API Client, 전역 Store, 외부 라이브러리).
   - **하위 유닛**: SUT 내부에서만 사용되고 해당 SUT의 책임을 완수하기 위해 분할/캡슐화된 하위 구성 요소나 모듈을 의미합니다 (예: Page 컴포넌트 내의 Form/Button 서브 컴포넌트, 복잡한 Service 내의 데이터 변환 유틸/헬퍼 함수).
2. **검증 방식 및 범위의 판단**:
   - **단순 결합형 하위 유닛 (재사용 불가)**: 하위 유닛이 오직 부모 SUT 내에서만 소비되고 독립적인 재사용 목적이 없다면, 별도의 개별 단위 테스트를 작성하지 않고 부모 SUT의 단위 테스트에서 함께 통합하여 검증합니다. (상위 SUT 메타데이터 주석에 `하위 유닛 (Sub-units): [유닛명]` 형태로 목록만 기입)
   - **독립 격리형 하위 유닛 (재사용 가능 / 복잡함)**: 하위 유닛이 독립적으로 재사용되거나 독자적인 비즈니스 공식이 정밀하게 설계되어 고립 검증이 필요하다면, 해당 하위 유닛을 하나의 SUT로 격리하여 독립된 단위 테스트 파일을 생성합니다. 이 경우 상위 부모 SUT의 단위 테스트에서는 해당 하위 유닛을 `Dependencies`로 분류하여 모킹(Mocking) 처리하거나 협력 계약을 확인하는 테스트를 작성합니다.
3. **동작 규칙의 하향 전파 (No Stealth Rules)**:
   - 하위 유닛을 설계하거나 코드를 분할(Refactoring)할 때, 최초 설계(통합 테스트 및 시나리오)에서 기재된 **부모 유닛의 비즈니스 동작 규칙(Business Rules)의 범위**를 넘어서는 임의의 기능이나 보이지 않는 비즈니스 로직(Stealth logic)을 하위 유닛에 임의로 구현할 수 없습니다.
   - 하위 유닛에 새로운 동작 규칙이 추가되어야 하는 경우, 프로세스를 역행하여 코드를 직접 고치는 대신 **상위 통합 테스트(및 필요시 시나리오)의 메타데이터에 먼저 규칙을 추가**한 후, 단위 테스트 ➔ 기능 구현 단계로 순차적으로 내려와야 합니다.

---

## 5) 완전한 검증 및 업데이트
1. **완전한 검증**: 시나리오 및 통합 테스트 단계에서 도출된 개별 유닛 규칙들은 단 하나도 유실되지 않고 유닛 테스트로 검증되어야 합니다.
2. **동시 업데이트**: 기획/시나리오나 통합 테스트의 규칙 명세가 업데이트되면, 이에 매핑되는 모든 단위 테스트 코드와 그 내용도 즉시 동기화되어 수정되어야 합니다.


