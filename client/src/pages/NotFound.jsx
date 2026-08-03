import React from 'react';
import { Link } from 'react-router-dom';
import { AlertTriangle, Home } from 'lucide-react';

const NotFound = () => {
  return (
    <div className="py-5 my-5 text-center text-white">
      <div className="container max-w-md">
        <div className="glass-card p-5 border-rose-500/40 glow-accent">
          <div className="p-3 rounded-circle bg-rose-600/20 text-rose-400 d-inline-block mb-3">
            <AlertTriangle size={48} />
          </div>
          <h1 className="display-4 fw-extrabold text-rose-400 mb-2">404</h1>
          <h4 className="fw-bold mb-2">Page Not Found</h4>
          <p className="text-sm text-slate-400 mb-4">
            The route or evaluation record you requested does not exist or has been moved.
          </p>
          <Link to="/" className="btn btn-fintech d-inline-flex align-items-center gap-2">
            <Home size={18}/> Return to Safety (Home)
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
