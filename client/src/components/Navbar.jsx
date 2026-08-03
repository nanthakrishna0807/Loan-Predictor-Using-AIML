import React, { useContext } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { ThemeContext } from '../context/ThemeContext';
import { ShieldCheck, Moon, Sun, LogOut, User, LayoutDashboard, Calculator, BarChart3, FileText, Cpu } from 'lucide-react';

const Navbar = () => {
  const { user, logoutUser } = useContext(AuthContext);
  const { theme, toggleTheme } = useContext(ThemeContext);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logoutUser();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path ? 'text-cyan-400 font-semibold' : 'text-slate-300 hover:text-cyan-300';

  return (
    <nav className="navbar navbar-expand-lg sticky-top border-b border-slate-800" style={{ background: 'rgba(9, 13, 22, 0.85)', backdropFilter: 'blur(16px)' }}>
      <div className="container py-1">
        <Link to="/" className="navbar-brand d-flex align-items-center gap-2 text-decoration-none">
          <div className="p-2 rounded-3 bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-lg">
            <ShieldCheck size={26} />
          </div>
          <div>
            <span className="h4 fw-bold mb-0 text-white tracking-tight">AI Loan <span className="text-cyan-400">Predictor</span></span>
            <span className="badge bg-blue-900 text-cyan-300 ms-2 text-xs border border-cyan-500/30">v2.4 ML</span>
          </div>
        </Link>

        <button className="navbar-toggler border-slate-700" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navMenu">
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0 align-items-lg-center gap-lg-3">
            <li className="nav-item">
              <Link className={`nav-link ${isActive('/')}`} to="/">Home</Link>
            </li>
            <li className="nav-item">
              <Link className={`nav-link ${isActive('/features')}`} to="/features">Features</Link>
            </li>
            <li className="nav-item">
              <Link className={`nav-link ${isActive('/about')}`} to="/about">About ML</Link>
            </li>
            <li className="nav-item">
              <Link className={`nav-link ${isActive('/calculator')}`} to="/calculator">
                <span className="d-inline-flex align-items-center gap-1"><Calculator size={16}/> Calculator</span>
              </Link>
            </li>
            <li className="nav-item">
              <Link className={`nav-link ${isActive('/predict')}`} to="/predict">
                <span className="d-inline-flex align-items-center gap-1"><Cpu size={16}/> Apply & Predict</span>
              </Link>
            </li>

            {user && (
              <>
                <li className="nav-item">
                  <Link className={`nav-link ${isActive(user.role === 'admin' ? '/admin/dashboard' : '/dashboard')}`} to={user.role === 'admin' ? '/admin/dashboard' : '/dashboard'}>
                    <span className="d-inline-flex align-items-center gap-1"><LayoutDashboard size={16}/> Dashboard</span>
                  </Link>
                </li>
                {user.role === 'admin' && (
                  <li className="nav-item">
                    <Link className={`nav-link ${isActive('/analytics')}`} to="/analytics">
                      <span className="d-inline-flex align-items-center gap-1"><BarChart3 size={16}/> Analytics</span>
                    </Link>
                  </li>
                )}
              </>
            )}

            {/* Theme Toggle Button */}
            <li className="nav-item me-lg-2">
              <button onClick={toggleTheme} className="btn text-slate-300 hover:text-cyan-400 p-2 rounded-circle border border-slate-700/50" title="Toggle Theme">
                {theme === 'dark' ? <Sun size={18} className="text-amber-400" /> : <Moon size={18} className="text-blue-400" />}
              </button>
            </li>

            {/* Auth Buttons */}
            {user ? (
              <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle d-flex align-items-center gap-2 text-white" href="#" role="button" data-bs-toggle="dropdown">
                  <div className="bg-blue-600 text-white rounded-circle d-flex align-items-center justify-content-center fw-bold" style={{ width: 34, height: 34 }}>
                    {user.name.charAt(0).toUpperCase()}
                  </div>
                  <span className="fw-medium">{user.name.split(' ')[0]}</span>
                </a>
                <ul className="dropdown-menu dropdown-menu-end glass-card p-2 border-slate-700 shadow-2xl">
                  <li><Link className="dropdown-item text-slate-200 hover:bg-slate-800 rounded-2" to="/profile"><User size={16} className="me-2"/> Profile</Link></li>
                  <li><Link className="dropdown-item text-slate-200 hover:bg-slate-800 rounded-2" to="/settings">Settings</Link></li>
                  <li><hr className="dropdown-divider border-slate-700"/></li>
                  <li>
                    <button onClick={handleLogout} className="dropdown-item text-red-400 hover:bg-red-900/30 rounded-2 d-flex align-items-center">
                      <LogOut size={16} className="me-2"/> Logout
                    </button>
                  </li>
                </ul>
              </li>
            ) : (
              <div className="d-flex align-items-center gap-2 mt-2 mt-lg-0">
                <Link to="/login" className="btn btn-outline-fintech py-1.5 px-3 text-sm">Login</Link>
                <Link to="/register" className="btn btn-fintech py-1.5 px-3 text-sm">Register</Link>
              </div>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
