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
├── apps/
│   ├── frontend/                 # 🖥️ 프론트엔드 애플리케이션 루트 (FE Root)
│   │   └── src/
│   │       ├── app/
│   │       │   ├── router.tsx    # 라우팅 설정 파일 (FE-ROUTER)
│   │       │   └── provider.tsx  # 전역 Context / Query Provider 설정 (FE-PROVIDER)
│   │       ├── components/       # 도메인 비의존적인 공통 컴포넌트
│   │       │   └── ui/           # 버튼, 모달, 입력필드 등 (FE-SHARED-COMP)
│   │       └── features/         # 비즈니스 영역별 Bounded Context 피처 폴더
│   │           └── {feature}/    # 피처 도메인명 (예: auth, monitoring)
│   │               ├── components/ # 피처 종속적 UI 컴포넌트 (FE-FEATURE-COMP)
│   │               ├── api/      # react-query API 훅 (FE-QUERY, FE-MUTATION)
│   │               ├── stores/   # zustand 상태 관리 스토어 (FE-STORE)
│   │               ├── hooks/    # UI 제어용 커스텀 훅 (FE-HOOK)
│   │               ├── utils/    # 도메인 전용 헬퍼 함수 (FE-UTIL)
│   │               └── types/    # TS 타입/인터페이스 선언 (FE-TYPE)
│   │
│   ├── backend/                  # ⚙️ 백엔드 서비스 루트 (BE Root)
│   │   └── src/
│   │       ├── main.py           # 애플리케이션 진입점 및 Lifespan 제어
│   │       ├── config.py         # 전역/도메인 공통 설정 (BE-CONFIG)
│   │       ├── database.py       # DB 커넥션 및 Session 주입 모듈 (BE-DATABASE)
│   │       ├── shared/           # 전역 공유 모듈 (BE-SHARED-*)
│   │       │   ├── models.py     # SQLAlchemy Base 모델 선언 (BE-SHARED-MODEL)
│   │       │   └── exceptions.py # 공통 ExceptionHandler 등록 (BE-SHARED-EXCEPTION)
│   │       └── {domain}/         # 도메인별 Bounded Context 폴더 (예: auth, monitoring)
│   │           ├── router.py     # API 라우터 진입점 (BE-DOMAIN-ROUTER)
│   │           ├── service.py    # Usecase 비즈니스 로직 클래스 (BE-DOMAIN-SERVICE)
│   │           ├── vo.py         # 도메인 불변 값 객체 (BE-DOMAIN-VO)
│   │           ├── models.py     # 도메인 ORM 테이블 모델 (BE-DOMAIN-MODEL)
│   │           ├── schemas.py    # 입출력 직렬화 DTO 스키마 (BE-DOMAIN-SCHEMA)
│   │           ├── dependencies.py # API 파라미터 사전 검증 Depends (BE-DOMAIN-DEPENDENCY)
│   │           └── client.py     # 도메인 전용 외부 호출 클라이언트 (BE-DOMAIN-CLIENT)
│   │
│   └── ai-server/                # 🤖 AI 추론 모듈 루트 (AI Root)
│       ├── app.py                # FastAPI 진입점 및 lifespan DI 컨테이너 조립
│       ├── main.py               # CLI 배치/추론 명령 진입점
│       ├── artifacts/            # ONNX 가중치 파일 및 메타데이터 보관
│       └── src/
│           ├── bootstrap.py      # DI Container 및 싱글톤 팩토리 (AI-BOOTSTRAP)
│           └── {domain}/         # 도메인별 Bounded Context 폴더 (예: fhr_predictor)
│               ├── router.py     # FastAPI APIRouter 엔드포인트 (AI-DOMAIN-ROUTER)
│               ├── inference.py  # 추론 조율 오케스트레이터 (AI-DOMAIN-USECASE)
│               ├── adapter.py    # ONNX 세션 모델 구동 엔진 (AI-DOMAIN-ADAPTER)
│               ├── types.py      # DTO 및 예측 모델 입출력 타입 (AI-DOMAIN-TYPE)
│               ├── preprocessing.py # 시그널 전처리 핵심 연산 (AI-DOMAIN-CORE)
│               └── postprocessing.py # 임계값 필터링 등 후처리 연산 (AI-DOMAIN-CORE)
└── packages/                     # 모노레포 공통 패키지 (선택 사항)
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
