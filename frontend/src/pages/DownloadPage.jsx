import React from "react";
import { getDownloadURL } from "../api/client";

export default function DownloadPage() {
  const handleDownload = () => {
    window.location.href = getDownloadURL();
  };

  return (
    <div>
      <div className="border-l-4 border-brand-gold pl-3 mb-6">
        <h2 className="text-lg md:text-xl font-bold text-brand-white tracking-wide uppercase">Download Data</h2>
      </div>
      <div className="bg-brand-charcoal rounded-lg border border-brand-gray p-6 md:p-8 text-center">
        <div className="text-4xl mb-4">📥</div>
        <p className="text-brand-light mb-6">
          Download all processed data as an Excel file with sheets for CPI Weighted, Daily, Monthly, and Quarterly data.
        </p>
        <button
          onClick={handleDownload}
          className="inline-flex items-center px-6 py-3 bg-brand-gold text-brand-black font-semibold rounded-lg hover:bg-brand-gold-light active:bg-brand-gold-dark transition-colors shadow-sm tracking-wider uppercase"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Download Excel
        </button>
      </div>
    </div>
  );
}
