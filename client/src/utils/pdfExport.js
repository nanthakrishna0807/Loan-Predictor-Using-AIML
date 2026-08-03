import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export const generatePDFReport = async (elementId, filename = "Loan_Prediction_Report.pdf") => {
  const element = document.getElementById(elementId);
  if (!element) {
    alert("Report element not found");
    return;
  }

  try {
    const canvas = await html2canvas(element, {
      scale: 2,
      backgroundColor: '#0F172A',
      useCORS: true
    });

    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
    pdf.save(filename);
  } catch (error) {
    console.error("PDF generation failed:", error);
    alert("Could not generate PDF. Please try again.");
  }
};
