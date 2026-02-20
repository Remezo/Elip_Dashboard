import React, { useMemo } from "react";
import Plot from "react-plotly.js";

/**
 * CPIChart renders the stacked bar chart + "All items" line.
 *
 * Props:
 *   data: {
 *     dates: string[],
 *     categories: { [name: string]: number[] },
 *     all_items: number[],
 *   }
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
      line: { color: "red", width: 2 },
      marker: { size: 4 },
    };

    return [...barTraces, lineTrace];
  }, [dates, categories, all_items]);

  const layout = useMemo(
    () => ({
      barmode: "stack",
      title: { text: "CPI Components", font: { size: 14 } },
      xaxis: { title: { text: "Years", font: { size: 10 } } },
      yaxis: { title: { text: "Weighted CPI", font: { size: 10 } } },
      autosize: true,
      margin: { l: 50, r: 20, t: 40, b: 30 },
      legend: {
        orientation: "h",
        yanchor: "top",
        y: -0.2,
        xanchor: "center",
        x: 0.5,
        font: { size: 10 },
      },
      hovermode: "x unified",
      paper_bgcolor: "white",
      plot_bgcolor: "white",
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
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-2 md:p-4">
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
