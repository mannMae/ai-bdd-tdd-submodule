---
name: api-standards
description: REST API URL 명명 규칙, HTTP 상태 코드 매핑, 표준 응답 봉투(Response Envelope) 및 에러 구조를 정의하여 일관된 API 스펙을 보장합니다.
version: 1.0.0
globs: apps/backend/src/**/router.py, apps/ai/src/**/router.py, apps/frontend/src/**/api/**/*.ts
---

# 🌐 REST API Design & Response Standardization Guidelines

이 스킬은 프론트엔드와 백엔드/AI 모듈 간의 통신 정합성을 확보하고, 통일된 API 인터페이스 스펙을 강제하기 위한 표준 가이드라인입니다.

---

## 1. 🔗 API URL 및 명명 규칙 (API Naming Conventions)

1. **소문자 및 kebab-case 사용**:
   - URL 경로에는 대문자나 snake_case를 사용하지 않으며, 오직 소문자와 하이픈(`-`)만 사용합니다.
   - *Good*: `/api/v1/patient-records`
   - *Bad*: `/api/v1/patient_records`, `/api/v1/patientRecords`
2. **복수 명사 사용**:
   - 리소스를 나타내는 엔드포인트 세그먼트는 단수형이 아닌 복수형 명사를 지정합니다.
   - *Good*: `/api/v1/posts`, `/api/v1/users`
   - *Bad*: `/api/v1/post`, `/api/v1/user`
3. **계층적 경로 표현**:
   - 하위 리소스를 조회할 때는 상위 리소스를 명시하고 계층형 구조로 결합합니다.
   - *Good*: `/api/v1/users/{user_id}/posts` (특정 사용자의 게시글 리스트 조회)
   - *Bad*: `/api/v1/get-user-posts/{user_id}` (동사형 경로 지양)

---

## 2. 📬 HTTP 상태 코드 매핑 표준 (HTTP Status Code Standards)

FastAPI 라우터(`BE-DOMAIN-ROUTER` 등)를 구현할 때 아래 HTTP Status Code 정책을 100% 준수해야 합니다.

| Status Code | FastAPI Constant | 사용 목적 및 조건 |
| :--- | :--- | :--- |
| **`200 OK`** | `status.HTTP_200_OK` | 조회(GET) 및 기존 자원의 성공적인 변경(PUT, PATCH) 요청 완료 시 반환 |
| **`201 Created`** | `status.HTTP_201_CREATED` | 신규 자원 생성(POST) 완료 시 반환 |
| **`204 No Content`** | `status.HTTP_204_NO_CONTENT` | 요청은 성공했으나 응답 바디에 반환할 데이터가 없는 경우(DELETE) 반환 |
| **`400 Bad Request`** | `status.HTTP_400_BAD_REQUEST` | 클라이언트의 요청 파라미터 유실, 포맷 오류 등 일반적인 클라이언트 요청 실패 시 반환 |
| **`401 Unauthorized`** | `status.HTTP_401_UNAUTHORIZED` | 인증 자격 증명이 유실되었거나 유효하지 않은 경우 반환 |
| **`403 Forbidden`** | `status.HTTP_403_FORBIDDEN` | 인증은 성공했으나 해당 자원에 접근할 수 있는 권한이 부족한 경우 반환 |
| **`404 Not Found`** | `status.HTTP_404_NOT_FOUND` | 요청한 경로가 없거나 자원(ID 매핑 데이터 등)이 존재하지 않는 경우 반환 |
| **`422 Unprocessable Entity`** | `status.HTTP_422_UNPROCESSABLE_ENTITY` | Pydantic DTO DTO 바인딩 과정에서 입력값 벨리데이션 통과 실패 시 자동/수동 반환 |
| **`500 Internal Server Error`** | `status.HTTP_500_INTERNAL_SERVER_ERROR` | 서버 내부 로직 미흡으로 인해 발생한 예외 및 예측하지 못한 장애 발생 시 반환 |

---

## 3. 📦 표준 응답 봉투 및 에러 포맷 (Standard Response Envelopes)

모든 API 응답은 구조의 예측 가능성을 위해 다음과 같이 통일된 규격을 따릅니다.

### ① 성공 응답 포맷 (Success Envelope)
데이터를 반환하는 성공 응답은 반드시 `success: true` 필드와 함께 `data` 필드 내에 본 데이터를 담아 전달합니다.
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "게시글 제목",
    "content": "게시글 본문 내용"
  }
}
```

### ② 실패/에러 응답 포맷 (Error Envelope)
실패 시에는 `success: false` 필드와 함께 표준화된 `error` 상세 객체를 담아 반환해야 하며, 비즈니스 에러 코드를 제공하여 프론트엔드가 적합한 분기 처리를 하도록 돕습니다.
```json
{
  "success": false,
  "error": {
    "code": "POST_NOT_FOUND",
    "message": "요청하신 게시글을 찾을 수 없습니다.",
    "details": {
      "post_id": 123
    }
  }
}
```
*   `code`: 프론트엔드가 다국어 처리 또는 모달 분기용으로 인식 가능한 고유의 대문자 에러 코드값.
*   `message`: 화면에 그대로 노출될 수 있는 직관적인 한글 에러 메세지.
*   `details`: 디버깅 정보 또는 밸리데이션 상세 에러 맵.
