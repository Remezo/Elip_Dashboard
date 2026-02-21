import React, { useMemo, useState } from "react";
import Plot from "react-plotly.js";
import ChartModal from "./ChartModal";

/**
 * ChartCard renders a dual-axis Plotly chart with Ascentris dark theme.
 * Click to expand into full-screen modal.
 */
export default function ChartCard({ chart }) {
  const { name, data_key, frequency, processing, raw_trace, processed_trace, recession_trace } = chart;
  const [expanded, setExpanded] = useState(false);

  const data = useMemo(() => {
    const traces = [];

    // Recession bars (secondary y-axis) - drawn first so they appear behind
    if (recession_trace && recession_trace.x.length > 0) {
      traces.push({
        type: "bar",
        x: recession_trace.x,
        y: recession_trace.y,
        name: "US Recession",
        marker: { color: "rgba(250, 0, 0, 0.7)" },
        yaxis: "y2",
        hoverinfo: "skip",
      });
    }

    // Raw FRED data (primary y-axis)
    traces.push({
      type: "scatter",
      mode: "lines",
      x: raw_trace.x,
      y: raw_trace.y,
      name: data_key,
      yaxis: "y",
      line: { width: 1.5 },
    });

    // Processed data (secondary y-axis)
    if (processed_trace && processed_trace.x.length > 0) {
      traces.push({
        type: "scatter",
        mode: "lines",
        x: processed_trace.x,
        y: processed_trace.y,
        name: processing || "Processed",
        yaxis: "y2",
        line: { width: 1.5 },
      });
    }

    return traces;
  }, [chart]);

  const layout = useMemo(
    () => ({
      title: { text: name, font: { size: 13, color: "#c8a84e" } },
      autosize: true,
      margin: { l: 50, r: 50, t: 40, b: 30 },
      legend: {
        orientation: "h",
        yanchor: "top",
        y: -0.15,
        xanchor: "center",
        x: 0.5,
        font: { size: 10, color: "#a0a0a0" },
      },
      xaxis: {
        title: { text: "Year", font: { size: 10, color: "#a0a0a0" } },
        tickfont: { color: "#6b6b6b", size: 9 },
        gridcolor: "#3a3a3a",
        zerolinecolor: "#4a4a4a",
      },
      yaxis: {
        title: { text: data_key, font: { size: 10, color: "#a0a0a0" } },
        side: "left",
        tickfont: { color: "#6b6b6b", size: 9 },
        gridcolor: "#3a3a3a",
        zerolinecolor: "#4a4a4a",
      },
      yaxis2: {
        title: { text: frequency, font: { size: 10, color: "#a0a0a0" } },
        side: "right",
        overlaying: "y",
        tickfont: { color: "#6b6b6b", size: 9 },
        gridcolor: "#3a3a3a",
        zerolinecolor: "#4a4a4a",
      },
      hovermode: "x unified",
      paper_bgcolor: "#2d2d2d",
      plot_bgcolor: "#2d2d2d",
    }),
    [name, data_key, frequency]
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
        className="bg-brand-charcoal rounded-lg border border-brand-gray border-t-2 border-t-brand-gold p-2 md:p-4 mb-4 hover:shadow-lg hover:shadow-black/30 transition-shadow cursor-pointer group relative"
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
          data={data}
          layout={layout}
          config={config}
          useResizeHandler
          style={{ width: "100%", height: "100%" }}
          className="w-full pointer-events-none"
        />
      </div>

      {expanded && (
        <ChartModal
          data={data}
          layout={layout}
          onClose={() => setExpanded(false)}
        />
      )}
    </>
  );
}
