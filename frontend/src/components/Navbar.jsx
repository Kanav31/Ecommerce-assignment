import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  if (!user) return null;

  return (
    <nav style={styles.nav}>
      <span style={styles.brand}>Order Management</span>
      <div style={styles.links}>
        {user.role !== 'delivery' && <Link to="/products" style={styles.link}>Products</Link>}
        {user.role === 'customer'  && <Link to="/cart"   style={styles.link}>Cart</Link>}
        {user.role === 'customer'  && <Link to="/orders" style={styles.link}>My Orders</Link>}
        {user.role === 'admin'     && <Link to="/orders" style={styles.link}>All Orders</Link>}
        {user.role === 'delivery'  && <Link to="/orders" style={styles.link}>My Deliveries</Link>}
        <span style={styles.role}>{user.name} ({user.role})</span>
        <button onClick={handleLogout} style={styles.button}>Logout</button>
      </div>
    </nav>
  );
}

const styles = {
  nav:    { display:'flex', justifyContent:'space-between', alignItems:'center', padding:'10px 20px', background:'#333', color:'#fff' },
  brand:  { fontWeight:'bold', fontSize:'18px' },
  links:  { display:'flex', alignItems:'center', gap:'15px' },
  link:   { color:'#fff', textDecoration:'none' },
  role:   { color:'#aaa', fontSize:'14px' },
  button: { padding:'5px 12px', background:'#e74c3c', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer' },
};
