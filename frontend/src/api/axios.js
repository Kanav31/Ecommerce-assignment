import axios from 'axios';

// withCredentials sends HttpOnly cookies on every request
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Shared promise across concurrent requests — prevents multiple simultaneous refresh calls.
// If 3 requests 401 at once, they all wait on the same refresh, not 3 separate ones.
let refreshPromise = null;

api.interceptors.response.use(
  response => response,
  async error => {
    const original = error.config;
    const isRefreshCall  = original.url.includes('/auth/refresh/');
    const isAuthMeCall   = original.url.includes('/auth/me/');

    if (error.response?.status === 401 && !isRefreshCall && !isAuthMeCall && !original._retried) {
      original._retried = true;

      try {
        if (!refreshPromise) {
          refreshPromise = api.post('/auth/refresh/').finally(() => {
            refreshPromise = null;
          });
        }
        await refreshPromise;
        return api(original);
      } catch {
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default api;
