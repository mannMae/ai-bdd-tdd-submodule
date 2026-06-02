import React, { useState, useEffect, useRef } from 'react';
import type { UseFormReturn } from 'react-hook-form';
import { login, LoginError } from '../api/login';
import type { LoginRequest } from '../api/login';
import { useLanguage } from '../../../app/LanguageContext';
import FormError from '../../../components/ui/form-error/FormError';
import Form, { InputField } from '../../../components/ui/form';

interface LoginFormProps {
  onLoginSuccess: () => void;
}

interface LoginFormInnerProps {
  methods: UseFormReturn<LoginRequest>;
  onLoginSuccess: () => void;
  onSubmitRef: React.MutableRefObject<
    ((values: LoginRequest, methods: UseFormReturn<LoginRequest>) => void) | undefined
  >;
}

const LoginFormInner: React.FC<LoginFormInnerProps> = ({
  methods,
  onLoginSuccess,
  onSubmitRef,
}) => {
  const { t } = useLanguage();
  const [isLoading, setIsLoading] = useState(false);
  const { register, watch, setError, clearErrors, formState: { errors } } = methods;

  const userId = watch('user_id');
  const password = watch('password');

  const handleLoginSubmit = async (data: LoginRequest) => {
    setIsLoading(true);
    clearErrors();

    try {
      const response = await login({ data });
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user_name', response.user_name);
      localStorage.setItem('user_id', data.user_id);
      onLoginSuccess();
    } catch (err: unknown) {
      if (err instanceof LoginError && err.validationErrors) {
        if (err.validationErrors.user_id) {
          setError('user_id', { type: 'manual', message: err.validationErrors.user_id });
        }
        if (err.validationErrors.password) {
          setError('password', { type: 'manual', message: err.validationErrors.password });
        }
      } else {
        setError('root', {
          type: 'manual',
          message: err instanceof Error ? err.message : '알 수 없는 에러가 발생했습니다.',
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    onSubmitRef.current = handleLoginSubmit;
  }, [handleLoginSubmit]);

  return (
    <>
      <InputField
        id="user_id"
        label={t('username')}
        placeholder={t('touchToInput')}
        value={userId}
        registration={register('user_id')}
        error={errors.user_id}
      />

      <InputField
        id="password"
        label={t('password')}
        type="password"
        placeholder={t('touchToInput')}
        value={password}
        registration={register('password')}
        error={errors.password}
      />

      <div className="relative h-6 w-full">
        {errors.root?.message && (
          <FormError message={errors.root.message} />
        )}
      </div>

      <button
        type="submit"
        disabled={isLoading || !userId || !password}
        className="w-full h-16 rounded-lg text-xl"
      >
        {isLoading ? t('authenticating') : t('login')}
      </button>
    </>
  );
};

export const LoginForm: React.FC<LoginFormProps> = ({ onLoginSuccess }) => {
  const onSubmitRef = useRef<(values: LoginRequest, methods: UseFormReturn<LoginRequest>) => void>(undefined);

  return (
    <Form<LoginRequest>
      onSubmit={(values, methods) => onSubmitRef.current?.(values, methods)}
      options={{
        defaultValues: {
          user_id: localStorage.getItem('user_id') || '',
          password: '',
        },
      }}
      schema={{} as any}
      className="w-full max-w-lg space-y-10"
    >
      {(methods) => (
        <LoginFormInner
          methods={methods}
          onLoginSuccess={onLoginSuccess}
          onSubmitRef={onSubmitRef}
        />
      )}
    </Form>
  );
};

export default LoginForm;
