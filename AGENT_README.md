# Antigravity AI-BDD-TDD Template (Submodule)

이 저장소는 **Google Antigravity(Gemini) 기반 AI Agent와 협업하여 BDD-TDD 방법론을 실천하기 위한 규칙 저장소**입니다.
이 저장소를 프로젝트의 Git Submodule로 연결하면, 여러 프로젝트에서 동일한 AI 협업 규칙을 일관되게 적용하고 쉽게 업데이트할 수 있습니다.

## 🚀 왜 이 템플릿을 Submodule로 쓰나요?
프로젝트마다 AI 규칙을 복사해서 붙여넣으면, 프로세스가 개선될 때마다 모든 프로젝트를 일일이 수정해야 합니다.
Git Submodule을 사용하면 중앙 레포지토리(이 저장소)에서 규칙을 한 번만 업데이트하고, 각 프로젝트에서는 `git submodule update --remote` 명령어로 최신 워크플로우를 즉시 반영할 수 있습니다.

## 🏁 서브모듈로 프로젝트에 적용하기

새 프로젝트에 이 템플릿을 서브모듈로 추가하는 방법은 다음과 같습니다:

1. **서브모듈 추가**: 프로젝트 최상단 디렉토리에서 아래 명령어를 실행하여 이 저장소를 `.agents` 폴더로 가져옵니다.
   ```bash
   git submodule add https://github.com/mannMae/ai-bdd-tdd-template.git .agents
   ```

2. **초기 진입점 및 프로젝트 맵 생성**: `AGENTS.sample.md` 및 `PROJECT_MAP.sample.md` 파일을 부모 프로젝트의 최상단(root) 경로에 복사합니다.
   ```bash
   cp .agents/AGENTS.sample.md ./AGENTS.md
   cp .agents/PROJECT_MAP.sample.md ./PROJECT_MAP.md
   ```
   *(복사한 `PROJECT_MAP.md` 파일은 해당 프로젝트의 디렉토리 구조와 기술 스택에 맞게 수정하십시오. AI 에이전트는 작업을 시작할 때 이 맵 문서를 먼저 읽고 소스 폴더를 탐색합니다.)*

3. **팀원 공유**: 다른 팀원들이 이 프로젝트를 클론할 때는 다음 명령어를 사용해야 서브모듈까지 한 번에 가져올 수 있습니다.
   ```bash
   git clone --recursive <your-project-url>
   ```
   (이미 클론한 후라면 `git submodule update --init --recursive` 실행)

## 📂 서브모듈 내부 구조 (`.agents/`)

- **`rules/`**: Antigravity가 자동으로 감지하고 로드하는 BDD-TDD 라이프사이클 및 검증 게이트 규칙들입니다.
  - **`rules/templates/`**: 하위 프로젝트별 로컬 개발 가이드레일(`AI_GUIDERAILS`) 템플릿입니다. 프론트엔드, 백엔드(FastAPI), AI 모듈용 템플릿이 있습니다.
- **`docs/`**: RTM, User Flow 등을 저장할 문서 폴더의 뼈대입니다. 부모 프로젝트에서 필요에 따라 참조하여 작성하세요.
- **`AGENT_README.md`**: 이 문서입니다.
- **`AGENTS.sample.md`**: 부모 프로젝트의 최상단에 복사해야 할 초기 진입점 샘플 파일입니다.
- **`PROJECT_MAP.sample.md`**: 부모 프로젝트 최상단에 복사해서 사용할 구조 및 테스트 명령어 정의 템플릿입니다.

## 🛠️ 프로젝트별 로컬 개발 가이드레일 (`AI_GUIDERAILS`) 주입하기

AI 에이전트가 코드를 작성할 때 프로젝트 고유의 아키텍처나 디자인 시스템 규칙을 준수하도록 유도하려면, 서브프로젝트별 가이드레일 정의가 필수적입니다.

1. **로컬 규칙 디렉토리 생성**: 부모 프로젝트 최상단에 `.agents-local/rules/` 폴더를 생성합니다.
   ```bash
   mkdir -p .agents-local/rules
   ```

2. **기술 스택에 맞는 템플릿 복사**: 사용 중인 스택에 맞는 규칙 템플릿을 복사하여 배치합니다. (필요 없는 것은 삭제하거나 제외)
   ```bash
   # 프론트엔드 규칙 주입
   cp .agents/rules/templates/06-frontend-rules.sample.md .agents-local/rules/06-frontend-rules.md
   
   # 백엔드(FastAPI) 규칙 주입
   cp .agents/rules/templates/07-backend-rules.sample.md .agents-local/rules/07-backend-rules.md
   
   # AI 모듈 서버 규칙 주입
   cp .agents/rules/templates/08-ai-module-rules.sample.md .agents-local/rules/08-ai-module-rules.md
   ```

3. **프로젝트 환경에 맞게 커스텀**: 복사한 마크다운 파일 상단의 **`glob` 필터**와 내부의 **아키텍처 규칙**을 입맛에 맞게 커스텀하여 저장합니다. AI 에이전트는 해당 경로의 코드를 수정할 때 적절한 규칙만 자동으로 로드하여 반영합니다.

## 🔄 최신 규칙으로 업데이트하기
AI 협업 프로세스가 개선되어 이 중앙 템플릿 레포지토리가 업데이트되었다면, 각 프로젝트에서는 아래 명령어로 최신 규칙을 동기화할 수 있습니다:

```bash
git submodule update --remote .agents
git add .agents
git commit -m "Update AI BDD-TDD rules to latest"
```

