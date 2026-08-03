import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { ShieldCheck, UserPlus, AlertCircle } from 'lucide-react';

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('user');
  const [errorMsg, setErrorMsg] = useState('');
  
  const { registerUser, loading } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    const res = await registerUser(name, email, password, role);
    if (res.success) {
      navigate(role === 'admin' ? '/admin/dashboard' : '/dashboard');
    } else {
      setErrorMsg(res.message || 'Registration failed.');
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
            <h3 className="fw-bold mb-1">Create Account</h3>
            <p className="text-sm text-slate-400">Join AI Loan Predictor Platform</p>
          </div>

          {errorMsg && (
            <div className="alert alert-danger glass-card border-rose-500/50 text-rose-300 text-xs d-flex align-items-center gap-2 mb-4 p-2.5">
              <AlertCircle size={18} />
              <span>{errorMsg}</span>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="text-xs text-slate-300 mb-1 d-block">Full Name *</label>
              <input
                type="text"
                className="fintech-input"
                placeholder="Aarav Sharma"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div className="mb-3">
              <label className="text-xs text-slate-300 mb-1 d-block">Email Address *</label>
              <input
                type="email"
                className="fintech-input"
                placeholder="aarav@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="mb-3">
              <label className="text-xs text-slate-300 mb-1 d-block">Password *</label>
              <input
                type="password"
                className="fintech-input"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div className="mb-4">
              <label className="text-xs text-slate-300 mb-1 d-block">Account Type</label>
              <select className="fintech-input" value={role} onChange={(e) => setRole(e.target.value)}>
                <option value="user">Applicant / Loan User</option>
                <option value="admin">System Administrator</option>
              </select>
            </div>

            <button type="submit" disabled={loading} className="btn btn-fintech w-100 py-3 text-sm fw-semibold mb-3">
              {loading ? "Registering..." : "Create Free Account"}
            </button>
          </form>

          <div className="text-center text-xs text-slate-400">
            Already have an account?{' '}
            <Link to="/login" className="text-cyan-400 hover:text-cyan-300 fw-semibold text-decoration-none">
              Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
