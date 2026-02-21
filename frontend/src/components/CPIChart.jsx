import React, { useMemo } from "react";
import Plot from "react-plotly.js";

/**
 * CPIChart renders the stacked bar chart + "All items" line with Ascentris dark theme.
 */
export default function CPIChart({ data }) {
  const { dates, categories, all_items } = data;

  const traces = useMemo(() => {
    const barTraces = Object.entries(categories).map(([name, values]) => ({
      type: "bar",
      x: dates,
      y: values,
      name,
    }));

    const lineTrace = {
      type: "scatter",
      mode: "lines+markers",
      x: dates,
      y: all_items,
      name: "All items",
      line: { color: "red" },
      marker: { size: 4 },
    };

    return [...barTraces, lineTrace];
  }, [dates, categories, all_items]);

  const layout = useMemo(
    () => ({
      barmode: "stack",
      title: { text: "CPI Components", font: { size: 14, color: "#c8a84e" } },
      xaxis: {
        title: { text: "Years", font: { size: 10, color: "#a0a0a0" } },
        tickfont: { color: "#6b6b6b", size: 9 },
        gridcolor: "#3a3a3a",
        zerolinecolor: "#4a4a4a",
      },
      yaxis: {
        title: { text: "Weighted CPI", font: { size: 10, color: "#a0a0a0" } },
        tickfont: { color: "#6b6b6b", size: 9 },
        gridcolor: "#3a3a3a",
        zerolinecolor: "#4a4a4a",
      },
      autosize: true,
      margin: { l: 50, r: 20, t: 40, b: 30 },
      legend: {
        orientation: "h",
        yanchor: "top",
        y: -0.2,
        xanchor: "center",
        x: 0.5,
        font: { size: 10, color: "#a0a0a0" },
      },
      hovermode: "x unified",
      paper_bgcolor: "#2d2d2d",
      plot_bgcolor: "#2d2d2d",
    }),
    []
  );

  const config = useMemo(
    () => ({
      responsive: true,
      displayModeBar: false,
      scrollZoom: false,
    }),
    []
  );

  return (
    <div className="bg-brand-charcoal rounded-lg border border-brand-gray border-t-2 border-t-brand-gold p-2 md:p-4 hover:shadow-lg hover:shadow-black/30 transition-shadow">
      <Plot
        data={traces}
        layout={layout}
        config={config}
        useResizeHandler
        style={{ width: "100%", height: "100%" }}
        className="w-full"
      />
    </div>
  );
}
