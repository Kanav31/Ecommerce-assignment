import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/useAuth';

const getCartCount = () => {
  try {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    return cart.reduce((sum, i) => sum + i.quantity, 0);
  } catch { return 0; }
};

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [cartCount, setCartCount] = useState(getCartCount);

  useEffect(() => {
    const sync = () => setCartCount(getCartCount());
    window.addEventListener('cart-updated', sync);
    return () => window.removeEventListener('cart-updated', sync);
  }, []);

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
        {user.role === 'customer'  && (
          <Link to="/cart" style={styles.link}>
            Cart{cartCount > 0 && <span style={styles.badge}>{cartCount}</span>}
          </Link>
        )}
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
  badge:  { marginLeft:'5px', background:'#e74c3c', color:'#fff', borderRadius:'10px', padding:'1px 7px', fontSize:'12px', fontWeight:'bold' },
};
