import React, { useState, useEffect } from "react";
import { getCPIData } from "../api/client";
import CPIChart from "../components/CPIChart";
import LoadingSpinner from "../components/LoadingSpinner";

export default function CPIPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCPIData()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner message="Loading CPI data..." />;
  if (error) return <div className="text-red-400 bg-brand-charcoal rounded-lg p-4 border border-red-900">Error: {error}</div>;
  if (!data) return null;

  return (
    <div>
      <div className="border-l-4 border-brand-gold pl-3 mb-6">
        <h2 className="text-lg md:text-xl font-bold text-brand-white tracking-wide uppercase">CPI</h2>
      </div>
      <CPIChart data={data} />
    </div>
  );
}
