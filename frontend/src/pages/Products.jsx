import { useState, useEffect } from 'react';
import api from '../api/axios';
import { useAuth } from '../context/useAuth';

export default function Products() {
  const [products, setProducts] = useState([]);
  const [cart, setCart]         = useState(() => {
    try { return JSON.parse(localStorage.getItem('cart')) || []; } catch { return []; }
  });
  const [form, setForm]         = useState({ name: '', price: '' });
  const [error, setError]       = useState('');
  const [page, setPage]         = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const { user }                = useAuth();
  const PAGE_SIZE               = 10;

  useEffect(() => {
    fetchProducts();
  }, [page]);

  const fetchProducts = async () => {
    try {
      const offset = (page - 1) * PAGE_SIZE;
      const res = await api.get(`/products/?limit=${PAGE_SIZE}&offset=${offset}`);
      setProducts(res.data.results);
      setTotalCount(res.data.count);
    } catch {
      setError('Failed to load products');
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/products/', form);
      setForm({ name: '', price: '' });
      fetchProducts();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create product');
    }
  };

  const cartQty = (productId) => cart.find(i => i.product_id === productId)?.quantity ?? 0;

  const saveCart = (updated) => {
    setCart(updated);
    localStorage.setItem('cart', JSON.stringify(updated));
    window.dispatchEvent(new Event('cart-updated'));
  };

  const addToCart = (product) => {
    const updated = cart.find(i => i.product_id === product.id)
      ? cart.map(i => i.product_id === product.id ? { ...i, quantity: i.quantity + 1 } : i)
      : [...cart, { product_id: product.id, quantity: 1, name: product.name, price: product.price }];
    saveCart(updated);
  };

  const removeFromCart = (productId) => {
    const updated = cart
      .map(i => i.product_id === productId ? { ...i, quantity: i.quantity - 1 } : i)
      .filter(i => i.quantity > 0);
    saveCart(updated);
  };

  const totalPages = Math.ceil(totalCount / PAGE_SIZE);

  return (
    <div style={styles.container}>
      <h2>Products</h2>

      {user?.role === 'admin' && (
        <form onSubmit={handleCreate} style={styles.form}>
          <h3>Add Product</h3>
          {error && <p style={styles.error}>{error}</p>}
          <input style={styles.input} placeholder="Product name" value={form.name}
            onChange={e => setForm({ ...form, name: e.target.value })} required />
          <input style={styles.input} type="number" placeholder="Price" value={form.price}
            onChange={e => setForm({ ...form, price: e.target.value })} required />
          <button type="submit" style={styles.button}>Add Product</button>
        </form>
      )}

      <div style={styles.grid}>
        {products.map(p => (
          <div key={p.id} style={styles.card}>
            <h4>{p.name}</h4>
            <p>₹{p.price}</p>
            <p style={styles.meta}>By: {p.created_by_name}</p>
            {user?.role === 'customer' && (
              cartQty(p.id) > 0 ? (
                <div style={styles.qtyControl}>
                  <button onClick={() => removeFromCart(p.id)} style={styles.qtyBtn}>−</button>
                  <span style={styles.qtyCount}>{cartQty(p.id)}</span>
                  <button onClick={() => addToCart(p)} style={styles.qtyBtn}>+</button>
                </div>
              ) : (
                <button onClick={() => addToCart(p)} style={styles.cartBtn}>Add to Cart</button>
              )
            )}
          </div>
        ))}
      </div>

      {totalPages > 1 && (
        <div style={styles.pagination}>
          <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>Prev</button>
          <span> Page {page} of {totalPages} </span>
          <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)}>Next</button>
        </div>
      )}
    </div>
  );
}

const styles = {
  container:  { padding:'20px' },
  form:       { display:'flex', gap:'10px', alignItems:'flex-end', marginBottom:'20px', padding:'15px', background:'#f9f9f9', borderRadius:'8px' },
  input:      { padding:'8px', border:'1px solid #ccc', borderRadius:'4px' },
  button:     { padding:'8px 16px', background:'#3498db', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer' },
  grid:       { display:'grid', gridTemplateColumns:'repeat(auto-fill, minmax(200px,1fr))', gap:'15px' },
  card:       { padding:'15px', border:'1px solid #ddd', borderRadius:'8px' },
  meta:       { color:'#888', fontSize:'12px' },
  cartBtn:    { padding:'6px 12px', background:'#2ecc71', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer', marginTop:'8px' },
  qtyControl: { display:'flex', alignItems:'center', gap:'8px', marginTop:'8px' },
  qtyBtn:     { width:'28px', height:'28px', background:'#2ecc71', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer', fontSize:'16px', lineHeight:1 },
  qtyCount:   { minWidth:'20px', textAlign:'center', fontWeight:'bold' },
  pagination: { marginTop:'20px', display:'flex', gap:'10px', alignItems:'center' },
  error:      { color:'red', fontSize:'13px' },
};
