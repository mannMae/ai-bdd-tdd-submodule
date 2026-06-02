# 📖 프론트엔드 코드 폼 사전 (Frontend Code Form Dictionary)

이 문서는 프론트엔드 프로젝트에서 허용되는 표준 아키텍처 및 공통 보일러플레이트 구조를 관리하는 사전입니다. 
*   **`.md` 사전**: 각 코드 폼의 추상화된 **코드 템플릿(뼈대 코드 블록)** 및 규약(Do's & Don'ts)을 명시합니다.
*   **`rules/exams/` 디렉토리**: 실제 프로젝트 구조를 모방하여 작동 및 참고가 가능한 구체적인 **예시 코드(Example Code)**를 물리 파일로 보관합니다.

---

## 🖥️ 프론트엔드 코드 폼 (Frontend Code Forms)

### 1) [FE-01] API Query Hook (React Query)
- **목적**: GET 요청을 처리하고, 서버 데이터를 조회/캐싱하기 위한 Custom Hook입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/api/get-{domain}.ts`
- **구조 예시 파일**: [rules/exams/apps/frontend/src/features/users/api/get-user.ts](file:///rules/exams/apps/frontend/src/features/users/api/get-user.ts)
- **추상 코드 템플릿 (Template)**:
```typescript
import { useQuery, queryOptions } from '@tanstack/react-query';
import { z } from 'zod';
import { api } from '@/lib/api-client';

// 1. Input/Response Schema & Type
export const userResponseSchema = z.object({
  id: z.string(),
  name: z.string(),
});
export type UserResponse = z.infer<typeof userResponseSchema>;

// 2. Fetcher Function
export const getUser = ({ userId }: { userId: string }): Promise<UserResponse> => {
  return api.get(`/users/${userId}`);
};

// 3. Query Options Helper (Caching/Invalidation)
export const getUserQueryOptions = (userId: string) => {
  return queryOptions({
    queryKey: ['users', userId],
    queryFn: () => getUser({ userId }),
  });
};

// 4. Custom Query Hook
export const useUser = ({ userId, queryConfig }: { userId: string; queryConfig?: any }) => {
  return useQuery({
    ...getUserQueryOptions(userId),
    ...queryConfig,
  });
};
```
- **준수 사항 (Do's & Don'ts)**:
  - 반드시 Zod 스키마와 타입(`z.infer`) 정의가 상단에 위치해야 합니다.
  - TanStack Query v5의 `queryOptions` 표준 API를 사용하여 쿼리 키와 함수 정의를 단일화해야 합니다.

### 2) [FE-02] API Fetch/Mutation Module (fetch / react-query)
- **목적**: POST, PUT, DELETE 등 서버 상태를 변경하는 요청을 처리하며, 422 밸리데이션 에러를 커스텀 핸들링합니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/api/{action}.ts`
- **구조 예시 파일**: [rules/exams/apps/frontend/src/features/auth/api/login.ts](file:///rules/exams/apps/frontend/src/features/auth/api/login.ts)
- **추상 코드 템플릿 (Template)**:
```typescript
export interface RequestData {
  field: string;
}

export class CustomError extends Error {
  status?: number;
  validationErrors?: { field?: string };

  constructor(message: string, status?: number, validationErrors?: { field?: string }) {
    super(message);
    this.name = 'CustomError';
    this.status = status;
    this.validationErrors = validationErrors;
  }
}

export const postData = async ({ data }: { data: RequestData }): Promise<any> => {
  const response = await fetch('http://localhost:8000/api/path', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    if (response.status === 422 && Array.isArray(errorData.detail)) {
      const validationErrors: { field?: string } = {};
      errorData.detail.forEach((e: any) => {
        const field = e.loc?.[e.loc.length - 1];
        validationErrors[field as 'field'] = e.msg;
      });
      throw new CustomError('입력 항목을 확인해주세요.', response.status, validationErrors);
    }
    throw new CustomError(errorData.detail || '요청 실패', response.status);
  }
  return response.json();
};
```
- **준수 사항 (Do's & Don'ts)**:
  - 422 에러와 같은 validationError 수신 시, 각 입력 폼 필드와 연동될 수 있는 에러 맵 형태로 던져야 합니다.

### 3) [FE-03] Global Store (Zustand Store)
- **목적**: 전역 UI 상태(모달 열림 상태, 알림, 다크모드 등)를 제어하기 위한 스토어입니다.
- **물리 경로**: `apps/frontend/src/stores/{store-name}.ts` 또는 `apps/frontend/src/features/{feature}/stores/{store-name}.ts`
- **구조 예시 파일**: [rules/exams/apps/frontend/src/stores/notification.ts](file:///rules/exams/apps/frontend/src/stores/notification.ts)
- **추상 코드 템플릿 (Template)**:
```typescript
import { create } from 'zustand';

type UIState = {
  isOpen: boolean;
  open: () => void;
  close: () => void;
};

export const useUIStore = create<UIState>((set) => ({
  isOpen: false,
  open: () => set({ isOpen: true }),
  close: () => set({ isOpen: false }),
}));
```
- **준수 사항 (Do's & Don't)**:
  - 자주 바뀌는 도메인 서버 데이터를 이 스토어에 임의로 영속화하여 동기화하지 마십시오. (서버 데이터는 `FE-01` 서버 캐시로 관리)

### 4) [FE-04] Common Controlled Form Input Component
- **목적**: React Hook Form과 Zod를 결합하여 입력 유효성 검사 및 에러 상태를 표시하는 공통 입력 컴포넌트입니다.
- **물리 경로**: `apps/frontend/src/components/ui/form/{name}.tsx`
- **구조 예시 파일**: [rules/exams/apps/frontend/src/components/ui/form/InputField.tsx](file:///rules/exams/apps/frontend/src/components/ui/form/InputField.tsx)
- **추상 코드 템플릿 (Template)**:
```typescript
import React, { useState } from 'react';
import type { UseFormRegisterReturn } from 'react-hook-form';
import FormError from '../form-error/FormError';

export interface InputFieldProps {
  id?: string;
  label?: string;
  type?: string;
  registration?: Partial<UseFormRegisterReturn>;
  error?: { message?: string };
}

export const InputField: React.FC<InputFieldProps> = ({ id, label, type = 'text', registration, error }) => {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const isPassword = type === 'password';
  const inputType = isPassword && isPasswordVisible ? 'text' : type;

  return (
    <div>
      {label && <label htmlFor={id}>{label}</label>}
      <div className="relative">
        <input id={id} type={inputType} {...registration} />
        {isPassword && (
          <button type="button" onClick={() => setIsPasswordVisible(!isPasswordVisible)}>
            {isPasswordVisible ? '숨기기' : '보기'}
          </button>
        )}
        <FormError message={error?.message} />
      </div>
    </div>
  );
};
```

### 5) [FE-05] Form Container Wrapper Component
- **목적**: react-hook-form과 Zod resolver를 감싸 폼 데이터를 선언형으로 통제하는 공통 `<Form>` 래퍼 컴포넌트입니다.
- **물리 경로**: `apps/frontend/src/components/ui/form/Form.tsx`
- **구조 예시 파일**: [rules/exams/apps/frontend/src/components/ui/form/Form.tsx](file:///rules/exams/apps/frontend/src/components/ui/form/Form.tsx)
- **추상 코드 템플릿 (Template)**:
```typescript
import type { ReactNode } from 'react';
import React from 'react';
import { useForm } from 'react-hook-form';
import type { UseFormReturn, UseFormProps, FieldValues } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { ZodType } from 'zod';

type FormProps<TFormValues extends FieldValues, Schema> = {
  onSubmit: (values: TFormValues, methods: UseFormReturn<TFormValues>) => void;
  children: (methods: UseFormReturn<TFormValues>) => ReactNode;
  options?: UseFormProps<TFormValues>;
  schema: Schema;
};

export const Form = <
  Schema extends ZodType<any, any, any>,
  TFormValues extends FieldValues = any,
>({ onSubmit, children, options, schema }: FormProps<TFormValues, Schema>) => {
  const methods = useForm<TFormValues>({ ...options, resolver: zodResolver(schema) });
  return (
    <form onSubmit={methods.handleSubmit((values) => onSubmit(values, methods))}>
      {children(methods)}
    </form>
  );
};
```

### 6) [FE-06] Application Provider Wrapper (Providers)
- **목적**: QueryClient, Language Context, Notification Context 등을 최상단에서 통합 래핑하는 전역 프로바이더 양식입니다.
- **물리 경로**: `apps/frontend/src/app/provider.tsx`
- **구조 예시 파일**: [rules/exams/apps/frontend/src/app/provider.tsx](file:///rules/exams/apps/frontend/src/app/provider.tsx)
- **추상 코드 템플릿 (Template)**:
```typescript
import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export const AppProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};
```

### 7) [FE-07] App Entry & Route Config (Router)
- **목적**: react-router-dom을 사용하여 페이지 경로 분기를 선언하고 주입하는 앱 라우터 설정 파일 양식입니다.
- **물리 경로**: `apps/frontend/src/app/router.tsx`
- **구조 예시 파일**: [rules/exams/apps/frontend/src/app/router.tsx](file:///rules/exams/apps/frontend/src/app/router.tsx)
- **추상 코드 템플릿 (Template)**:
```typescript
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

export const createAppRouter = () =>
  createBrowserRouter([
    {
      path: '/path',
      element: <div>Page Component</div>,
    },
  ]);

export const AppRouter = () => {
  const router = createAppRouter();
  return <RouterProvider router={router} />;
};
```

### 8) [FE-08] Feature UI Component (피처 컴포넌트)
- **목적**: 폼 컨텍스트, API Fetch/Mutation 모듈, UI 인풋 요소들을 모아 비즈니스 가치를 완수하는 단위 도메인 피처 조립 컴포넌트입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/components/{name}.tsx`
- **구조 예시 파일**: [rules/exams/apps/frontend/src/features/auth/components/LoginForm.tsx](file:///rules/exams/apps/frontend/src/features/auth/components/LoginForm.tsx)
- **추상 코드 템플릿 (Template)**:
```typescript
import React, { useRef, useEffect } from 'react';
import { UseFormReturn } from 'react-hook-form';
import Form, { InputField } from '../../../components/ui/form';

interface FeatureProps {
  onSuccess: () => void;
}

interface FeatureInnerProps {
  methods: UseFormReturn<any>;
  onSuccess: () => void;
  onSubmitRef: React.MutableRefObject<any>;
}

// 1. Inner Component (비즈니스 상태 제어 및 UI 렌더링)
const FeatureInner: React.FC<FeatureInnerProps> = ({ methods, onSuccess, onSubmitRef }) => {
  const { register, watch, formState: { errors } } = methods;
  const fieldValue = watch('fieldName');

  const handleAction = async (data: any) => {
    // API Mutation/Fetch 호출
    onSuccess();
  };

  useEffect(() => {
    onSubmitRef.current = handleAction;
  }, [handleAction]);

  return (
    <>
      <InputField
        id="fieldName"
        registration={register('fieldName')}
        error={errors.fieldName}
      />
      <button type="submit">Submit</button>
    </>
  );
};

// 2. Outer/Container Component (Context & Schema 주입)
export const FeatureComponent: React.FC<FeatureProps> = ({ onSuccess }) => {
  const onSubmitRef = useRef<any>(null);

  return (
    <Form
      onSubmit={(values, methods) => onSubmitRef.current?.(values, methods)}
      schema={{} as any} // Zod Schema
      options={{
        defaultValues: { fieldName: '' }
      }}
    >
      {(methods) => (
        <FeatureInner methods={methods} onSuccess={onSuccess} onSubmitRef={onSubmitRef} />
      )}
    </Form>
  );
};
```
- **준수 사항 (Do's & Don'ts)**:
  - 폼 리렌더링 최적화를 위해 Context를 주입하는 **Outer(컨테이너) 컴포넌트**와 요소를 렌더링하는 **Inner(렌더러) 컴포넌트**를 명확하게 분리하여 작성해야 합니다.
  - 가상 키보드나 외부 트리거를 처리하기 위해 `onSubmitRef` 와 같은 ref 바인딩 형식을 준수해야 합니다.

---

## ⚙️ 백엔드 코드 폼 (Backend Code Forms)

### 1) [BE-01] API Router (FastAPI APIRouter)
- **목적**: API 엔드포인트를 정의하고 HTTP 응답 스펙과 Status Code를 정의하는 레이어입니다.
- **물리 경로**: `apps/backend/src/{domain}/router.py`
- **구조 예시 파일**: [rules/exams/apps/backend/src/posts/router.py](file:///rules/exams/apps/backend/src/posts/router.py)
- **추상 코드 템플릿 (Template)**:
```python
from typing import Annotated
from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from .schemas import PostResponse, PostCreate, ErrorResponse
from .dependencies import valid_owned_post, valid_active_user

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="게시글 작성",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "잘못된 요청"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "인증 실패"}
    }
)
async def create_post(
    payload: PostCreate,
    current_user: Annotated[dict, Depends(valid_active_user)]
):
    # 서비스 계층 호출
    pass
```
- **준수 사항 (Do's & Don'ts)**:
  - 의존성 주입은 legacy default-arg 형태(`Depends(...)`) 대신 `Annotated[T, Depends(...)]` 형식을 의무 사용하십시오.
  - 성공 status_code 및 주요 에러 status_code(`responses=`) 모델들을 명확히 기술해야 합니다.
  - 비동기 코루틴 연산이 불필요한 동기 I/O가 있을 경우 `async def`가 아닌 `def` 라우터로 선언하여 스레드풀로 위임하도록 설계하십시오.

### 2) [BE-02] Service / Usecase (비즈니스 로직 서비스)
- **목적**: 단일 책임을 지는 비즈니스 로직 및 Usecase를 수행하는 서비스 클래스입니다.
- **물리 경로**: `apps/backend/src/{domain}/service.py`
- **구조 예시 파일**: [rules/exams/apps/backend/src/posts/service.py](file:///rules/exams/apps/backend/src/posts/service.py)
- **추상 코드 템플릿 (Template)**:
```python
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import PostCreate
from .vo import PostVO
from .models import PostModel

class CreatePostUsecase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, payload: PostCreate, creator_id: str) -> PostModel:
        # 1. Input DTO를 무결성이 보장되는 불변 값 객체(VO)로 변환
        vo = PostVO(title=payload.title, content=payload.content)
        
        # 2. 비즈니스 규칙 처리 및 ORM 영속화
        model = PostModel(
            title=vo.title,
            content=vo.content,
            creator_id=creator_id
        )
        self.db.add(model)
        await self.db.flush()
        return model
```
- **준수 사항 (Do's & Don'ts)**:
  - 서비스 클래스는 내부 상태를 유지하지 않는 Stateless 형태로 설계하고, 외부 의존성(예: DB Session)은 생성자(`__init__`)를 통해 주입받아야 합니다.
  - 도메인 무결성을 위협하는 원시 입력 데이터는 비즈니스 가공 전에 반드시 불변 값 객체(VO)로 변환하십시오.

### 3) [BE-03] Value Object (불변 값 객체 - VO)
- **목적**: 비즈니스 도메인의 값을 캡슐화하고 데이터의 무결성 제약조건을 강제하기 위한 객체입니다.
- **물리 경로**: `apps/backend/src/{domain}/vo.py` (또는 `post_vo.py`)
- **구조 예시 파일**: [rules/exams/apps/backend/src/posts/vo.py](file:///rules/exams/apps/backend/src/posts/vo.py)
- **추상 코드 템플릿 (Template)**:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class PostVO:
    title: str
    content: str

    def __post_init__(self):
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("제목은 비어 있을 수 없습니다.")
        if len(self.title) > 100:
            raise ValueError("제목은 100자를 초과할 수 없습니다.")
```
- **준수 사항 (Do's & Don'ts)**:
  - 반드시 `@dataclass(frozen=True)` 데코레이터를 사용하여 수정 불가능한 객체로 생성해야 합니다.
  - 생성 시 무결성을 확보하기 위해 `__post_init__` 메서드를 통해 제약 조건을 엄격히 검증하여 예외를 발생시키십시오.

### 4) [BE-04] Database Session Manager (비동기 DB 세션 관리)
- **목적**: SQLAlchemy 2.0 비동기 데이터베이스 커넥션 엔진과 세션 팩토리를 관리합니다.
- **물리 경로**: `apps/backend/src/database.py`
- **구조 예시 파일**: [rules/exams/apps/backend/src/database.py](file:///rules/exams/apps/backend/src/database.py)
- **추상 코드 템플릿 (Template)**:
```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/db"

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with SessionFactory() as session:
        yield session
```
- **준수 사항 (Do's & Don'ts)**:
  - 동기 드라이버 및 `databases` 패키지를 지양하고, SQLAlchemy 2.0 `create_async_engine` 및 `async_sessionmaker` 표준을 따르십시오.
  - 커넥션 유실 방지를 위해 `pool_pre_ping=True` 옵션을 필수로 활성화해야 합니다.

### 5) [BE-05] Database ORM Model (SQLAlchemy ORM)
- **목적**: 데이터베이스 테이블 스키마에 매핑되는 선언적 데이터 모델입니다.
- **물리 경로**: `apps/backend/src/{domain}/models.py`
- **구조 예시 파일**: [rules/exams/apps/backend/src/posts/models.py](file:///rules/exams/apps/backend/src/posts/models.py)
- **추상 코드 템플릿 (Template)**:
```python
from sqlalchemy import MetaData, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

class Base(DeclarativeBase):
    metadata = metadata

class PostModel(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    creator_id: Mapped[str] = mapped_column(String, nullable=False)
```
- **준수 사항 (Do's & Don'ts)**:
  - 테이블 명칭은 `lower_case_snake` 형식의 **단수 명사**로 지정하십시오. (예: `post`, `post_like` 등)
  - 명시적이고 일관된 데이터베이스 인덱스 명명 규약을 위해 상단에 `naming_convention` 설정을 내장해야 합니다.

### 6) [BE-06] Route Dependency & Validator (FastAPI Dependencies)
- **목적**: 인가, 데이터 존재 여부 검증, 자원 획득 등 API 엔드포인트 도달 전에 실행되는 공용 검증 함수군입니다.
- **물리 경로**: `apps/backend/src/{domain}/dependencies.py`
- **구조 예시 파일**: [rules/exams/apps/backend/src/posts/dependencies.py](file:///rules/exams/apps/backend/src/posts/dependencies.py)
- **추상 코드 템플릿 (Template)**:
```python
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from .service import CreatePostUsecase # 실제 조회용 Usecase 등
from .models import PostModel

async def valid_post_id(
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> PostModel:
    # 1. DB에서 리소스 조회
    post = await db.get(PostModel, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 게시글입니다."
        )
    return post
```
- **준수 사항 (Do's & Don'ts)**:
  - 불필요한 스레드 생성을 막기 위해 non-I/O 및 비동기 작업은 최대한 `async def` dependencies로 작성해 주십시오.
  - 동일한 엔드포인트 내에서 의존성이 중복 호출되더라도, FastAPI가 한 요청 스코프 내에서 실행 결과를 캐싱하므로 잘게 쪼개진 단위 디펜던시들을 적극 체이닝하여 재사용하십시오.

### 7) [BE-07] Request/Response DTO (Pydantic Schema)
- **목적**: 입출력 데이터의 유효성 검증과 직렬화를 담당합니다.
- **물리 경로**: `apps/backend/src/{domain}/schemas.py`
- **구조 예시 파일**: [rules/exams/apps/backend/src/posts/schemas.py](file:///rules/exams/apps/backend/src/posts/schemas.py)
- **추상 코드 템플릿 (Template)**:
```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_serializer, ConfigDict

class CustomModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    @field_serializer("*", when_used="json", check_fields=False)
    def _serialize_datetimes(self, value):
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=ZoneInfo("UTC"))
            return value.strftime("%Y-%m-%dT%H:%M:%S%z")
        return value

class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)

class PostResponse(CustomModel):
    id: int
    title: str
    content: str
    creator_id: str

class ErrorResponse(BaseModel):
    detail: str
```
- **준수 사항 (Do's & Don'ts)**:
  - Pydantic v2 규칙을 적용하여 v1 API(`.dict()`, `json_encoders`) 사용을 일절 금지하며, `model_dump()`, `@field_serializer` 등을 활용해야 합니다.
  - `Field(min_length=1, default=None)`와 같이 제약조건과 디폴트값이 모순되는 선언은 금지하며, 디폴트 값을 정확히 맞추어 기입하십시오.

### 8) [BE-08] Async Integration/Unit Test (pytest + httpx)
- **목적**: 비동기 API 클라이언트를 이용하여 백엔드 비즈니스 흐름 및 에러 처리를 검증합니다.
- **물리 경로**: `apps/backend/tests/...` (예: `apps/backend/tests/unit/test_create_post.py`)
- **구조 예시 파일**: [rules/exams/apps/backend/tests/unit/test_create_post.py](file:///rules/exams/apps/backend/tests/unit/test_create_post.py)
- **추상 코드 템플릿 (Template)**:
```python
import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from src.posts.dependencies import valid_active_user

# 1. 가짜 인증 유저 의존성 오버라이드
def fake_active_user():
    return {"user_id": "test_user"}

@pytest.fixture
async def client():
    # app.dependency_overrides 오버라이딩 처리
    app.dependency_overrides[valid_active_user] = fake_active_user
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_post_endpoint(client: AsyncClient):
    payload = {"title": "테스트 제목", "content": "테스트 내용"}
    response = await client.post("/posts", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "테스트 제목"
    assert data["creator_id"] == "test_user"
  - 동기 방식의 `TestClient`는 지양하고, 반드시 `httpx.AsyncClient`와 `ASGITransport`를 사용하여 비동기적으로 호출해야 합니다.
  - 가짜 의존성을 처리할 때는 모듈 내부를 monkeypatch 하지 말고 FastAPI의 공식 `app.dependency_overrides`를 활용하여 깨끗하게 주입하십시오.

---

## 🤖 AI 모듈 코드 폼 (AI Code Forms)

### 1) [AI-01] Inbound Router (추론 API 라우터)
- **목적**: 외부 요청을 수신하여 AI 추론 Usecase를 호출하고 결과를 반환하는 진입점 레이어입니다.
- **물리 경로**: `apps/ai/src/inbound/router.py`
- **구조 예시 파일**: [rules/exams/apps/ai/src/inbound/router.py](file:///rules/exams/apps/ai/src/inbound/router.py)
- **추상 코드 템플릿 (Template)**:
```python
from fastapi import APIRouter, Depends, status
from typing import Annotated
from src.bootstrap import container
from src.types.value import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post(
    "",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="모델 추론 요청"
)
async def predict(
    payload: PredictionRequest,
    usecase = Depends(lambda: container.inference_usecase)
):
    # 비즈니스 로직 및 전처리를 배제하고 Usecase만 즉시 호출
    result = await usecase.execute(payload)
    return result
```
- **준수 사항 (Do's & Don'ts)**:
  - 라우터 내부에서는 데이터 파싱이나 모델 추론 연산을 수행하지 말고 반드시 Usecase 레이어를 호출하십시오.
  - DI 컨테이너(`bootstrap.py`)로부터 Usecase 인스턴스를 주입받아야 합니다.

### 2) [AI-02] Inference Usecase (추론 오케스트레이터)
- **목적**: Core(전/후처리) 및 Outbound(모델 추론 및 외부 API) 레이어를 조율하여 추론 연산을 오케스트레이션합니다.
- **물리 경로**: `apps/ai/src/usecases/inference.py`
- **구조 예시 파일**: [rules/exams/apps/ai/src/usecases/inference.py](file:///rules/exams/apps/ai/src/usecases/inference.py)
- **추상 코드 템플릿 (Template)**:
```python
from src.types.value import PredictionRequest, PredictionResponse
from src.core.processor import FeatureExtractor
from src.outbound.gateway import ModelGateway

class InferenceUsecase:
    def __init__(self, model_gateway: ModelGateway, extractor: FeatureExtractor):
        self.model_gateway = model_gateway
        self.extractor = extractor

    async def execute(self, request: PredictionRequest) -> PredictionResponse:
        # 1. 입력 데이터를 core 분석용 구조로 전처리
        features = self.extractor.extract_features(request.data)
        
        # 2. Outbound Gateway를 통해 실제 모델 추론 수행
        raw_prediction = await self.model_gateway.predict(features)
        
        # 3. 모델 결과 후처리 및 반환
        processed_data = self.extractor.postprocess(raw_prediction)
        return PredictionResponse(result=processed_data)
```
- **준수 사항 (Do's & Don'ts)**:
  - 데이터의 비즈니스 룰 및 산식 연산은 Usecase 내부가 아닌 Core Processor(`AI-04`)에서 수행해야 합니다.
  - 필요한 게이트웨이 및 코어 기능은 생성자 주입을 통해 전달받으십시오.

### 3) [AI-03] Stateful Workflow (상태/에이전트 제어 흐름)
- **목적**: LangGraph 등 상태 기반 제어 흐름 또는 다단계 프롬프트 체인, 인간 검증(HITL) 단계를 갖는 AI 에이전트/워크플로우 오케스트레이션입니다.
- **물리 경로**: `apps/ai/src/workflow/process.py`
- **구조 예시 파일**: [rules/exams/apps/ai/src/workflow/process.py](file:///rules/exams/apps/ai/src/workflow/process.py)
- **추상 코드 템플릿 (Template)**:
```python
from typing import TypedDict, Annotated
import operator

class WorkflowState(TypedDict):
    input_text: str
    intermediate_steps: Annotated[list, operator.add]
    final_output: str
    status: str

class AgentWorkflow:
    def __init__(self, model_gateway):
        self.model_gateway = model_gateway

    async def run(self, text: str) -> dict:
        # 1. 워크플로우 상태 컨텍스트 초기화
        state: WorkflowState = {
            "input_text": text,
            "intermediate_steps": [],
            "final_output": "",
            "status": "pending"
        }
        
        # 2. 다단계 프롬프트/LLM 추론 실행 루프 (상태 전이)
        llm_response = await self.model_gateway.call_llm(state["input_text"])
        state["intermediate_steps"].append("llm_call")
        state["final_output"] = llm_response
        state["status"] = "completed"
        return state
```
- **준수 사항 (Do's & Don'ts)**:
  - 대용량 임베딩 데이터나 파일은 워크플로우 상태(State)에 담지 마십시오. 오직 제어 정보와 산출물의 참조 ID(Artifact Ref)만 보관해야 합니다.
  - LLM 모델 호출 및 외부 데이터 획득은 반드시 Outbound Gateway(`AI-05`) 또는 Ports에 위임해야 합니다.

### 4) [AI-04] Core Processor (도메인 코어 프로세서)
- **목적**: 원시 특징(Feature) 추출, 텐서 가공, 수학적 수치 분석 및 비즈니스 룰 후처리를 담당하는 Pure Python 비즈니스 도메인 레이어입니다.
- **물리 경로**: `apps/ai/src/core/processor.py`
- **구조 예시 파일**: [rules/exams/apps/ai/src/core/processor.py](file:///rules/exams/apps/ai/src/core/processor.py)
- **추상 코드 템플릿 (Template)**:
```python
import numpy as np

class FeatureExtractor:
    def extract_features(self, raw_data: list[float]) -> np.ndarray:
        # 1. 원시 데이터 전처리 및 텐서 변환
        if not raw_data:
            raise ValueError("원시 데이터는 필수입니다.")
        return np.array(raw_data, dtype=np.float32).reshape(1, -1)

    def postprocess(self, model_output: np.ndarray) -> str:
        # 2. 비즈니스 룰 기반 후처리 및 상태 판정
        score = float(model_output[0][0])
        if score > 0.8:
            return "위험"
        elif score > 0.4:
            return "경고"
        return "정상"
```
- **준수 사항 (Do's & Don'ts)**:
  - 외부 파일 IO, 런타임 GPU 바인딩, 네트워크 SDK 임포트를 절대 금지합니다. 구조화된 기본 데이터 타입과 행렬 연산 라이브러리만 활용하십시오.
  - 이 영역은 부수 효과가 없는 순수 함수 위주로 작성하여 오프라인에서 단위 테스트가 가능하게 만드십시오.

### 5) [AI-05] Outbound Gateway (ML/LLM Gateway 어댑터)
- **목적**: 실제 ONNX/Torch 가중치 엔진을 구동하거나 외부 LLM API(OpenAI/Claude 등) 통신을 독점적으로 수행하는 어댑터 레이어입니다.
- **물리 경로**: `apps/ai/src/outbound/gateway.py`
- **구조 예시 파일**: [rules/exams/apps/ai/src/outbound/gateway.py](file:///rules/exams/apps/ai/src/outbound/gateway.py)
- **추상 코드 템플릿 (Template)**:
```python
import onnxruntime as ort
import numpy as np

class ModelGateway:
    def __init__(self, model_path: str):
        # 1. ONNX 런타임 세션 로딩
        self.session = ort.InferenceSession(model_path)

    async def predict(self, input_tensor: np.ndarray) -> np.ndarray:
        # 2. 비동기 래퍼 혹은 threadpool을 통한 실제 추론 연산
        input_name = self.session.get_inputs()[0].name
        output_name = self.session.get_outputs()[0].name
        raw_output = self.session.run([output_name], {input_name: input_tensor})
        return raw_output[0]

    async def call_llm(self, prompt: str) -> str:
        # 3. 외부 LLM API 호출 캡슐화 (예: httpx.AsyncClient 이용)
        return "LLM 응답 샘플"
```
- **준수 사항 (Do's & Don'ts)**:
  - 모든 파일 바이트 연산, 모델 바이너리 컴파일, 외부 API 전송 SDK는 이 Outbound 패키지 내부에서만 머물러야 합니다. 외부 레이어로 원시 IO 객체가 유출되어서는 안 됩니다.

### 6) [AI-06] Bootstrap & DI Container (의존성 주입)
- **목적**: 전역 환경 설정을 로드하고, 게이트웨이 및 Usecase 의존성을 단일 지점에서 조립하여 생성합니다.
- **물리 경로**: `apps/ai/src/bootstrap.py`
- **구조 예시 파일**: [rules/exams/apps/ai/src/bootstrap.py](file:///rules/exams/apps/ai/src/bootstrap.py)
- **추상 코드 템플릿 (Template)**:
```python
from src.outbound.gateway import ModelGateway
from src.core.processor import FeatureExtractor
from src.usecases.inference import InferenceUsecase

class DIContainer:
    def __init__(self):
        # 1. 가중치 모델 로딩 및 게이트웨이 어댑터 초기화 (1회만 캐싱 실행)
        self.model_gateway = ModelGateway(model_path="models/model.onnx")
        self.extractor = FeatureExtractor()
        
        # 2. Usecase 서비스에 조립 의존성 주입
        self.inference_usecase = InferenceUsecase(
            model_gateway=self.model_gateway,
            extractor=self.extractor
        )

container = DIContainer()
```
- **준수 사항 (Do's & Don'ts)**:
  - API 매 요청마다 모델 가중치를 다시 로드하는 것은 연산 병목의 원인이 되므로, 반드시 DI Container 초기화(Lifespan) 시점에 한 번만 로드하여 싱글톤 객체로 관리해야 합니다.

### 7) [AI-07] Domain Types (불변 VO 및 DTO)
- **목적**: API 경계용 Pydantic DTO(`types/boundary`)와 코어 내부 검증용 frozen dataclass VO(`types/value`)를 정의합니다.
- **물리 경로**: `apps/ai/src/types/...` (예: `apps/ai/src/types/value.py`)
- **구조 예시 파일**: [rules/exams/apps/ai/src/types/value.py](file:///rules/exams/apps/ai/src/types/value.py)
- **추상 코드 템플릿 (Template)**:
```python
from pydantic import BaseModel
from dataclasses import dataclass

# 1. types/boundary (Pydantic DTO)
class PredictionRequest(BaseModel):
    data: list[float]

class PredictionResponse(BaseModel):
    result: str

# 2. types/value (frozen dataclass VO)
@dataclass(frozen=True)
class TensorConfigVO:
    input_dim: int
    output_dim: int
```
- **준수 사항 (Do's & Don'ts)**:
  - 순환 참조(Circular Dependency) 방지를 위해 Types 모듈은 오직 순수 타입 정의로만 구성하며 타 레이어의 코드를 임포트하지 마십시오.

### 8) [AI-08] Evals & Integration Test (pytest 기반 추론 검증)
- **목적**: 모의 어댑터를 이용해 로컬 환경에서 추론 파이프라인 및 에이전트 상태 전이를 검증합니다.
- **물리 경로**: `apps/ai/tests/...` (예: `apps/ai/tests/unit/test_inference.py`)
- **구조 예시 파일**: [rules/exams/apps/ai/tests/unit/test_inference.py](file:///rules/exams/apps/ai/tests/unit/test_inference.py)
- **추상 코드 템플릿 (Template)**:
```python
import pytest
from unittest.mock import AsyncMock
import numpy as np
from src.usecases.inference import InferenceUsecase
from src.core.processor import FeatureExtractor
from src.types.value import PredictionRequest

@pytest.mark.asyncio
async def test_inference_usecase_flow():
    # 1. Outbound Gateway Mocking
    mock_gateway = AsyncMock()
    mock_gateway.predict.return_value = np.array([[0.85]], dtype=np.float32)
    
    # 2. Usecase에 주입하여 실행 검증
    extractor = FeatureExtractor()
    usecase = InferenceUsecase(model_gateway=mock_gateway, extractor=extractor)
    
    request = PredictionRequest(data=[0.1, 0.2, 0.3])
    response = await usecase.execute(request)
    
    # 3. 비즈니스 룰 및 예외 처리 단언 검증
    assert response.result == "위험"
    mock_gateway.predict.assert_called_once()
```
- **준수 사항 (Do's & Don'ts)**:
  - 테스트 코드는 외부 GPU나 유료 클라우드 LLM API 연결 없이 완벽히 격리된 상태에서 로컬 실행(Locally Testable)되어야 합니다.


