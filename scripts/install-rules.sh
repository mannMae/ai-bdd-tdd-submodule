#!/bin/bash
# install-rules.sh
# 이 스크립트는 .agents 서브모듈의 공통 설정을 부모 프로젝트 루트에 연결하고 Git Hook을 설정합니다.

set -e

# 스크립트 파일 위치 기준 경로 계산
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SUBMODULE_DIR="$( dirname "$SCRIPT_DIR" )"
PARENT_DIR="$( dirname "$SUBMODULE_DIR" )"

echo "========================================================"
echo "   AI-BDD-TDD Submodule Rules & Configs Setup"
echo "========================================================"
echo "부모 프로젝트 루트: $PARENT_DIR"
echo "서브모듈 루트:     $SUBMODULE_DIR"
echo "--------------------------------------------------------"

cd "$PARENT_DIR"

# 1. 심링크 생성 함수 정의
link_config() {
    local source_file="$1"
    local target_link="$2"

    # 기존 타겟 검사 및 처리
    if [ -L "$target_link" ]; then
        echo "기존 심링크 제거: $target_link"
        rm "$target_link"
    elif [ -f "$target_link" ]; then
        echo "주의: 기존 파일이 $target_link 에 존재합니다. '${target_link}.backup' 으로 이름을 바꿉니다."
        mv "$target_link" "${target_link}.backup"
    fi

    # 심링크 생성
    echo "심링크 연결: $target_link -> $source_file"
    ln -s "$source_file" "$target_link"
}

# 2. 공통 설정 파일들 심링크 연결
if [ -d ".agents/configs" ]; then
    # Prettier 설정 연결
    if [ -f ".agents/configs/.prettierrc.template.json" ]; then
        link_config ".agents/configs/.prettierrc.template.json" ".prettierrc"
    fi

    # ESLint 설정 연결
    if [ -f ".agents/configs/.eslintrc.template.json" ]; then
        link_config ".agents/configs/.eslintrc.template.json" ".eslintrc.json"
    fi

    # Python Ruff 설정 연결
    if [ -f ".agents/configs/pyproject.template.toml" ]; then
        link_config ".agents/configs/pyproject.template.toml" "pyproject.toml"
    fi

    # pre-commit 설정 연결
    if [ -f ".agents/configs/.pre-commit-config.template.yaml" ]; then
        link_config ".agents/configs/.pre-commit-config.template.yaml" ".pre-commit-config.yaml"
    fi
else
    echo "에러: .agents/configs 폴더를 찾을 수 없습니다. 서브모듈 경로를 확인해 주세요."
    exit 1
fi

# 3. pre-commit hook 설치 실행
if command -v pre-commit >/dev/null 2>&1; then
    echo "Git pre-commit 훅을 설치 중..."
    pre-commit install
    echo "pre-commit 훅이 정상적으로 등록되었습니다."
else
    echo "경고: 'pre-commit' 명령어를 찾을 수 없습니다."
    echo "     파이썬 환경에서 'pip install pre-commit' 또는 macOS 환경에서 'brew install pre-commit'을 통해"
    echo "     설치한 뒤, 프로젝트 루트에서 'pre-commit install'을 직접 실행해 주세요."
fi

# 4. AGENTS.md 및 PROJECT_MAP.md 기본 복사 (존재하지 않을 경우에만)
if [ ! -f "AGENTS.md" ]; then
    echo "초기 AGENTS.md 생성..."
    cp ".agents/AGENTS.sample.md" "AGENTS.md"
fi

if [ ! -f "PROJECT_MAP.md" ]; then
    echo "초기 PROJECT_MAP.md 생성..."
    cp ".agents/PROJECT_MAP.sample.md" "PROJECT_MAP.md"
fi

echo "--------------------------------------------------------"
echo "설치가 완료되었습니다! 모든 설정이 연동되었습니다."
echo "========================================================"
