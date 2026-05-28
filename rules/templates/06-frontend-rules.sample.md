---
description: 프론트엔드 UI/UX 설계, Feature-First 아키텍처 및 Bulletproof React 준수 규칙
glob: "apps/frontend/**/*"
---
# 6. 프론트엔드(Frontend) 개발 가이드레일

본 규칙은 **[Bulletproof React](https://github.com/alan2207/bulletproof-react)**의 베스트 프랙티스를 기반으로 하며, 프론트엔드 애플리케이션의 높은 유지보수성, 확장성, 그리고 기능(Feature) 단위의 캡슐화를 보장하기 위해 AI 에이전트가 반드시 준수해야 하는 지침입니다.

---

## 1. UI 스타일링 및 컴포넌트 라이브러리 규칙

### ① 디자인 시스템 및 스타일링 규칙
- **디자인 토큰 사용**: 하드코딩된 색상값(`color: #ff5722`), 마진/패딩 수치(`margin: 13px`)를 직접 사용하는 것을 금지합니다. 반드시 프로젝트에 정의된 Tailwind 테마 또는 디자인 토큰(CSS Variables)을 사용해야 합니다.
  * 예: `text-primary-500`, `bg-neutral-100`, `p-4`, `m-2`
- **임의 값(Arbitrary values) 제한**: `w-[347px]`와 같은 임의 스타일은 레이아웃 컴포넌트나 외부 미디어 크기 조절 등 꼭 필요한 예외 상황을 제외하고 사용하지 마십시오.
- **반응형 디자인**: 모든 레이아웃 및 주요 컴포넌트는 기본적으로 모바일 우선(Mobile-First) 또는 반응형 중단점(`sm:`, `md:`, `lg:`, `xl:`)을 고려하여 작성해야 합니다.
- **스타일링 솔루션**: 스타일링 방식을 다수 혼용하지 말고, 프로젝트에 정의된 기술 스택에 맞춰 단일 또는 합의된 스택(Tailwind CSS, CSS Modules, styled-components, Panda CSS 등)을 일관되게 사용하십시오. React Server Components(RSC)를 활용하는 경우, 스타일 연산 비용을 줄이기 위해 zero-runtime 스타일링 방식(예: Tailwind, CSS Modules)을 우선적으로 사용합니다.

### ② 컴포넌트 라이브러리 선택 규칙
프로젝트의 요구사항에 맞게 검증된 UI 컴포넌트 라이브러리를 활용하되, 직접 구현하는 범위를 최소화합니다.
- **완성형 스타일 라이브러리 (Fully Featured)**: 스타일이 미리 정의되어 빠른 프로토타이핑이나 일관된 UI 구축에 유리한 라이브러리입니다.
  - **MUI (Material UI)**: React에서 가장 널리 사용되며 정형화된 머티리얼 디자인 구현에 적합합니다. (Unstyled/Headless 기능도 지원)
  - **Chakra UI**: 훌륭한 개발자 경험(DX)과 사용자 커스텀 유연성 및 접근성(a11y)을 내장하고 있습니다.
  - **Mantine / Ant Design**: 다양한 컴포넌트와 대시보드 등에 최적화된 컴포넌트를 제공합니다.
- **헤드리스 라이브러리 (Headless)**: 스타일이 입혀져 있지 않아 디자이너가 정의한 커스텀 디자인 시스템을 유연하게 구현해야 할 때 적합합니다.
  - **Radix UI / Headless UI / Base UI / Ark UI / react-aria** 등
- **코드 복사형 컴포넌트 (Code-based / Copy & Paste)**: 패키지 설치 방식이 아닌 소스 코드를 프로젝트에 복사해 와서 직접 커스터마이징하여 사용하는 스타일 솔루션입니다.
  - **Shadcn UI (Tailwind 기반) / Park UI (Panda CSS 기반)** 등

### ③ Storybook 활용 규칙 (컴포넌트 독립 개발)
- UI 컴포넌트는 단독적인 환경에서 테스트 및 개발이 가능하도록 **Storybook**을 적극 활용해 카탈로그화하여 관리할 것을 권장합니다.
- 새로운 공통 UI 컴포넌트를 설계할 때는 이에 대응하는 Storybook 파일(`.stories.tsx`)을 함께 작성하여 발견 가능성(Discoverability)을 높이십시오.

---

## 2. 컴포넌트 설계 및 베스트 프랙티스 (Components Best Practices)
컴포넌트의 가독성, 렌더링 성능 및 유지보수성을 극대화하기 위해 다음 설계 표준을 따릅니다.

### ① 연관 코드의 인접 배치 (Colocation)
- **가까이 두기**: 컴포넌트, 유틸리티 함수, 스타일, 상태 등은 **사용되는 위치와 가장 가까운 곳에 위치**시키십시오.
- 전역으로 분리할 필요가 없는 로컬 컴포넌트나 로컬 훅은 해당 feature 또는 상위 컴포넌트와 동일한 폴더 내에 배치하여 불필요한 파일 찾기를 방지하고, 불필요한 리렌더링을 줄여 성능을 향상시킵니다.

### ② 중첩 렌더링 함수 작성 금지
- 하나의 컴포넌트 파일 내에서 UI 일부를 렌더링하는 중첩된 헬퍼 함수(예: `renderItems()`)를 작성하지 마십시오. 이는 컴포넌트가 커질 때 유지보수를 매우 어렵게 만듭니다.
- 렌더링해야 할 UI 단위가 명확하다면 **별도의 독립적인 서브 컴포넌트로 추출**하여 분리하십시오.
  * ❌ **나쁜 예 (유지보수가 어려운 구조)**:
    ```javascript
    function Component() {
      function renderItems() {
        return <ul>...</ul>;
      }
      return <div>{renderItems()}</div>;
    }
    ```
  *  **올바른 예 (독립된 컴포넌트로 추출)**:
    ```javascript
    function Items() {
      return <ul>...</ul>;
    }
    function Component() {
      return (
        <div>
          <Items />
        </div>
      );
    }
    ```

### ③ 일관성 유지 (Stay Consistent)
- 프로젝트 전역에서 동일한 코드 스타일과 네이밍 컨벤션을 유지하십시오. (예: React 컴포넌트 파일 및 이름은 항상 PascalCase 등)
- 이러한 일관성은 ESLint와 Prettier 등의 도구를 통해 자동화되어 검증되어야 합니다.

### ④ Props 개수 제한 및 합성(Composition) 활용
- 컴포넌트가 받아들이는 Props의 개수가 너무 많아지면(예: 7~8개 이상), 컴포넌트를 더 작은 단위로 분리하거나 `children` 또는 `slots`를 이용한 **컴포넌트 합성(Composition) 기법**을 활용해 단순화하십시오.

### ⑤ 공통 UI 컴포넌트의 추상화 및 3rd Party 라이브러리 래핑
- **공통 컴포넌트 라이브러리화 (`src/components/`)**: 프로젝트 전역에서 반복 사용되는 범용 컴포넌트(Button, Input, Modal, Table 등)는 비즈니스 로직을 배제하고 스타일과 기본 마크업만 담은 공통 컴포넌트로 추상화하여 관리하십시오.
- **외부(3rd Party) 라이브러리 래핑**: 외부 UI 라이브러리나 툴(예: 외부 링크 컴포넌트 등)을 사용할 때는 이를 직접 사용하지 말고, **프로젝트 공통 컴포넌트로 한 번 감싸서(Wrapping) 사용**하십시오. 이를 통해 미래에 라이브러리를 변경하거나 변경 사항이 생겼을 때, 애플리케이션의 핵심 비즈니스 로직에 영향을 주지 않고 한 곳에서 쉽게 제어할 수 있습니다.

### ⑥ 바렐 파일(index.ts) 사용 제약 및 직접 참조 권장
- 과거에는 기능(Feature) 내의 모든 파일을 루트의 `index.ts` (바렐 파일)로 한데 모아 export하는 방식이 권장되었습니다.
- 하지만 번들러 및 빌드 도구(특히 Vite) 환경에서는 바렐 파일의 남용이 **트리 셰이킹(Tree Shaking) 동작을 방해하고 빌드 성능 저하**를 일으킬 수 있습니다.
- 따라서 feature 내부의 개별 컴포넌트나 훅을 가져올 때는 바렐 파일을 통한 일괄 노출보다는 **해당 파일 경로를 직접 지정하여 임포트(Direct Import)하는 것을 권장**합니다.

### ⑦ 에셋 및 아이콘 사용 규칙
- **인라인 SVG 금지**: 컴포넌트 내부에 수십 줄에 달하는 raw SVG 코드를 직접 인라인으로 하드코딩하지 마십시오.
- **아이콘 단일화**: 프로젝트가 제공하는 통합 아이콘 팩(예: `lucide-react`, `react-icons` 등)을 우선 사용하거나, 커스텀 SVG는 별도 파일로 분리하여 React 컴포넌트로 import해서 사용하십시오.

### ⑧ 이벤트 핸들러 명명 규칙
- **콜백 Props**: 부모에게 전달하는 이벤트 콜백 Prop 명은 **`on[Action]`** 규칙을 따릅니다. (예: `onClose`, `onSubmit`, `onSelect`)
- **내부 핸들러**: 컴포넌트 내부에서 이벤트를 핸들링하는 함수명은 **`handle[Action]`** 규칙을 따릅니다. (예: `handleClose`, `handleSubmit`, `handleSelect`)

### ⑨ 리스트 렌더링 최적화
- **고유 Key 사용**: `map()`을 사용해 리스트를 렌더링할 때 배열의 index를 `key`로 사용하지 마십시오. 리스트 순서의 동적 변경이나 필터링 발생 시 예기치 못한 버그를 방지하기 위해 반드시 고유 식별자(예: `item.id`)를 `key`로 부여해야 합니다.

---

## 3. 프로젝트 디렉토리 구조 및 Feature-First 규칙

### ① 프로젝트 전체 디렉토리 구조 (Project Structure)
대부분의 애플리케이션 코드는 `src` 디렉토리 하위에 위치하며, 유지보수성과 일관성을 위해 다음과 같은 표준 구조를 따릅니다.

```sh
src
├── app               # 애플리케이션 레이어 (라우트/페이지 정의, app.tsx, 글로벌 프로바이더 등)
│   ├── routes        # 애플리케이션 라우트 / 페이지 컴포넌트
│   ├── app.tsx       # 애플리케이션 메인 루트 컴포넌트
│   ├── provider.tsx  # 전체 애플리케이션을 감싸는 글로벌 프로바이더 설정
│   └── router.tsx    # 라우터 설정 (React Router 등)
├── assets            # 정적 에셋 (이미지, 폰트 등)
├── components        # 애플리케이션 전역에서 공유되는 공통 UI 컴포넌트 (Shared)
├── config            # 글로벌 환경 설정 및 환경 변수 내보내기
├── features          # 비즈니스 도메인별 기능 중심 모듈 (Core)
├── hooks             # 애플리케이션 전역에서 공유되는 공통 커스텀 훅
├── lib               # 특정 라이브러리의 사전 설정 및 클라이언트 (Axios, React Query 등)
├── stores            # 애플리케이션 전역 상태 저장소 (Zustand 등)
├── testing           # 테스트용 유틸리티 및 모의 데이터 (Mocks)
├── types             # 전역 공유 TypeScript 타입 정의
└── utils             # 전역 공유 유틸리티 함수
```
*참고: 메타 프레임워크(Next.js, Remix 등)를 사용하는 경우 `app` 폴더 등의 구성이 프레임워크의 사양에 따라 일부 달라질 수 있습니다.*

### ② Feature-First 디렉토리 구조
애플리케이션의 손쉬운 확장과 독립적인 관리를 위해, 핵심 비즈니스 로직은 기술 계층이 아닌 `features/` 디렉토리 하위에 도메인 단위로 구조화합니다.

각 개별 기능(Feature) 폴더는 다음과 같은 내부 구조를 가질 수 있습니다:
```sh
src/features/[feature-name]
├── api         # 해당 기능 전용 API 요청 및 React Query 훅
├── assets      # 해당 기능 전용 정적 에셋
├── components  # 해당 기능 내에서만 재사용되는 로컬 컴포넌트
├── hooks       # 해당 기능 내에서만 사용되는 로컬 커스텀 훅
├── stores      # 해당 기능 전용 상태 저장소 (Zustand 스토어 등)
├── types       # 해당 기능 내부에서 사용되는 TypeScript 타입 정의
└── utils       # 해당 기능 전용 로컬 유틸리티 함수
```
> **[주의]** 모든 기능 폴더가 위 디렉토리를 모두 가질 필요는 없습니다. 해당 기능 구현에 **필요한 폴더만 생성**하여 사용하십시오.
> 
> *예외 상황*: 여러 기능 간에 공통으로 자주 호출되는 API가 많아 관리가 복잡해질 경우, 예외적으로 모든 API 호출을 `features` 폴더 외부의 글로벌 `src/api` 디렉토리로 모아서 정의하는 방식이 더 실용적일 수 있습니다.

---

## 4. 수평 참조 금지 및 단방향 아키텍처 규칙
코드베이스가 꼬이고 복잡해지는 것을 막기 위해, 기능(Feature) 간 수평적 직접 임포트를 제한하고 단방향 흐름을 유지해야 합니다.

### ① 기능 간 수평 임포트 금지 (Forbidden Cross-Feature Imports)
- 각 feature는 다른 feature의 코드를 직접 임포트하여 강하게 결합해서는 안 됩니다.
- 여러 기능이 결합되어야 하는 시나리오는 개별 feature 내부가 아닌, 상위 애플리케이션 레이어(`src/app/` 또는 `src/routes/`)에서 조립(Compose)되도록 설계해야 합니다.
- 이를 강제하기 위해 아래와 같이 ESLint 규칙(`import/no-restricted-paths`)을 설정합니다:
  ```js
  'import/no-restricted-paths': [
      'error',
      {
          zones: [
              // 기능(Feature) 간의 수평 참조를 금지합니다.
              { target: './src/features/auth', from: './src/features', except: ['./auth'] },
              { target: './src/features/comments', from: './src/features', except: ['./comments'] },
              { target: './src/features/discussions', from: './src/features', except: ['./discussions'] },
              { target: './src/features/teams', from: './src/features', except: ['./teams'] },
              { target: './src/features/users', from: './src/features', except: ['./users'] },
              // 추가적인 피처 제한 규칙들...
          ],
      },
  ],
  ```

### ② 단방향 아키텍처 규칙 (Unidirectional Codebase)
- 코드의 흐름은 예측 가능성을 높이기 위해 오직 한 방향으로만 흘러야 합니다: **`Shared` ➔ `Features` ➔ `App`**
  - **Shared 모듈**(`components`, `hooks`, `lib`, `types`, `utils`)은 애플리케이션의 모든 영역에서 임포트할 수 있습니다.
  - **Features 모듈**은 오직 `Shared` 모듈에서만 임포트할 수 있으며, 상위 레이어(`app`)를 임포트할 수 없습니다.
  - **App 레이어**는 `Features`와 `Shared` 모듈 모두를 임포트하여 조립할 수 있습니다.
- 이를 강제하기 위한 ESLint 설정 예시:
  ```js
  'import/no-restricted-paths': [
      'error',
      {
          zones: [
              // 이전 기능 간 제한 규칙에 이어서 적용...
              
              // 1. Features에서 상위 App 레이어 임포트 금지
              { target: './src/features', from: './src/app' },
              
              // 2. Shared 모듈에서 Features 및 App 레이어 임포트 금지
              {
                  target: [
                      './src/components',
                      './src/hooks',
                      './src/lib',
                      './src/types',
                      './src/utils',
                  ],
                  from: ['./src/features', './src/app'],
              },
          ],
      },
  ],
  ```

---

## 5. API 계층 및 데이터 페칭 규칙 (API Layer)
애플리케이션과 서버 간의 모든 통신은 일관된 예외 처리, 보안 인터셉션, 그리고 예측 가능한 데이터 상태 관리를 위해 격리된 API 레이어를 통해 처리되어야 합니다.

### ① 단일 API 클라이언트 인스턴스 사용
- REST 또는 GraphQL API와 통신할 때, 사전 설정이 적용된 **단일 API 클라이언트 인스턴스를 재사용**하십시오.
- 프로젝트 전역에서 사용할 공통 클라이언트(예: `src/lib/api-client.ts`)를 선언하고, 기본 URL 설정, 헤더 인터셉터, 401 미인증 상태 시 로그인 페이지 리다이렉트, 에러 공통 알림(Notification) 등의 인터셉터 로직을 한 곳에 집중시키십시오.

* **API 클라이언트 구성 예시 (`src/lib/api-client.ts`)**:
  ```typescript
  import Axios, { InternalAxiosRequestConfig } from 'axios';
  import { useNotifications } from '@/components/ui/notifications';
  import { env } from '@/config/env';
  import { paths } from '@/config/paths';

  function authRequestInterceptor(config: InternalAxiosRequestConfig) {
    if (config.headers) {
      config.headers.Accept = 'application/json';
    }
    config.withCredentials = true;
    return config;
  }

  export const api = Axios.create({
    baseURL: env.API_URL,
  });

  api.interceptors.request.use(authRequestInterceptor);
  api.interceptors.response.use(
    (response) => {
      return response.data;
    },
    (error) => {
      const message = error.response?.data?.message || error.message;
      useNotifications.getState().addNotification({
        type: 'error',
        title: 'Error',
        message,
      });

      if (error.response?.status === 401) {
        const searchParams = new URLSearchParams();
        const redirectTo = searchParams.get('redirectTo') || window.location.pathname;
        window.location.href = paths.auth.login.getHref(redirectTo);
      }

      return Promise.reject(error);
    },
  );
  ```

### ② 요청 선언(Request Declarations)의 구조적 정의 및 내보내기
- 컴포넌트 내부에서 온더플라이(On-the-fly)로 API 요청을 하드코딩하여 호출하지 마십시오.
- 모든 API 요청은 피처별 `api/` 디렉토리에 명확하게 구조화하여 정의해야 합니다. 모든 요청 선언은 다음 3가지 요소를 포함해야 합니다:
  1. **데이터 검증 스키마 및 타입**: Zod 스키마를 활용하여 요청(Request)/응답(Response) 데이터 규격을 검증하고 TypeScript 타입을 추론(`z.infer`)합니다.
  2. **페처(Fetcher) 함수**: 설정된 공통 API 클라이언트 인스턴스(`api`)를 사용하여 엔드포인트를 호출하는 순수 함수를 정의합니다.
  3. **커스텀 데이터 페칭 훅**: 페처 함수를 래핑하고 React Query (`useQuery` 또는 `useMutation`) 위에 구축되어 캐싱, 유효성 검사, 캐시 무효화(Invalidation) 상태를 관리하는 훅을 노출합니다.

* **요청 선언 예시 - Mutation (`features/[feature-name]/api/create-discussion.ts`)**:
  ```typescript
  import { useMutation, useQueryClient } from '@tanstack/react-query';
  import { z } from 'zod';
  import { api } from '@/lib/api-client';
  import { MutationConfig } from '@/lib/react-query';
  import { Discussion } from '@/types/api';
  import { getDiscussionsQueryOptions } from './get-discussions';

  // 1. Zod 입력 유효성 검사 스키마 및 타입 정의
  export const createDiscussionInputSchema = z.object({
    title: z.string().min(1, 'Required'),
    body: z.string().min(1, 'Required'),
  });

  export type CreateDiscussionInput = z.infer<typeof createDiscussionInputSchema>;

  // 2. API 클라이언트를 사용하는 순수 페처(Fetcher) 함수
  export const createDiscussion = ({
    data,
  }: {
    data: CreateDiscussionInput;
  }): Promise<Discussion> => {
    return api.post(`/discussions`, data);
  };

  type UseCreateDiscussionOptions = {
    mutationConfig?: MutationConfig<typeof createDiscussion>;
  };

  // 3. React Query 래퍼 훅 (캐시 무효화 및 성공 콜백 처리 포함)
  export const useCreateDiscussion = ({
    mutationConfig,
  }: UseCreateDiscussionOptions = {}) => {
    const queryClient = useQueryClient();
    const { onSuccess, ...restConfig } = mutationConfig || {};

    return useMutation({
      onSuccess: (...args) => {
        // 성공 시 관련 Discussions 쿼리 캐시를 무효화하여 자동 새로고침 처리
        queryClient.invalidateQueries({
          queryKey: getDiscussionsQueryOptions().queryKey,
        });
        onSuccess?.(...args);
      },
      ...restConfig,
      mutationFn: createDiscussion,
    });
  };
  ```

---

## 6. 상태 관리 전략 및 분류 규칙 (State Management)
효율적인 렌더링 성능과 유지보수를 위해, 모든 상태를 하나의 중앙 저장소에 넣지 말고 상태의 **성격과 사용 범위에 따라 다음과 같이 분류하여 관리**해야 합니다.

### ① 컴포넌트 상태 (Component State)
- 특정 단일 컴포넌트 내부에서만 폐쇄적으로 쓰이는 상태입니다.
- 필요한 경우 자식 컴포넌트에 Props로 전달할 수 있으나, 전역적으로 공유해서는 안 됩니다.
- 처음에는 컴포넌트 내부에서 상태를 좁게 정의하고, 필요한 경우에만 점진적으로 상위 컴포넌트로 끌어올리십시오(State Lifting).
  * **`useState`**: 서로 독립적이고 단순한 값의 상태 관리에 사용합니다.
  * **`useReducer`**: 하나의 행동(Action)에 의해 여러 상태값이 동시에 복잡하게 연동되어 변경되어야 할 때 사용합니다.

### ② 애플리케이션 상태 (Application State)
- 전역 모달 제어, 알림(Notifications), 컬러 모드(Dark/Light) 토글 등 애플리케이션 전역의 UI 동작을 관리하는 글로벌 상태입니다.
- 초기 단계부터 모든 상태를 성급하게 전역화하지 말고, 상태가 필요한 컴포넌트 트리와 가장 가깝게 위치(Localize)시키는 것을 우선으로 합니다.
- **추천 솔루션**: **Zustand**, Context API + 커스텀 훅, Redux Toolkit, Jotai 등
  * 전역 알림(Notifications) 관리를 위해 Zustand를 사용하는 예시입니다. Axios 등 React 외부 영역에서도 스토어에 접근해 액션을 수행할 수 있습니다.

* **글로벌 상태 예시 (`src/stores/notifications.ts` 또는 유사 경로)**:
  ```typescript
  import { create } from 'zustand';

  export type Notification = {
    id: string;
    type: 'info' | 'warning' | 'success' | 'error';
    title: string;
    message?: string;
  };

  type NotificationsStore = {
    notifications: Notification[];
    addNotification: (notification: Omit<Notification, 'id'>) => void;
    dismissNotification: (id: string) => void;
  };

  export const useNotifications = create<NotificationsStore>((set) => ({
    notifications: [],
    addNotification: (notification) =>
      set((state) => ({
        notifications: [
          ...state.notifications,
          { id: Math.random().toString(36).substring(2, 9), ...notification },
        ],
      })),
    dismissNotification: (id) =>
      set((state) => ({
        notifications: state.notifications.filter((n) => n.id !== id),
      })),
  }));
  ```

### ③ 서버 캐시 상태 (Server Cache State)
- API 서버로부터 받아온 데이터로, 나중에 재사용하기 위해 클라이언트 사이드에 캐싱해두는 로컬 데이터입니다.
- 원격 데이터를 Redux나 Zustand 같은 UI 상태 관리 스토어에 직접 수동으로 매핑하여 저장하지 마십시오.
- **추천 라이브러리**: **React Query (TanStack Query)**, SWR, RTK Query 등
- 데이터 페칭, 캐시 만료, 자동 백그라운드 갱신, 가비지 컬렉션 등의 비즈니스 로직은 이러한 전용 데이터 캐싱 라이브러리에 위임하십시오. (예시: `## 5`의 `useCreateDiscussion` 및 쿼리 무효화 구조 활용)

### ④ URL 상태 (URL State)
- 브라우저 주소창에 저장 및 조작되는 동적 데이터입니다.
- URL 파라미터(예: `/app/:id`) 또는 쿼리 파라미터(예: `/app?tab=profile&page=2`) 형태로 관리됩니다.
- 상태 관리를 위해 React 상태를 정의하는 대신, **React Router (`react-router-dom`)** 등의 라우팅 라이브러리 훅(`useParams`, `useSearchParams`)을 활용하여 URL로부터 상태를 직접 읽고 제어하도록 구현하십시오.

---

## 7. 글로벌 프로바이더 및 로딩/에러 대응 규칙 (AppProvider & Error Handling)

### ① 글로벌 프로바이더 패키징 (AppProvider)
- **중첩 프로바이더 정리**: `main.tsx`나 `App.tsx`가 수많은 Context Provider(QueryClientProvider, RouterProvider, ThemeProvider 등)로 중첩되는 "Provider Hell"을 예방하기 위해, `src/app/provider.tsx` (혹은 `src/providers/app.tsx`)에 하나의 `AppProvider` 컴포넌트를 정의하고 이곳에서 모든 글로벌 컨텍스트와 전역 Error Boundary를 래핑하십시오.

### ② 로딩 및 에러 UI 대응 (UX 보장)
- **플레이스홀더 구성**: 네트워크 요청 등 비동기 데이터를 가져오는 컴포넌트는 데이터 로딩 상태일 때 보여줄 **Skeleton UI** 또는 로딩 인디케이터가 반드시 존재해야 합니다.
- **에러 바운더리 격리**: 애플리케이션의 일부 렌더링 실패로 인해 화면 전체가 먹통이 되는 현상을 예방하기 위해, 주요 페이지나 복잡한 피처 단위마다 독립적인 `ErrorBoundary`를 두어 에러를 국소적으로 격리하고 대체 UI 및 재시도 기능을 제공하십시오. (전체 전역 Boundary 단일 배치는 지양)

### ③ 에러 핸들링 및 예외 추적 전략 (Error Handling)
운영 중인 프로덕션 환경의 안정성과 중단 없는 서비스 흐름을 제공하기 위해 에러를 유형별로 체계적으로 격리하고 추적해야 합니다.

- **API 통신 에러 처리**:
  - **인터셉터 연동**: Axios 등 공통 API 클라이언트의 Response Interceptor를 구성하여 API 에러를 전역 관리하십시오.
  - **에러 대응 액션**: 통신 에러 발생 시 사용자에게 에러 상황을 알리는 알림 토스트(Toast/Notification)를 트리거하거나, 미인증 사용자(401) 발생 시 즉시 세션을 정리하고 로그인 페이지로 리다이렉트하는 흐름을 구축하여 예외 처리를 단일화하십시오.
- **애플리케이션 내부 렌더링 에러 격리 (In-App Errors)**:
  - React의 **Error Boundary**를 활용해 특정 영역에서 터진 JS 에러가 전체 화면을 하얗게 블랭크 처리(White-out)하지 않도록 막아야 합니다.
  - 전체 애플리케이션을 감싸는 단 하나의 글로벌 Error Boundary에 의존하지 마십시오. 기능상 독립적인 컴포넌트 단위나 라우트 페이지 단위마다 Error Boundary를 분산 배치하여, 실패가 발생하더라도 에러가 발생한 컴포넌트만 정지시키고 나머지 기능은 정상 작동할 수 있도록 격리하십시오.
- **프로덕션 에러 트래킹 (Error Tracking)**:
  - 실서비스에서 발생하는 모든 치명적 에러는 로깅 도구(예: **Sentry**)를 통해 실시간 수집 및 모니터링해야 합니다.
  - 에러가 발생한 운영체제(OS), 브라우저 버전을 식별할 수 있어야 하며, 빌드 시 생성되는 **소스 맵(Source Maps)을 트래킹 도구에 업로드**하여 난독화된 코드에서 실제 소스 코드 상의 에러 줄 번호와 파일명을 정확히 파악할 수 있도록 CI/CD 및 빌드 설정을 강제하십시오.

---

## 8. 웹 접근성(a11y) 및 시맨틱 HTML 규칙
- **시맨틱 마크업**: 클릭 가능한 모든 상호작용 요소는 `div`나 `span` 대신 반드시 `<button>` 또는 `<a>` 태그를 사용하십시오.
- **이미지 필수 속성**: 모든 `<img>` 태그에는 스크린 리더 지원을 위해 반드시 의미 있는 `alt` 속성을 명시해야 합니다. (비주얼 장식용인 경우 `alt=""`로 명시)
- **키보드 접근성**: 마우스 클릭 외에도 키보드(`Tab`, `Enter`, `Space`)를 통한 내비게이션 및 활성화가 가능하도록 구현하십시오.

---

## 9. 폼(Form) 처리 및 유효성 검사 규칙 (Form State)
폼은 많은 입력 필드와 동적 유효성 검사가 얽혀 있어 복잡해지기 쉽습니다. 입력 필드가 많은 폼은 React 원시 상태(`useState`)만을 사용해 개별 제어하기보다, 전문 라이브러리를 활용해 추상화해야 합니다.

### ① Controlled & Uncontrolled 컴포넌트 활용 및 추상화
- 입력 필드의 개수와 검증 로직의 강도에 따라 적절한 폼 제어 방식을 택합니다.
- 복잡한 폼일수록 렌더링 최적화를 위해 비제어(Uncontrolled) 컴포넌트 방식을 활용하는 라이브러리를 채택하여 불필요한 상태 변경 리렌더링을 차단하십시오.
- **추천 라이브러리**: **React Hook Form**, Formik, React Final Form
- 프로젝트 내부적으로 라이브러리의 핵심 기능을 감싸는 공통 폼 래퍼 컴포넌트(`<Form>`)와 공통 입력 컴포넌트(`<InputField>`)를 만들어 UI 스타일을 일관되게 단일화하고 결합도를 낮추십시오.

* **공통 폼 래퍼 컴포넌트 예시 (`src/components/ui/form/form.tsx`)**:
  ```tsx
  import { zodResolver } from '@hookform/resolvers/zod';
  import * as React from 'react';
  import { useForm, UseFormReturn, UseFormProps, FieldValues } from 'react-hook-form';
  import { ZodSchema, TypeOf } from 'zod';

  type FormProps<TFormValues extends FieldValues, Schema extends ZodSchema<any>> = {
    onSubmit: (values: TypeOf<Schema>) => void;
    schema: Schema;
    children: (methods: UseFormReturn<TFormValues>) => React.ReactNode;
    options?: UseFormProps<TFormValues>;
    id?: string;
    className?: string;
  };

  export const Form = <
    TFormValues extends Record<string, any> = Record<string, any>,
    Schema extends ZodSchema<any> = ZodSchema<any>
  >({
    onSubmit,
    schema,
    children,
    options,
    id,
    className,
  }: FormProps<TFormValues, Schema>) => {
    const methods = useForm<TFormValues>({
      ...options,
      resolver: zodResolver(schema),
    });
    return (
      <form
        onSubmit={methods.handleSubmit(onSubmit)}
        id={id}
        className={className}
      >
        {children(methods)}
      </form>
    );
  };
  ```

* **공통 입력 필드 컴포넌트 예시 (`src/components/ui/form/input.tsx`)**:
  ```tsx
  import * as React from 'react';
  import { UseFormRegisterReturn } from 'react-hook-form';

  type InputFieldProps = {
    label?: string;
    type?: string;
    className?: string;
    registration: Partial<UseFormRegisterReturn>;
    error?: {
      message?: string;
    };
  };

  export const InputField = ({
    label,
    type = 'text',
    className = '',
    registration,
    error,
  }: InputFieldProps) => {
    return (
      <div className={className}>
        {label && <label className="block text-sm font-medium text-gray-700">{label}</label>}
        <div className="mt-1">
          <input
            type={type}
            aria-invalid={error ? 'true' : 'false'}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            {...registration}
          />
        </div>
        {error?.message && (
          <p role="alert" className="mt-2 text-sm text-red-600">
            {error.message}
          </p>
        )}
      </div>
    );
  };
  ```

### ② 클라이언트 사이드 유효성 스키마 통합 (Zod / Yup)
- 데이터 전송 전 사용자 입력을 검증하기 위해 **Zod** 또는 Yup 등의 유효성 검사 라이브러리를 연동하십시오.
- 앞서 정의한 공통 `<Form>` 컴포넌트에 Zod schema와 Submit 핸들러를 주입하여 선언적인 코드를 유지하십시오.

---

## 10. 보안 및 접근 권한 규칙 (Security)
안전한 애플리케이션 운영과 사용자 정보 보호를 위해 프론트엔드와 서버 측 전반에 걸친 보안 규칙을 적용합니다.

### ① 인증 (Authentication - 신원 검증)
- **토큰 관리**: 싱글 페이지 애플리케이션(SPA)에서 주로 활용하는 JWT(JSON Web Token)를 관리할 때, 가장 안전한 방법은 앱 상태(메모리)에 저장하는 것입니다. 단, 브라우저 새로고침 시 인증이 유실되는 것을 막기 위해 쿠키 또는 스토리지 활용 시 다음 규칙을 준수합니다.
- **쿠키 및 로컬스토리지 보안**:
  - `localStorage` 또는 `sessionStorage`에 토큰을 저장하는 것은 교차 사이트 스크립팅(XSS) 취약점 노출 시 악의적인 행위자에게 토큰을 탈취당할 위험이 큽니다.
  - 따라서 인증 토큰은 JavaScript가 접근할 수 없는 **`HttpOnly` 속성이 설정된 쿠키**에 저장하여 전송하는 것을 강력히 권장합니다. (클라이언트 JavaScript 코드에서는 토큰에 직접 접근할 수 없어야 합니다.)
- **HTML 세니타이징 (XSS 방지)**: 사용자가 입력한 데이터나 Markdown 렌더링 결과 등을 JSX 화면에 출력할 때는 악성 스크립트 실행을 방지하기 위해 렌더링 전 반드시 **HTML Sanitization**(예: `dompurify` 등의 라이브러리 활용) 과정을 거치도록 강제하십시오.
- **유저 정보 공유**: 인증에 성공한 유저 정보는 전역에서 언제든 참조할 수 있도록 전역 상태(`react-query-auth` 설정 또는 Zustand 스토어)로 공유되어야 하며, 유저 객체의 유무를 기반으로 전역 레이아웃 및 페이지 진입을 통제하십시오.

### ② 인가 (Authorization - 권한 부여)
사용자의 역할 및 소유권 여부에 따라 리소스 접근 권한을 엄격하게 제한합니다.
- **역할 기반 권한 제어 (RBAC - Role Based Access Control)**:
  - 사용자의 역할(예: `USER`, `ADMIN` 등)과 이에 따른 권한 범위를 명확히 정의합니다.
  - 컴포넌트 트리 상에서 특정 역할 전용 기능(예: 삭제 버튼, 관리자 메뉴)을 제한할 수 있는 **공통 권한 감싸기 컴포넌트**(`<Authorization>` 또는 `<RBAC>`)를 구성하여 사용하십시오.
  * 예시: `<Authorization allowedRoles={[ROLES.ADMIN]}> <DeleteButton /> </Authorization>`
- **권한 기반 제어 (PBAC - Permission/Policy Based Access Control)**:
  - 역할 제어보다 더 세분화된 접근 제어가 필요할 때 사용합니다. (예: "자신이 작성한 댓글만 삭제할 수 있음")
  - 단순히 사용자 역할 체크에 그치지 않고, 리소스 작성자 ID와 로그인한 유저 ID의 일치 여부를 평가하는 **정책(Policies) 평가 함수**를 작성하여 조건부 렌더링을 통제하도록 설계하십시오.

---

## 11. 성능 최적화 가이드라인 (Performance Optimization)
웹 애플리케이션의 빠른 응답성과 검색 엔진 최적화(SEO) 및 우수한 사용자 경험을 위해 성능을 최적화하고 지표를 모니터링합니다.

### ① 코드 분할 (Code Splitting)
- 대용량의 프로덕션 자바스크립트 번들을 작은 번들 단위로 분할하여 로딩 시간을 줄이십시오.
- 코드 분할은 기본적으로 **라우트(Route)/페이지 수준에서 적용**하여 유저가 필요한 화면에 진입할 때 지연 로딩(Lazy Loading)으로 청크를 가져오도록 구성하십시오.
- 이상적으로는 라우트 수준에서 코드 분할을 구현하여 처음에는 필수 코드만 로드하고 추가 청크는 필요에 따라 지연 호출(Lazy Fetching)해야 합니다.
- 단, 무분별하고 과도한 코드 분할은 오히려 전체 코드 청크를 가져오기 위해 필요한 요청 횟수를 증가시켜 성능 저하를 초래할 수 있으므로 주의하십시오. 애플리케이션의 핵심 부분에 집중된 전략적인 코드 분할을 통해 리소스 로딩 효율성과 성능 최적화의 균형을 맞추어야 합니다.
- **예제 코드**: [Code Splitting 예시 코드](file:///../apps/react-vite/src/app/router.tsx)

### ② 컴포넌트 및 상태 렌더링 최적화
- **상태의 쪼개기**: 단일 전역 상태에 모든 것을 넣지 마십시오. 이는 불필요한 리렌더링을 유발할 수 있습니다. 상태 업데이트 시 무관한 컴포넌트들이 대량으로 리렌더링되는 것을 방지하기 위해 글로벌 상태를 사용처에 맞게 여러 상태로 분할하십시오.
- **로컬 상태 위치 최적화**: 상태는 해당 상태에 직접 종속된 컴포넌트와 가장 가까운 곳(Colocation)에 배치하여 영향 범위를 줄이고, 업데이트된 상태에 의존하지 않는 컴포넌트가 리렌더링되는 것을 방지하십시오.
- **지연 상태 초기화 (Lazy State Initialization)**: 비용이 많이 드는 계산 결과값을 `useState` 초기 값으로 주입해야 한다면 함수를 즉시 호출하지 말고 **초기화 함수(Callback)** 형태로 주입해 리렌더링 시마다 함수가 재실행되는 것을 방지하십시오.
  * ❌ **나쁜 예**: `const [state, setState] = useState(myExpensiveFn());` (리렌더링 시 매번 실행)
  *  **올바른 예**: `const [state, setState] = useState(() => myExpensiveFn());` (최초 1회만 실행)
- **원자적 상태 관리의 도입**: 한 번에 많은 요소를 추적하고 세밀한 상태 업데이트가 필요하다면 [Jotai](https://jotai.pmnd.rs/)와 같이 원자적(Atomic) 업데이트를 지원하는 상태 관리 라이브러리를 고려하십시오.
- **컨텍스트 API의 현명한 활용**: `React Context`는 테마, 로그인 유저 등 자주 바뀌지 않는 저속 데이터(Low-velocity data)에 적합합니다. 빈번하게 바뀌는 고속 데이터를 공유할 때는 셀렉터를 지원하는 라이브러리(Zustand 등)를 선택하거나 [use-context-selector](https://github.com/dai-shi/use-context-selector)를 고려하십시오. (Zustand나 Jotai 같은 라이브러리에는 셀렉터가 이미 내장되어 있습니다.)
- **컴포넌트 합성 우선 검토**: Props Drilling 해결을 위해 컨텍스트를 도입하기 전, 먼저 [상태 끌어올리기(Lifting State Up)](https://react.dev/learn/sharing-state-between-components#lifting-state-up-by-example)나 [적절한 컴포넌트 합성(Component Composition)](https://react.dev/learn/passing-data-deeply-with-context#before-you-use-context)으로 해결할 수 있는지 우선 검토하십시오. 전역 상태나 Context를 섣불리 사용하지 마십시오.
- **Zero-runtime 스타일 도입**: 빈번한 화면 업데이트와 렌더링 성능이 핵심인 서비스라면 런타임에 CSS를 계산해 스타일을 주입하는 CSS-in-JS([Emotion](https://emotion.sh/docs/introduction), [styled-components](https://styled-components.com/) 등) 대신 빌드 시점에 정적 스타일이 생성되는 빌드타임 스타일링 솔루션([Tailwind CSS](https://tailwindcss.com/), [vanilla-extract](https://github.com/seek-oss/vanilla-extract), [CSS Modules](https://github.com/css-modules/css-modules) 등)을 채택하십시오.

### ③ Children Props를 활용한 최적화 (가장 쉽고 강력한 기법)
- 컴포넌트 구조화 시 `children` 프로퍼티를 적절히 활용하면 부모 컴포넌트 상태 변화로 인한 자식 컴포넌트의 불필요한 리렌더링을 완전히 차단할 수 있습니다. 
- 자식으로 주입된 JSX 요소는 독립된 VDOM 구조를 가지므로 부모 리렌더링 시 매번 재생성되지 않습니다(부모가 자식을 리렌더링할 필요가 없고 할 수도 없습니다).
* **최적화 전후 코드 예시**:
  ```javascript
  // ❌ 최적화 전: Counter 상태가 변경될 때마다 PureComponent도 강제 리렌더링됨
  const App = () => <Counter />;

  const Counter = () => {
    const [count, setCount] = useState(0);
    return (
      <div>
        <button onClick={() => setCount((c) => c + 1)}>count is {count}</button>
        <PureComponent /> 
      </div>
    );
  };

  //  최적화 후: count가 변경되어도 children으로 들어온 PureComponent는 리렌더링되지 않음
  const App = () => (
    <Counter>
      <PureComponent />
    </Counter>
  );

  const Counter = ({ children }) => {
    const [count, setCount] = useState(0);
    return (
      <div>
        <button onClick={() => setCount((c) => c + 1)}>count is {count}</button>
        {children}
      </div>
    );
  };
  ```

### ④ 이미지 최적화 (Image Optimization)
- 뷰포트(Viewport) 밖에 위치한 이미지는 브라우저 기본 사양인 `loading="lazy"` 속성을 부여하여 지연 로딩을 수행하십시오.
- 로딩 속도를 향상시키기 위해 `PNG`/`JPG` 대신 차세대 이미지 포맷인 **`WEBP`** 또는 `AVIF`를 우선적으로 활용하십시오.
- 다양한 해상도에 실시간 대응하기 위해 `srcset` 속성을 지정하여 모바일/데스크톱 화면 해상도에 가장 잘 맞는 최적의 이미지 크기를 로드하게 유도하십시오.

### ⑤ 데이터 프리페칭 (Data Prefetching)
- 사용자가 특정 라우트로 이동할 것이 거의 확실하거나(예: 링크 마우스 오버 등), 특정 모달을 열기 전 행동 흐름이 예측될 경우 React Query의 **`queryClient.prefetchQuery`** 메서드를 사용하여 화면 전환 전 API 데이터를 미리 로드하십시오. 
- 이 기법을 사용하면 사용자가 해당 페이지로 이동하기 전에 데이터를 미리 가져오므로, 페이지 전환 시 데이터가 캐싱되어 있어 깜빡임 없이 즉각적인 화면 로딩을 제공할 수 있어 성능 체감을 극적으로 높일 수 있습니다.
- **예제 코드**: [Data Prefetching 예시 코드](file:///../apps/react-vite/src/features/discussions/components/discussions-list.tsx)

### ⑥ 웹 바이탈 지표 관리 (Web Vitals)
- 구글이 웹사이트 인덱싱 시 검색 순위 평가 요소로 웹 바이탈을 반영하므로, [Lighthouse](https://web.dev/measure/) 및 [PageSpeed Insights](https://pagespeed.web.dev/) 분석을 정기적으로 검토하고, Core Web Vitals(LCP, FID/INP, CLS) 지표가 기준치를 넘지 않도록 코드를 조율하십시오.

---

## 12. 테스트 전략 및 권장 도구 규칙 (Testing)
테스트를 작성하는 주된 목적은 구현 세부 사항(Implementation details) 검증이 아니라, 애플리케이션의 비즈니스 안정성을 확인하여 배포 시의 신뢰성을 확보하는 것입니다. 효과적인 검증을 위해 단위(Unit), 통합(Integration), 종단간(E2E) 테스트의 균형을 맞춥니다.

### ① 테스트 범위의 분류 및 작성 요령
- **단위 테스트 (Unit Tests)**:
  - 애플리케이션의 가장 작은 기능 단위를 격리하여 검증합니다.
  - 주로 프로젝트 전역에서 사용되는 공통 UI 컴포넌트(Button, Input 등)나 순수 유틸리티 함수, 그리고 한 컴포넌트 안의 복잡한 로직을 테스트하는 데 적합합니다.
- **통합 테스트 (Integration Tests)**: ⭐ *가장 권장 및 집중해야 할 영역*
  - 여러 모듈이나 컴포넌트가 결합하여 실제로 의도된 비즈니스 흐름을 올바르게 수행하는지 검증합니다.
  - 단위 테스트가 개별 모듈의 통과를 보장하더라도, 모듈 간의 협력(데이터 흐름 등)이 깨지면 애플리케이션이 비정상 작동하므로 대부분의 테스트 비용은 통합 테스트에 집중하십시오.
- **E2E 테스트 (End-to-End Tests)**:
  - 프론트엔드와 백엔드를 연동한 실제 작동 환경 전체를 브라우저 상에서 시뮬레이션하여 유저 시나리오를 처음부터 끝까지 자동 검증합니다.

### ② 권장 테스팅 도구 규칙
- **Vitest**: 현대적인 빌드 툴링 및 ESM과 완벽하게 호환되는 고성능 테스팅 프레임워크입니다. 단위 및 통합 테스트의 러너로 사용합니다.
- **React Testing Library**: 
  - **핵심 철학**: *"테스트는 사용자가 소프트웨어를 사용하는 방식과 유사하게 수행될 때 가장 신뢰할 수 있습니다."*
  - 컴포넌트 내부의 상태값(`state`)이나 내부 변수를 직접 검사하지 마십시오. 대신 사용자가 스크린에서 보고 동작을 취하는 요소(예: `screen.getByRole('button', { name: /submit/i })`)를 쿼리하여 실제 사용자 상호작용처럼 테스트해야 합니다.
  - 이를 통해 프론트엔드의 상태 관리 솔루션을 리팩터링하더라도(예: Redux에서 Zustand로 변경), 사용자가 보는 화면 결과와 동작이 동일하다면 테스트 코드가 수정 없이 통과할 수 있게 작성하십시오.
- **Playwright (E2E 테스트)**:
  - 브라우저 자동화 테스트 도구입니다. 개발 환경에서는 브라우저 모드(Browser mode)를 활성화하여 단계별 UI 변화를 시각적으로 디버깅하고, CI/CD 환경에서는 헤드리스 모드(Headless mode)로 실행하여 배포 시 안전망 역할을 하도록 구성하십시오.
- **MSW (Mock Service Worker)**:
  - **네트워크 모킹**: API 클라이언트 수준(`fetch`나 `axios` 래퍼)을 가짜로 모킹하지 말고, 서비스 워커 레벨에서 네트워크 요청을 직접 가로채도록 MSW를 활용하십시오.
  - 실제 API 요청이 네트워크 레벨에서 전달되는 시나리오와 완전히 동일하게 테스트할 수 있으며, 백엔드 API가 아직 완성되지 않은 프로토타이핑 단계에서도 실제 서버가 도는 것처럼 프론트엔드 기능을 온전하게 개발하고 테스트할 수 있게 해줍니다.

---

## 13. 프로젝트 품질 표준 및 도구 규칙 (Project Standards)
코드의 일관성, 가독성 및 대규모 코드베이스의 확장을 위해 프로젝트에 설정된 품질 기준 및 도구 사용 규칙을 엄격히 준수합니다.

### ① ESLint (코드 린팅)
- ESLint는 코드 품질을 유지하고 사전에 에러를 감지하기 위한 핵심 도구입니다. `.eslintrc` 파일에 정의된 규칙에 부합하도록 작성해야 합니다.
- 잠재적인 버그나 일관되지 않은 코드 스타일은 린트 수준에서 경고/에러로 처리되므로, AI 에이전트는 코드 작성 완료 후 반드시 린트를 확인하여 수정하십시오.

### ② Prettier (코드 포맷팅)
- 프로젝트 전역에서 동일한 포맷을 유지하기 위해 Prettier 설정을 준수합니다.
- IDE의 **"저장 시 자동 포맷(Format on Save)"** 기능을 활용하여 `.prettierrc`에 설정된 스타일 가이드를 강제 적용하십시오. 
- 만약 저장 시 자동 포맷팅이 실패한다면 코드에 구문 에러(Syntax Error)가 존재할 가능성이 높으므로 원인을 확인해야 합니다.

### ③ TypeScript (타입 정적 검증)
- JavaScript의 동적 타입에서 발생할 수 있는 런타임 에러를 빌드 시점에 차단하고, 대규모 리팩터링의 안정성을 확보하기 위해 엄격한 TypeScript 작성을 준수합니다.
- **리팩터링 우선순위**: 리팩터링 작업을 수행할 때는 **1) 타입 선언(Type Declarations)을 최우선으로 변경**하고, **2) 발생한 타입 에러를 순차적으로 해결**해 나가는 방식으로 진행하십시오.
- 단, 빌드 시점의 타입 검증이 런타임 에러를 모두 방지하는 것은 아니므로 외부 API나 사용자 입력 데이터는 런타임 검증(Pydantic, Zod 등)을 병행해야 합니다.

### ④ Husky (Git Hooks 제어)
- 원격 레포지토리에 불완전한 코드가 푸시되는 것을 차단하기 위해 Git Hooks 관리 도구인 Husky를 활용합니다.
- 커밋(`pre-commit`) 혹은 푸시(`pre-push`) 시점에 자동으로 린트(ESLint), 코드 포맷(Prettier), 타입 체크(TypeScript) 및 테스트가 수행되도록 구성하고, 이 검증 과정에서 에러가 발생하면 커밋/푸시가 반려됩니다.

### ⑤ 절대 경로 임포트 (Absolute Imports)
- 복잡하고 디렉토리 구조 변경 시 깨지기 쉬운 상대 경로(`../../../components/Button`) 대신 절대 경로 임포트(`@/*` -> `./src/*`)를 사용합니다.
- `tsconfig.json` 또는 `jsconfig.json`에 아래와 같이 구성하여 사용하십시오:
  ```json
  "compilerOptions": {
      "baseUrl": ".",
      "paths": {
        "@/*": ["./src/*"]
      }
    }
  ```
- 개별 폴더별로 무분별하게 별칭(Alias)을 파편화하여 만드는 것(예: `@components`, `@hooks`)은 피하고, `@/*` 단일 별칭을 사용하여 `node_modules` 패키지와 소스 코드를 직관적으로 구분하십시오.

### ⑥ 파일 및 폴더 명명 규칙 (Naming Conventions)
- 프로젝트 파일 구조의 일관성을 유지하기 위해 `src/` 폴더 내의 모든 파일과 폴더명(테스트 폴더 제외)은 소문자 케밥 케이스(`kebab-case`) 사용을 원칙으로 합니다.
- 이를 강제하기 위해 아래와 같이 ESLint 규칙을 설정하고 준수하십시오:
  ```js
  'check-file/filename-naming-convention': [
    'error',
    {
        '**/*.{ts,tsx}': 'KEBAB_CASE',
    },
    {
        ignoreMiddleExtensions: true, // bable.config.js 또는 smoke.spec.ts 와 같은 파일명 지원
    },
  ],
  'check-file/folder-naming-convention': [
    'error',
    {
      'src/**/!(__tests__)': 'KEBAB_CASE', // src/ 하위의 모든 폴더(__tests__ 제외)는 kebab-case 강제
    },
  ],
  ```
