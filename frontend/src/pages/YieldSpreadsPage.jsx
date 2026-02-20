import React, { useState, useEffect } from "react";
import { getSectorCharts } from "../api/client";
import ChartCard from "../components/ChartCard";
import LoadingSpinner from "../components/LoadingSpinner";

export default function YieldSpreadsPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSectorCharts("Yield Spreads")
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner message="Loading Yield Spreads..." />;
  if (error) return <div className="text-red-600 p-4">Error: {error}</div>;
  if (!data) return null;

  return (
    <div>
      <h2 className="text-lg md:text-xl font-bold text-gray-800 mb-4">Yield Spreads</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {data.charts.map((chart) => (
          <ChartCard key={chart.data_key} chart={chart} />
        ))}
      </div>
    </div>
  );
}
