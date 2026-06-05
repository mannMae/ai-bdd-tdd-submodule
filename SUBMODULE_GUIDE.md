# 📖 Git Submodule 활용 가이드

이 저장소는 여러 프로젝트에서 공통으로 사용되는 **AI-BDD-TDD 규칙 및 Antigravity Skills**를 관리합니다. 이 문서는 이 레포지토리를 Git Submodule로 연결하여 사용하는 방법과 관리 원칙을 설명합니다.

---

## 1. 신규 프로젝트에 추가하기
새 프로젝트에서 이 규칙들을 사용하려면 최상단(Root) 디렉토리에서 아래 명령어를 실행하세요.

```bash
# 1. 서브모듈 추가 (반드시 .agents 폴더 이름으로 지정)
git submodule add https://github.com/mannMae/ai-bdd-tdd-template.git .agents

# 2. 공통 설정 파일, AI 진입점 및 Git pre-commit 훅 자동 연동 실행
.agents/scripts/install-rules.sh
```

## 2. 기존 프로젝트에서 전환하기 (Migration)
이미 `.agents` 폴더를 수동으로 만들어 사용 중인 경우, 아래 순서로 전환하세요.

```bash
# 1. 기존 폴더 백업
mv .agents .agents_backup

# 2. 기존 폴더가 Git 관리 대상이었다면 삭제
git rm -r .agents
git commit -m "Remove old .agents directory for submodule migration"

# 3. 서브모듈로 새롭게 추가
git submodule add https://github.com/mannMae/ai-bdd-tdd-template.git .agents

# 4. 공통 설정 파일, AI 진입점 및 Git pre-commit 훅 자동 연동 실행
.agents/scripts/install-rules.sh

# 5. 백업 확인 후 삭제
rm -rf .agents_backup
```

---

## 3. 규칙 업데이트 및 동기화 (Sync & Update)

### 3.1 중앙 템플릿의 최신 규칙 가져오기
중앙 저장소(이 레포지토리)에 새로운 규칙이 추가되었을 때, 개별 프로젝트에서 이를 반영하는 방법입니다.

```bash
# 1. 서브모듈 최신화
git submodule update --remote .agents

# 2. 부모 프로젝트에 변경된 이정표(Hash) 저장
git add .agents
git commit -m "Update AI rules to latest version"
git push
```

### 3.2 프로젝트에서 수정한 규칙을 중앙에 반영하기
특정 프로젝트에서 개선한 규칙을 모든 프로젝트가 공유할 수 있도록 중앙 저장소에 푸시하는 방법입니다.

```bash
# 1. 서브모듈 내부로 이동
cd .agents

# 2. 서브모듈 내부에서 커밋 및 푸시
git add .
git commit -m "Update common BDD rules"
git push origin master

# 3. 다시 부모 프로젝트로 돌아와 이정표 업데이트
cd ..
git add .agents
git commit -m "Sync submodule reference after update"
git push
```

---

## 4. 고도화 자동화 기능 가이드 (Advanced Automation Features)

본 서브모듈은 린트/포맷터 연동 외에 AI 에이전트와 개발 생산성을 향상시키는 10대 고도화 도구를 제공합니다.

### 1) PROJECT_MAP.md 자동 갱신
프로젝트 폴더 트리가 변경될 때 지도를 자동으로 최신화합니다.
```bash
python3 .agents/scripts/update-map.py
```

### 2) 커밋 메시지 컨벤션 검사 (Commit Message Linter)
Conventional Commits 규칙을 만족하는 커밋 메시지만 허용하도록 Git Hook 수준에서 차단합니다.
*   연동이 완료된 경우 `git commit` 수행 시 `.agents/scripts/commit-msg-linter.py`가 자동 실행됩니다.
*   **허용 형식**: `feat: ...`, `fix: ...`, `docs: ...`, `test: ...`, `chore: ...` 등.

### 3) AI 에이전트 루프 감지기 (Loop Detector)
테스트 실패 루프에 빠져 무한히 비용을 낭비하는 문제를 방지하기 위해 테스트 명령어를 감싸 수행합니다.
```bash
python3 .agents/scripts/test-runner-guard.py [실제 테스트 명령어]
# 예: python3 .agents/scripts/test-runner-guard.py pytest
# 예: python3 .agents/scripts/test-runner-guard.py npm test
```
*   동일 명령어가 연속 5회 실패하면 즉시 AI 에이전트를 강제 중단(Stop)시키고 피드백을 요구합니다.

### 4) 재사용 가능한 GitHub Actions CI 워크플로우
부모 프로젝트의 `.github/workflows/reusable-ci.yml` 심링크를 통해 공통 린트/테스트 CI 환경을 즉시 상속받습니다.

### 5) RTM 자가 채점표 자동 검증기
구현된 코드와 `docs/requirements/rtm_*.md` 파일의 채점 표기를 자동 매핑하고 성공 여부를 검증합니다.
```bash
python3 .agents/scripts/rtm-evaluator.py
```

### 6) BDD 시나리오 기반 테스트 뼈대 자동 생성기
`.feature` 파일을 파싱하여 프론트엔드(`*.test.tsx`) 및 백엔드(`test_*.py`) 스텝 정의 함수의 Boilerplate 코드를 자동 생성합니다.
```bash
python3 .agents/scripts/generate-test-stubs.py [feature 파일 경로] [출력 폴더 경로]
# 예: python3 .agents/scripts/generate-test-stubs.py docs/user-flow/monitoring.feature src/features/monitoring/tests
```

### 7) AI 컨텍스트 요약 도구 (Context Optimizer)
백엔드 API 엔드포인트 및 DTO 스키마, 프론트엔드 컴포넌트 목록을 한눈에 볼 수 있는 가벼운 요약 문서(`PROJECT_CONTEXT.md`)를 루트에 빌드합니다. AI의 프로젝트 파악 시 토큰 비용을 최소화합니다.
```bash
python3 .agents/scripts/summarize-project.py
```

### 8) 순환 참조 및 아키텍처 불변성 검사기 (Cycle Checker)
프로젝트 내 소스 파일들(Python 및 JS/TS)의 import 의존성을 분석하여 구조를 꼬이게 만드는 순환 의존성(Circular Dependency)을 감지하고 에러로 반환합니다.
```bash
python3 .agents/scripts/check-cycles.py
```

### 9) AI 전용 커밋 및 PR 본문 자동 작성기
현재 `git diff`의 변경된 물리 파일 목록과 RTM 채점 현황을 분석하여 권장 Conventional Commit 메시지 및 PR 본문 템플릿 마크다운 파일(`PR_DESCRIPTION.md`)을 생성합니다.
```bash
python3 .agents/scripts/prepare-commit.py
```

### 10) AI 에이전트 자가 치유 CLI (Self-Healer)
린트/포맷 룰 위반 시 `eslint --fix` 및 `ruff check --fix`를 돌려 자동 자가 수정을 수행하고, 남은 에러는 AI가 이해하기 좋은 요약 포맷으로 모아 `SELF_HEAL_REPORT.md` 문서로 생성합니다.
```bash
python3 .agents/scripts/self-heal.py
```

---

## 5. 핵심 원칙 (Core Principles)

1.  **독립된 이정표**: 부모 프로젝트를 푸시한다고 해서 서브모듈의 내용이 자동으로 중앙에 푸시되지 않습니다. 중앙 규칙을 바꾸려면 반드시 `.agents` 폴더 안에서 별도로 푸시해야 합니다.
2.  **버전 고정**: 각 프로젝트는 자신이 마지막으로 `update`한 특정 시점의 규칙 버전에 고정(Pinning)됩니다. 따라서 중앙 규칙이 바뀌어도 명시적으로 업데이트하지 않는 한 기존 프로젝트의 AI 환경은 변하지 않아 안전합니다.
3.  **개별 프로젝트 전용 규칙**: 이 서브모듈은 '공통 규칙'만 담아야 합니다. 특정 프로젝트에만 해당하는 규칙은 부모 프로젝트의 `.agents-local/` 같은 별도 폴더에 저장하고 `AGENTS.md`에서 참조하도록 구성하세요.
