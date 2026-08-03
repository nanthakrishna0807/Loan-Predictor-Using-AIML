import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Line, Pie } from 'react-chartjs-2';
import { exportToExcel } from '../utils/excelExport';
import { LayoutDashboard, PlusCircle, FileText, TrendingUp, ShieldCheck, Download, Trash2, User } from 'lucide-react';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ArcElement);

const UserDashboard = () => {
  const { user } = useContext(AuthContext);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await axios.get('/api/loan/history');
      const payloadData = res.data?.data || res.data;
      if (payloadData && payloadData.history) {
        setHistory(payloadData.history);
      }
    } catch (e) {
      console.log("Could not load user prediction history.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to remove this prediction record?")) return;
    try {
      await axios.delete(`/api/loan/${id}`);
      setHistory(prev => prev.filter(item => item._id !== id));
    } catch (e) {
      alert("Could not delete record.");
    }
  };

  // Summary Metrics
  const totalApps = history.length;
  const approvedCount = history.filter(h => h.approved || h.loanStatus === 'Approved').length;
  const rejectedCount = totalApps - approvedCount;
  const avgProbability = totalApps > 0
    ? Math.round(history.reduce((acc, curr) => acc + (curr.approvalProbability || 75), 0) / totalApps)
    : 85;

  // Chart Data
  const pieData = {
    labels: ['Approved', 'Rejected'],
    datasets: [
      {
        data: [approvedCount || 2, rejectedCount || 1],
        backgroundColor: ['#22C55E', '#EF4444'],
        borderColor: ['#15803D', '#991B1B'],
        borderWidth: 1
      }
    ]
  };

  const lineData = {
    labels: history.slice(0, 6).reverse().map((_, idx) => `App #${idx + 1}`),
    datasets: [
      {
        label: 'CIBIL Score',
        data: history.slice(0, 6).reverse().map(h => h.cibilScore || 650),
        borderColor: '#38BDF8',
        backgroundColor: 'rgba(56, 189, 248, 0.2)',
        tension: 0.3
      }
    ]
  };

  return (
    <div className="py-5">
      <div className="container">
        {/* Welcome Card */}
        <div className="glass-card p-4 p-md-5 mb-4 border-blue-500/30 text-white d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
          <div>
            <span className="badge bg-blue-900/60 text-cyan-400 border border-cyan-500/30 px-3 py-1 rounded-pill text-xs fw-semibold mb-2">
              USER DASHBOARD
            </span>
            <h2 className="fw-extrabold mb-1">Welcome back, {user?.name || "Applicant"}! 👋</h2>
            <p className="text-sm text-slate-300 mb-0">Track your credit risk metrics, loan history, and ML eligibility recommendations.</p>
          </div>
          <div className="d-flex gap-2">
            <Link to="/predict" className="btn btn-fintech py-2.5 px-4 text-sm d-flex align-items-center gap-2">
              <PlusCircle size={18}/> New Application
            </Link>
          </div>
        </div>

        {/* Financial Summary Cards */}
        <div className="row g-3 mb-4">
          <div className="col-md-3 col-6">
            <div className="glass-card p-3 text-white">
              <span className="text-2xs text-slate-400 d-block">TOTAL APPLICATIONS</span>
              <span className="h3 fw-bold text-cyan-400">{totalApps}</span>
              <span className="text-2xs text-slate-400 d-block">Evaluated by ML</span>
            </div>
          </div>
          <div className="col-md-3 col-6">
            <div className="glass-card p-3 text-white">
              <span className="text-2xs text-slate-400 d-block">APPROVED LOANS</span>
              <span className="h3 fw-bold text-emerald-400">{approvedCount}</span>
              <span className="text-2xs text-emerald-400 d-block">Success Eligibility</span>
            </div>
          </div>
          <div className="col-md-3 col-6">
            <div className="glass-card p-3 text-white">
              <span className="text-2xs text-slate-400 d-block">REJECTED LOANS</span>
              <span className="h3 fw-bold text-rose-400">{rejectedCount}</span>
              <span className="text-2xs text-rose-400 d-block">High Risk Flags</span>
            </div>
          </div>
          <div className="col-md-3 col-6">
            <div className="glass-card p-3 text-white">
              <span className="text-2xs text-slate-400 d-block">AVG APPROVAL PROB.</span>
              <span className="h3 fw-bold text-amber-400">{avgProbability}%</span>
              <span className="text-2xs text-slate-400 d-block">Credit Confidence</span>
            </div>
          </div>
        </div>

        {/* Analytics & Profile Row */}
        <div className="row g-4 mb-4">
          <div className="col-lg-4">
            <div className="glass-card p-4 text-white h-100">
              <h6 className="fw-semibold text-slate-200 mb-3">Loan Approval Ratio</h6>
              <div className="w-75 mx-auto">
                <Pie data={pieData} />
              </div>
            </div>
          </div>

          <div className="col-lg-8">
            <div className="glass-card p-4 text-white h-100">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h6 className="fw-semibold text-slate-200 mb-0">CIBIL Trend Across Applications</h6>
                <button onClick={() => exportToExcel(history)} className="btn btn-outline-fintech btn-sm text-xs">
                  <Download size={14}/> Export History
                </button>
              </div>
              <div style={{ height: 220 }}>
                <Line data={lineData} options={{ maintainAspectRatio: false }} />
              </div>
            </div>
          </div>
        </div>

        {/* Previous Predictions History Table */}
        <div className="glass-card p-4 text-white">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h5 className="fw-bold mb-0">Application Prediction History</h5>
            <span className="text-xs text-slate-400">{history.length} Record(s)</span>
          </div>

          <div className="table-responsive">
            <table className="table table-dark table-hover align-middle border-slate-800 text-sm">
              <thead>
                <tr className="text-slate-400 text-xs">
                  <th>Date</th>
                  <th>Applicant</th>
                  <th>CIBIL</th>
                  <th>Loan Amount</th>
                  <th>Status</th>
                  <th>Risk Level</th>
                  <th>Est. EMI</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {history.length > 0 ? (
                  history.map((item) => (
                    <tr key={item._id}>
                      <td className="text-slate-400 text-xs">{new Date(item.createdAt).toLocaleDateString()}</td>
                      <td className="fw-medium text-white">{item.applicantName}</td>
                      <td>
                        <span className="fw-bold" style={{ color: item.cibilColor || '#38BDF8' }}>
                          {item.cibilScore}
                        </span>
                      </td>
                      <td className="fw-semibold text-cyan-400">₹{Number(item.loanAmount).toLocaleString()}</td>
                      <td>
                        <span className={`badge px-2.5 py-1 text-xs rounded-pill ${item.approved || item.loanStatus === 'Approved' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-400 border border-rose-500/40'}`}>
                          {item.loanStatus || (item.approved ? 'Approved' : 'Rejected')}
                        </span>
                      </td>
                      <td>
                        <span className="badge px-2 py-0.5 text-2xs" style={{ backgroundColor: `${item.creditRiskColor || '#22C55E'}25`, color: item.creditRiskColor || '#22C55E' }}>
                          {item.creditRiskLevel || 'Low'} Risk
                        </span>
                      </td>
                      <td className="text-slate-300">₹{Number(item.emiEstimate || 0).toLocaleString()}</td>
                      <td>
                        <div className="d-flex gap-2">
                          <Link to={`/result/${item._id}`} className="btn btn-sm btn-outline-fintech py-0.5 px-2 text-xs">
                            View Report
                          </Link>
                          <button onClick={() => handleDelete(item._id)} className="btn btn-sm btn-outline-danger py-0.5 px-2 text-xs">
                            <Trash2 size={14}/>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="8" className="text-center py-4 text-slate-400">
                      No loan applications evaluated yet. Click <strong>New Application</strong> above to start!
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
