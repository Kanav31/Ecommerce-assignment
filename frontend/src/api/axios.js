import axios from 'axios';

// withCredentials sends HttpOnly cookies on every request
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// On 401, attempt a silent token refresh and retry the original request once.
// If the refresh also fails (token expired after 7 days), redirect to login.
api.interceptors.response.use(
  response => response,
  async error => {
    const original = error.config;

    if (error.response?.status === 401 && !original._retried) {
      original._retried = true;
      try {
        await api.post('/auth/refresh/');
        return api(original);
      } catch {
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default api;
