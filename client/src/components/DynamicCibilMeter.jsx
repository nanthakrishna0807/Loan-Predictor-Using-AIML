import React from 'react';
import { motion } from 'framer-motion';
import { ShieldAlert, CheckCircle2, AlertTriangle, AlertCircle } from 'lucide-react';

const DynamicCibilMeter = ({ score = 650, threshold = 650 }) => {
  // Normalize score between 300 and 900
  const normalizedScore = Math.max(300, Math.min(900, score));

  // Determine category & colors
  let category = "Good";
  let color = "#38BDF8";
  let icon = <CheckCircle2 size={20} className="text-sky-400" />;
  let description = "Good credit standing. Eligible for standard interest rates.";

  if (normalizedScore >= 750) {
    category = "Excellent";
    color = "#22C55E";
    icon = <CheckCircle2 size={20} className="text-emerald-400" />;
    description = "Prime credit score! Eligible for premium loan rates & maximum approval limits.";
  } else if (normalizedScore >= 650) {
    category = "Good";
    color = "#38BDF8";
    icon = <CheckCircle2 size={20} className="text-sky-400" />;
    description = "Solid credit profile. High probability of approval with good terms.";
  } else if (normalizedScore >= 550) {
    category = "Fair";
    color = "#F59E0B";
    icon = <AlertTriangle size={20} className="text-amber-400" />;
    description = "Fair score. Below recommended threshold (650). Approval subject to higher interest rate or collateral.";
  } else {
    category = "Poor";
    color = "#EF4444";
    icon = <AlertCircle size={20} className="text-rose-400" />;
    description = "Critical risk score (<550). Automated rejection lean unless supported by high income & zero debt.";
  }

  // Calculate gauge angle (from -90deg to +90deg for semicircle)
  const percentage = (normalizedScore - 300) / (900 - 300); // 0 to 1
  const strokeDashoffset = 283 - 283 * percentage; // radius 45 -> circumference 2*pi*45 ~ 283

  return (
    <div className="glass-card p-4 text-center text-white position-relative">
      <h5 className="fw-semibold text-slate-200 mb-2">Dynamic CIBIL Score Meter</h5>
      <p className="text-xs text-slate-400 mb-3">Live Credit Rating Gauge (Range: 300 – 900)</p>

      {/* SVG Radial Gauge */}
      <div className="position-relative d-inline-block mx-auto mb-3" style={{ width: 180, height: 180 }}>
        <svg viewBox="0 0 100 100" className="w-100 h-100" style={{ transform: 'rotate(-90deg)' }}>
          {/* Background Track */}
          <circle
            cx="50"
            cy="50"
            r="42"
            fill="transparent"
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth="10"
          />
          {/* Animated Gauge Progress */}
          <motion.circle
            cx="50"
            cy="50"
            r="42"
            fill="transparent"
            stroke={color}
            strokeWidth="10"
            strokeDasharray="264"
            initial={{ strokeDashoffset: 264 }}
            animate={{ strokeDashoffset: 264 - 264 * percentage }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            strokeLinecap="round"
          />
        </svg>

        {/* Center Display */}
        <div className="position-absolute top-50 start-50 translate-middle text-center">
          <motion.div
            key={normalizedScore}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="h2 fw-bold mb-0"
            style={{ color: color }}
          >
            {normalizedScore}
          </motion.div>
          <span className="badge px-2.5 py-1 text-xs fw-bold rounded-pill" style={{ backgroundColor: `${color}25`, color: color, border: `1px solid ${color}` }}>
            {category}
          </span>
        </div>
      </div>

      {/* CIBIL Range Legends */}
      <div className="row g-1 text-xs text-slate-300 mt-1 mb-3">
        <div className="col-3 p-1 rounded" style={{ background: 'rgba(239, 68, 68, 0.15)', border: normalizedScore < 550 ? '1px solid #EF4444' : 'none' }}>
          <div className="fw-bold text-rose-400">300-549</div>
          <div className="text-2xs">Poor</div>
        </div>
        <div className="col-3 p-1 rounded" style={{ background: 'rgba(245, 158, 11, 0.15)', border: (normalizedScore >= 550 && normalizedScore < 650) ? '1px solid #F59E0B' : 'none' }}>
          <div className="fw-bold text-amber-400">550-649</div>
          <div className="text-2xs">Fair</div>
        </div>
        <div className="col-3 p-1 rounded" style={{ background: 'rgba(56, 189, 248, 0.15)', border: (normalizedScore >= 650 && normalizedScore < 750) ? '1px solid #38BDF8' : 'none' }}>
          <div className="fw-bold text-sky-400">650-749</div>
          <div className="text-2xs">Good</div>
        </div>
        <div className="col-3 p-1 rounded" style={{ background: 'rgba(34, 197, 94, 0.15)', border: normalizedScore >= 750 ? '1px solid #22C55E' : 'none' }}>
          <div className="fw-bold text-emerald-400">750-900</div>
          <div className="text-2xs">Excellent</div>
        </div>
      </div>

      {/* Threshold Warning Banner if score < 650 */}
      {normalizedScore < threshold && (
        <div className="p-2.5 rounded-3 bg-amber-950/40 border border-amber-500/40 text-amber-300 text-xs d-flex align-items-center gap-2">
          <ShieldAlert size={18} className="flex-shrink-0 text-amber-400" />
          <div className="text-start">
            <span className="fw-bold">Threshold Alert:</span> CIBIL is below {threshold}. Machine Learning algorithm leans towards rejection unless income & bank balance strongly compensate.
          </div>
        </div>
      )}
    </div>
  );
};

export default DynamicCibilMeter;
