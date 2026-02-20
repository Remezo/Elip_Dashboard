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
  if (error) return <div className="text-red-600 p-4">Error: {error}</div>;
  if (!data) return null;

  return (
    <div>
      <h2 className="text-lg md:text-xl font-bold text-gray-800 mb-4">CPI Page</h2>
      <CPIChart data={data} />
    </div>
  );
}
