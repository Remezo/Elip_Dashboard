import React, { useState, useEffect } from "react";
import { getSectorCharts } from "../api/client";
import ChartCard from "../components/ChartCard";
import LoadingSpinner from "../components/LoadingSpinner";

export default function GlobalGrowthPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSectorCharts("Global Growth")
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner message="Loading Global Growth..." />;
  if (error) return <div className="text-red-400 bg-brand-charcoal rounded-lg p-4 border border-red-900">Error: {error}</div>;
  if (!data) return null;

  return (
    <div>
      <div className="border-l-4 border-brand-gold pl-3 mb-6">
        <h2 className="text-lg md:text-xl font-bold text-brand-white tracking-wide uppercase">Global Growth</h2>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {data.charts.map((chart) => (
          <ChartCard key={chart.data_key} chart={chart} />
        ))}
      </div>
    </div>
  );
}
