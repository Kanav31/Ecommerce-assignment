import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';

export default function Register() {
  const [form, setForm]   = useState({ name: '', email: '', password: '', role: 'customer' });
  const [error, setError] = useState('');
  const navigate          = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/auth/register/', form);
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed');
    }
  };

  return (
    <div style={styles.container}>
      <form onSubmit={handleSubmit} style={styles.form}>
        <h2>Register</h2>
        {error && <p style={styles.error}>{error}</p>}
        <input style={styles.input} placeholder="Name" value={form.name}
          onChange={e => setForm({ ...form, name: e.target.value })} required />
        <input style={styles.input} type="email" placeholder="Email" value={form.email}
          onChange={e => setForm({ ...form, email: e.target.value })} required />
        <input style={styles.input} type="password" placeholder="Password (min 8 chars)" value={form.password}
          onChange={e => setForm({ ...form, password: e.target.value })} required />
        <select style={styles.input} value={form.role}
          onChange={e => setForm({ ...form, role: e.target.value })}>
          <option value="customer">Customer</option>
          <option value="admin">Admin</option>
          <option value="delivery">Delivery Man</option>
        </select>
        <button type="submit" style={styles.button}>Register</button>
        <p>Have an account? <Link to="/login">Login</Link></p>
      </form>
    </div>
  );
}

const styles = {
  container: { display:'flex', justifyContent:'center', marginTop:'80px' },
  form:      { display:'flex', flexDirection:'column', gap:'12px', width:'320px', padding:'30px', border:'1px solid #ddd', borderRadius:'8px' },
  input:     { padding:'10px', border:'1px solid #ccc', borderRadius:'4px', fontSize:'14px' },
  button:    { padding:'10px', background:'#2ecc71', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer', fontSize:'14px' },
  error:     { color:'red', fontSize:'13px' },
};
