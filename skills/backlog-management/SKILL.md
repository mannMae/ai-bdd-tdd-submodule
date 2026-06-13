---
name: backlog-management
description: Enforces Master Backlog (master_backlog.md) management rules, task status control, and linking to technical RTM files.
version: 1.0.0
globs: "docs/requirements/master_backlog.md"
alwaysApply: false
---

# 1. 마스터 백로그 (Master Backlog) 관리 원칙

모든 프로젝트의 기능 목록과 진척 상황은 마스터 백로그(`master_backlog.md`)에서 중앙 관리하며, 다음의 원칙을 따릅니다.

## 1) 설계 및 구성 원칙
1. **전체 로드맵 가시성 확보**: 프로젝트의 모든 페이지 인벤토리(Page List)와 비즈니스 요구사항 목록(Feature Backlog)을 하나의 마크다운 문서 내 테이블로 구성하여 전체 진행 흐름을 한눈에 파악할 수 있도록 설계합니다.
2. **이원화 연계 링크**: 백로그 테이블의 각 기능(Feature) 행의 끝에는 연관된 기능별 **기술 RTM 문서(`technical_rtm_{기능명}.md`)**로 바로 이동할 수 있는 마크다운 파일 링크를 반드시 등록하여, 기획 요구사항과 물리 코드 구현 매핑 문서 간의 이동 편의성을 보장합니다.

## 2) 운영 및 상태(Status) 제어 원칙
개발 진행 단계에 따라 기능의 상태(Status) 필드를 다음과 같이 명확히 통제합니다.
1. **`Pending` (대기)**: 구현 계획은 있으나 개발 작업이 아직 시작되지 않은 상태입니다.
2. **`WIP` (진행 중)**: 해당 요구사항의 개발이 시작된 상태입니다. BDD-TDD 라이프사이클에 따라 유저플로우/시나리오 작성 및 **통합 테스트 [Red] 단계**에 진입하는 즉시 상태를 `WIP`로 전환해야 합니다.
3. **`Done` (완료)**: 해당 요구사항의 모든 테스트가 Pass되고, 기능별 기술 RTM 내의 **자가 채점표(Convention Self-Grading)**가 모두 체크 통과 상태(`Pass`)로 검증 완료되었을 때만 마스터 백로그의 상태를 `Done`으로 업데이트합니다.

## 3) 갱신 및 커밋 규칙
* 기능 구현 완료 시점에는 기술 RTM 자가 채점 완료와 마스터 백로그의 상태 `Done` 업데이트가 반드시 완료되어야 하며, 변경된 문서들과 소스 코드는 하나의 논리적 단위 커밋으로 묶여 커밋되어야 합니다.
