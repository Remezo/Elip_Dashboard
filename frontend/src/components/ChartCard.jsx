import React, { useMemo } from "react";
import Plot from "react-plotly.js";

/**
 * ChartCard renders a dual-axis Plotly chart matching the Streamlit dashboard.
 *
 * Props:
 *   chart: {
 *     name: string,
 *     data_key: string,
 *     frequency: string,
 *     processing: string | null,
 *     raw_trace: { x: string[], y: number[] },
 *     processed_trace: { x: string[], y: number[] },
 *     recession_trace: { x: string[], y: number[] },
 *   }
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
      title: { text: name, font: { size: 14 } },
      autosize: true,
      margin: { l: 50, r: 50, t: 40, b: 30 },
      legend: {
        orientation: "h",
        yanchor: "top",
        y: -0.15,
        xanchor: "center",
        x: 0.5,
        font: { size: 10 },
      },
      xaxis: {
        title: { text: "Year", font: { size: 10 } },
      },
      yaxis: {
        title: { text: data_key, font: { size: 10 } },
        side: "left",
      },
      yaxis2: {
        title: { text: frequency, font: { size: 10 } },
        side: "right",
        overlaying: "y",
      },
      hovermode: "x unified",
      paper_bgcolor: "white",
      plot_bgcolor: "white",
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
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-2 md:p-4 mb-4">
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
