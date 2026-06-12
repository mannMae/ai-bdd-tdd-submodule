# 🗺️ AI-ATDD-TDD 자동화 파이프라인 구축 로드맵 및 문서 분류

이 문서는 n8n과 AI 에이전트를 결합하여 **"인간 개입 최소화형 웹앱 개발 자동화 파이프라인"**을 구축하기 위해 정의하고 완성해야 하는 모든 문서의 목록과 분류를 제공합니다.

---

## 📌 문서 전체 분류 일람표

| 대분류 | 문서명 | 주요 목적 | 위치 / 관리 주체 |
| :--- | :--- | :--- | :--- |
| **1. Submodule 표준 가이드** | `ATDD_GUIDE.md` | ATDD 개념, 6단계 실천 규칙, 용어 분리 기준 제시 | 서브모듈 `/docs` |
| | `bdd_vs_atdd_process.md` | BDD와 ATDD의 시나리오 작업 흐름 차이 설명 | 서브모듈 `/docs` |
| | `ai-atdd-tdd-lifecycle.md` | 프로세스 흐름도 (Mermaid) | 서브모듈 `/docs` |
| | `rtm_template.md` [NEW] | 마스터 RTM 마크다운 파일 표준 템플릿 | 서브모듈 `/templates` |
| | `evaluator_manual.md` [NEW] | RTM 검증 및 스텁 제너레이터 스크립트 사용 설명서 | 서브모듈 `/docs` |
| **2. n8n 워크플로우 & 프롬프트** | `n8n_workflow_blueprint.md` [NEW] | n8n 노드 배치, 트리거, 예외 처리 설계도 | 서브모듈 `/docs/n8n` |
| | `agent_prompts.md` [NEW] | n8n LLM 노드에 사용될 역할별 시스템 프롬프트 모음집 | 서브모듈 `/docs/n8n` |
| | `sut_spec_schema.md` [NEW] | 환각을 막기 위한 SUT(검증 대상) 요구사항 작성 가이드 및 JSON 스키마 | 서브모듈 `/docs/n8n` |
| | `n8n_infra_guide.md` [NEW] | n8n의 로컬 파일시스템 접근, Docker 컨테이너 실행, 웹훅 설정 가이드 | 서브모듈 `/docs/n8n` |
| **3. 기타 프로젝트 적용 문서** | `rtm_*.md` (실제 프로젝트용) | 기획 요구사항 및 물리 파일 매핑 매트릭스 | 메인 프로젝트 `/docs` |
| | `github_issue_templates` [NEW] | n8n이 자동 발행할 GitHub Issue/PR 템플릿 (Markdown) | 메인 프로젝트 `.github/` |
| | `local_llm_setup.md` [NEW] | Ollama/vLLM 기반 로컬 코딩 모델(Qwen2.5-Coder 등) 세팅 가이드 | 메인 프로젝트 `/docs` |

---

## 1. AI-ATDD-BDD-Submodule에 해당하는 문서 (표준 & 도구 가이드)
*이 서브모듈이 다른 프로젝트들에 배포되어 공통적으로 참조할 **표준 규칙과 자동화 검증 도구용 명세서**입니다.*

*   **`ATDD_GUIDE.md` (완료/수정)**
    - 개념적 가이드라인. ATDD와 TDD의 명확한 용어 분리 규칙 및 실전 예제(로그인, 모니터링) 수록.
*   **`bdd_vs_atdd_process.md` (완료)**
    - 개발자용 작업 워크플로우 대조 문서.
*   **`ai-atdd-tdd-lifecycle.md` (완료)**
    - Mermaid 시퀀스 기반 라이프사이클 흐름도.
*   **`rtm_template.md` (작성 예정)**
    - 프로젝트 시작 시 가져다 쓸 RTM 마크다운 테이블 구조 표준 서식.
    - 기획, FE 컴포넌트, BE 라우터, DB 스키마, 테스트 스텁, 상태 컬럼을 표준화된 양식으로 제공.
*   **`evaluator_manual.md` (작성 예정)**
    - `rtm-evaluator.py`(RTM 자가 채점기)와 `generate-test-stubs.py`(테스트 뼈대 생성기)의 동작 방식, 인수 옵션, 에러 코드 정의 문서.

---

## 2. n8n에 제공 또는 워크플로우 작성 과정에 필요한 문서 (자동화 인프라 & 프롬프트)
*n8n 워크플로우를 설계할 때 참조하거나, n8n 내부 LLM 노드에 **직접 컨텍스트로 제공할 기계적 규칙 및 프롬프트 정의서**입니다.*

*   **`n8n_workflow_blueprint.md` (작성 예정)**
    - Git Commit 웹훅 ➡️ RTM 감지 ➡️ LLM 노드 호출 ➡️ Docker 테스트 실행 ➡️ GitHub API 호출로 이어지는 n8n 노드들의 배치도와 분기 설계서.
*   **`agent_prompts.md` (작성 예정)**
    - **RTM 생성 에이전트 프롬프트**: 비정형 텍스트 ➡️ RTM 테이블 변환 프롬프트.
    - **UserFlow/BDD 생성 에이전트 프롬프트**: RTM ➡️ Mermaid 및 거킨 파일 변환 프롬프트.
    - **TDD 구현 에이전트 프롬프트**: 테스트 stub + SUT 명세 ➡️ 프로덕션 코드 구현 프롬프트.
    - **Self-Healing 에이전트 프롬프트**: 컴파일/런타임 에러 메시지 ➡️ 버그 수정 프롬프트.
*   **`sut_spec_schema.md` (작성 예정)**
    - AI가 환각을 일으키지 않도록 SUT(검증 대상 모듈)의 Input/Output 타입, 의존성 모의(Mocking) 규칙을 명시하기 위한 가이드와 JSON 포맷 정의서.
*   **`n8n_infra_guide.md` (작성 예정)**
    - n8n 서버가 로컬 프로젝트 디렉토리에 접근해 파일을 읽고 쓰고, 격리된 Docker 컨테이너에서 테스트를 안전하게 구동할 수 있도록 환경을 구축하는 인프라 설치 매뉴얼.

---

## 3. 그 외 문서 (실제 프로젝트 적용 및 인프라 문서)
*서브모듈 외부에서 **개별 프로젝트별로 작성하거나 인프라 단에서 준비해야 하는 소유 문서**입니다.*

*   **실제 프로젝트 요구사항 매트릭스 (`rtm_*.md`)**
    - 개발 도중 생성되는 프로젝트 고유의 피처별 RTM 파일들.
*   **`github_issue_templates` (작성 예정)**
    - n8n이 설계 단계(RTM, 유저플로우 생성 완료)가 끝난 후 GitHub에 이슈 카드를 발행할 때 채워 넣을 마크다운 포맷(인수조건 체크리스트, 매핑 파일 체크리스트 등).
*   **`local_llm_setup.md` (작성 예정)**
    - 비용 없는 자가 치유 루프를 위해 로컬 서버에 Ollama/vLLM을 올리고, Qwen2.5-Coder 또는 Llama-3-Instruct 코딩 전용 모델을 다운로드받아 API 엔드포인트를 노출하는 세팅 가이드.
