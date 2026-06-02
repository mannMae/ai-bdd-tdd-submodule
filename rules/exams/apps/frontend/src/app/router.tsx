import React from 'react';
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import LoginForm from '../features/auth/components/LoginForm';

const handleLoginSuccess = () => {
  window.location.href = '/menu';
};

export const createAppRouter = () =>
  createBrowserRouter([
    {
      path: '/login',
      element: <LoginForm onLoginSuccess={handleLoginSuccess} />,
    },
    {
      path: '/menu',
      element: <div>시스템 메인 메뉴 화면</div>,
    },
    {
      path: '*',
      element: <Navigate to="/login" replace />,
    },
  ]);

export const AppRouter = () => {
  const router = createAppRouter();
  return <RouterProvider router={router} />;
};

export default AppRouter;
