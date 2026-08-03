import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Github, Twitter, Linkedin, Mail, Phone, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="border-t border-slate-800 bg-slate-950 text-slate-400 py-5 mt-auto">
      <div className="container">
        <div className="row g-4 mb-4">
          <div className="col-lg-4 col-md-6">
            <div className="d-flex align-items-center gap-2 mb-3">
              <div className="p-2 rounded-3 bg-blue-600 text-white">
                <ShieldCheck size={24} />
              </div>
              <span className="h5 fw-bold mb-0 text-white">AI Loan <span className="text-cyan-400">Predictor</span></span>
            </div>
            <p className="text-sm text-slate-400">
              Next-generation Machine Learning Loan Eligibility & Credit Risk Evaluation system. Powered by Random Forest, Gradient Boosting, and intelligent CIBIL score analytics.
            </p>
            <div className="d-flex gap-3 text-slate-400">
              <a href="#" className="hover:text-cyan-400 transition"><Github size={18}/></a>
              <a href="#" className="hover:text-cyan-400 transition"><Twitter size={18}/></a>
              <a href="#" className="hover:text-cyan-400 transition"><Linkedin size={18}/></a>
            </div>
          </div>

          <div className="col-lg-2 col-md-6">
            <h6 className="text-white fw-semibold mb-3">Quick Links</h6>
            <ul className="list-unstyled d-flex flex-column gap-2 text-sm">
              <li><Link to="/" className="text-slate-400 hover:text-cyan-400 text-decoration-none">Home</Link></li>
              <li><Link to="/features" className="text-slate-400 hover:text-cyan-400 text-decoration-none">Features</Link></li>
              <li><Link to="/about" className="text-slate-400 hover:text-cyan-400 text-decoration-none">About ML Engine</Link></li>
              <li><Link to="/calculator" className="text-slate-400 hover:text-cyan-400 text-decoration-none">EMI Calculator</Link></li>
              <li><Link to="/predict" className="text-slate-400 hover:text-cyan-400 text-decoration-none">Loan Application</Link></li>
            </ul>
          </div>

          <div className="col-lg-3 col-md-6">
            <h6 className="text-white fw-semibold mb-3">CIBIL Ranges</h6>
            <ul className="list-unstyled d-flex flex-column gap-2 text-xs">
              <li className="d-flex justify-content-between"><span className="text-emerald-400 fw-medium">750 – 900</span> <span className="badge bg-emerald-900/50 text-emerald-300">Excellent</span></li>
              <li className="d-flex justify-content-between"><span className="text-sky-400 fw-medium">650 – 749</span> <span className="badge bg-sky-900/50 text-sky-300">Good</span></li>
              <li className="d-flex justify-content-between"><span className="text-amber-400 fw-medium">550 – 649</span> <span className="badge bg-amber-900/50 text-amber-300">Fair</span></li>
              <li className="d-flex justify-content-between"><span className="text-rose-400 fw-medium">300 – 549</span> <span className="badge bg-rose-900/50 text-rose-300">Poor</span></li>
            </ul>
          </div>

          <div className="col-lg-3 col-md-6">
            <h6 className="text-white fw-semibold mb-3">Support & Legal</h6>
            <ul className="list-unstyled d-flex flex-column gap-2 text-sm">
              <li className="d-flex align-items-center gap-2"><Mail size={16}/> support@loanpredictor.ai</li>
              <li className="d-flex align-items-center gap-2"><Phone size={16}/> +1 (800) 555-LOAN</li>
              <li className="d-flex align-items-center gap-2"><MapPin size={16}/> FinTech Tower, Level 14</li>
            </ul>
          </div>
        </div>

        <hr className="border-slate-800 my-3" />

        <div className="d-flex flex-column flex-md-row justify-content-between align-items-center text-xs text-slate-500">
          <p className="mb-0">© 2026 AI Loan Predictor. All rights reserved. Designed for Modern FinTech Applications.</p>
          <div className="d-flex gap-3 mt-2 mt-md-0">
            <a href="#" className="text-slate-500 hover:text-slate-300 text-decoration-none">Privacy Policy</a>
            <a href="#" className="text-slate-500 hover:text-slate-300 text-decoration-none">Terms of Service</a>
            <a href="#" className="text-slate-500 hover:text-slate-300 text-decoration-none">Security Compliance</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
