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

## 4. 핵심 원칙 (Core Principles)

1.  **독립된 이정표**: 부모 프로젝트를 푸시한다고 해서 서브모듈의 내용이 자동으로 중앙에 푸시되지 않습니다. 중앙 규칙을 바꾸려면 반드시 `.agents` 폴더 안에서 별도로 푸시해야 합니다.
2.  **버전 고정**: 각 프로젝트는 자신이 마지막으로 `update`한 특정 시점의 규칙 버전에 고정(Pinning)됩니다. 따라서 중앙 규칙이 바뀌어도 명시적으로 업데이트하지 않는 한 기존 프로젝트의 AI 환경은 변하지 않아 안전합니다.
3.  **개별 프로젝트 전용 규칙**: 이 서브모듈은 '공통 규칙'만 담아야 합니다. 특정 프로젝트에만 해당하는 규칙은 부모 프로젝트의 `.agents-local/` 같은 별도 폴더에 저장하고 `AGENTS.md`에서 참조하도록 구성하세요.
