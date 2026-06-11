# 🔄 ATDD-TDD 개발 프로세스 흐름도 (BDD에서 ATDD로의 전환)

이 문서는 기존의 BDD 워크플로우를 **ATDD (인수 테스트 주도 개발)** 관점으로 재정의한 개발 흐름도입니다. 추가적인 AI/LLM 자동화 파이프라인이나 외부 도구 없이, 마스터 RTM과 기존 검증 도구(`rtm-evaluator.py`)를 활용하여 인수 조건 중심의 개발을 수행합니다.

---

```mermaid
flowchart TD
    classDef req fill:#ffe0b2,stroke:#fb8c00,stroke-width:2px;
    classDef atdd fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px;
    classDef gate fill:#fff9c4,stroke:#fdd835,stroke-width:2px;
    classDef tdd fill:#e8f5e9,stroke:#43a047,stroke-width:2px;
    classDef verify fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px;

    %% 1. 인수 조건 정의 및 설계 (ATDD)
    subgraph ATDD_Phase ["1. 인수 조건 및 설계 (ATDD)"]
        RTM_Define["📊 1단계: 마스터 RTM 및 AC 정의<br>(docs/requirements/rtm_*.md)"]:::req
        User_Flow["📈 2단계: 유저플로우 시퀀스 설계<br>(docs/user-flow/*_flow.md)"]:::atdd
        BDD_Gherkin["📝 3단계: BDD 거킨 시나리오 작성<br>(features/*.feature 또는 docs/user-flow/*.feature)"]:::atdd
        Test_Stubs["⚙️ 4단계: 테스트 뼈대(Stubs) 자동 생성<br>(generate-test-stubs.py 실행)"]:::atdd
        
        RTM_Define --> User_Flow
        User_Flow --> BDD_Gherkin
        BDD_Gherkin --> Test_Stubs
    end


    %% 2. 승인 게이트
    subgraph Gate_Phase ["2. 승인 게이트 (Strict Gate)"]
        Stop_Wait["🛑 AI 에이전트 진행 중단<br>(설계 및 BDD 시나리오 검토 대기)"]:::gate
        User_Approve["👤 User: 인수 조건 및 설계 승인"]:::gate
        
        Test_Stubs --> Stop_Wait
        Stop_Wait --> User_Approve
    end

    %% 3. 코드 구현 및 리팩토링 (TDD - 5단계)
    subgraph TDD_Phase ["3. 코드 구현 및 리팩토링 (TDD - 5단계: TDD 기반 코드 구현)"]
        TDD_Red["🔴 [RED] 테스트 작성 및 실패 확인<br>(통합 및 유닛 테스트)"]:::tdd
        TDD_Green["🟢 [GREEN] 프로덕션 코드 구현<br>(최소 코드로 테스트 통과)"]:::tdd
        TDD_Refactor["🔵 [REFACTOR] 리팩토링 및 린트 수정<br>(self-heal.py 실행)"]:::tdd
        
        User_Approve --> TDD_Red
        TDD_Red --> TDD_Green
        TDD_Green --> TDD_Refactor
        TDD_Refactor -->|추가 구현 필요 시| TDD_Red
    end

    %% 4. 인수 검증 및 완료 (Verify - 6단계)
    subgraph Verify_Phase ["4. 인수 테스트 검증 및 RTM 완료 (6단계: RTM 자가 채점 및 검증)"]
        RTM_Evaluate["⚙️ RTM 자가 채점 및 검증 실행<br>(rtm-evaluator.py 실행)"]:::verify
        RTM_Update["📊 RTM 내 시나리오 상태 완료(Pass) 갱신"]:::req
        Git_Commit["💾 최종 소스코드 및 RTM 커밋"]:::verify
        
        TDD_Refactor --> RTM_Evaluate
        RTM_Evaluate --> RTM_Update
        RTM_Update --> Git_Commit
    end

```

### 💡 핵심 핵심 변화 (BDD ➔ ATDD):
1. **인수 조건(RTM)이 설계의 중심**: 단순히 Given-When-Then 행동을 묘사하는 것을 넘어, **RTM에 정의된 시나리오와 인수 조건(Acceptance Criteria)**이 개발을 주도(Driven)합니다.
2. **테스트 뼈대(Stubs)와 매핑**: BDD 시나리오를 바탕으로 생성된 테스트 코드(`.test.tsx`, `.spec.ts`, `_test.py`)가 RTM의 특정 인수 조건을 실제로 검증하는 증거(Evidence)로 연결됩니다.
3. **물리적 검증 자동화**: `rtm-evaluator.py`는 RTM 문서에 링크된 테스트 파일들이 실제로 존재하고 패스하는지 스캔하여 RTM 채점표를 완료(`Pass`) 처리합니다.
