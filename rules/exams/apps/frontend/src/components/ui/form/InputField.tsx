import React, { useState } from 'react';
import type { UseFormRegisterReturn } from 'react-hook-form';
import { useLanguage } from '../../../app/LanguageContext';
import FormError from '../form-error/FormError';

export interface InputFieldProps {
  id?: string;
  label?: string;
  type?: string;
  placeholder?: string;
  value?: string;
  readOnly?: boolean;
  onClick?: () => void;
  registration?: Partial<UseFormRegisterReturn>;
  error?: {
    message?: string;
  };
  className?: string;
}

export const InputField: React.FC<InputFieldProps> = ({
  id,
  label,
  type = 'text',
  placeholder,
  value,
  readOnly,
  onClick,
  registration,
  error,
  className = '',
}) => {
  const { t } = useLanguage();
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  const isPassword = type === 'password';
  const inputType = isPassword && isPasswordVisible ? 'text' : type;
  const inputId = id || registration?.name;

  return (
    <div className={`w-full ${className}`}>
      {label && (
        <label
          htmlFor={inputId}
          className="block text-white text-sm font-medium mb-3 ml-1"
        >
          {label}
        </label>
      )}
      <div className="relative">
        <input
          id={inputId}
          type={inputType}
          placeholder={placeholder}
          value={value}
          readOnly={readOnly}
          onClick={onClick}
          className="w-full h-16 bg-[#1a1f26] border-none rounded-lg px-6 text-white focus:outline-none focus:ring-1 focus:ring-gray-500 transition-all text-xl cursor-pointer"
          {...registration}
        />
        {isPassword && (
          <div className="absolute right-0 top-0 h-full flex items-center">
            <button
              type="button"
              aria-label={t('viewPassword') || '비밀번호 보기'}
              onClick={(e) => {
                e.stopPropagation();
                setIsPasswordVisible(!isPasswordVisible);
              }}
              className="h-full w-16 flex items-center justify-center text-gray-500 hover:text-white active:bg-white/5 transition-all"
            >
              {isPasswordVisible ? '숨기기' : '보기'}
            </button>
          </div>
        )}
        <FormError message={error?.message} />
      </div>
    </div>
  );
};

export default InputField;
