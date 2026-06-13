# 🗺️ Project Structure & Architecture Map (PROJECT_MAP.md)

이 문서는 AI 에이전트가 본 프로젝트의 물리적 디렉토리 구조, 아키텍처 패턴, 기술 스택, 그리고 테스트 및 실행 명령어를 한눈에 이해하고 일관되게 행동할 수 있도록 돕는 맵핑 메타데이터 파일입니다. 

프로젝트 셋업 시 이 파일을 **부모 프로젝트의 루트(또는 `.agents-local/PROJECT_MAP.md`)**에 복사하여 프로젝트 사양에 맞게 작성하십시오. AI 에이전트는 작업 시작 전 이 문서를 가장 먼저 탐색하여 환경 정보를 학습합니다.

---

## 1. 프로젝트 개요 & 아키텍처 (Project Overview)
- **프로젝트 명**: [예: fetal-decel]
- **레포지토리 유형**: [예: Monorepo / Multi-repo / Single Service]
- **핵심 아키텍처 패턴**: [예: Clean Architecture / DDD (Domain-Driven Design) / Feature-First / Layered Architecture]
- **설명**: [프로젝트의 간단한 목적과 구성에 대한 요약 설명]

---

## 2. 물리 디렉토리 구조 맵핑 (Directory Structure Mapping)
아래 표를 작성하여 AI 에이전트가 각 모듈(FE, BE, AI)의 실제 물리적 경로와 역할군을 올바르게 매핑하도록 지시합니다. (해당하지 않는 모듈은 `N/A` 처리 또는 행 삭제)

| 아키텍처 계층 / 역할군 | 기본 규칙 내 매핑 경로 | 이 프로젝트의 실제 물리 경로 (예시) | 비고 / 상세 설명 |
| :--- | :--- | :--- | :--- |
| **프론트엔드 루트 (FE Root)** | `apps/frontend/` | `apps/frontend/` (또는 `/`) | 프론트엔드 소스 루트 경로 |
| └ UI 컴포넌트 (Shared) | `src/components/` | `src/components/` | 공통 UI 컴포넌트 |
| └ 피처 모듈 (Features) | `src/features/` | `src/features/` | Feature-First 도메인 피처 폴더 |
| └ 상태 관리 (Store) | `src/stores/` | `src/stores/` | Zustand 등 전역 스토어 경로 |
| └ 통합/단위 테스트 | `src/**/*.test.tsx` | `src/**/*.test.tsx` | Vitest / Jest 테스트 파일 경로 |
| **백엔드 루트 (BE Root)** | `apps/backend/` | `apps/backend/` (또는 `/`) | 백엔드 소스 루트 경로 |
| └ 라우터 (Routers) | `src/{domain}/` | `src/{domain}/router.py` | API Endpoint 계층 |
| └ 비즈니스 로직 (Services) | `src/{domain}/` | `src/{domain}/service.py` | Usecase / Service 계층 |
| └ 데이터 모델 (Models) | `src/{domain}/` | `src/{domain}/models.py` | DB ORM 스키마 및 엔티티 |
| └ 통합 테스트 | `tests/integration/` | `tests/integration/` | pytest-bdd 등 API 통합 테스트 |
| └ 단위 테스트 | `tests/unit/` | `tests/unit/` | 서비스/모델 격리 단위 테스트 |
| **AI 모듈 루트 (AI Root)** | `apps/ai/` | `apps/ai/` (또는 `/`) | AI 추론 엔진 및 관련 모듈 루트 |
| └ 가중치/모델 | `models/` | `models/` | ML/DL 모델 가중치 파일 (.bin, .pth) |
| └ 추론 라우터 | `src/prediction/` | `src/prediction/router.py` | 추론 라우터 및 전처리 파이프라인 |

### 시각적 프로젝트 구조 예시 (Visual Directory Tree Example)

```text
root/
├── .gitignore
├── AGENTS.md
├── AGENTS.sample.md
├── AGENT_README.md
├── PROJECT_MAP.md
├── PROJECT_MAP.sample.md
├── SUBMODULE_GUIDE.md
├── configs/
│   ├── .eslintrc.template.json
│   ├── .pre-commit-config.template.yaml
│   ├── .prettierrc.template.json
│   ├── boundary-rules.template.json
│   ├── pyproject.template.toml
│   └── reusable-ci.template.yml
├── docs/
│   ├── ATDD_GUIDE.md
│   ├── ai-atdd-tdd-lifecycle.md
│   ├── atdd_automation_roadmap.md
│   ├── atdd_milestone_plan.md
│   ├── bdd_vs_atdd_process.md
│   ├── requirements/
│   │   ├── master_backlog.md
│   │   ├── technical_rtm_feature_template.md
│   │   └── technical_rtm_monitoring_example.md
│   └── user-flow/
│       ├── _template.feature
│       └── _template_flow.md
├── features/
├── scripts/
│   ├── bdd-dashboard.py
│   ├── check-boundaries.py
│   ├── check-cycles.py
│   ├── commit-msg-linter.py
│   ├── generate-test-stubs.py
│   ├── install-rules.sh
│   ├── mcp-server.py
│   ├── prepare-commit.py
│   ├── rtm-evaluator.py
│   ├── self-heal.py
│   ├── summarize-project.py
│   ├── test-runner-guard.py
│   └── update-map.py
├── skills/
│   ├── ai-evaluation-evals/
│   │   └── SKILL.md
│   ├── ai-inference-guardrails/
│   │   └── SKILL.md
│   ├── api-standards/
│   │   └── SKILL.md
│   ├── backlog-management/
│   │   └── SKILL.md
│   ├── bdd-workflow/
│   │   └── SKILL.md
│   ├── code-dictionary/
│   │   └── SKILL.md
│   ├── database-conventions/
│   │   └── SKILL.md
│   ├── rtm-management/
│   │   └── SKILL.md
│   └── tdd-development/
│       └── SKILL.md
└── templates/
    ├── 06-frontend-rules.sample.md
    ├── 07-backend-rules.sample.md
    └── 08-ai-module-rules.sample.md
```

---

## 3. 기술 스택 & 테스트 실행 명령어 레시피 (Tech Stack & Test Recipes)
AI 에이전트가 코드를 검증하거나 빌드할 때 직접 수행해야 할 CLI 명령어 목록을 정의합니다.

### 1) 프론트엔드 (Frontend)
- **언어/프레임워크**: [예: React 18, TypeScript, Vite, Tailwind CSS]
- **패키지 매니저**: [예: npm / yarn / pnpm / bun]
- **테스트 실행 명령어**:
  - 통합 테스트: `[예: npm run test:integration]`
  - 단위 테스트: `[예: npm run test:unit]`
  - 전체 테스트: `[예: npm run test]`
- **개발 서버 구동**: `[예: npm run dev]`

### 2) 백엔드 (Backend)
- **언어/프레임워크**: [예: Python 3.11, FastAPI, SQLAlchemy]
- **의존성/가상환경 매니저**: [예: poetry / pipenv / uv / venv]
- **테스트 실행 명령어**:
  - 통합 테스트 (BDD): `[예: poetry run pytest tests/integration]`
  - 단위 테스트: `[예: poetry run pytest tests/unit]`
  - 전체 테스트: `[예: poetry run pytest]`
- **데이터베이스 마이그레이션**:
  - 마이그레이션 생성: `[예: poetry run alembic revision --autogenerate -m "description"]`
  - 마이그레이션 적용: `[예: poetry run alembic upgrade head]`
- **개발 서버 구동**: `[예: poetry run uvicorn app.main:app --reload]`

---

## 4. 코딩 컨벤션 & 품질 도구 (Coding Conventions & Linting)
- **코드 포맷터**: [예: Prettier / Black / Ruff]
- **린터**: [예: ESLint / Ruff / Flake8]
- **유의 사항**:
  - [예: 비동기 처리 시 반드시 async/await만 사용할 것]
  - [예: 테일윈드 임의 값(`w-[250px]`) 사용은 절대 지양할 것]
  - [예: 모든 예외 응답은 HTTPException을 사용하고 전역 ExceptionHandler로 처리할 것]
