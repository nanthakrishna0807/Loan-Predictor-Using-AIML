import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('loan_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [token, setToken] = useState(() => {
    return localStorage.getItem('loan_token') || null;
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  const loginUser = async (email, password) => {
    setLoading(true);
    try {
      const res = await axios.post('/api/auth/login', { email, password });
      if (res.data.success) {
        const payloadData = res.data.data || res.data;
        const token = payloadData.token;
        const user = payloadData.user;
        setToken(token);
        setUser(user);
        localStorage.setItem('token', token);
        localStorage.setItem('loan_token', token);
        localStorage.setItem('loan_user', JSON.stringify(user));
        return { success: true, user };
      }
      return { success: false, message: res.data.message || 'Login failed' };
    } catch (err) {
      return {
        success: false,
        message: err.response?.data?.message || err.message || 'Server error during login'
      };
    } finally {
      setLoading(false);
    }
  };

  const registerUser = async (name, email, password, role = 'user') => {
    setLoading(true);
    try {
      const res = await axios.post('/api/auth/register', { name, email, password, role });
      if (res.data.success) {
        const payloadData = res.data.data || res.data;
        const token = payloadData.token;
        const user = payloadData.user;
        setToken(token);
        setUser(user);
        localStorage.setItem('token', token);
        localStorage.setItem('loan_token', token);
        localStorage.setItem('loan_user', JSON.stringify(user));
        return { success: true, user };
      }
      return { success: false, message: res.data.message || 'Registration failed' };
    } catch (err) {
      return {
        success: false,
        message: err.response?.data?.message || err.message || 'Registration error'
      };
    } finally {
      setLoading(false);
    }
  };

  const logoutUser = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('loan_token');
    localStorage.removeItem('loan_user');
  };


  return (
    <AuthContext.Provider value={{ user, token, loading, loginUser, registerUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
};
