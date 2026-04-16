import { createContext, useState, useEffect } from 'react';
import api from '../api/axios';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser]       = useState(null);
  const [loading, setLoading] = useState(true);

  // On mount — if a token exists, fetch the current user to restore session
  useEffect(() => {
    if (!localStorage.getItem('access_token')) {
      setLoading(false);
      return;
    }
    api.get('/auth/me/')
      .then(res => setUser(res.data.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const login = async (email, password) => {
    const res  = await api.post('/auth/login/', { email, password });
    const { access_token, refresh_token, ...userData } = res.data.data;
    localStorage.setItem('access_token',  access_token);
    localStorage.setItem('refresh_token', refresh_token);
    setUser(userData);
    return userData;
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    // Fire-and-forget — backend logout is a no-op for stateless JWT,
    // but we call it to keep a clean audit trail.
    api.post('/auth/logout/').catch(() => {});
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

