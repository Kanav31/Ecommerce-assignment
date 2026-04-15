import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Products from './pages/Products';
import Cart from './pages/Cart';
import Orders from './pages/Orders';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/login"    element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/products" element={
            <ProtectedRoute roles={['customer', 'admin']}><Products /></ProtectedRoute>
          } />

          <Route path="/cart" element={
            <ProtectedRoute roles={['customer']}><Cart /></ProtectedRoute>
          } />

          <Route path="/orders" element={
            <ProtectedRoute><Orders /></ProtectedRoute>
          } />

          <Route path="*" element={<Navigate to="/orders" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
