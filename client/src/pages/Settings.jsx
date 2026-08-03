import React, { useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';
import { Moon, Sun, Bell, Shield, Key } from 'lucide-react';

const Settings = () => {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <div className="py-5">
      <div className="container max-w-lg">
        <div className="glass-card p-4 p-md-5 text-white">
          <h4 className="fw-bold border-b border-slate-800 pb-3 mb-4">Application Settings</h4>

          <div className="d-flex justify-content-between align-items-center mb-4 p-3 rounded-3 bg-slate-900/60 border border-slate-800">
            <div>
              <h6 className="fw-semibold mb-0">Theme Preference</h6>
              <span className="text-xs text-slate-400">Current: {theme === 'dark' ? 'Glassmorphic Dark Mode' : 'Clean Light Mode'}</span>
            </div>
            <button onClick={toggleTheme} className="btn btn-outline-fintech btn-sm d-flex align-items-center gap-1">
              {theme === 'dark' ? <Sun size={16} className="text-amber-400"/> : <Moon size={16} className="text-blue-400"/>}
              Toggle Theme
            </button>
          </div>

          <div className="d-flex justify-content-between align-items-center mb-4 p-3 rounded-3 bg-slate-900/60 border border-slate-800">
            <div>
              <h6 className="fw-semibold mb-0">Email Notifications</h6>
              <span className="text-xs text-slate-400">Receive instant evaluation reports & tips</span>
            </div>
            <input type="checkbox" className="form-check-input" defaultChecked />
          </div>

          <div className="d-flex justify-content-between align-items-center p-3 rounded-3 bg-slate-900/60 border border-slate-800">
            <div>
              <h6 className="fw-semibold mb-0">API Security Encryption</h6>
              <span className="text-xs text-slate-400">JWT Token Expiry (30 days)</span>
            </div>
            <span className="badge bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 text-xs">Active</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
