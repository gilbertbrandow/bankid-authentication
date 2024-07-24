import React, { createContext, useContext, useState } from 'react';
import { setTokens, clearTokens, getAccessToken, getRefreshToken } from '../lib/auth';

interface AuthContextProps {
  accessToken: string | null;
  refreshToken: string | null;
  setAuthTokens: (accessToken: string, refreshToken: string) => void;
  clearAuth: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [accessToken, setAccessToken] = useState<string | null>(getAccessToken());
  const [refreshToken, setRefreshToken] = useState<string | null>(getRefreshToken());

  const setAuthTokens = (accessToken: string, refreshToken: string) => {
    setAccessToken(accessToken);
    setRefreshToken(refreshToken);
    setTokens(accessToken, refreshToken);
  };

  const clearAuth = () => {
    setAccessToken(null);
    setRefreshToken(null);
    clearTokens();
  };

  return (
    <AuthContext.Provider value={{ accessToken, refreshToken, setAuthTokens, clearAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
