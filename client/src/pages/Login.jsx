import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { ShieldCheck, LogIn, Lock, Mail, AlertCircle } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const { loginUser, loading } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    const res = await loginUser(email, password);
    if (res.success) {
      if (res.user.role === 'admin') {
        navigate('/admin/dashboard');
      } else {
        navigate('/dashboard');
      }
    } else {
      setErrorMsg(res.message || 'Invalid email or password.');
    }
  };

  const handleDemoFill = (role) => {
    if (role === 'admin') {
      setEmail('admin@loanpredictor.ai');
      setPassword('admin123');
    } else {
      setEmail('demo@loanpredictor.ai');
      setPassword('password');
    }
  };

  return (
    <div className="py-5 my-3 d-flex align-items-center justify-content-center">
      <div className="container max-w-md">
        <div className="glass-card p-4 p-md-5 text-white border-blue-500/30 glow-blue">
          <div className="text-center mb-4">
            <div className="p-3 rounded-circle bg-blue-600/20 text-cyan-400 d-inline-block mb-3">
              <ShieldCheck size={36} />
            </div>
            <h3 className="fw-bold mb-1">Welcome Back</h3>
            <p className="text-sm text-slate-400">Sign in to your AI Loan Predictor Account</p>
          </div>

          {errorMsg && (
            <div className="alert alert-danger glass-card border-rose-500/50 text-rose-300 text-xs d-flex align-items-center gap-2 mb-4 p-2.5">
              <AlertCircle size={18} />
              <span>{errorMsg}</span>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="text-xs text-slate-300 mb-1 d-block">Email Address</label>
              <div className="position-relative">
                <input
                  type="email"
                  className="fintech-input ps-4"
                  placeholder="name@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="mb-3">
              <div className="d-flex justify-content-between align-items-center mb-1">
                <label className="text-xs text-slate-300 mb-0">Password</label>
                <Link to="/forgot-password" className="text-2xs text-cyan-400 hover:text-cyan-300 text-decoration-none">
                  Forgot password?
                </Link>
              </div>
              <input
                type="password"
                className="fintech-input"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit" disabled={loading} className="btn btn-fintech w-100 py-3 text-sm fw-semibold mb-3">
              {loading ? "Signing in..." : "Sign In to Account"}
            </button>
          </form>

          {/* Preset Quick Fill Demo Buttons */}
          <div className="p-3 rounded-3 bg-slate-900/60 border border-slate-800 text-center mb-3">
            <span className="text-2xs text-slate-400 d-block mb-2">QUICK DEMO ACCESSS</span>
            <div className="d-flex gap-2">
              <button onClick={() => handleDemoFill('user')} className="btn btn-sm btn-outline-fintech w-50 text-xs">
                Demo User
              </button>
              <button onClick={() => handleDemoFill('admin')} className="btn btn-sm btn-outline-fintech w-50 text-xs">
                Demo Admin
              </button>
            </div>
          </div>

          <div className="text-center text-xs text-slate-400">
            Don't have an account yet?{' '}
            <Link to="/register" className="text-cyan-400 hover:text-cyan-300 fw-semibold text-decoration-none">
              Register now
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
