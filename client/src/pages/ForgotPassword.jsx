import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Mail, CheckCircle2, ArrowLeft } from 'lucide-react';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/auth/forgot-password', { email });
    } catch (err) {}
    setSubmitted(true);
  };

  return (
    <div className="py-5 my-4 d-flex align-items-center justify-content-center">
      <div className="container max-w-md">
        <div className="glass-card p-4 p-md-5 text-white border-blue-500/30">
          <Link to="/login" className="text-xs text-cyan-400 hover:text-cyan-300 text-decoration-none d-inline-flex align-items-center gap-1 mb-3">
            <ArrowLeft size={14}/> Back to Login
          </Link>
          <h3 className="fw-bold mb-2">Forgot Password</h3>
          <p className="text-sm text-slate-400 mb-4">Enter your registered email address to receive password reset instructions.</p>

          {submitted ? (
            <div className="p-3 rounded-3 bg-emerald-950/60 border border-emerald-500/40 text-emerald-300 text-sm mb-3 d-flex align-items-center gap-2">
              <CheckCircle2 size={20} />
              <span>Instructions sent to <strong>{email}</strong>! Please check your inbox.</span>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="text-xs text-slate-300 mb-1 d-block">Email Address</label>
                <input
                  type="email"
                  className="fintech-input"
                  placeholder="name@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <button type="submit" className="btn btn-fintech w-100 py-3 text-sm font-semibold">
                Send Reset Password Link
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
