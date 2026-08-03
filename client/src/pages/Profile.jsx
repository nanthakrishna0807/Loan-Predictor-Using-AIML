import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import axios from 'axios';
import { User, Mail, Phone, Briefcase, ShieldCheck, CheckCircle2 } from 'lucide-react';

const Profile = () => {
  const { user } = useContext(AuthContext);
  const [name, setName] = useState(user?.name || '');
  const [phone, setPhone] = useState(user?.phone || '+1 (555) 234-5678');
  const [occupation, setOccupation] = useState(user?.occupation || 'Senior Software Engineer');
  const [saved, setSaved] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put('/api/auth/profile', { name, phone, occupation });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (e) {
      alert("Failed to update profile.");
    }
  };

  return (
    <div className="py-5">
      <div className="container max-w-lg">
        <div className="glass-card p-4 p-md-5 text-white">
          <div className="d-flex align-items-center gap-3 mb-4 border-b border-slate-800 pb-3">
            <div className="bg-blue-600 text-white rounded-circle d-flex align-items-center justify-content-center fw-bold h2 mb-0" style={{ width: 60, height: 60 }}>
              {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
            </div>
            <div>
              <h4 className="fw-bold mb-0">{user?.name}</h4>
              <span className="badge bg-blue-900/60 text-cyan-300 border border-cyan-500/30 text-xs px-2.5 py-0.5 rounded-pill">
                {user?.role?.toUpperCase()}
              </span>
            </div>
          </div>

          {saved && (
            <div className="p-3 rounded-3 bg-emerald-950/60 border border-emerald-500/40 text-emerald-300 text-xs mb-3 d-flex align-items-center gap-2">
              <CheckCircle2 size={16}/> Profile information updated successfully!
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="text-xs text-slate-300 mb-1 d-block">Full Name</label>
              <input
                type="text"
                className="fintech-input"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="mb-3">
              <label className="text-xs text-slate-300 mb-1 d-block">Email Address (Read Only)</label>
              <input
                type="email"
                className="fintech-input opacity-75"
                value={user?.email || ''}
                disabled
              />
            </div>

            <div className="mb-3">
              <label className="text-xs text-slate-300 mb-1 d-block">Phone Number</label>
              <input
                type="text"
                className="fintech-input"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
              />
            </div>

            <div className="mb-4">
              <label className="text-xs text-slate-300 mb-1 d-block">Occupation</label>
              <input
                type="text"
                className="fintech-input"
                value={occupation}
                onChange={(e) => setOccupation(e.target.value)}
              />
            </div>

            <button type="submit" className="btn btn-fintech w-100 py-2.5 text-sm font-semibold">
              Save Profile Changes
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Profile;
