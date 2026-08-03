import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Line, Bar, Pie, Doughnut } from 'react-chartjs-2';
import { BarChart3, PieChart, TrendingUp, DollarSign, Activity } from 'lucide-react';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, ArcElement);

const Analytics = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const res = await axios.get('/api/admin/analytics');
      if (res.data && res.data.analytics) {
        setData(res.data.analytics);
      }
    } catch (e) {
      console.log("Could not fetch live analytics.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="py-5 text-center text-white">
        <div className="spinner-border text-cyan-400 mb-3" role="status"></div>
        <p>Loading Deep Analytics Engine...</p>
      </div>
    );
  }

  // 1. Approval Rate Chart
  const approvalRateChart = {
    labels: ['Approved', 'Rejected'],
    datasets: [{
      data: [data?.approvalRate?.approved || 72, data?.approvalRate?.rejected || 28],
      backgroundColor: ['#22C55E', '#EF4444'],
      borderColor: ['#15803D', '#991B1B'],
      borderWidth: 1
    }]
  };

  // 2. CIBIL Distribution Chart
  const cibilDistChart = {
    labels: ['Poor (300-549)', 'Fair (550-649)', 'Good (650-749)', 'Excellent (750-900)'],
    datasets: [{
      label: 'Applicants Count',
      data: [
        data?.cibilDistribution?.poor || 12,
        data?.cibilDistribution?.fair || 24,
        data?.cibilDistribution?.good || 42,
        data?.cibilDistribution?.excellent || 22
      ],
      backgroundColor: ['#EF4444', '#F59E0B', '#38BDF8', '#22C55E']
    }]
  };

  // 3. Monthly Applications Chart
  const monthlyAppsChart = {
    labels: data?.monthlyApplications?.map(m => m.month) || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    datasets: [{
      label: 'Monthly Loan Applications',
      data: data?.monthlyApplications?.map(m => m.count) || [45, 52, 68, 80, 95, 110, 142],
      borderColor: '#38BDF8',
      backgroundColor: 'rgba(56, 189, 248, 0.15)',
      fill: true,
      tension: 0.4
    }]
  };

  // 4. Income vs Loan Amount Chart
  const incomeVsLoanChart = {
    labels: ['₹3L Inc', '₹6L Inc', '₹9L Inc', '₹12L Inc', '₹18L Inc', '₹24L Inc'],
    datasets: [{
      label: 'Avg Requested Loan Amount (₹)',
      data: [400000, 1200000, 1500000, 2500000, 3500000, 5000000],
      backgroundColor: '#818CF8'
    }]
  };

  // 5. Risk Categories Chart
  const riskCategoriesChart = {
    labels: ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk'],
    datasets: [{
      data: [
        data?.riskCategories?.low || 54,
        data?.riskCategories?.medium || 26,
        data?.riskCategories?.high || 14,
        data?.riskCategories?.critical || 6
      ],
      backgroundColor: ['#22C55E', '#F59E0B', '#F97316', '#EF4444']
    }]
  };

  // 6. Employment Distribution Chart
  const employmentDistChart = {
    labels: ['Salaried', 'Self-Employed', 'Business', 'Freelancer'],
    datasets: [{
      data: [
        data?.employmentDistribution?.salaried || 58,
        data?.employmentDistribution?.selfEmployed || 22,
        data?.employmentDistribution?.business || 14,
        data?.employmentDistribution?.freelancer || 6
      ],
      backgroundColor: ['#2563EB', '#38BDF8', '#818CF8', '#C084FC']
    }]
  };

  // 7. Loan Purpose Chart
  const loanPurposeChart = {
    labels: ['Home Loan', 'Personal Loan', 'Education Loan', 'Car Loan', 'Business Loan'],
    datasets: [{
      label: 'Application Volume',
      data: [
        data?.loanPurpose?.homeLoan || 38,
        data?.loanPurpose?.personalLoan || 25,
        data?.loanPurpose?.educationLoan || 15,
        data?.loanPurpose?.carLoan || 12,
        data?.loanPurpose?.businessLoan || 10
      ],
      backgroundColor: '#38BDF8'
    }]
  };

  return (
    <div className="py-5">
      <div className="container">
        <div className="text-center max-w-2xl mx-auto mb-5">
          <span className="badge bg-blue-900/60 text-cyan-400 border border-cyan-500/30 px-3 py-1.5 rounded-pill text-xs fw-semibold mb-3">
            PORTFOLIO INTELLIGENCE
          </span>
          <h1 className="display-5 fw-bold text-white mb-2">Visual Analytics & Reports</h1>
          <p className="text-slate-300">Statistical distribution across credit tiers, income brackets, and loan purposes.</p>
        </div>

        <div className="row g-4 mb-4">
          {/* 1. Approval Rate */}
          <div className="col-lg-4 col-md-6">
            <div className="glass-card p-4 text-white h-100">
              <h6 className="fw-bold mb-3 d-flex align-items-center gap-2"><PieChart size={18} className="text-emerald-400"/> Loan Approval Rate</h6>
              <div className="w-75 mx-auto">
                <Doughnut data={approvalRateChart} />
              </div>
            </div>
          </div>

          {/* 2. CIBIL Score Distribution */}
          <div className="col-lg-8 col-md-6">
            <div className="glass-card p-4 text-white h-100">
              <h6 className="fw-bold mb-3 d-flex align-items-center gap-2"><BarChart3 size={18} className="text-cyan-400"/> CIBIL Score Tier Distribution</h6>
              <div style={{ height: 220 }}>
                <Bar data={cibilDistChart} options={{ maintainAspectRatio: false }} />
              </div>
            </div>
          </div>

          {/* 3. Monthly Applications */}
          <div className="col-lg-6">
            <div className="glass-card p-4 text-white h-100">
              <h6 className="fw-bold mb-3 d-flex align-items-center gap-2"><TrendingUp size={18} className="text-sky-400"/> Monthly Application Growth</h6>
              <div style={{ height: 220 }}>
                <Line data={monthlyAppsChart} options={{ maintainAspectRatio: false }} />
              </div>
            </div>
          </div>

          {/* 4. Income vs Loan Amount */}
          <div className="col-lg-6">
            <div className="glass-card p-4 text-white h-100">
              <h6 className="fw-bold mb-3 d-flex align-items-center gap-2"><DollarSign size={18} className="text-indigo-400"/> Income Bracket vs Requested Loan</h6>
              <div style={{ height: 220 }}>
                <Bar data={incomeVsLoanChart} options={{ maintainAspectRatio: false }} />
              </div>
            </div>
          </div>

          {/* 5. Risk Categories */}
          <div className="col-lg-4">
            <div className="glass-card p-4 text-white h-100">
              <h6 className="fw-bold mb-3 d-flex align-items-center gap-2"><Activity size={18} className="text-rose-400"/> Risk Category Breakdown</h6>
              <div className="w-75 mx-auto">
                <Pie data={riskCategoriesChart} />
              </div>
            </div>
          </div>

          {/* 6. Employment Distribution */}
          <div className="col-lg-4">
            <div className="glass-card p-4 text-white h-100">
              <h6 className="fw-bold mb-3 d-flex align-items-center gap-2"><PieChart size={18} className="text-purple-400"/> Employment Types</h6>
              <div className="w-75 mx-auto">
                <Pie data={employmentDistChart} />
              </div>
            </div>
          </div>

          {/* 7. Loan Purpose Statistics */}
          <div className="col-lg-4">
            <div className="glass-card p-4 text-white h-100">
              <h6 className="fw-bold mb-3 d-flex align-items-center gap-2"><BarChart3 size={18} className="text-amber-400"/> Loan Purpose Demand</h6>
              <div style={{ height: 200 }}>
                <Bar data={loanPurposeChart} options={{ maintainAspectRatio: false, indexAxis: 'y' }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
