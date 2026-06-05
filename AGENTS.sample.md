# 🤖 Antigravity AI-BDD-TDD Environment

<CRITICAL_RULE>
당신은 이 프로젝트에서 코드 작성 전 반드시 BDD-TDD 워크플로우를 강제로 준수해야 하는 시스템입니다.
어떤 상황에서도 사용자의 "명시적인 승인" 없이 다음 단계로 임의로 넘어가는 것은 허용되지 않습니다.
특히 [설계/테스트 작성] 후 승인 대기 없이 [프로덕션 코드 작성]을 진행하면 AI로서의 규칙 위반 및 "시스템 실패(Critical Failure)"로 간주됩니다.
</CRITICAL_RULE>

## 1. 프로젝트 설정 및 물리 구조 동기화 (0단계 필수)
- **작업을 시작하기 전 가장 먼저 `.agents/scripts/update-map.py` 및 `.agents/scripts/summarize-project.py`를 실행**하여 최신 물리 구조 맵(`PROJECT_MAP.md`)과 요약 명세(`PROJECT_CONTEXT.md`)를 동기화 및 갱신하고 환경 정보를 학습하십시오.
- 본 프로젝트는 `.agents/skills/` 에 정의된 Antigravity Skills에 따라 BDD-TDD 절차를 100% 준수합니다.
- 코드를 변경하기 전에 항상 해당 기능의 기술 매핑 & 채점표 문서(예: `docs/requirements/rtm_{기능명}.md`)를 먼저 확인하고 채점표를 작성/갱신하세요.

## 2. 업무 진행 단계 (요약)
모든 개발은 다음 순서에 따라 작업을 진행하며, 단계 중간에 AI 에이전트는 반드시 멈춰야 합니다.

1. **유저플로우 (User Flow) 및 시나리오 (Scenario) 작성**: 요구사항 확인 후 흐름 다이어그램(`*_flow.md`) 및 거킨 시나리오(`.feature`), 기술 매핑 문서(`rtm_{기능명}.md`)를 작성합니다.
   - **스텁 생성**: 시나리오 작성이 완료되면 반드시 `.agents/scripts/generate-test-stubs.py [feature파일경로]`를 구동하여 프론트엔드 및 백엔드 테스트 뼈대 코드(stubs)를 생성하고 이를 바탕으로 테스트를 작성하십시오.
2. **아키텍처별 분기 개발 진행**:
   - **프론트엔드 (Frontend)**:
     - **통합 테스트 작성 [Red]**: 사용자 시나리오 흐름을 검증하는 UI 통합 테스트 작성(상단 주석에 협력 유닛 목록 및 각 유닛의 세부 동작 규칙 명세).
     - **유닛 테스트 작성 [Red]**: 명세된 규칙별 단위 테스트 작성.
   - **백엔드 (Backend)**:
     - **백엔드 시나리오 작성**: API 엔드포인트와 페이로드, DB 상태를 기술하는 **백엔드 시나리오 (`*_backend.feature`)** 작성.
     - **통합 테스트 작성 [Red]**: 백엔드 시나리오를 검증하는 API 통합 테스트(pytest 등) 작성(상단 주석에 협력 유닛 목록 및 동작 규칙 명세).
     - **유닛 테스트 작성 [Red]**: 명세된 규칙별 단위 테스트 작성.
3. **🛑 승인 게이트 (대기)**: 통합 및 유닛 테스트 코드 작성을 모두 완료한 후, 사용자(User)의 명시적 승인 없이 **절대 다음 프로덕션 코드 구현 단계로 진행하지 말고 턴(Turn)을 종료**해야 합니다.
4. **유닛 코드 (Unit Code / Production Code) 구현**: 단위 테스트와 매핑된 **동작 규칙에 대해서만 프로덕션 코드로 구현(Green)**하고, 최종적으로 상위 통합 테스트를 통과시킵니다.
   - **테스트 감시**: 무한 실패 루프 및 비용 낭비를 예방하기 위해 테스트 구동 시 반드시 `.agents/scripts/test-runner-guard.py [명령어]` 형식(혹은 Makefile 타겟인 `make test`)을 통해서만 테스트를 실행하십시오.
5. **자가 채점 및 커밋**: 완료 후 기술 매핑 문서의 자가 채점 진행 및 Status를 업데이트하고 변경 사항을 논리적 단위로 커밋합니다.
   - **자가 복구 & 채점**: 커밋 전 반드시 `.agents/scripts/self-heal.py`를 실행하여 린트 오류를 자동 치유하고, `.agents/scripts/rtm-evaluator.py`를 돌려 RTM 문서를 완료 상태로 최신화하십시오.
   - **PR 생성 및 커밋**: 최종 커밋 전 `.agents/scripts/prepare-commit.py`를 돌려 권장 Conventional Commit 메시지와 PR 본문을 생성한 뒤 커밋을 제출하십시오.

상세한 개발 지침과 코딩 컨벤션은 `.agents/skills/` 폴더 내의 Antigravity Skills로 정의되어 있습니다. 에이전트는 해당 태스크를 진행할 때 연관된 스킬을 자동으로 감지하고 로드하여 준수해야 합니다.

