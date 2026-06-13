# 📋 프로젝트 마스터 백로그 (Master Backlog)

본 문서는 프로젝트의 전체 **비즈니스 요구사항(Feature)**의 우선순위와 진척도를 한눈에 관리하고 추적하기 위한 마스터 백로그 대시보드입니다. 

개발 상황에 따라 상태(`Pending` / `WIP` / `Done`)를 업데이트하며, 각 기능의 세부 구현 검증 및 규칙 자가 채점은 연관된 **기술 RTM (Technical RTM)** 문서 링크를 통해 추적합니다.

---

## 1. 페이지 인벤토리 (Page List)

프로젝트를 구성하는 주요 화면 목록입니다.

| ID | Page Name | Description | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| P01 | 모니터링 홈 화면 | 실시간 이상 탐지 상태를 모니터링하는 메인 화면 | WIP | |
| P02 | 설정 페이지 | 모니터링 상세 및 슬라이딩 윈도우 파라미터 설정 | Pending | |

---

## 2. 요구사항 및 기능 백로그 (Feature Backlog)

| ID | Category | Feature (Requirement) | Page ID | Pri | Status | 상세 기술 검증 문서 (Technical RTM) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **F01** | 모니터링 | 실시간 설비 모니터링 시작, 종료 및 시뮬레이션 | P01 | P0 | **WIP** | 📄 [기술 RTM](technical_rtm_monitoring_example.md) |
| **F02** | 설정 | 슬라이딩 윈도우 파라미터 및 필터 세팅 변경 | P02 | P1 | **Pending** | 📄 [기술 RTM](technical_rtm_setting_template.md) *(미작성)* |

> **상태(Status) 정의:**
> - `Pending`: 작업 전 (백로그 대기)
> - `WIP`: 테스트 작성 및 구현 진행 중 (통합 테스트 Red 단계 진입 포함)
> - `Done`: 모든 테스트 Pass, 자가 채점 완료 및 커밋 완료

---

## 3. 검토 및 작업 워크플로우 (Workflow)

사용자와 개발자(AI)는 다음 순서에 따라 작업을 진행하고 검토합니다.

1. **요구사항 확인**: 작업 시작 전 이 마스터 백로그에서 대상 기능의 ID와 우선순위를 확인하고 상태를 `WIP`로 변경합니다.
2. **기술 RTM 설계**: 해당 기능의 기술 RTM 문서(`technical_rtm_{기능명}.md`)를 템플릿으로부터 복사 생성하고, 거킨 시나리오와 연계할 소스 코드 물리 구조를 매핑합니다.
3. **구현 및 채점**: [BDD-TDD 워크플로우](file:///rules/00-workflow-rules.md)를 따라 개발을 완료한 후, 기술 RTM 문서 내의 **자가 채점표(Convention Self-Grading)**를 작성하고 실제 코드 라인 링크를 증거로 남깁니다.
4. **최종 완료**: 전체 검증이 끝나면 이 마스터 백로그의 상태를 `Done`으로 변경하고 커밋합니다.
