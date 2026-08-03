import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { ShieldCheck, Lock } from 'lucide-react';

const AdminLogin = () => {
  const [email, setEmail] = useState('admin@loanpredictor.ai');
  const [password, setPassword] = useState('admin123');
  const [errorMsg, setErrorMsg] = useState('');
  const { loginUser, loading } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    const res = await loginUser(email, password);
    if (res.success && res.user.role === 'admin') {
      navigate('/admin/dashboard');
    } else {
      setErrorMsg('Admin login failed. Please verify credentials.');
    }
  };

  return (
    <div className="py-5 my-4 d-flex align-items-center justify-content-center">
      <div className="container max-w-md">
        <div className="glass-card p-4 p-md-5 text-white border-purple-500/40 glow-accent">
          <div className="text-center mb-4">
            <div className="p-3 rounded-circle bg-purple-600/20 text-purple-400 d-inline-block mb-3">
              <ShieldCheck size={36} />
            </div>
            <h3 className="fw-bold mb-1">Admin Portal</h3>
            <p className="text-sm text-slate-400">Secure System Administrator Access</p>
          </div>

          {errorMsg && (
            <div className="alert alert-danger glass-card border-rose-500 text-rose-300 text-xs mb-3 p-2.5">
              {errorMsg}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="text-xs text-slate-300 mb-1 d-block">Admin Email</label>
              <input
                type="email"
                className="fintech-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="mb-4">
              <label className="text-xs text-slate-300 mb-1 d-block">Password</label>
              <input
                type="password"
                className="fintech-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit" disabled={loading} className="btn btn-fintech bg-gradient-to-r from-purple-600 to-blue-600 w-100 py-3 text-sm font-semibold">
              {loading ? "Authenticating Admin..." : "Login to Admin Console"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;
