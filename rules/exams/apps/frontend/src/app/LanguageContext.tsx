import React, { createContext, useContext } from 'react';

type LanguageContextType = {
  t: (key: string) => string;
};

const LanguageContext = createContext<LanguageContextType>({
  t: (key) => key,
});

export const useLanguage = () => useContext(LanguageContext);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const t = (key: string) => {
    const translations: Record<string, string> = {
      username: '아이디',
      password: '비밀번호',
      touchToInput: '터치하여 입력하세요',
      login: '로그인',
      authenticating: '인증 중...',
      viewPassword: '비밀번호 보기',
    };
    return translations[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ t }}>
      {children}
    </LanguageContext.Provider>
  );
};
export default LanguageProvider;
