import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

export default function Cart() {
  const [cart, setCart]     = useState([]);
  const [error, setError]   = useState('');
  const [success, setSuccess] = useState('');
  const navigate             = useNavigate();

  useEffect(() => {
    const saved = localStorage.getItem('cart');
    if (saved) setCart(JSON.parse(saved));
  }, []);

  const updateQty = (product_id, qty) => {
    const updated = qty <= 0
      ? cart.filter(i => i.product_id !== product_id)
      : cart.map(i => i.product_id === product_id ? { ...i, quantity: qty } : i);
    setCart(updated);
    localStorage.setItem('cart', JSON.stringify(updated));
    window.dispatchEvent(new Event('cart-updated'));
  };

  const placeOrder = async () => {
    setError('');
    if (!cart.length) { setError('Cart is empty'); return; }
    try {
      await api.post('/orders/', {
        items: cart.map(i => ({ product_id: i.product_id, quantity: i.quantity }))
      });
      localStorage.removeItem('cart');
      setCart([]);
      window.dispatchEvent(new Event('cart-updated'));
      setSuccess('Order placed successfully!');
      setTimeout(() => navigate('/orders'), 1500);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to place order');
    }
  };

  const total = cart.reduce((sum, i) => sum + parseFloat(i.price) * i.quantity, 0);

  return (
    <div style={styles.container}>
      <h2>Cart</h2>
      {error   && <p style={styles.error}>{error}</p>}
      {success && <p style={styles.success}>{success}</p>}
      {cart.length === 0 ? <p>Your cart is empty.</p> : (
        <>
          <table style={styles.table}>
            <thead>
              <tr><th>Product</th><th>Price</th><th>Qty</th><th>Subtotal</th><th></th></tr>
            </thead>
            <tbody>
              {cart.map(item => (
                <tr key={item.product_id}>
                  <td>{item.name}</td>
                  <td>₹{item.price}</td>
                  <td>
                    <button onClick={() => updateQty(item.product_id, item.quantity - 1)}>-</button>
                    {' '}{item.quantity}{' '}
                    <button onClick={() => updateQty(item.product_id, item.quantity + 1)}>+</button>
                  </td>
                  <td>₹{(parseFloat(item.price) * item.quantity).toFixed(2)}</td>
                  <td><button style={styles.remove} onClick={() => updateQty(item.product_id, 0)}>Remove</button></td>
                </tr>
              ))}
            </tbody>
          </table>
          <h3>Total: ₹{total.toFixed(2)}</h3>
          <button onClick={placeOrder} style={styles.button}>Place Order</button>
        </>
      )}
    </div>
  );
}

const styles = {
  container: { padding:'20px' },
  table:     { width:'100%', borderCollapse:'collapse', marginBottom:'15px' },
  button:    { padding:'10px 20px', background:'#e67e22', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer', fontSize:'15px' },
  remove:    { padding:'4px 8px', background:'#e74c3c', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer' },
  error:     { color:'red' },
  success:   { color:'green' },
};
