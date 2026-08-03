import React from 'react';
import { Cpu, ShieldCheck, BarChart3, FileSpreadsheet, Lock, Sparkles, CheckCircle2, Sliders, FileText } from 'lucide-react';

const Features = () => {
  return (
    <div className="py-5">
      <div className="container">
        <div className="text-center max-w-2xl mx-auto mb-5">
          <span className="badge bg-blue-900/60 text-cyan-400 border border-cyan-500/30 px-3 py-1.5 rounded-pill text-xs fw-semibold mb-3">
            CAPABILITIES & ALGORITHMS
          </span>
          <h1 className="display-5 fw-bold text-white mb-3">System Features & Modules</h1>
          <p className="lead text-slate-300">Explore the advanced technological components driving our smart loan prediction framework.</p>
        </div>

        <div className="row g-4">
          <div className="col-lg-6">
            <div className="glass-card p-4 h-100">
              <div className="d-flex align-items-center gap-3 mb-3">
                <div className="p-3 rounded-3 bg-blue-600/20 text-cyan-400">
                  <Cpu size={28} />
                </div>
                <h4 className="fw-bold text-white mb-0">Automated Machine Learning Benchmark</h4>
              </div>
              <p className="text-slate-300 text-sm mb-3">
                Evaluates 4 standard algorithms against historical loan datasets: Random Forest Classifier, XGBoost / Gradient Boosting, Decision Trees, and Logistic Regression. Automatically selects and deploys the highest accuracy model.
              </p>
              <ul className="list-unstyled text-xs text-slate-400 d-flex flex-column gap-2">
                <li className="d-flex align-items-center gap-2"><CheckCircle2 size={16} className="text-emerald-400"/> Hyperparameter Tuning via Scikit-Learn</li>
                <li className="d-flex align-items-center gap-2"><CheckCircle2 size={16} className="text-emerald-400"/> Scaled numerical features with StandardScaler</li>
                <li className="d-flex align-items-center gap-2"><CheckCircle2 size={16} className="text-emerald-400"/> Preserved artifacts serialized using Joblib</li>
              </ul>
            </div>
          </div>

          <div className="col-lg-6">
            <div className="glass-card p-4 h-100">
              <div className="d-flex align-items-center gap-3 mb-3">
                <div className="p-3 rounded-3 bg-emerald-600/20 text-emerald-400">
                  <Sliders size={28} />
                </div>
                <h4 className="fw-bold text-white mb-0">CIBIL Threshold Logic Engine</h4>
              </div>
              <p className="text-slate-300 text-sm mb-3">
                Integrates financial credit scoring logic into model predictions. CIBIL scores below 650 automatically bias prediction toward rejection unless compensated by low debt ratios and strong bank reserves.
              </p>
              <div className="row g-2 text-xs text-slate-200 mt-2">
                <div className="col-6 p-2 rounded bg-slate-900/60 border border-slate-800">300 – 549: Poor Score</div>
                <div className="col-6 p-2 rounded bg-slate-900/60 border border-slate-800">550 – 649: Fair Score</div>
                <div className="col-6 p-2 rounded bg-slate-900/60 border border-slate-800">650 – 749: Good Score</div>
                <div className="col-6 p-2 rounded bg-slate-900/60 border border-slate-800">750 – 900: Excellent Score</div>
              </div>
            </div>
          </div>

          <div className="col-lg-6">
            <div className="glass-card p-4 h-100">
              <div className="d-flex align-items-center gap-3 mb-3">
                <div className="p-3 rounded-3 bg-sky-600/20 text-sky-400">
                  <FileText size={28} />
                </div>
                <h4 className="fw-bold text-white mb-0">PDF Reports & Excel Data Export</h4>
              </div>
              <p className="text-slate-300 text-sm mb-3">
                Instantly generate clean PDF evaluation certificates containing application breakdown, credit risk ratings, EMI estimations, and tailored improvement recommendations. Export full historical records to XLSX format.
              </p>
            </div>
          </div>

          <div className="col-lg-6">
            <div className="glass-card p-4 h-100">
              <div className="d-flex align-items-center gap-3 mb-3">
                <div className="p-3 rounded-3 bg-purple-600/20 text-purple-400">
                  <Lock size={28} />
                </div>
                <h4 className="fw-bold text-white mb-0">Role-Based JWT Security</h4>
              </div>
              <p className="text-slate-300 text-sm mb-3">
                End-to-end security architecture. JSON Web Tokens ensure user route protection, password hashing via Bcrypt, and strict role separation for Admin and User dashboards.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Features;
