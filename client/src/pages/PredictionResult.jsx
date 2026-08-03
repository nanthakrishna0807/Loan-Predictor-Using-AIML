import React, { useState, useEffect } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import axios from 'axios';
import CreditRiskGauge from '../components/CreditRiskGauge';
import DynamicCibilMeter from '../components/DynamicCibilMeter';
import { generatePDFReport } from '../utils/pdfExport';
import { exportToExcel } from '../utils/excelExport';
import { CheckCircle2, XCircle, Download, FileSpreadsheet, ArrowLeft, Lightbulb, ShieldCheck, Cpu } from 'lucide-react';

const PredictionResult = () => {
  const { id } = useParams();
  const location = useLocation();
  
  const [prediction, setPrediction] = useState(location.state?.prediction || null);
  const [loading, setLoading] = useState(!prediction);

  useEffect(() => {
    if (!prediction && id) {
      fetchPrediction();
    }
  }, [id]);

  const fetchPrediction = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`/api/loan/${id}`);
      if (res.data && res.data.success) {
        setPrediction(res.data.prediction);
      }
    } catch (e) {
      console.log("Could not load prediction details.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="py-5 text-center text-white">
        <div className="spinner-border text-cyan-400 mb-3" role="status"></div>
        <p>Loading AI Loan Evaluation Results...</p>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="py-5 text-center text-white">
        <h4 className="text-rose-400">Prediction Record Not Found</h4>
        <Link to="/predict" className="btn btn-fintech mt-3">Back to Application</Link>
      </div>
    );
  }

  const isApproved = prediction.approved || prediction.loanStatus === 'Approved';

  return (
    <div className="py-5">
      <div className="container">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <Link to="/predict" className="btn btn-outline-fintech btn-sm d-inline-flex align-items-center gap-1">
            <ArrowLeft size={16}/> New Application
          </Link>
          
          <div className="d-flex gap-2">
            <button
              onClick={() => generatePDFReport('report-card', `Loan_Report_${prediction.applicantName.replace(/\s+/g, '_')}.pdf`)}
              className="btn btn-fintech btn-sm"
            >
              <Download size={16}/> Download PDF Report
            </button>
            <button
              onClick={() => exportToExcel([prediction], `Prediction_${prediction.applicantName.replace(/\s+/g, '_')}.xlsx`)}
              className="btn btn-outline-fintech btn-sm"
            >
              <FileSpreadsheet size={16}/> Export Excel
            </button>
          </div>
        </div>

        {/* Exportable PDF Canvas Container */}
        <div id="report-card" className="glass-card p-4 p-md-5 text-white border-blue-500/30 glow-accent">
          {/* Header Banner */}
          <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center border-b border-slate-800 pb-4 mb-4 gap-3">
            <div>
              <span className="badge bg-blue-900/60 text-cyan-400 border border-cyan-500/30 px-3 py-1 rounded-pill text-xs fw-semibold mb-2">
                OFFICIAL AI ASSESSMENT REPORT
              </span>
              <h2 className="fw-extrabold text-white mb-0">{prediction.applicantName}</h2>
              <span className="text-xs text-slate-400">Generated on {new Date(prediction.createdAt || Date.now()).toLocaleString()}</span>
            </div>

            <div className="d-flex align-items-center gap-3">
              <div className="text-end">
                <span className="text-2xs text-slate-400 d-block">ML MODEL STATUS</span>
                <span className="text-xs fw-bold text-cyan-400">{prediction.modelUsed || "Random Forest Classifier"}</span>
              </div>
              <div className={`p-3 rounded-4 d-flex align-items-center gap-2 ${isApproved ? 'bg-emerald-950/80 border border-emerald-500 text-emerald-400' : 'bg-rose-950/80 border border-rose-500 text-rose-400'}`}>
                {isApproved ? <CheckCircle2 size={32} /> : <XCircle size={32} />}
                <div>
                  <span className="text-2xs text-slate-300 d-block">PREDICTION DECISION</span>
                  <span className="h4 fw-extrabold mb-0">{isApproved ? "LOAN APPROVED" : "LOAN REJECTED"}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Core Prediction Gauges Row */}
          <div className="row g-4 mb-4">
            <div className="col-md-4">
              <DynamicCibilMeter score={prediction.cibilScore} threshold={650} />
            </div>

            <div className="col-md-4">
              <CreditRiskGauge
                riskLevel={prediction.creditRiskLevel}
                riskColor={prediction.creditRiskColor}
                probability={prediction.approvalProbability}
              />
            </div>

            <div className="col-md-4">
              <div className="glass-card p-4 h-100 d-flex flex-column justify-content-between">
                <h6 className="fw-semibold text-slate-200 mb-2">Model Confidence Score</h6>
                <div className="text-center my-auto">
                  <div className="display-5 fw-extrabold text-cyan-400 mb-1">{prediction.confidenceScore}%</div>
                  <span className="text-xs text-slate-400">Ensemble Statistical Certainty</span>
                </div>
                <div className="p-2 rounded-3 bg-slate-900/60 border border-slate-800 text-center text-xs text-slate-300">
                  Calculated using 20+ Financial Indicators
                </div>
              </div>
            </div>
          </div>

          {/* Key Loan Financial Metrics */}
          <div className="row g-3 mb-4">
            <div className="col-md-3 col-6">
              <div className="p-3 rounded-3 bg-slate-900/80 border border-slate-800">
                <span className="text-2xs text-slate-400 d-block">SUGGESTED MAX LOAN</span>
                <span className="h4 fw-bold text-emerald-400">₹{Number(prediction.suggestedMaxLoan || 0).toLocaleString()}</span>
              </div>
            </div>
            <div className="col-md-3 col-6">
              <div className="p-3 rounded-3 bg-slate-900/80 border border-slate-800">
                <span className="text-2xs text-slate-400 d-block">ESTIMATED EMI</span>
                <span className="h4 fw-bold text-sky-400">₹{Number(prediction.emiEstimate || 0).toLocaleString()}</span>
              </div>
            </div>
            <div className="col-md-3 col-6">
              <div className="p-3 rounded-3 bg-slate-900/80 border border-slate-800">
                <span className="text-2xs text-slate-400 d-block">ESTIMATED APR RATE</span>
                <span className="h4 fw-bold text-amber-400">{prediction.interestRateEstimate}%</span>
              </div>
            </div>
            <div className="col-md-3 col-6">
              <div className="p-3 rounded-3 bg-slate-900/80 border border-slate-800">
                <span className="text-2xs text-slate-400 d-block">DEBT-TO-INCOME (DTI)</span>
                <span className="h4 fw-bold text-purple-400">{Math.round((prediction.debtToIncomeRatio || 0) * 100)}%</span>
              </div>
            </div>
          </div>

          {/* Recommendations & Tips */}
          <div className="row g-4">
            <div className="col-lg-6">
              <div className="p-4 rounded-3 bg-blue-950/30 border border-blue-500/30 h-100">
                <h6 className="fw-bold text-cyan-400 mb-2 d-flex align-items-center gap-2">
                  <ShieldCheck size={18}/> AI Loan Recommendation
                </h6>
                <p className="text-sm text-slate-200 mb-0">{prediction.loanRecommendation}</p>
              </div>
            </div>

            <div className="col-lg-6">
              <div className="p-4 rounded-3 bg-amber-950/30 border border-amber-500/30 h-100">
                <h6 className="fw-bold text-amber-400 mb-2 d-flex align-items-center gap-2">
                  <Lightbulb size={18}/> Financial Improvement Tips
                </h6>
                <ul className="list-unstyled text-xs text-slate-200 d-flex flex-column gap-1.5 mb-0">
                  {prediction.financialImprovementTips?.map((tip, idx) => (
                    <li key={idx} className="d-flex align-items-start gap-2">
                      <span className="text-amber-400 font-bold">•</span>
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionResult;
