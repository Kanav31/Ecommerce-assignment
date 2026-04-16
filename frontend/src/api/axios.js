import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
});

// Attach access token from localStorage to every request
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers['Authorization'] = `Bearer ${token}`;
  return config;
});

// Shared promise — if 3 requests 401 at once, they all wait on one refresh, not 3 separate ones.
let refreshPromise = null;

api.interceptors.response.use(
  response => response,
  async error => {
    const original       = error.config;
    const isRefreshCall  = original.url.includes('/auth/refresh/');
    const isAuthMeCall   = original.url.includes('/auth/me/');

    if (error.response?.status === 401 && !isRefreshCall && !isAuthMeCall && !original._retried) {
      original._retried = true;

      try {
        if (!refreshPromise) {
          const refreshToken = localStorage.getItem('refresh_token');
          refreshPromise = api
            .post('/auth/refresh/', { refresh_token: refreshToken })
            .then(res => {
              localStorage.setItem('access_token',  res.data.data.access_token);
              localStorage.setItem('refresh_token', res.data.data.refresh_token);
            })
            .finally(() => { refreshPromise = null; });
        }
        await refreshPromise;
        return api(original);   // retry original request with new token
      } catch {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default api;
