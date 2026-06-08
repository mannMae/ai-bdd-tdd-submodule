---
name: code-dictionary
description: Component & Unit Division guidelines, file modularization rules, and standardized Code Form boilerplates for Frontend, Backend, and AI modules.
version: 1.0.0
globs: "*"
alwaysApply: true
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
*   **BE-DOMAIN-ROUTER (라우터)**: 오직 HTTP Endpoint 정의, Payload 입력 직렬화 검증, 상태 코드 선언만 담당하며, 어떠한 비즈니스 로직도 갖지 않습니다.
*   **BE-DOMAIN-SERVICE (Usecase)**: 서비스는 단 하나의 비즈니스 목적을 처리하는 Usecase 단위 클래스로 분할됩니다. (예: `CreatePostUsecase`, `DeletePostUsecase` 등)
*   **BE-DOMAIN-VO (Value Object)**: 복잡한 입력값의 상호 의존적 유효성 제약조건(예: 시작 시각은 종료 시각 이전이어야 함 등)은 서비스 내부가 아닌 불변 값 객체(VO)의 `__post_init__` 검증 단계로 분할합니다.

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
*   **백엔드 Usecase 서비스 (Clean Architecture 적용 시 `BE-DOMAIN-SERVICE`)**:
    - *기준*: 프로젝트 아키텍처 규모가 크거나 완전한 Clean 아키텍처를 지향하는 경우, `service.py` 하나에 모으지 않고 **Usecase 단위별 파일로 격리**합니다. (예: `usecases/create_post.py`, `usecases/delete_post.py` 등)
*   **단위 테스트 파일 (`FE-TEST`, `BE-DOMAIN-TEST`, `AI-DOMAIN-TEST`)**:
    - *기준*: 테스트 대상 유닛(SUT) 파일 혹은 특정 엔드포인트별 시나리오 단위로 **1:1 매핑하여 테스트 파일을 분리**합니다.

### ② 단일 파일 내 그룹화 대상 (Multiple Units in 1 File)
다음 요소들은 파일 개수의 무분별한 증가를 막고 도메인 응집력을 높이기 위해 **하나의 파일 내에서 여러 연관 객체를 정의**할 수 있습니다.
*   **도메인별 백엔드 인프라/데이터 모델 (`BE-DOMAIN-MODEL` / `BE-SHARED-MODEL`, `BE-DOMAIN-SCHEMA` / `BE-SHARED-SCHEMA`, `BE-DOMAIN-DEPENDENCY` / `BE-SHARED-DEPENDENCY`)**:
    - *기준*: 동일 도메인(Bounded Context) 내에 속하는 테이블 모델(`models.py`), Pydantic DTO 스키마(`schemas.py`), 라우터 Depends 함수(`dependencies.py`)들은 **파일 단위로 그룹화**하여 모아둡니다.
    - *이유*: 하나의 도메인 안에서 데이터베이스 스키마와 DTO는 서로 밀접하게 연동되므로 한눈에 볼 수 있도록 응집시키는 것이 관리에 유리합니다.
*   **도메인 값 객체 (`BE-DOMAIN-VO`, `BE-DOMAIN-SERVICE` CRUD 위주)**:
    - *기준*: 도메인 내의 여러 불변 값 객체는 `vo.py` 파일 내에 클래스 단위로 모아서 정의합니다.
    - *기준*: 간단한 CRUD 중심 프로젝트의 경우, 비즈니스 흐름이 단순하므로 Usecase 파일들을 쪼개지 않고 단일 `service.py` 파일 내에 여러 Usecase/Service 클래스를 모아서 정의할 수 있습니다.
*   **공통 및 피처 유틸리티 모듈 (`FE-FEATURE-UTIL` / `FE-SHARED-UTIL`, `BE-DOMAIN-UTIL` / `BE-SHARED-UTIL`, `AI-DOMAIN-UTIL` / `AI-SHARED-UTIL`)**:
    - *기준*: 기능적 관심사(예: 날짜 처리, 브라우저 스토리지 연동 등)에 따라 파일 하나에 연관된 여러 개의 순수 함수를 모아서 작성합니다. (예: `utils/date.ts` 파일 안에 `formatDate`, `getDifference` 등을 함께 작성)
*   **도메인 및 피처 전역 타입 정의 (`FE-FEATURE-TYPE` / `FE-SHARED-TYPE`, `AI-DOMAIN-TYPE` / `AI-SHARED-TYPE`)**:
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

#### 8) [FE-FEATURE-COMP-TEST] Feature-specific Component Test
- **목적**: 피처 컴포넌트([FE-FEATURE-COMP])의 UI 렌더링, 사용자 입력/클릭 동작 및 화면 상태 변화를 격리 검증하는 테스트 양식입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/tests/{name}.test.tsx`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/features/auth/tests/LoginForm.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { LoginForm } from '../components/LoginForm';

describe('FE-FEATURE-COMP-TEST: LoginForm', () => {
  it('입력 필드가 입력되지 않은 상태에서 제출 클릭 시 검증 에러가 나야 한다', () => {
    // 1. Setup - Mock handlers & render SUT
    const handleSuccess = vi.fn();
    render(<LoginForm onSuccess={handleSuccess} />);

    // 2. Action - Click submit button
    const submitButton = screen.getByRole('button', { name: /Submit/i });
    fireEvent.click(submitButton);

    // 3. Assertion - Check validation error and handler not called
    expect(screen.getByText(/fieldName/i)).toBeInTheDocument();
    expect(handleSuccess).not.toHaveBeenCalled();
  });

  it('올바른 값을 입력한 후 시작 버튼을 클릭하면 핸들러가 호출된다', () => {
    // 1. Setup
    const handleSuccess = vi.fn();
    render(<LoginForm onSuccess={handleSuccess} />);

    // 2. Action - Input value and click submit
    const input = screen.getByLabelText(/fieldName/i);
    fireEvent.change(input, { target: { value: 'testValue' } });
    
    const submitButton = screen.getByRole('button', { name: /Submit/i });
    fireEvent.click(submitButton);

    // 3. Assertion - Verifying behavioral outcome
    expect(handleSuccess).toHaveBeenCalled();
  });
});
```
- **준수 사항 (Do's & Don't's)**:
  - 🛑 외부 API를 컴포넌트 내에서 직접 mock/spyOn 하지 마십시오. 컴포넌트가 의존하는 API 통신은 `[FE-FEATURE-QUERY-TEST]` 영역에서 모킹되어야 합니다.
  - 🛑 `jest.spyOn()` 또는 `vi.spyOn()`을 이용해 컴포넌트 내부의 로컬 렌더링 도우미 함수나 inner 요소를 모킹하지 마십시오. 오직 props 콜백이나 외부 API 인터페이스만 모킹을 허용합니다.

#### 9) [FE-FEATURE-HOOK-TEST] Feature-specific Custom Hook Test
- **목적**: React 커스텀 훅([FE-FEATURE-HOOK])의 라이프사이클 및 상태 변경 비즈니스 로직을 UI와 격리하여 단위 검증하는 테스트 양식입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/tests/{name}.test.ts`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/features/{feature}/tests/useFeatureTimer.test.ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { useFeatureTimer } from '../hooks/useFeatureTimer';

describe('FE-FEATURE-HOOK-TEST: useFeatureTimer', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('초기 타이머 값 설정이 올바르게 로드되고 매초 1씩 감소한다', () => {
    // 1. Setup - Render hook
    const { result } = renderHook(() => useFeatureTimer(10));
    expect(result.current).toBe(10);

    // 2. Action - Advance timer by 1 second
    act(() => {
      vi.advanceTimersByTime(1000);
    });

    // 3. Assertion - State change verification
    expect(result.current).toBe(9);
  });
});
```
- **준수 사항 (Do's & Don't's)**:
  - 훅 내부 상태(state) 변경 시점은 반드시 `@testing-library/react` 패키지의 `act()` 블록으로 래핑하여 리렌더링 사이클이 동기적으로 완료되도록 해야 합니다.

#### 10) [FE-FEATURE-QUERY-TEST] Feature-specific API Query Hook Test
- **목적**: TanStack Query 기반의 API 요청 훅([FE-FEATURE-QUERY] / [FE-FEATURE-MUTATION])의 캐싱 및 에러 발생 분기 동작을 MSW(Mock Service Worker)와 결합하여 검증하는 테스트 양식입니다.
- **물리 경로**: `apps/frontend/src/features/{feature}/tests/{name}.test.ts`
- **구조 예시 및 템플릿**:
```typescript
// Path: apps/frontend/src/features/{feature}/tests/useUser.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect } from 'vitest';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { useUser } from '../api/get-user';

// MSW Server Setup
const server = setupServer(
  http.get('/api/users/1', () => {
    return HttpResponse.json({ id: '1', name: '홍길동' });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe('FE-FEATURE-QUERY-TEST: useUser', () => {
  it('성공 시 사용자 데이터를 정상적으로 패치하고 캐시한다', async () => {
    const { result } = renderHook(() => useUser({ userId: '1' }), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual({ id: '1', name: '홍길동' });
  });

  it('네트워크 오류(500) 발생 시 에러 플래그와 함께 적절한 예외 객체를 반환한다', async () => {
    server.use(
      http.get('/api/users/1', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );

    const { result } = renderHook(() => useUser({ userId: '1' }), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error).toBeDefined();
  });
});
```
- **준수 사항 (Do's & Don't's)**:
  - 🛑 Mocking을 위해 전역 API fetcher 함수 자체를 `vi.fn()`으로 덮어쓰는 행위(Mocking client method)를 금지합니다. 반드시 실제 HTTP 계층을 시뮬레이트하는 MSW(Mock Service Worker)를 구성하여 통신 레이어의 원본 규격을 검증해야 합니다.

---

## ⚙️ 백엔드 코드 폼 (Backend Code Forms)

이 절에서는 백엔드 코드의 역할을 전역/인프라 영역, 도메인 전용 영역, 공통 공유 영역의 3가지 대분류로 분할하여 관리합니다.

---

### ① Global / Infrastructure (전역 / 인프라) 코드 폼

이 영역의 코드 폼들은 데이터베이스 엔진 커넥션, Pydantic Settings 환경 설정 등 시스템의 글로벌 공통 구동 기반에 해당하며, 프로젝트에 통상 단 한 개씩만 존재합니다.

#### 1) [BE-DATABASE] Database Session Manager
- **목적**: SQLAlchemy 비동기 데이터베이스 커넥션 엔진과 세션 팩토리를 관리합니다.
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

#### 2) [BE-CONFIG] Config Settings (전역 설정값 관리)
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

---

### ② Domain-specific (도메인 전용) 코드 폼

이 영역의 코드 폼들은 특정 비즈니스 도메인 폴더(`src/{domain}/`) 하위에 격리되어, 특정 비즈니스 요구사항을 처리하는 레이어에 매핑됩니다.

#### 1) [BE-DOMAIN-ROUTER] API Router (FastAPI APIRouter)
- **목적**: API 엔드포인트를 정의하고 HTTP 응답 스펙과 Status Code를 정의하는 레이어입니다.
- **물리 경로**: `apps/backend/src/{domain}/router.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/router.py
from typing import Annotated
from fastapi import APIRouter, Depends, status
from .schemas import PostResponse, PostCreate, ErrorResponse # BE-DOMAIN-SCHEMA
from .dependencies import valid_post_id # BE-DOMAIN-DEPENDENCY
from src.shared.dependencies import valid_active_user # BE-SHARED-DEPENDENCY

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="게시글 작성"
)
async def create_post(
    payload: PostCreate,
    current_user: Annotated[dict, Depends(valid_active_user)]
):
    # 서비스 호출
    pass
```

#### 2) [BE-DOMAIN-SERVICE] Service / Usecase (비즈니스 로직 서비스)
- **목적**: 단일 책임을 지는 비즈니스 로직 및 Usecase를 수행하는 서비스 클래스입니다.
- **물리 경로**: `apps/backend/src/{domain}/service.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/service.py
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import PostCreate # BE-DOMAIN-SCHEMA
from .vo import PostVO # BE-DOMAIN-VO
from .models import PostModel # BE-DOMAIN-MODEL

class CreatePostUsecase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, payload: PostCreate, creator_id: str) -> PostModel:
        # 1. DTO를 VO로 변환하여 무결성 검증
        vo = PostVO(title=payload.title, content=payload.content)
        
        # 2. ORM 엔티티 모델에 반영
        model = PostModel(
            title=vo.title,
            content=vo.content,
            creator_id=creator_id
        )
        self.db.add(model)
        await self.db.flush()
        return model
```

#### 3) [BE-DOMAIN-VO] Value Object (불변 값 객체 - VO)
- **목적**: 비즈니스 도메인의 값을 캡슐화하고 데이터의 무결성 제약조건을 강제하는 불변 값 객체입니다.
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

#### 4) [BE-DOMAIN-MODEL] Database ORM Model (SQLAlchemy ORM)
- **목적**: 특정 도메인의 테이블 스키마에 매핑되는 선언적 데이터 모델입니다.
- **물리 경로**: `apps/backend/src/{domain}/models.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/models.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.shared.models import Base # BE-SHARED-MODEL 참조

class PostModel(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    creator_id: Mapped[str] = mapped_column(String, nullable=False)
```

#### 5) [BE-DOMAIN-DEPENDENCY] Route Dependency & Validator
- **목적**: 특정 도메인 내의 리소스 존재 여부 등을 라우터 진입 전에 사전 검증하는 FastAPI Depends 용도 함수입니다.
- **물리 경로**: `apps/backend/src/{domain}/dependencies.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db # BE-DATABASE
from .models import PostModel # BE-DOMAIN-MODEL

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

#### 6) [BE-DOMAIN-SCHEMA] Request/Response DTO (Pydantic Schema)
- **목적**: 특정 도메인 API 통신 시 입출력 데이터 규격을 검증하고 직렬화합니다.
- **물리 경로**: `apps/backend/src/{domain}/schemas.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/schemas.py
from pydantic import BaseModel, Field

class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    creator_id: str
```

#### 7) [BE-DOMAIN-CLIENT] Domain External Client
- **목적**: 특정 도메인에 한정되어 사용되는 서드파티 연동 HTTP 클라이언트나 API 호출기입니다.
- **물리 경로**: `apps/backend/src/{domain}/client.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/client.py
# 특정 도메인 전용 외부 클라이언트 구현부
class DomainSpecificClient:
    def __init__(self, key: str):
        self.key = key
```

#### 8) [BE-DOMAIN-EXCEPTION] Domain Exception
- **목적**: 특정 비즈니스 도메인 규칙을 위반할 때 발생하는 커스텀 도메인 예외군을 정의합니다.
- **물리 경로**: `apps/backend/src/{domain}/exceptions.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/exceptions.py
from src.shared.exceptions import DomainException # BE-SHARED-EXCEPTION 상속

class PostNotFoundException(DomainException):
    def __init__(self, post_id: int):
        super().__init__(
            message=f"게시글 {post_id}를 찾을 수 없습니다.",
            status_code=404
        )
```

#### 9) [BE-DOMAIN-UTIL] Domain Utility Module
- **목적**: 특정 도메인 내부에서만 단독으로 재사용되는 가공/유틸리티 함수입니다.
- **물리 경로**: `apps/backend/src/{domain}/utils.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/posts/utils.py
def format_post_title(title: str) -> str:
    return title.strip().title()
```

#### 10) [BE-DOMAIN-ROUTER-TEST] API Router Integration Test
- **목적**: 백엔드 API 라우터([BE-DOMAIN-ROUTER])의 엔드포인트 요청/응답 규격, HTTP 상태 코드 및 인증 의존성 필터를 통합 검증하는 테스트 양식입니다.
- **물리 경로**: `apps/backend/tests/integration/test_{name}.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/tests/integration/test_posts.py
import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from src.shared.dependencies import valid_active_user

# 1. Dependency Override Fixture
@pytest.fixture
async def client():
    # Mock authentication to isolate API endpoint logic
    app.dependency_overrides[valid_active_user] = lambda: {"user_id": "test_user"}
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
        
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_post_endpoint_success(client: AsyncClient):
    # [Given] Valid request payload
    payload = {"title": "테스트 제목", "content": "테스트 내용"}
    
    # [When] Post request to endpoint
    response = await client.post("/posts", json=payload)
    
    # [Then] Verify status code and exact schema envelope
    assert response.status_code == 201
    res_data = response.json()
    assert "id" in res_data
    assert res_data["title"] == "테스트 제목"

@pytest.mark.asyncio
async def test_create_post_endpoint_validation_error(client: AsyncClient):
    # [Given] Invalid empty title
    payload = {"title": "", "content": "테스트 내용"}
    
    # [When] Post request
    response = await client.post("/posts", json=payload)
    
    # [Then] Verify 422 Unprocessable Entity
    assert response.status_code == 422
```
- **준수 사항 (Do's & Don't's)**:
  -  인증 및 인가 Depends 함수(`valid_active_user` 등)는 반드시 `app.dependency_overrides`를 활용하여 모킹해 우회하십시오. 테스트가 인증 처리 모듈 자체의 결함으로 블록되는 것을 방지합니다.

#### 11) [BE-DOMAIN-SERVICE-TEST] Service/Usecase Unit Test
- **목적**: 단일 책임을 지는 비즈니스 서비스([BE-DOMAIN-SERVICE])의 도메인 로직 및 데이터 정합성을 데이터베이스 트랜잭션 롤백과 연동하여 격리 단위 검증하는 테스트 양식입니다.
- **물리 경로**: `apps/backend/tests/unit/services/test_{name}.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/tests/unit/services/test_posts.py
import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.posts.service import CreatePostUsecase
from src.posts.schemas import PostCreate

@pytest.mark.asyncio
async def test_create_post_saves_to_db():
    # 1. Setup - Mock Database AsyncSession
    mock_db = AsyncMock(spec=AsyncSession)
    usecase = CreatePostUsecase(db=mock_db)
    payload = PostCreate(title="테스트 제목", content="테스트 내용")
    
    # 2. Action - Execute usecase
    result = await usecase.execute(payload, creator_id="test_user")
    
    # 3. Assertion - Verify business rules and database side effects
    assert result.title == "테스트 제목"
    assert result.content == "테스트 내용"
    
    # Ensure entity was added to session and flush was called
    mock_db.add.assert_called_once()
    mock_db.flush.assert_called_once()
```
- **준수 사항 (Do's & Don't's)**:
  - 🛑 서비스 내에서 호출하는 다른 서비스 레이어나 유틸 클래스를 무분별하게 모킹하지 마십시오. 단위 테스트 범위 내에서 데이터베이스 입출력(`AsyncSession`) 외의 순수 연산은 실제 객체를 주입해야 정상적인 로직 오류를 잡아낼 수 있습니다.


---

### ③ Shared / Common (공통 공유) 코드 폼

이 영역의 코드 폼들은 여러 도메인 폴더에서 공유되어 재사용되는 인프라 모델, 공통 DTO, 전역 미들웨어성 종속성 주입, 공통 클라이언트 등을 담당합니다.

#### 1) [BE-SHARED-MODEL] Shared Database Model (SQLAlchemy ORM)
- **목적**: SQLAlchemy DeclarativeBase 매핑 기본 클래스(`Base`) 및 공통 감사 필드(`TimestampMixin`) 등을 정의합니다.
- **물리 경로**: `apps/backend/src/shared/models.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/shared/models.py
from datetime import datetime
from sqlalchemy import MetaData, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.shared.utils.date_helper import get_utc_now # BE-SHARED-UTIL

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

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=get_utc_now
    )
```

#### 2) [BE-SHARED-DEPENDENCY] Shared Dependency
- **목적**: 사용자 세션 인증 필터링, 데이터베이스 세션 주입 등 전역 및 여러 도메인에서 공용으로 매핑하는 Depends 용도 헬퍼 함수입니다.
- **물리 경로**: `apps/backend/src/shared/dependencies.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/shared/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def valid_active_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 정보가 유효하지 않습니다."
        )
    return {"user_id": "authenticated_user"}
```

#### 3) [BE-SHARED-SCHEMA] Shared Schema (Pydantic Common Schema)
- **목적**: API 응답 봉투(Standard Response Envelope) 구조, 페이지네이션 쿼리 등 전역적으로 공유하는 데이터 구조 규격을 강제합니다.
- **물리 경로**: `apps/backend/src/shared/schemas.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/shared/schemas.py
from pydantic import BaseModel, Field

class PaginationQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)

class ErrorResponse(BaseModel):
    detail: str
```

#### 4) [BE-SHARED-CLIENT] Shared External Client (공통 연동 클라이언트)
- **목적**: 외부 결제, 알림 API 등 백엔드 모듈 전반에서 필요에 따라 가져다 쓰는 외부 연동 HTTP 클라이언트 엔진을 캡슐화합니다.
- **물리 경로**: `apps/backend/src/shared/clients/{client_name}_client.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/shared/clients/payment_client.py
import httpx
from typing import Dict, Any

class PaymentAPIClient:
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url
        self.timeout = timeout

    async def charge(self, amount: int) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.post("/charge", json={"amount": amount})
            response.raise_for_status()
            return response.json()
```

#### 5) [BE-SHARED-EXCEPTION] Shared Exception & Handler (공통 예외)
- **목적**: 커스텀 도메인 비즈니스 예외들의 부모가 되는 기본 예외 계층을 구성하고, FastAPI에 전역 에러 핸들러로 등록하기 위한 모듈 양식입니다.
- **물리 경로**: `apps/backend/src/shared/exceptions.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/shared/exceptions.py
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

#### 6) [BE-SHARED-UTIL] Shared Utility Module (백엔드 공통 유틸)
- **목적**: 암호화 처리, 날짜 연산 등 도메인 제약이 없는 범용적인 Pure 함수 모듈입니다.
- **물리 경로**: `apps/backend/src/shared/utils/{name}.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/backend/src/shared/utils/date_helper.py
from datetime import datetime, timezone

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)
```


---

## 🤖 AI 모듈 코드 폼 (AI Code Forms)

이 절에서는 AI 모듈 코드의 역할을 전역/인프라 영역, 도메인 전용 영역, 공통 공유 영역의 3가지 대분류로 분할하여 관리합니다.

---

### ① Global / Infrastructure (전역 / 인프라) 코드 폼

이 영역의 코드 폼들은 DI 컨테이너 및 생명주기 제어, 모델 하이퍼파라미터 공통 환경 설정 등 AI 서버의 구동 프레임워크 기반을 다룹니다.

#### 1) [AI-BOOTSTRAP] Bootstrap & DI Container (의존성 주입)
- **목적**: 전역 환경 설정을 로드하고, 게이트웨이 및 Usecase 의존성을 단일 지점에서 조립하여 생성합니다.
- **물리 경로**: `apps/ai/src/bootstrap.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/bootstrap.py
from src.fetal_decel.adapter import FetalDecelAdapter # AI-DOMAIN-ADAPTER
from src.fetal_decel.processor import FeatureExtractor # AI-DOMAIN-CORE
from src.fetal_decel.inference import InferenceUsecase # AI-DOMAIN-USECASE

class DIContainer:
    def __init__(self):
        self.model_gateway = FetalDecelAdapter(model_path="models/model.onnx")
        self.extractor = FeatureExtractor()
        
        self.inference_usecase = InferenceUsecase(
            model_gateway=self.model_gateway,
            extractor=self.extractor
        )

container = DIContainer()
```

#### 2) [AI-CONFIG] Model Config & Specs (모델/하이퍼파라미터 설정)
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

---

### ② Domain-specific (도메인 전용) 코드 폼

이 영역의 코드 폼들은 특정 추론/에이전트 비즈니스 도메인 폴더(`src/{domain}/`) 하위에 격리되어, 특정 비즈니스 분석 유스케이스를 처리하는 레이어에 매핑됩니다.

#### 1) [AI-DOMAIN-ROUTER] Inbound Router (추론 API 라우터)
- **목적**: 외부 요청을 수신하여 AI 추론 Usecase를 호출하고 결과를 반환하는 진입점 레이어입니다.
- **물리 경로**: `apps/ai/src/{domain}/router.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/fetal_decel/router.py
from fastapi import APIRouter, Depends, status
from src.bootstrap import container # AI-BOOTSTRAP 절대 경로 참조
from .types import PredictionRequest, PredictionResponse # AI-DOMAIN-TYPE 참조

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

#### 2) [AI-DOMAIN-USECASE] Inference Usecase (추론 오케스트레이터)
- **목적**: Core(전/후처리) 및 Outbound(모델 추론 및 외부 API) 레이어를 조율하여 추론 연산을 오케스트레이션합니다.
- **물리 경로**: `apps/ai/src/{domain}/inference.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/fetal_decel/inference.py
from .types import PredictionRequest, PredictionResponse # AI-DOMAIN-TYPE
from .processor import FeatureExtractor # AI-DOMAIN-CORE
from .adapter import FetalDecelAdapter # AI-DOMAIN-ADAPTER

class InferenceUsecase:
    def __init__(self, model_gateway: FetalDecelAdapter, extractor: FeatureExtractor):
        self.model_gateway = model_gateway
        self.extractor = extractor

    async def execute(self, request: PredictionRequest) -> PredictionResponse:
        # 1. 입력 데이터를 core 분석용 구조로 전처리
        features = self.extractor.extract_features(request.data)
        
        # 2. Outbound Adapter를 통해 실제 모델 추론 수행
        raw_prediction = await self.model_gateway.predict(features)
        
        # 3. 모델 결과 후처리 및 반환
        processed_data = self.extractor.postprocess(raw_prediction)
        return PredictionResponse(result=processed_data)
```

#### 3) [AI-DOMAIN-WORKFLOW] Stateful Workflow (상태/에이전트 제어 흐름)
- **목적**: LangGraph 등 상태 기반 제어 흐름 또는 다단계 프롬프트 체인, 인간 검증(HITL) 단계를 갖는 AI 에이전트/워크플로우 오케스트레이션입니다.
- **물리 경로**: `apps/ai/src/{domain}/process.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/fetal_decel/process.py
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

#### 4) [AI-DOMAIN-CORE] Core Processor (도메인 코어 프로세서)
- **목적**: 원시 특징(Feature) 추출, 텐서 가공, 수학적 수치 분석 및 비즈니스 룰 후처리를 담당하는 Pure Python 비즈니스 도메인 레이어입니다.
- **물리 경로**: `apps/ai/src/{domain}/processor.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/fetal_decel/processor.py
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

#### 5) [AI-DOMAIN-ADAPTER] Domain Model Adapter
- **목적**: 특정 도메인의 로컬 모델 가중치 파일(ONNX/PyTorch 등)을 구동하기 위한 전용 어댑터 레이어입니다.
- **물리 경로**: `apps/ai/src/{domain}/adapter.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/fetal_decel/adapter.py
import onnxruntime as ort
import numpy as np

class FetalDecelAdapter:
    def __init__(self, model_path: str):
        self.session = ort.InferenceSession(model_path)

    async def predict(self, input_tensor: np.ndarray) -> np.ndarray:
        input_name = self.session.get_inputs()[0].name
        output_name = self.session.get_outputs()[0].name
        raw_output = self.session.run([output_name], {input_name: input_tensor})
        return raw_output[0]
```

#### 6) [AI-DOMAIN-PROMPT] Domain Prompt Templates
- **목적**: 특정 AI 태스크 및 에이전트 구동에 특화되어 사용되는 전용 프롬프트 템플릿입니다.
- **물리 경로**: `apps/ai/src/{domain}/prompts.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/fetal_decel/prompts.py
from src.shared.prompts import BASE_SYSTEM_PROMPT # AI-SHARED-PROMPT 참조

DECEL_WARNING_PROMPT = """이전 상태 기록: {history}
현재 신호 입력 시, 발생한 태아 심박수 감속 원인을 임상 지침 양식으로 해석해 주세요.
"""
```

#### 7) [AI-DOMAIN-TYPE] Domain Types (불변 VO 및 DTO)
- **목적**: 특정 도메인 API 통신을 위한 Pydantic DTO나 도메인 전용 frozen dataclass VO를 관리합니다.
- **물리 경로**: `apps/ai/src/{domain}/types.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/fetal_decel/types.py
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    data: list[float]

class PredictionResponse(BaseModel):
    result: str
```

#### 8) [AI-DOMAIN-EXCEPTION] Domain Inference Exception
- **목적**: 특정 모델 추론의 타임아웃, 포맷 불일치 등 해당 도메인에 특화된 비즈니스 예외군입니다.
- **물리 경로**: `apps/ai/src/{domain}/exceptions.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/fetal_decel/exceptions.py
from src.shared.exceptions import InferenceEngineException # AI-SHARED-EXCEPTION 상속

class DecelModelTimeoutException(InferenceEngineException):
    def __init__(self):
        super().__init__(
            detail="감속 판정 모델 로드 및 추론 시간이 초과되었습니다.",
            model_name="fetal_decel_onnx",
            status_code=504
        )
```

#### 9) [AI-DOMAIN-UTIL] Domain Utility Module
- **목적**: 특정 AI 추론 연산 내부에서만 제한적으로 활용되는 가공/수학적 연산 헬퍼 모듈입니다.
- **물리 경로**: `apps/ai/src/{domain}/utils.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/fetal_decel/utils.py
import numpy as np

def interpolate_missing_signals(signals: np.ndarray) -> np.ndarray:
    # 데이터 유실 구간 보간 로직
    return signals
```

#### 10) [AI-DOMAIN-ROUTER-TEST] Inbound Router Integration Test
- **목적**: 추론 서버의 진입점 API 라우터([AI-DOMAIN-ROUTER])의 데이터 형식 수신 규격 및 분류 결과를 통합 검증하는 테스트 양식입니다.
- **물리 경로**: `apps/ai/tests/integration/test_router.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/tests/integration/test_router.py
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_predict_endpoint_success(client: AsyncClient):
    # [Given] Generic input payload matching PredictionRequest schema
    payload = {
        "data": [0.1, 0.2, 0.3]
    }
    
    # [When] Post inference request
    response = await client.post("/predict", json=payload)
    
    # [Then] Verify status code and classification result
    assert response.status_code == 200
    res_data = response.json()
    assert "result" in res_data
```
- **준수 사항 (Do's & Don't's)**:
  -  엔드포인트 연동 테스트 시에는 가벼운 가상 입력 패킷(Synthetic dataset)을 모킹하거나 더미 데이터를 사용하여 모델 로드 오버헤드를 줄이십시오.

#### 11) [AI-DOMAIN-CORE-TEST] Core Processor Unit Test
- **목적**: 데이터 전/후처리를 관장하는 코어 프로세서([AI-DOMAIN-CORE])의 신호 처리 알고리즘, 특징 추출(Feature Engineering) 수치 연산을 모킹 없이 격리 검증하는 순수 단위 테스트 양식입니다.
- **물리 경로**: `apps/ai/tests/unit/test_{name}.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/tests/unit/test_feature_engineering.py
import pytest
import numpy as np
from src.fetal_decel.processor import FeatureExtractor

def test_feature_extraction_correct_dimensions():
    # 1. Setup - Instantiate pure processor
    extractor = FeatureExtractor()
    raw_data = [0.1, 0.2, 0.3]
    
    # 2. Action - Extract features
    features = extractor.extract_features(raw_data)
    
    # 3. Assertion - Validate shape and exact mathematical outcome
    assert isinstance(features, np.ndarray)
    assert features.shape == (1, 3)
    assert np.allclose(features, np.array([[0.1, 0.2, 0.3]], dtype=np.float32))

def test_feature_extraction_empty_input_raises_value_error():
    extractor = FeatureExtractor()
    
    # Assert negative/exception paths
    with pytest.raises(ValueError, match="원시 데이터는 필수입니다."):
        extractor.extract_features([])
```
- **준수 사항 (Do's & Don't's)**:
  - 🛑 코어 프로세서는 입력에 따른 수학적 결과만 내보내는 순수 함수/클래스로 구성되므로, **테스트 내에서 어떠한 Mock 객체 사용도 엄격히 금지**합니다. 실제 Numpy Array를 가공하여 단언(Assert)해야 합니다.


---

### ③ Shared / Common (공통 공유) 코드 폼

이 영역의 코드 폼들은 여러 도메인 추론기에서 공유하여 참조하는 공통 LLM API 어댑터, 시스템 기본 프롬프트, 공통 타입 설정 및 유틸리티 등을 담당합니다.

#### 1) [AI-SHARED-ADAPTER] Shared API/Model Adapter
- **목적**: OpenAI, Claude 등 외부 상용 LLM API 호출 인터페이스 및 공통 Rate Limit/Retry 설정을 제공하는 공유 어댑터입니다.
- **물리 경로**: `apps/ai/src/shared/adapters/{name}_adapter.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/shared/adapters/openai_adapter.py
import httpx

class OpenAIAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def call_llm(self, prompt: str) -> str:
        # OpenAI Chat API 호출 및 예외 처리 캡슐화
        return "LLM Response Sample"
```

#### 2) [AI-SHARED-PROMPT] Shared Prompt Templates
- **목적**: 시스템 기본 페르소나 설정 등 여러 태스크 에이전트가 상속/공용하여 빌드하는 프롬프트 템플릿입니다.
- **물리 경로**: `apps/ai/src/shared/prompts.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/shared/prompts.py
BASE_SYSTEM_PROMPT = """당신은 의료 임상 데이터 분석을 지원하는 전문 의학 AI 비서입니다.
주어진 물리 생체 신호 데이터 분석 양식에 맞춰 감지 결과를 보고하십시오.
"""
```

#### 3) [AI-SHARED-TYPE] Shared Types
- **목적**: 공통 텐서 쉐이프 설정값 및 다단계 워크플로우에 공유되는 기본 상태 데이터 타입 선언 모듈입니다.
- **물리 경로**: `apps/ai/src/shared/types.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/shared/types.py
from typing import TypedDict

class CommonTensorShape(TypedDict):
    batch_size: int
    channels: int
    seq_len: int
```

#### 4) [AI-SHARED-EXCEPTION] Shared AI Exception & Handler (공통 AI 예외)
- **목적**: 가중치 로딩 실패, API 제한 초과 등 AI 서버 전반의 공통 오류 클래스를 구축하고 처리합니다.
- **물리 경로**: `apps/ai/src/shared/exceptions.py`
- **구조 예시 및 템늘릿**:
```python
# Path: apps/ai/src/shared/exceptions.py
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

#### 5) [AI-SHARED-UTIL] Shared Utility Module (AI 공통 유틸)
- **목적**: 특수문자 제거 정규화, 공용 텐서 배열 포맷 처리 등 도메인 경계가 없는 pure 헬퍼 연산 파일입니다.
- **물리 경로**: `apps/ai/src/shared/utils/{name}.py`
- **구조 예시 및 템플릿**:
```python
# Path: apps/ai/src/shared/utils/text_helper.py
import re

def clean_text(text: str) -> str:
    cleaned = re.sub(r"[^\w\s]", "", text)
    return cleaned.strip()
```

---

## 4. 🔄 컴포넌트 및 모듈 추출/승격 기준 (Component & Module Extraction & Promotion Criteria)

모든 서브프로젝트 개발 시 에이전트는 중복 코드를 무분별하게 양산하거나 반대로 불필요한 추상화를 조기에 도입(Premature Abstraction)하지 않도록 아래의 정량적 **추출(Extraction) 및 승격(Promotion) 기준**을 반드시 준수해야 합니다.

### ① 🖥️ 프론트엔드 (Frontend) 컴포넌트 및 모듈 진화 규칙

프론트엔드에서는 **"컴포넌트 크기"**, **"단일 책임(SRP)"**, 그리고 **"재사용 횟수"**를 기준으로 모듈화를 단계적으로 진화시킵니다.

1. **인라인 구현 (Inline Stage)**:
   - 새로운 피처 작성 시에는 빠른 구현과 결합력 확인을 위해 하나의 컴포넌트 파일 안에 서브 요소를 인라인(Inline) 함수나 로컬 상태로 구현합니다.
2. **피처 컴포넌트 추출 (Extract to [FE-FEATURE-COMP])**:
   - **트리거**:
     - 동일 피처 내에서 코드가 **1회 이상 중복**되어 사용될 때.
     - 단일 컴포넌트 파일의 총 라인 수가 **150라인을 초과**할 때.
     - 컴포넌트가 **서로 다른 두 개 이상의 상태 흐름이나 큰 비즈니스 관심사**를 한꺼번에 처리할 때 (단일 책임 원칙 위배).
   - **조치**: 해당 피처 폴더(`features/{feature}/components/`) 아래에 개별 파일로 분리합니다.
3. **공통 컴포넌트 승격 (Promote to [FE-SHARED-COMP])**:
   - **트리거**: **2개 이상의 독립된 피처**(`features/A`, `features/B`)에서 동일한 UI 요소 및 기능의 공유가 요구될 때.
   - **조치**: `src/components/ui/` 또는 `src/components/shared/` 하위로 파일을 이관합니다.
   - **🛑 필수 제약조건 (의존성 제거)**: 공통 컴포넌트로 승격할 때는 **특정 피처에 종속된 비즈니스 쿼리(React Query), 전역 상태 스토어(Zustand), 혹은 라우터 종속성(useParams 등)을 내부에서 직접 참조해서는 안 됩니다**. 모든 제어 인터페이스는 오직 외부 Props(예: `variant`, `size`, `children` 등) 기반의 범용 API로 재정리(Decoupling)되어야 합니다.
4. **하위 비즈니스 로직 추출 (Extract to [FE-FEATURE-HOOK/UTIL])**:
   - **트리거**: 서로 다른 컴포넌트가 전혀 다른 UI 마크업(HTML/CSS)을 그리지만, **내부 상태 변경 로직이나 복잡한 계산식 등의 비즈니스 공식이 중복**될 때.
   - **조치**: 로직만을 훅(`[FE-FEATURE-HOOK]`)이나 유틸리티 함수(`[FE-FEATURE-UTIL]`)로 분할 추출하고, 컴포넌트들은 이를 가져다 쓰는 형태로 리팩토링합니다.

---

### ② ⚙️ 백엔드 (Backend) 서비스 및 인프라 모듈 진화 규칙

백엔드에서는 **"비즈니스 공식의 크기"**와 **"인프라 관심사의 중복"**을 기준으로 진화시킵니다.

1. **라우터 인라인 구현 (Inline Stage)**:
   - 단순한 데이터베이스 단일 조회, 혹은 1단계 수준의 간단한 CRUD는 서비스 클래스를 만들지 않고 라우터(`router.py`) 함수 내부에 인라인 코드로 작성할 수 있습니다.
2. **도메인 서비스 추출 (Extract to [BE-DOMAIN-SERVICE])**:
   - **트리거**:
     - 비즈니스 로직이 **2단계 이상의 데이터베이스 트랜잭션**을 묶어서 실행할 때.
     - 라우터 내 비즈니스 공식 코드가 **5줄을 초과**할 때.
     - **둘 이상의 라우터 엔드포인트**에서 동일한 비즈니스 계산식을 실행해야 할 때.
   - **조치**: 서비스 클래스(Usecase)로 들어내어 비즈니스 책임을 격리시킵니다.
3. **값 객체 및 도메인 유틸 분리 (Extract to [BE-DOMAIN-VO/UTIL])**:
   - **트리거**: 데이터 입력에 대한 비즈니스 무결성 조건 검증(Validation)이 중복되거나, 순수한 데이터 포맷팅 코드가 겹칠 때.
   - **조치**: 값 객체(`[BE-DOMAIN-VO]`)로 감싸 무결성 검사 책임을 부여하거나, `utils.py`의 순수 함수로 추출합니다.
4. **공통 인프라 모듈 승격 (Promote to [BE-SHARED-CLIENT/DEPENDENCY])**:
   - **트리거**: 2개 이상의 독립 도메인에서 동일한 서드파티 통신 클라이언트(SDK, Mail API 등)나 전역 보안 필터링(Depends)이 필요할 때.
   - **조치**: `shared/clients/` 또는 `shared/dependencies.py` 등의 전역 공유 모듈로 승격 이관합니다.

---

### ③ 🤖 AI 서버 (AI Module) 레이어 및 유틸 진화 규칙

AI 추론기 및 에이전트 서비스에서는 **"추론 엔진의 결합도"**와 **"전처리 연산의 공용성"**을 기준으로 진화시킵니다.

1. **단일 스크립트 구현 (Inline Stage)**:
   - 새로운 분석 가중치 모델의 초기 성능 검증 및 테스트 시에는 `main.py`나 배치 스크립트 하나에 전처리, 추론, 후처리 로직 전체를 인라인으로 작성하여 확인합니다.
2. **핵심 연산 및 추론 격리 (Extract to [AI-DOMAIN-CORE/ADAPTER])**:
   - **트리거**: 입력 특징(Feature) 추출 알고리즘과 ONNX/PyTorch 등의 런타임 세션 구동 코드가 섞여 **추론기 엔진 없이 데이터 전처리만 따로 단위 테스트하기가 불가능**할 때.
   - **조치**: 전/후처리 로직은 `processor.py`(`[AI-DOMAIN-CORE]`)로, 가중치 구동 코드는 어댑터(`adapter.py` - `[AI-DOMAIN-ADAPTER]`)로 레이어를 물리적으로 격리 추출합니다.
3. **공통 전처리 모듈 승격 (Promote to [AI-SHARED-UTIL])**:
   - **트리거**: 서로 다른 AI 추론 파이프라인에서 동일한 신호 정규화(Normalization), 데이터 보간(Interpolation) 연산을 실행할 때.
   - **조치**: `shared/utils/` 하위의 전역 유틸 모듈로 이동시켜 공통 상속받아 사용하게 합니다.



