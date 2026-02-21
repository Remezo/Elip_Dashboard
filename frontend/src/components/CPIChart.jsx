import React, { useMemo, useState } from "react";
import Plot from "react-plotly.js";
import ChartModal from "./ChartModal";

/**
 * CPIChart renders the stacked bar chart + "All items" line with Ascentris dark theme.
 * Click to expand into full-screen modal.
 */
export default function CPIChart({ data }) {
  const { dates, categories, all_items } = data;
  const [expanded, setExpanded] = useState(false);

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
    <>
      <div
        className="bg-brand-charcoal rounded-lg border border-brand-gray border-t-2 border-t-brand-gold p-2 md:p-4 hover:shadow-lg hover:shadow-black/30 transition-shadow cursor-pointer group relative"
        onClick={() => setExpanded(true)}
      >
        {/* Expand hint icon */}
        <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity z-10">
          <div className="w-7 h-7 flex items-center justify-center rounded bg-brand-dark/80 text-brand-light">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
            </svg>
          </div>
        </div>
        <Plot
          data={traces}
          layout={layout}
          config={config}
          useResizeHandler
          style={{ width: "100%", height: "100%" }}
          className="w-full pointer-events-none"
        />
      </div>

      {expanded && (
        <ChartModal
          data={traces}
          layout={layout}
          onClose={() => setExpanded(false)}
        />
      )}
    </>
  );
}
