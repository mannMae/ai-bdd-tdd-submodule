---
name: code-dictionary
description: 프로젝트 코드에서 변수명, 클래스명, API 경로, DB 필드명 등을 작성할 때 공통 용어 사전 및 약어 사전을 참고하여 일관성을 맞추기 위해 사용합니다.
version: 1.0.0
---

# 📐 아키텍처 컴포넌트 및 테스트 유닛 분할 기준 (Component & Unit Division Criteria)

개발 중 새로운 코드 파일(SUT)을 생성하거나 기존 코드를 리팩토링하여 분할할 때, 아래의 명확한 아키텍처적/테스트적 기준을 준수해야 합니다. 임의의 기준으로 파일을 쪼개거나 무분별하게 병합하는 것은 엄격히 금지됩니다.

---

## 1. 🖥️ 프론트엔드 컴포넌트 분할 기준

프론트엔드 UI 컴포넌트는 역할과 의존성 범위에 따라 `FE-PAGE` (페이지), `FE-FEATURE-COMP` (피처 컴포넌트), `FE-SHARED-COMP` (공통 공유 컴포넌트) 계층으로 엄격히 분할하여 관리합니다.

### ① FE-PAGE (페이지 진입점) vs FE-FEATURE-COMP (피처 컴포넌트)
*   **분할 기준**: 라우터와 직접 매핑되어 화면 전체를 그리는 레이아웃 파일은 `FE-PAGE`로 선언합니다. 페이지 내부의 독립적이고 응집력 있는 비즈니스 기능(예: 회원 정보 수정 폼, 상품 상세 패널 등)은 모두 `FE-FEATURE-COMP`로 분할하여 `FE-PAGE`에 조립합니다.
*   **핵심 원칙**: `FE-PAGE`는 상태(Zustand, React Query 등)를 직접 참조하거나 API를 호출해서는 안 됩니다. 오직 URL 파라미터 수집과 레이아웃 제공, 그리고 하위 `FE-FEATURE-COMP`들을 선언적으로 배치하고 필요한 인자만 props로 위임하는 역할만 수행합니다.

### ② FE-FEATURE-COMP 내의 Outer(Container) vs Inner(Renderer) 분할
*   **분할 기준**: 복잡한 사용자 입력 폼이나 데이터 수집 흐름이 들어가는 피처 컴포넌트는 반드시 Outer와 Inner 컴포넌트로 2중 분할합니다.
*   **역할 분담**:
    *   **Outer Component (`{Feature}.tsx`)**: 비즈니스 상태 컨텍스트(react-hook-form Provider, Query Mutation, Zod 스키마 주입 등)를 제공하고, 외부 및 부모로 전달할 API 액션 핸들러(`onSubmitRef` 등)를 주입하는 컨테이너 역할만 수행합니다.
    *   **Inner Component (`{Feature}Inner.tsx` 또는 내부 분리)**: 실제 UI를 렌더링하고, 인풋 필드를 배치하며 사용자 액션을 수집하는 렌더러 역할만 수행합니다.
*   **효과**: 폼 입력값 변화에 따른 불필요한 전체 리렌더링을 방지하고 비즈니스 설정값 주입과 UI 표현을 분리하여 유지보수성을 극대화합니다.

### ③ 공통 공유 컴포넌트 (FE-SHARED-COMP) 분할
*   **분할 기준**: 특정 비즈니스 도메인(예: 결제, 주문 등)에 종속되지 않고, 여러 피처에서 범용적으로 재사용되는 UI 요소(Button, Modal, InputField, Card, Toast 등)는 비즈니스 로직을 완전히 배제하고 `src/components/ui/` 하위로 분할합니다.
*   **핵심 원칙**: 공통 공유 컴포넌트는 `FE-FEATURE-QUERY`, `FE-FEATURE-MUTATION`, `FE-FEATURE-STORE` 등 피처 전용 비즈니스 상태를 임포트할 수 없으며, 모든 제어는 외부 props를 통해서만 수행해야 합니다.

---

## 2. 🧪 테스트 유닛 (SUT - System Under Test) 분할 기준

BDD-TDD 프로세스 하에서 단위 테스트의 대상이 되는 "유닛(Unit)"을 도출하고 분할할 때 다음 기준을 따릅니다.

### ① 컴포넌트 로직의 훅(Hook) / 스토어(Store) 추출 분할
*   **분할 기준**: 컴포넌트 내부의 비즈니스 로직(API 호출, 복잡한 상태 분기, 타이머 제어 등)이 15라인을 넘어가거나 독립적인 검증이 필요할 때, 해당 로직을 컴포넌트에 남겨두지 말고 **피처 커스텀 훅 (`FE-FEATURE-HOOK`)** 또는 **피처 전용 스토어 (`FE-FEATURE-STORE`)**로 분할하여 독립 유닛화합니다.
*   **효과**: UI 렌더링에 얽매이지 않고 비즈니스 상태 변화만을 메모리 상에서 격리하여 단위 테스트할 수 있습니다.

### ② 헬퍼 함수 및 가공 로직의 유틸(Util) 추출 분할
*   **분할 기준**: 날짜 포맷팅, 문자열 파싱, 복잡한 수학적 수치 계산, 결측치 보간 등 부수 효과(Side Effect)가 없고 입력값에 따른 출력값만 존재하는 데이터 연산은 반드시 **유틸리티 모듈 (`FE-FEATURE-UTIL`, `FE-SHARED-UTIL` 등)**의 순수 함수로 완전히 쪼갭니다.
*   **효과**: Mocking의 오버헤드가 없는 완벽한 순수 함수 형태의 유닛이 되므로, 단위 테스트 작성 비용을 대폭 줄일 수 있습니다.

### ③ 백엔드(FastAPI) 계층 간 유닛 분할
*   **BE-ROUTER (라우터)**: 오직 HTTP Endpoint 정의, Payload 입력 직렬화 검증, 상태 코드 선언만 담당하며, 어떠한 비즈니스 로직도 갖지 않습니다.
*   **BE-SERVICE (Usecase)**: 서비스는 단 하나의 비즈니스 목적을 처리하는 Usecase 단위 클래스로 분할됩니다. (예: `CreatePostUsecase`, `DeletePostUsecase` 등)
*   **BE-VO (Value Object)**: 복잡한 입력값의 상호 의존적 유효성 제약조건(예: 시작 시각은 종료 시각 이전이어야 함 등)은 서비스 내부가 아닌 불변 값 객체(VO)의 `__post_init__` 검증 단계로 분할합니다.

---

## 3. 📂 파일 단위 모듈화 및 분리 기준 (File-level Modularization & Separation Criteria)

코드를 구성할 때 파일을 **단일 파일로 분리할 것인가** 또는 **하나의 파일로 그룹화할 것인가**에 대한 명확한 기준입니다.

### ① 단일 파일 분리 대상 (1 File per Unit)
다음 요소들은 관심사 분리와 변경 영향 최소화를 위해 **반드시 1개 파일당 1개의 단위(클래스/함수)만 정의**하도록 단일 파일로 격리합니다.
*   **프론트엔드 API 요청 (`FE-FEATURE-QUERY` / `FE-SHARED-QUERY` / `FE-FEATURE-MUTATION` / `FE-SHARED-MUTATION`)**: 
    - *기준*: 단일 API 엔드포인트 호출 모듈(zod schema + fetcher + react-query hook)마다 **개별 파일로 분리**합니다. (예: `get-user.ts`, `update-profile.ts` 등)
    - *이유*: 특정 API 호출부의 스키마 변경이 다른 API 코드에 영향을 주지 않도록 하고, 트리 셰이킹 최적화를 극대화합니다.
*   **프론트엔드 라우트 페이지 (`FE-PAGE`)**:
    - *기준*: URL 라우팅 경로와 매핑되는 진입점 페이지는 **페이지당 1개의 파일**로 작성합니다.
*   **커스텀 훅 및 공통 컴포넌트 (`FE-FEATURE-HOOK` / `FE-SHARED-HOOK`, `FE-FEATURE-COMP` / `FE-SHARED-COMP`)**:
    - *기준*: 재사용을 전제로 하는 개별 훅과 공통 컴포넌트는 **파일당 1개씩 분리**하여 선언합니다.
*   **백엔드 Usecase 서비스 (Clean Architecture 적용 시 `BE-SERVICE`)**:
    - *기준*: 프로젝트 아키텍처 규모가 크거나 완전한 Clean 아키텍처를 지향하는 경우, `service.py` 하나에 모으지 않고 **Usecase 단위별 파일로 격리**합니다. (예: `usecases/create_post.py`, `usecases/delete_post.py` 등)
*   **단위 테스트 파일 (`FE-TEST`, `BE-TEST`, `AI-TEST`)**:
    - *기준*: 테스트 대상 유닛(SUT) 파일 혹은 특정 엔드포인트별 시나리오 단위로 **1:1 매핑하여 테스트 파일을 분리**합니다.

### ② 단일 파일 내 그룹화 대상 (Multiple Units in 1 File)
다음 요소들은 파일 개수의 무분별한 증가를 막고 도메인 응집력을 높이기 위해 **하나의 파일 내에서 여러 연관 객체를 정의**할 수 있습니다.
*   **도메인별 백엔드 인프라/데이터 모델 (`BE-MODEL`, `BE-SCHEMA`, `BE-DEPENDENCY`)**:
    - *기준*: 동일 도메인(Bounded Context) 내에 속하는 테이블 모델(`models.py`), Pydantic DTO 스키마(`schemas.py`), 라우터 Depends 함수(`dependencies.py`)들은 **파일 단위로 그룹화**하여 모아둡니다.
    - *이유*: 하나의 도메인 안에서 데이터베이스 스키마와 DTO는 서로 밀접하게 연동되므로 한눈에 볼 수 있도록 응집시키는 것이 관리에 유리합니다.
*   **도메인 값 객체 (`BE-VO`, `BE-SERVICE` CRUD 위주)**:
    - *기준*: 도메인 내의 여러 불변 값 객체는 `vo.py` 파일 내에 클래스 단위로 모아서 정의합니다.
    - *기준*: 간단한 CRUD 중심 프로젝트의 경우, 비즈니스 흐름이 단순하므로 Usecase 파일들을 쪼개지 않고 단일 `service.py` 파일 내에 여러 Usecase/Service 클래스를 모아서 정의할 수 있습니다.
*   **공통 및 피처 유틸리티 모듈 (`FE-FEATURE-UTIL` / `FE-SHARED-UTIL`, `BE-DOMAIN-UTIL` / `BE-SHARED-UTIL`, `AI-DOMAIN-UTIL` / `AI-SHARED-UTIL`)**:
    - *기준*: 기능적 관심사(예: 날짜 처리, 브라우저 스토리지 연동 등)에 따라 파일 하나에 연관된 여러 개의 순수 함수를 모아서 작성합니다. (예: `utils/date.ts` 파일 안에 `formatDate`, `getDifference` 등을 함께 작성)
*   **도메인 및 피처 전역 타입 정의 (`FE-FEATURE-TYPE` / `FE-SHARED-TYPE`, `AI-TYPE`)**:
    - *기준*: 동일 도메인/피처 내부에서 공유되는 여러 TypeScript interface/type 선언이나 AI API 입출력 Pydantic DTO + VO는 `types/index.ts` 혹은 `types/value.py`와 같이 **단일 파일 안에 그룹화**하여 모아둡니다.

---

## 🖥️ 프론트엔드 코드 폼 (Frontend Code Forms)

이 절에서는 프론트엔드 코드의 역할을 전역/인프라 영역, 피처 전용 영역, 공통 공유 영역의 3가지 대분류로 분할하여 관리합니다.

---

### ① Global / Infrastructure (전역 / 인프라) 코드 폼

이 영역의 코드 폼들은 애플리케이션의 최상단 제어 흐름, 라우팅, 전역 컨텍스트 주입 등 인프라스트럭처 수준의 역할을 담당합니다.

#### 1) [FE-PAGE] Page Component (화면 진입점/라우트)
- **목적**: 화면의 최상위 진입점으로서 레이아웃을 씌우고, URL 파라미터 파싱 및 하위 피처(Feature) 컴포넌트들을 배치/조립하는 조율자 컴포넌트입니다.
- **물리 경로**: `apps/frontend/src/app/routes/{name}.tsx` 또는 `apps/frontend/src/pages/{name}.tsx`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/app/routes/dashboard.tsx
import React from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { MainLayout } from '@/components/layouts/MainLayout';
import { UserProfileFeature } from '@/features/users/components/UserProfileFeature'; // FE-FEATURE-COMP
import { ScoreListFeature } from '@/features/scores/components/ScoreListFeature'; // FE-FEATURE-COMP

export const DashboardPage: React.FC = () => {
  // 1. 라우트 및 URL 상태 수집 (라우터 의존성 독점)
  const { id } = useParams<{ id: string }>();
  const [searchParams] = useSearchParams();
  const filter = searchParams.get('filter') || 'all';

  return (
    // 2. 글로벌 레이아웃 적용
    <MainLayout title="대시보드">
      <div className="grid grid-cols-12 gap-4">
        {/* 3. 하위 피처 컴포넌트들을 조립 및 상태 전달 */}
        <div className="col-span-4">
          <UserProfileFeature userId={id || ''} />
        </div>
        <div className="col-span-8">
          <ScoreListFeature defaultFilter={filter} />
        </div>
      </div>
    </MainLayout>
  );
};
```
- **준수 사항 (Do's & Don'ts)**:
  - 직접적인 API 호출(React Query), Zustand 스토어 구독, react-hook-form을 통한 복잡한 폼 벨리데이션 로직을 작성하지 마십시오. (해당 로직은 모두 하위의 `FE-FEATURE-COMP` 컴포넌트로 이관되어야 합니다.)

#### 2) [FE-ROUTER] App Entry & Route Config (Router)
- **목적**: react-router-dom을 사용하여 페이지 경로 분기를 선언하고 주입하는 앱 라우터 설정 파일 양식입니다.
- **물리 경로**: `apps/frontend/src/app/router.tsx`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/app/router.tsx
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

#### 3) [FE-PROVIDER] Application Provider Wrapper (Providers)
- **목적**: QueryClient, Language Context, Notification Context 등을 최상단에서 통합 래핑하는 전역 프로바이더 양식입니다.
- **물리 경로**: `apps/frontend/src/app/provider.tsx`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/app/provider.tsx
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

#### 4) [FE-FORM-WRAP] Form Container Wrapper Component
- **목적**: react-hook-form과 Zod resolver를 감싸 폼 데이터를 선언형으로 통제하는 공통 `<Form>` 래퍼 컴포넌트입니다.
- **물리 경로**: `apps/frontend/src/components/ui/form/Form.tsx`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/components/ui/form/Form.tsx
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

#### 5) [FE-LIB] External Library Wrapper (lib)
- **목적**: Axios, TanStack Query 등 외부 SDK 및 라이브러리 인스턴스를 프로젝트 표준 인터셉터/옵션과 결합하여 초기화하고 내보내기 위한 공통 설정 양식입니다.
- **물리 경로**: `apps/frontend/src/lib/{library-name}.ts`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/lib/api-client.ts
import axios from 'axios';

// 1. Configure and create instance
export const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 2. Setup interceptors (common pattern wrapper)
apiClient.interceptors.request.use((config) => {
  // Add Authorization headers or logging
  return config;
});
```

---

### ② Feature-specific (피처 전용) 코드 폼

이 영역의 코드 폼들은 특정 도메인 피처 폴더(`features/{feature}/`) 아래에 종속되며, 해당 피처 내에서만 사용되는 상태, 로직, UI 등을 담당합니다.

#### 1) [FE-FEATURE-COMP] Feature-specific Component (피처 컴포넌트)
- **목적**: 폼 컨텍스트, API Fetch/Mutation 모듈, UI 인풋 요소들을 모아 비즈니스 가치를 완수하는 단위 도메인 피처 조립 컴포넌트입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/components/{name}.tsx`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/features/auth/components/LoginForm.tsx
import React, { useRef, useEffect } from 'react';
import { UseFormReturn } from 'react-hook-form';
import Form, { InputField } from '@/components/ui/form'; // FE-FORM-WRAP 및 FE-SHARED-COMP 사용

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

#### 2) [FE-FEATURE-HOOK] Feature-specific Custom Hook (General)
- **목적**: 특정 피처 컴포넌트의 생명주기와 연동되거나, 해당 피처 특화 UI 동작 상태 및 이벤트를 처리하기 위한 커스텀 훅입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/hooks/{name}.ts`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/features/{feature}/hooks/useFeatureTimer.ts
import { useState, useEffect } from 'react';

export const useFeatureTimer = (initialSeconds: number = 60) => {
  const [seconds, setSeconds] = useState(initialSeconds);
  
  useEffect(() => {
    if (seconds <= 0) return;
    const interval = setInterval(() => {
      setSeconds((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [seconds]);

  return seconds;
};
```
- **준수 사항 (Do's & Don'ts)**:
  - 해당 피처 내부의 UI 비즈니스 로직과 UI 상태 제어 목적에 충실하게 디자인하십시오.

#### 3) [FE-FEATURE-QUERY] Feature-specific API Query Hook (React Query)
- **목적**: 특정 피처 도메인에 한정하여 서버 데이터를 조회/캐싱하기 위한 Custom Hook입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/api/get-{domain}.ts`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/features/{feature}/api/get-{domain}.ts
import { useQuery, queryOptions } from '@tanstack/react-query';
import { z } from 'zod';
import { api } from '@/lib/api-client'; // FE-LIB 경로 참조

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

#### 4) [FE-FEATURE-MUTATION] Feature-specific API Fetch/Mutation Module (fetch / react-query)
- **목적**: 특정 피처 도메인에서 POST, PUT, DELETE 등 서버 상태를 변경하는 요청을 처리하며, 422 밸리데이션 에러를 커스텀 핸들링합니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/api/{action}.ts`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/features/{feature}/api/{action}.ts

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

#### 5) [FE-FEATURE-STORE] Feature-specific Global Store (Zustand Store)
- **목적**: 특정 피처 도메인의 내부 UI 상태(선택된 필터 상태, 사이드 패널 토글, 임시 입력 값 등)를 공유/제어하기 위한 스토어입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/stores/{store-name}.ts`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/features/{feature}/stores/{store-name}.ts
import { create } from 'zustand';

type FeatureState = {
  activeTab: string;
  setActiveTab: (tab: string) => void;
};

export const useFeatureStore = create<FeatureState>((set) => ({
  activeTab: 'overview',
  setActiveTab: (tab) => set({ activeTab: tab }),
}));
```
- **준수 사항 (Do's & Don'ts)**:
  - 자주 바뀌는 도메인 서버 데이터를 이 스토어에 임의로 영속화하여 동기화하지 마십시오. (서버 데이터는 `FE-FEATURE-QUERY` 서버 캐시로 관리)
  - 이 스토어는 해당 피처 외부에서 임포트되어 의존성을 가지면 안 됩니다.

#### 6) [FE-FEATURE-UTIL] Feature-specific Utility Module (Utils / Helper)
- **목적**: 특정 피처 도메인 내부에서만 사용되는 데이터 포맷팅, 수치 계산 등 부수 효과가 없는 순수 함수/객체 헬퍼 모듈입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/utils/{name}.ts`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/features/{feature}/utils/scoreCalculator.ts

export const calculateAverageScore = (scores: number[]): number => {
  if (scores.length === 0) return 0;
  const sum = scores.reduce((acc, curr) => acc + curr, 0);
  return sum / scores.length;
};
```
- **준수 사항 (Do's & Don'ts)**:
  - 가능한 한 부수 효과(Side Effect)가 없는 순수 함수 형태로 작성하여 독립적인 단위 테스트가 가능하게 만드십시오.

#### 7) [FE-FEATURE-TYPE] Feature-specific Types
- **목적**: 특정 피처 도메인 내부에서만 공유되고 사용되는 TypeScript interface, type, 또는 local state type 선언부입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/types/index.ts` 또는 `apps/frontend/src/features/{feature}/types/{name}.ts`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/features/{feature}/types/index.ts

export interface FeatureLocalState {
  id: string;
  isSelected: boolean;
}
```
- **준수 사항 (Do's & Don'ts)**:
  - 이 파일에는 런타임 로직(클래스, 함수 등)을 포함할 수 없으며 오직 타입 선언만 위치해야 합니다.
  - 피처 외부로 유출되어 전역적인 의존성을 갖지 않도록 캡슐화 수준을 유지해야 합니다.

---

## ⚙️ 백엔드 코드 폼 (Backend Code Forms)

이 절에서는 백엔드 코드의 역할을 전역/인프라 영역과 도메인 전용 영역의 2가지 대분류로 분할하여 관리합니다.

---

### ① Global / Infrastructure (전역 / 인프라) 코드 폼

이 영역의 코드 폼들은 데이터베이스 세션 관리, 공통 예외 핸들러, 공통 설정값 및 외부 클라이언트 래핑 등 인프라스트럭처 수준의 역할을 담당합니다.

#### 1) [BE-DATABASE] Database Session Manager
- **목적**: SQLAlchemy 2.0 비동기 데이터베이스 커넥션 엔진과 세션 팩토리를 관리합니다.
- **물리 경로**: `apps/backend/src/database.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/db"

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with SessionFactory() as session:
        yield session
```

#### 2) [BE-CLIENT] External Client (외부 서비스 연동 클라이언트)
- **목적**: 외부 API 호출을 안전하게 처리하고, 타임아웃 및 재시도 로직을 캡슐화합니다.
- **물리 경로**: `apps/backend/src/lib/{client_name}_client.py` 또는 `apps/backend/src/lib/clients.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/lib/payment_client.py
import httpx
from typing import Dict, Any

class ExternalAPIClient:
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url
        self.timeout = timeout

    async def fetch_data(self, endpoint: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.get(endpoint)
            response.raise_for_status()
            return response.json()
```

#### 3) [BE-EXCEPTION] Custom Exception & Handler (예외 및 전역 핸들러)
- **목적**: 도메인 비즈니스 예외를 전역으로 일관되게 캡슐화하여 API 클라이언트에 표준화된 에러 응답을 반환합니다.
- **물리 경로**: `apps/backend/src/exceptions.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/exceptions.py
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )
```

#### 4) [BE-CONFIG] Config Settings (설정값 관리)
- **목적**: Pydantic Settings를 사용하여 환경 변수를 검증하고, 시스템 전역에서 사용할 설정 싱글톤을 로드합니다.
- **물리 경로**: `apps/backend/src/config.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "My FastAPI Application"
    database_url: str
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
```

#### 5) [BE-SHARED-UTIL] Shared Utility Module (Backend)
- **목적**: 날짜 연산, 암호화 헬퍼, 공통 문자열 처리 등 백엔드 전역에서 공통적으로 쓰이는 순수 비즈니스 유틸리티 모듈입니다.
- **물리 경로**: `apps/backend/src/utils/{name}.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/utils/date_helper.py
from datetime import datetime, timezone

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)
```

---

### ② Domain-specific (도메인 전용) 코드 폼

이 영역의 코드 폼들은 특정 비즈니스 도메인 폴더(`src/{domain}/`) 하위에 격리되어 관리됩니다.

#### 1) [BE-ROUTER] API Router (FastAPI APIRouter)
- **목적**: API 엔드포인트를 정의하고 HTTP 응답 스펙과 Status Code를 정의하는 레이어입니다.
- **물리 경로**: `apps/backend/src/{domain}/router.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/router.py
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

#### 2) [BE-SERVICE] Service / Usecase (비즈니스 로직 서비스)
- **목적**: 단일 책임을 지는 비즈니스 로직 및 Usecase를 수행하는 서비스 클래스입니다.
- **물리 경로**: `apps/backend/src/{domain}/service.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/service.py
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import PostCreate # BE-SCHEMA
from .vo import PostVO # BE-VO
from .models import PostModel # BE-MODEL

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

### 3) [BE-VO] Value Object (불변 값 객체 - VO)
- **목적**: 비즈니스 도메인의 값을 캡슐화하고 데이터의 무결성 제약조건을 강제하기 위한 객체입니다.
- **물리 경로**: `apps/backend/src/{domain}/vo.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/vo.py
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

### 4) [BE-MODEL] Database ORM Model (SQLAlchemy ORM)
- **목적**: 데이터베이스 테이블 스키마에 매핑되는 선언적 데이터 모델입니다.
- **물리 경로**: `apps/backend/src/{domain}/models.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/models.py
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

### 5) [BE-DEPENDENCY] Route Dependency & Validator (FastAPI Dependencies)
- **목적**: 인가, 데이터 존재 여부 검증, 자원 획득 등 API 엔드포인트 도달 전에 실행되는 공용 검증 함수군입니다.
- **물리 경로**: `apps/backend/src/{domain}/dependencies.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db # BE-DATABASE 절대 경로 참조
from .models import PostModel # BE-MODEL

async def valid_post_id(
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> PostModel:
    post = await db.get(PostModel, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 게시글입니다."
        )
    return post
```

### 6) [BE-SCHEMA] Request/Response DTO (Pydantic Schema)
- **목적**: 입출력 데이터의 유효성 검증과 직렬화를 담당합니다.
- **물리 경로**: `apps/backend/src/{domain}/schemas.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/schemas.py
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

### 7) [BE-TEST] Async Integration/Unit Test (pytest + httpx)
- **목적**: 비동기 API 클라이언트를 이용하여 백엔드 비즈니스 흐름 및 에러 처리를 검증합니다.
- **물리 경로**: `apps/backend/tests/unit/test_create_post.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/tests/unit/test_create_post.py
import pytest
from httpx import AsyncClient, ASGITransport
from main import app # 최상위 진입점 임포트
from src.posts.dependencies import valid_active_user

# 1. 가짜 인증 유저 의존성 오버라이드
def fake_active_user():
    return {"user_id": "test_user"}

@pytest.fixture
async def client():
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
```


---

## 🤖 AI 모듈 코드 폼 (AI Code Forms)

이 절에서는 AI 모듈 코드의 역할을 전역/인프라 영역과 도메인 전용 영역의 2가지 대분류로 분할하여 관리합니다.

---

### ① Global / Infrastructure (전역 / 인프라) 코드 폼

이 영역의 코드 폼들은 의존성 주입 컨테이너, 프롬프트 템플릿, AI 예외 핸들러 및 모델 스펙 설정값 등 인프라스트럭처 수준의 역할을 담당합니다.

#### 1) [AI-BOOTSTRAP] Bootstrap & DI Container (의존성 주입)
- **목적**: 전역 환경 설정을 로드하고, 게이트웨이 및 Usecase 의존성을 단일 지점에서 조립하여 생성합니다.
- **물리 경로**: `apps/ai/src/bootstrap.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/bootstrap.py
from src.outbound.gateway import ModelGateway
from src.core.processor import FeatureExtractor
from src.usecases.inference import InferenceUsecase

class DIContainer:
    def __init__(self):
        self.model_gateway = ModelGateway(model_path="models/model.onnx")
        self.extractor = FeatureExtractor()
        
        self.inference_usecase = InferenceUsecase(
            model_gateway=self.model_gateway,
            extractor=self.extractor
        )

container = DIContainer()
```

#### 2) [AI-PROMPT] Prompt Templates (프롬프트 템플릿 모듈)
- **목적**: LLM 애플리케이션 및 에이전트 구동에 필요한 전용 프롬프트 템플릿을 코드와 분리하여 선언적으로 관리합니다.
- **물리 경로**: `apps/ai/src/prompts/medical_prompts.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/prompts/medical_prompts.py
from langchain_core.prompts import PromptTemplate

SYSTEM_PROMPT = """당신은 의료 데이터 분석 AI 비서입니다. 
주어진 신호 데이터를 기반으로 상태를 감지하여 보고하십시오.
"""

USER_PROMPT_TEMPLATE = PromptTemplate.from_template(
    "이전 상태 기록: {history}\n현재 신호 데이터: {current_signal}\n위험 상태 여부를 판정해 주세요."
)
```

#### 3) [AI-EXCEPTION] AI Custom Exception & Handler (AI 예외 및 응답 핸들러)
- **목적**: 모델 가중치 로딩 실패, 이상치 감지, LLM API 호출 한도 초과 등 AI 추론 특화 예외를 처리하고 API 규격에 맞춰 에러 응답을 포맷팅합니다.
- **물리 경로**: `apps/ai/src/exceptions.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/exceptions.py
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

class InferenceEngineException(Exception):
    def __init__(self, detail: str, model_name: str, status_code: int = 500):
        self.detail = detail
        self.model_name = model_name
        self.status_code = status_code
        super().__init__(detail)

def register_ai_exception_handlers(app: FastAPI):
    @app.exception_handler(InferenceEngineException)
    async def ai_inference_exception_handler(request: Request, exc: InferenceEngineException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "AI Inference Failed",
                "model": exc.model_name,
                "message": exc.detail
            }
        )
```

#### 4) [AI-CONFIG] Model Config & Specs (모델/하이퍼파라미터 설정)
- **목적**: 모델 가중치 파일 경로, 입력/출력 텐서 차원(Dim), 임베딩 크기 등 AI 실행 하이퍼파라미터를 안전하게 로드하고 관리합니다.
- **물리 경로**: `apps/ai/src/config/model_config.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/config/model_config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class ModelSpecs(BaseSettings):
    model_path: str = Field(default="models/model.onnx")
    input_dimension: int = Field(default=120)
    output_dimension: int = Field(default=2)
    threshold: float = Field(default=0.85)

    class Config:
        env_prefix = "AI_MODEL_"
        env_file = ".env"

model_specs = ModelSpecs()
```

#### 5) [AI-SHARED-UTIL] Shared Utility Module (AI)
- **목적**: 텍스트 특수문자 제거(정규화), 텐서 연산 헬퍼, 오프라인 메트릭 계산 등 AI 파이프라인 전반에 사용되는 순수 헬퍼 모듈입니다.
- **물리 경로**: `apps/ai/src/utils/{name}.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/utils/text_helper.py
import re

def clean_text(text: str) -> str:
    cleaned = re.sub(r"[^\w\s]", "", text)
    return cleaned.strip()
```

---

### ② Domain-specific (도메인 전용) 코드 폼

이 영역의 코드 폼들은 특정 추론/에이전트 비즈니스 도메인 폴더 하위에 격리되어 관리됩니다.

#### 1) [AI-ROUTER] Inbound Router (추론 API 라우터)
- **목적**: 외부 요청을 수신하여 AI 추론 Usecase를 호출하고 결과를 반환하는 진입점 레이어입니다.
- **물리 경로**: `apps/ai/src/inbound/router.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/inbound/router.py
from fastapi import APIRouter, Depends, status
from typing import Annotated
from src.bootstrap import container # AI-BOOTSTRAP 절대 경로 참조
from src.types.value import PredictionRequest, PredictionResponse # AI-TYPE 참조

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
    result = await usecase.execute(payload)
    return result
```

#### 2) [AI-USECASE] Inference Usecase (추론 오케스트레이터)
- **목적**: Core(전/후처리) 및 Outbound(모델 추론 및 외부 API) 레이어를 조율하여 추론 연산을 오케스트레이션합니다.
- **물리 경로**: `apps/ai/src/usecases/inference.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/usecases/inference.py
from src.types.value import PredictionRequest, PredictionResponse # AI-TYPE
from src.core.processor import FeatureExtractor # AI-CORE
from src.outbound.gateway import ModelGateway # AI-GATEWAY

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

### 3) [AI-WORKFLOW] Stateful Workflow (상태/에이전트 제어 흐름)
- **목적**: LangGraph 등 상태 기반 제어 흐름 또는 다단계 프롬프트 체인, 인간 검증(HITL) 단계를 갖는 AI 에이전트/워크플로우 오케스트레이션입니다.
- **물리 경로**: `apps/ai/src/workflow/process.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/workflow/process.py
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
        state: WorkflowState = {
            "input_text": text,
            "intermediate_steps": [],
            "final_output": "",
            "status": "pending"
        }
        
        llm_response = await self.model_gateway.call_llm(state["input_text"])
        state["intermediate_steps"].append("llm_call")
        state["final_output"] = llm_response
        state["status"] = "completed"
        return state
```

### 4) [AI-CORE] Core Processor (도메인 코어 프로세서)
- **목적**: 원시 특징(Feature) 추출, 텐서 가공, 수학적 수치 분석 및 비즈니스 룰 후처리를 담당하는 Pure Python 비즈니스 도메인 레이어입니다.
- **물리 경로**: `apps/ai/src/core/processor.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/core/processor.py
import numpy as np

class FeatureExtractor:
    def extract_features(self, raw_data: list[float]) -> np.ndarray:
        if not raw_data:
            raise ValueError("원시 데이터는 필수입니다.")
        return np.array(raw_data, dtype=np.float32).reshape(1, -1)

    def postprocess(self, model_output: np.ndarray) -> str:
        score = float(model_output[0][0])
        if score > 0.8:
            return "위험"
        elif score > 0.4:
            return "경고"
        return "정상"
```

### 5) [AI-GATEWAY] Outbound Gateway (ML/LLM Gateway 어댑터)
- **목적**: 실제 ONNX/Torch 가중치 엔진을 구동하거나 외부 LLM API(OpenAI/Claude 등) 통신을 독점적으로 수행하는 어댑터 레이어입니다.
- **물리 경로**: `apps/ai/src/outbound/gateway.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/outbound/gateway.py
import onnxruntime as ort
import numpy as np

class ModelGateway:
    def __init__(self, model_path: str):
        self.session = ort.InferenceSession(model_path)

    async def predict(self, input_tensor: np.ndarray) -> np.ndarray:
        input_name = self.session.get_inputs()[0].name
        output_name = self.session.get_outputs()[0].name
        raw_output = self.session.run([output_name], {input_name: input_tensor})
        return raw_output[0]

    async def call_llm(self, prompt: str) -> str:
        return "LLM 응답 샘플"
```

### 6) [AI-TYPE] Domain Types (불변 VO 및 DTO)
- **목적**: API 경계용 Pydantic DTO와 코어 내부 검증용 frozen dataclass VO를 정의합니다.
- **물리 경로**: `apps/ai/src/types/value.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/types/value.py
from pydantic import BaseModel
from dataclasses import dataclass

# 1. API Boundary (Pydantic DTO)
class PredictionRequest(BaseModel):
    data: list[float]

class PredictionResponse(BaseModel):
    result: str

# 2. Domain VO (frozen dataclass)
@dataclass(frozen=True)
class TensorConfigVO:
    input_dim: int
    output_dim: int
```

### 7) [AI-TEST] Evals & Integration Test (pytest 기반 추론 검증)
- **목적**: 모의 어댑터를 이용해 로컬 환경에서 추론 파이프라인 및 에이전트 상태 전이를 검증합니다.
- **물리 경로**: `apps/ai/tests/unit/test_inference.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/tests/unit/test_inference.py
import pytest
from unittest.mock import AsyncMock
import numpy as np
from src.usecases.inference import InferenceUsecase # AI-USECASE
from src.core.processor import FeatureExtractor # AI-CORE
from src.types.value import PredictionRequest # AI-TYPE

@pytest.mark.asyncio
async def test_inference_usecase_flow():
    mock_gateway = AsyncMock()
    mock_gateway.predict.return_value = np.array([[0.85]], dtype=np.float32)
    
    extractor = FeatureExtractor()
    usecase = InferenceUsecase(model_gateway=mock_gateway, extractor=extractor)
    
    request = PredictionRequest(data=[0.1, 0.2, 0.3])
    response = await usecase.execute(request)
    
    assert response.result == "위험"
    mock_gateway.predict.assert_called_once()
```


