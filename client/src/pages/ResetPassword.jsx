import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Lock, CheckCircle2 } from 'lucide-react';

const ResetPassword = () => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [done, setDone] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    try {
      await axios.post('/api/auth/reset-password', { password });
      setDone(true);
      setTimeout(() => navigate('/login'), 2000);
    } catch (e) {
      alert("Reset password failed.");
    }
  };

  return (
    <div className="py-5 my-4 d-flex align-items-center justify-content-center">
      <div className="container max-w-md">
        <div className="glass-card p-4 p-md-5 text-white border-blue-500/30">
          <h3 className="fw-bold mb-2">Reset Password</h3>
          <p className="text-sm text-slate-400 mb-4">Set up a new secure password for your account.</p>

          {done ? (
            <div className="p-3 rounded-3 bg-emerald-950/60 border border-emerald-500/40 text-emerald-300 text-sm mb-3">
              Password updated successfully! Redirecting to login...
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="text-xs text-slate-300 mb-1 d-block">New Password</label>
                <input
                  type="password"
                  className="fintech-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              <div className="mb-4">
                <label className="text-xs text-slate-300 mb-1 d-block">Confirm Password</label>
                <input
                  type="password"
                  className="fintech-input"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>

              <button type="submit" className="btn btn-fintech w-100 py-3 text-sm font-semibold">
                Update Password
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
