import { useState, useEffect } from 'react';
import api from '../api/axios';
import { useAuth } from '../context/useAuth';

export default function Orders() {
  const [orders, setOrders]         = useState([]);
  const [deliveryUsers, setDeliveryUsers] = useState([]);
  const [error, setError]           = useState('');
  const { user }                    = useAuth();

  useEffect(() => {
    fetchOrders();
    if (user?.role === 'admin') fetchDeliveryUsers();
  }, []);

  const fetchOrders = async () => {
    try {
      const res = await api.get('/orders/');
      setOrders(res.data.results);
    } catch {
      setError('Failed to load orders');
    }
  };

  const fetchDeliveryUsers = async () => {
    try {
      const res = await api.get('/auth/delivery-users/');
      setDeliveryUsers(res.data);
    } catch {
      setError('Failed to load delivery users');
    }
  };

  const assignDelivery = async (orderId, deliveryManId) => {
    if (!deliveryManId) return;
    try {
      await api.post(`/orders/${orderId}/assign/`, { delivery_man_id: parseInt(deliveryManId) });
      fetchOrders();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to assign');
    }
  };

  const markDelivered = async (orderId) => {
    try {
      await api.patch(`/orders/${orderId}/status/`);
      fetchOrders();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update status');
    }
  };

  const statusColor = { pending: '#e67e22', assigned: '#3498db', delivered: '#2ecc71' };

  return (
    <div style={styles.container}>
      <h2>{user?.role === 'admin' ? 'All Orders' : user?.role === 'delivery' ? 'My Deliveries' : 'My Orders'}</h2>
      {error && <p style={styles.error}>{error}</p>}
      {orders.length === 0 ? <p>No orders found.</p> : orders.map(order => (
        <div key={order.id} style={styles.card}>
          <div style={styles.header}>
            <span><strong>Order #{order.id}</strong> — {order.customer_name}</span>
            <span style={{ ...styles.status, color: statusColor[order.status] }}>
              {order.status.toUpperCase()}
            </span>
          </div>
          {order.delivery_man_name && <p style={styles.meta}>Delivery: {order.delivery_man_name}</p>}

          <table style={styles.table}>
            <thead><tr><th>Product</th><th>Price</th><th>Qty</th></tr></thead>
            <tbody>
              {order.items.map(item => (
                <tr key={item.id}>
                  <td>{item.product_name}</td>
                  <td>₹{item.product_price}</td>
                  <td>{item.quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Admin: assign delivery man */}
          {user?.role === 'admin' && order.status === 'pending' && (
            <div style={styles.actionRow}>
              <select
                id={`dm-${order.id}`}
                defaultValue=""
                style={styles.select}
              >
                <option value="" disabled>Select delivery person</option>
                {deliveryUsers.map(dm => (
                  <option key={dm.id} value={dm.id}>{dm.name}</option>
                ))}
              </select>
              <button
                style={styles.button}
                onClick={() => assignDelivery(order.id, document.getElementById(`dm-${order.id}`).value)}
              >
                Assign
              </button>
            </div>
          )}

          {/* Delivery man: mark as delivered */}
          {user?.role === 'delivery' && order.status === 'assigned' && (
            <button style={styles.deliverBtn} onClick={() => markDelivered(order.id)}>
              Mark as Delivered
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

const styles = {
  container:  { padding:'20px' },
  card:       { border:'1px solid #ddd', borderRadius:'8px', padding:'15px', marginBottom:'15px' },
  header:     { display:'flex', justifyContent:'space-between', marginBottom:'8px' },
  status:     { fontWeight:'bold' },
  meta:       { color:'#888', fontSize:'13px', margin:'4px 0' },
  table:      { width:'100%', borderCollapse:'collapse', marginTop:'8px', fontSize:'13px' },
  actionRow:  { display:'flex', gap:'10px', marginTop:'10px', alignItems:'center' },
  select:     { padding:'6px', border:'1px solid #ccc', borderRadius:'4px', width:'200px' },
  button:     { padding:'6px 14px', background:'#3498db', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer' },
  deliverBtn: { marginTop:'10px', padding:'8px 16px', background:'#2ecc71', color:'#fff', border:'none', borderRadius:'4px', cursor:'pointer' },
  error:      { color:'red' },
};
