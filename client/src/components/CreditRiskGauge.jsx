import React from 'react';
import { motion } from 'framer-motion';

const CreditRiskGauge = ({ riskLevel = "Low", riskColor = "#22C55E", probability = 85 }) => {
  const levels = ["Low", "Medium", "High", "Critical"];
  const currentIdx = levels.indexOf(riskLevel) !== -1 ? levels.indexOf(riskLevel) : 0;

  return (
    <div className="glass-card p-4 text-white">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h6 className="fw-semibold text-slate-200 mb-0">Credit Risk Level</h6>
        <span className="badge px-3 py-1 text-xs fw-bold rounded-pill" style={{ backgroundColor: `${riskColor}25`, color: riskColor, border: `1px solid ${riskColor}` }}>
          {riskLevel} Risk
        </span>
      </div>

      <div className="mb-3">
        <div className="d-flex justify-content-between text-xs text-slate-400 mb-1">
          <span>Risk Assessment Index</span>
          <span className="fw-bold" style={{ color: riskColor }}>{probability}% Approval Prob.</span>
        </div>
        
        {/* Multicolored Segmented Progress Bar */}
        <div className="w-100 rounded-pill overflow-hidden d-flex p-1 bg-slate-900 border border-slate-800" style={{ height: 16 }}>
          <motion.div
            className="rounded-pill h-100"
            style={{ backgroundColor: riskColor }}
            initial={{ width: '0%' }}
            animate={{ width: `${probability}%` }}
            transition={{ duration: 1.0, ease: 'easeOut' }}
          />
        </div>
      </div>

      <div className="row g-1 text-center text-xs">
        <div className={`col-3 p-1 rounded ${currentIdx === 0 ? 'bg-emerald-950/60 border border-emerald-500 text-emerald-400' : 'text-slate-500'}`}>
          Low
        </div>
        <div className={`col-3 p-1 rounded ${currentIdx === 1 ? 'bg-amber-950/60 border border-amber-500 text-amber-400' : 'text-slate-500'}`}>
          Medium
        </div>
        <div className={`col-3 p-1 rounded ${currentIdx === 2 ? 'bg-orange-950/60 border border-orange-500 text-orange-400' : 'text-slate-500'}`}>
          High
        </div>
        <div className={`col-3 p-1 rounded ${currentIdx === 3 ? 'bg-rose-950/60 border border-rose-500 text-rose-400' : 'text-slate-500'}`}>
          Critical
        </div>
      </div>
    </div>
  );
};

export default CreditRiskGauge;
