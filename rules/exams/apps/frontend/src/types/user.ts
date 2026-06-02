// 1. Domain Entity Interface: 비즈니스 핵심 엔티티 선언
export interface UserEntity {
  id: string;
  email: string;
  createdAt: string;
}

// 2. UI / Generic State Types: 전역/공통 상태 제어 구조 선언
export type AsyncState<T> = {
  data: T | null;
  isLoading: boolean;
  error: Error | null;
};
