import React, { useMemo } from "react";
import Plot from "react-plotly.js";

/**
 * ChartCard renders a dual-axis Plotly chart with Ascentris dark theme.
 */
export default function ChartCard({ chart }) {
  const { name, data_key, frequency, processing, raw_trace, processed_trace, recession_trace } = chart;

  const data = useMemo(() => {
    const traces = [];

    // Recession bars (secondary y-axis) - drawn first so they appear behind
    if (recession_trace && recession_trace.x.length > 0) {
      traces.push({
        type: "bar",
        x: recession_trace.x,
        y: recession_trace.y,
        name: "US Recession",
        marker: { color: "rgba(220, 50, 50, 0.45)" },
        yaxis: "y2",
        hoverinfo: "skip",
      });
    }

    // Raw FRED data (primary y-axis) — gold
    traces.push({
      type: "scatter",
      mode: "lines",
      x: raw_trace.x,
      y: raw_trace.y,
      name: data_key,
      yaxis: "y",
      line: { color: "#c8a84e", width: 1.8 },
    });

    // Processed data (secondary y-axis) — blue
    if (processed_trace && processed_trace.x.length > 0) {
      traces.push({
        type: "scatter",
        mode: "lines",
        x: processed_trace.x,
        y: processed_trace.y,
        name: processing || "Processed",
        yaxis: "y2",
        line: { color: "#60a5fa", width: 1.8 },
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
    <div className="bg-brand-charcoal rounded-lg border border-brand-gray border-t-2 border-t-brand-gold p-2 md:p-4 mb-4 hover:shadow-lg hover:shadow-black/30 transition-shadow">
      <Plot
        data={data}
        layout={layout}
        config={config}
        useResizeHandler
        style={{ width: "100%", height: "100%" }}
        className="w-full"
      />
    </div>
  );
}
