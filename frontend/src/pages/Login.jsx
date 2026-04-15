import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [form, setForm]   = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const { login }         = useAuth();
  const navigate          = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const user = await login(form.email, form.password);
      navigate('/products');
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    }
  };

  return (
    <div style={styles.container}>
      <form onSubmit={handleSubmit} style={styles.form}>
        <h2>Login</h2>
        {error && <p style={styles.error}>{error}</p>}
        <input
          style={styles.input}
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={e => setForm({ ...form, email: e.target.value })}
          required
        />
        <input
          style={styles.input}
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={e => setForm({ ...form, password: e.target.value })}
          required
        />
        <button type="submit" style={styles.button}>Login</button>
        <p>No account? <Link to="/register">Register</Link></p>
      </form>
    </div>
  );
}

const styles = {
  container: { display:'flex', justifyContent:'center', marginTop:'80px' },
  form:      { display:'flex', flexDirection:'column', gap:'12px', width:'320px', padding:'30px', border:'1px solid #ddd', borderRadius:'8px' },
  input:     { padding:'10px', border:'1px solid #ccc', borderRadius:'4px', fontSize:'14px' },
  button:    { padding:'10px', background:'#3498db', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer', fontSize:'14px' },
  error:     { color:'red', fontSize:'13px' },
};
