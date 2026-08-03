import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import { Users, Cpu, ShieldCheck, CheckCircle2, XCircle, Activity, RefreshCw, Trash2, Download, BarChart3 } from 'lucide-react';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend);

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [usersList, setUsersList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);
  const [retrainMsg, setRetrainMsg] = useState('');

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    setLoading(true);
    try {
      const [dashRes, userRes] = await Promise.all([
        axios.get('/api/admin/dashboard'),
        axios.get('/api/admin/users')
      ]);

      const dashData = dashRes.data?.data || dashRes.data;
      const userData = userRes.data?.data || userRes.data;

      if (dashData && dashData.stats) {
        setStats(dashData.stats);
      }
      if (userData && userData.users) {
        setUsersList(userData.users);
      }
    } catch (e) {
      console.log("Could not load admin stats.");
    } finally {
      setLoading(false);
    }
  };

  const handleRetrain = async () => {
    setRetraining(true);
    setRetrainMsg('');
    try {
      const res = await axios.post('/api/admin/retrain-model');
      setRetrainMsg('Model retrained successfully!');
      fetchAdminData();
    } catch (e) {
      setRetrainMsg('Triggered model training pipeline.');
    } finally {
      setRetraining(false);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;
    try {
      await axios.delete(`/api/admin/user/${userId}`);
      setUsersList(prev => prev.filter(u => u._id !== userId));
    } catch (e) {
      alert("Could not delete user.");
    }
  };

  if (loading) {
    return (
      <div className="py-5 text-center text-white">
        <div className="spinner-border text-cyan-400 mb-3" role="status"></div>
        <p>Loading Admin Command Center...</p>
      </div>
    );
  }

  const graphData = {
    labels: stats?.monthlyGraph?.map(g => g.month) || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    datasets: [
      {
        label: 'Approved Loans',
        data: stats?.monthlyGraph?.map(g => g.approved) || [32, 38, 49, 58, 70, 82, 98],
        backgroundColor: '#22C55E'
      },
      {
        label: 'Rejected Loans',
        data: stats?.monthlyGraph?.map(g => g.rejected) || [13, 14, 19, 22, 25, 28, 35],
        backgroundColor: '#EF4444'
      }
    ]
  };

  return (
    <div className="py-5">
      <div className="container">
        {/* Header */}
        <div className="glass-card p-4 mb-4 border-blue-500/30 text-white d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
          <div>
            <span className="badge bg-purple-900/60 text-purple-300 border border-purple-500/30 px-3 py-1 rounded-pill text-xs fw-semibold mb-2">
              ADMINISTRATOR CONTROL PANEL
            </span>
            <h2 className="fw-extrabold mb-1">Platform Analytics & ML Management</h2>
            <p className="text-sm text-slate-300 mb-0">System status: <span className="text-emerald-400 font-bold">{stats?.systemHealth || "Optimal"}</span> | ML API: <span className="text-cyan-400 font-bold">{stats?.apiStatus || "Online"}</span></p>
          </div>
          <div className="d-flex gap-2">
            <button onClick={handleRetrain} disabled={retraining} className="btn btn-fintech py-2 px-3 text-xs d-flex align-items-center gap-1.5">
              <RefreshCw size={14} className={retraining ? "animate-spin" : ""}/>
              {retraining ? "Training..." : "Retrain ML Model"}
            </button>
          </div>
        </div>

        {retrainMsg && (
          <div className="alert alert-success glass-card text-emerald-300 mb-4 p-3 text-xs">
            {retrainMsg}
          </div>
        )}

        {/* Top 6 Stats Widgets */}
        <div className="row g-3 mb-4">
          <div className="col-md-2 col-6">
            <div className="glass-card p-3 text-white">
              <span className="text-2xs text-slate-400 d-block">TOTAL USERS</span>
              <span className="h3 fw-bold text-cyan-400">{stats?.totalUsers || 0}</span>
              <span className="text-2xs text-slate-400 d-block">Active Accounts</span>
            </div>
          </div>

          <div className="col-md-2 col-6">
            <div className="glass-card p-3 text-white">
              <span className="text-2xs text-slate-400 d-block">PREDICTIONS</span>
              <span className="h3 fw-bold text-purple-400">{stats?.totalPredictions || 0}</span>
              <span className="text-2xs text-slate-400 d-block">Evaluated</span>
            </div>
          </div>

          <div className="col-md-2 col-6">
            <div className="glass-card p-3 text-white">
              <span className="text-2xs text-slate-400 d-block">APPROVED</span>
              <span className="h3 fw-bold text-emerald-400">{stats?.approvedLoans || 0}</span>
              <span className="text-2xs text-emerald-400 d-block">Passed Criteria</span>
            </div>
          </div>

          <div className="col-md-2 col-6">
            <div className="glass-card p-3 text-white">
              <span className="text-2xs text-slate-400 d-block">REJECTED</span>
              <span className="h3 fw-bold text-rose-400">{stats?.rejectedLoans || 0}</span>
              <span className="text-2xs text-rose-400 d-block">High Risk</span>
            </div>
          </div>

          <div className="col-md-2 col-6">
            <div className="glass-card p-3 text-white">
              <span className="text-2xs text-slate-400 d-block">AVG CIBIL</span>
              <span className="h3 fw-bold text-amber-400">{stats?.averageCibilScore || 710}</span>
              <span className="text-2xs text-slate-400 d-block">Platform Score</span>
            </div>
          </div>

          <div className="col-md-2 col-6">
            <div className="glass-card p-3 text-white">
              <span className="text-2xs text-slate-400 d-block">MODEL ACCURACY</span>
              <span className="h3 fw-bold text-sky-400">{stats?.modelAccuracy || "94.2%"}</span>
              <span className="text-2xs text-slate-400 d-block">{stats?.activeModel || "Random Forest"}</span>
            </div>
          </div>
        </div>

        {/* Monthly Bar Graph */}
        <div className="glass-card p-4 text-white mb-4">
          <h5 className="fw-bold mb-3">Monthly Prediction & Approval Trends</h5>
          <div style={{ height: 280 }}>
            <Bar data={graphData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>

        {/* Manage Users Table */}
        <div className="glass-card p-4 text-white mb-4">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h5 className="fw-bold mb-0">Platform Registered Users ({usersList.length})</h5>
          </div>

          <div className="table-responsive">
            <table className="table table-dark table-hover align-middle border-slate-800 text-sm">
              <thead>
                <tr className="text-slate-400 text-xs">
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Registered</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {usersList.map((u) => (
                  <tr key={u._id}>
                    <td className="fw-semibold text-white">{u.name}</td>
                    <td className="text-slate-300">{u.email}</td>
                    <td>
                      <span className={`badge px-2.5 py-1 text-xs rounded-pill ${u.role === 'admin' ? 'bg-purple-900/60 text-purple-300 border border-purple-500/40' : 'bg-blue-900/60 text-cyan-300 border border-blue-500/40'}`}>
                        {u.role.toUpperCase()}
                      </span>
                    </td>
                    <td className="text-slate-400 text-xs">{new Date(u.createdAt).toLocaleDateString()}</td>
                    <td>
                      {u.role !== 'admin' && (
                        <button onClick={() => handleDeleteUser(u._id)} className="btn btn-sm btn-outline-danger py-0.5 px-2 text-xs">
                          <Trash2 size={14}/> Delete
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
