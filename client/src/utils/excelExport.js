import * as XLSX from 'xlsx';

export const exportToExcel = (data, filename = "Loan_Predictions_History.xlsx") => {
  if (!data || !data.length) {
    alert("No data available to export.");
    return;
  }

  const formattedData = data.map(item => ({
    "Applicant Name": item.applicantName,
    "Age": item.age,
    "Gender": item.gender,
    "Employment": item.employmentType,
    "Annual Income (₹)": item.annualIncome,
    "Loan Amount Requested (₹)": item.loanAmount,
    "Tenure (Months)": item.loanTenure,
    "CIBIL Score": item.cibilScore,
    "DTI Ratio": item.debtToIncomeRatio,
    "Loan Status": item.loanStatus,
    "Approval Prob (%)": item.approvalProbability,
    "Risk Level": item.creditRiskLevel,
    "Estimated EMI (₹)": item.emiEstimate,
    "Date": new Date(item.createdAt).toLocaleDateString()
  }));

  const worksheet = XLSX.utils.json_to_sheet(formattedData);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Loan Predictions");
  XLSX.writeFile(workbook, filename);
};
