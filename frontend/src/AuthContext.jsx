/**
 * AuthContext.jsx — Global authentication state provider.
 */

import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from './services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('commuteiq_token');
    if (token) {
      authAPI.me()
        .then(res => setUser(res.data))
        .catch(() => localStorage.removeItem('commuteiq_token'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    const res = await authAPI.login(email, password);
    localStorage.setItem('commuteiq_token', res.data.token);
    setUser(res.data.user);
    return res;
  };

  const signup = async (username, email, password) => {
    const res = await authAPI.signup(username, email, password);
    localStorage.setItem('commuteiq_token', res.data.token);
    setUser(res.data.user);
    return res;
  };

  const logout = () => {
    localStorage.removeItem('commuteiq_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
