import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Cpu, ShieldCheck, TrendingUp, BarChart3, Lock, CheckCircle, ArrowRight, Zap, FileSpreadsheet } from 'lucide-react';

const LandingPage = () => {
  return (
    <div className="landing-page overflow-hidden">
      {/* Hero Section */}
      <section className="position-relative py-5 my-4">
        <div className="container">
          <div className="row align-items-center g-5">
            <div className="col-lg-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                <div className="inline-flex align-items-center gap-2 px-3 py-1.5 rounded-pill bg-blue-900/40 border border-blue-500/30 text-cyan-400 text-xs font-semibold mb-4">
                  <Zap size={14} className="text-cyan-400" />
                  <span>AI-Powered FinTech Loan Evaluation Engine v2.4</span>
                </div>
                <h1 className="display-4 fw-extrabold text-white tracking-tight mb-3">
                  Smart <span className="gradient-text">Loan Eligibility</span> Prediction System
                </h1>
                <p className="lead text-slate-300 mb-4">
                  Evaluate instant loan approval probability using Machine Learning algorithms (Random Forest & XGBoost). Features real-time CIBIL score analytics, credit risk gauge, EMI estimations, and financial health scoring.
                </p>
                <div className="d-flex flex-wrap gap-3 mb-4">
                  <Link to="/predict" className="btn btn-fintech btn-lg px-4 py-3 text-base">
                    <Cpu size={20} /> Apply for Loan Eligibility
                  </Link>
                  <Link to="/calculator" className="btn btn-outline-fintech btn-lg px-4 py-3 text-base">
                    <TrendingUp size={20} /> Try EMI Calculator
                  </Link>
                </div>
                <div className="d-flex align-items-center gap-4 text-xs text-slate-400 border-t border-slate-800 pt-3">
                  <span className="d-flex align-items-center gap-1.5"><CheckCircle size={15} className="text-emerald-400"/> 94.2% ML Model Accuracy</span>
                  <span className="d-flex align-items-center gap-1.5"><CheckCircle size={15} className="text-emerald-400"/> Dynamic CIBIL Meter</span>
                  <span className="d-flex align-items-center gap-1.5"><CheckCircle size={15} className="text-emerald-400"/> JWT Encrypted</span>
                </div>
              </motion.div>
            </div>

            <div className="col-lg-6">
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.7, delay: 0.2 }}
                className="position-relative"
              >
                {/* Hero Glass Card Graphic */}
                <div className="glass-card p-4 p-md-5 border-cyan-500/30 glow-blue text-white">
                  <div className="d-flex justify-content-between align-items-center mb-4">
                    <div>
                      <span className="text-xs text-slate-400">MODEL PREDICTION DEMO</span>
                      <h5 className="fw-bold mb-0">Loan Approval Assessment</h5>
                    </div>
                    <span className="badge bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-3 py-1.5 rounded-pill text-xs fw-bold">
                      APPROVED (92.4%)
                    </span>
                  </div>

                  <div className="row g-3 mb-4">
                    <div className="col-6">
                      <div className="p-3 rounded-3 bg-slate-900/60 border border-slate-800">
                        <span className="text-2xs text-slate-400 d-block">APPLICANT CIBIL</span>
                        <span className="h4 fw-bold text-emerald-400">780</span>
                        <span className="text-2xs text-emerald-400 d-block ms-1">Excellent Score</span>
                      </div>
                    </div>
                    <div className="col-6">
                      <div className="p-3 rounded-3 bg-slate-900/60 border border-slate-800">
                        <span className="text-2xs text-slate-400 d-block">ESTIMATED EMI</span>
                        <span className="h4 fw-bold text-sky-400">₹12,450</span>
                        <span className="text-2xs text-slate-400 d-block">@ 9.2% APR</span>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 rounded-3 bg-slate-900/40 border border-slate-800 mb-4">
                    <div className="d-flex justify-content-between text-xs text-slate-300 mb-1">
                      <span>Approval Probability</span>
                      <span className="fw-bold text-cyan-400">92.4%</span>
                    </div>
                    <div className="w-100 bg-slate-800 rounded-pill overflow-hidden" style={{ height: 8 }}>
                      <div className="bg-gradient-to-r from-blue-500 to-cyan-400 h-100 rounded-pill" style={{ width: '92.4%' }}></div>
                    </div>
                  </div>

                  <div className="d-flex justify-content-between align-items-center text-xs text-slate-400">
                    <span>Algorithm: Random Forest</span>
                    <Link to="/predict" className="text-cyan-400 hover:text-cyan-300 fw-semibold text-decoration-none d-flex align-items-center gap-1">
                      Run Live Prediction <ArrowRight size={14} />
                    </Link>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-5 bg-slate-950/60 border-y border-slate-800">
        <div className="container py-4">
          <div className="text-center max-w-2xl mx-auto mb-5">
            <h2 className="h1 fw-bold text-white mb-3">Enterprise AI Features</h2>
            <p className="text-slate-400">Comprehensive machine learning evaluation pipeline built for transparency and accuracy.</p>
          </div>

          <div className="row g-4">
            <div className="col-md-4">
              <div className="glass-card p-4 h-100">
                <div className="p-3 rounded-3 bg-blue-600/20 text-cyan-400 d-inline-block mb-3">
                  <Cpu size={28} />
                </div>
                <h5 className="fw-bold text-white mb-2">ML Ensemble Engine</h5>
                <p className="text-sm text-slate-400 mb-0">
                  Automated comparison across Random Forest, XGBoost, Decision Tree, and Logistic Regression to select the highest accuracy model.
                </p>
              </div>
            </div>

            <div className="col-md-4">
              <div className="glass-card p-4 h-100">
                <div className="p-3 rounded-3 bg-emerald-600/20 text-emerald-400 d-inline-block mb-3">
                  <TrendingUp size={28} />
                </div>
                <h5 className="fw-bold text-white mb-2">Dynamic CIBIL Meter</h5>
                <p className="text-sm text-slate-400 mb-0">
                  Visual credit score gauge (300-900) enforcing configurable threshold logic for rejection lean under 650.
                </p>
              </div>
            </div>

            <div className="col-md-4">
              <div className="glass-card p-4 h-100">
                <div className="p-3 rounded-3 bg-cyan-600/20 text-cyan-300 d-inline-block mb-3">
                  <BarChart3 size={28} />
                </div>
                <h5 className="fw-bold text-white mb-2">Visual Analytics Dashboard</h5>
                <p className="text-sm text-slate-400 mb-0">
                  Chart.js powered charts visualizing approval rates, CIBIL distributions, monthly trends, and risk categories.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-5 my-4">
        <div className="container">
          <div className="glass-card p-5 text-center border-blue-500/40 glow-accent">
            <h2 className="display-6 fw-bold text-white mb-3">Ready to Predict Your Loan Eligibility?</h2>
            <p className="lead text-slate-300 mb-4 max-w-xl mx-auto">
              Get an instant AI prediction, risk rating, EMI estimate, and personalized financial tips in under 2 minutes.
            </p>
            <Link to="/predict" className="btn btn-fintech btn-lg px-5 py-3 text-base">
              Get Started Now
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
