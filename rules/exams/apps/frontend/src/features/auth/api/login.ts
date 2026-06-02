export interface LoginRequest {
  user_id: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user_name: string;
}

export class LoginError extends Error {
  status?: number;
  validationErrors?: { user_id?: string; password?: string };

  constructor(
    message: string,
    status?: number,
    validationErrors?: { user_id?: string; password?: string }
  ) {
    super(message);
    this.name = 'LoginError';
    this.status = status;
    this.validationErrors = validationErrors;
  }
}

const API_BASE_URL = 'http://localhost:8000/api';

export const login = async ({
  data,
}: {
  data: LoginRequest;
}): Promise<LoginResponse> => {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    if (response.status === 422 && Array.isArray(errorData.detail)) {
      const validationErrors: { user_id?: string; password?: string } = {};
      errorData.detail.forEach((e: any) => {
        const field = e.loc?.[e.loc.length - 1];
        if (field === 'user_id' || field === 'password') {
          validationErrors[field as 'user_id' | 'password'] = e.msg;
        }
      });
      throw new LoginError(
        '입력 항목을 확인해주세요.',
        response.status,
        validationErrors
      );
    }
    const errorMsg = typeof errorData.detail === 'string' ? errorData.detail : '로그인에 실패했습니다.';
    throw new LoginError(errorMsg, response.status);
  }

  return response.json();
};

export default login;
