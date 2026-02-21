import React, { useEffect } from "react";
import Plot from "react-plotly.js";

/**
 * Full-screen modal for expanded chart view.
 * Shows the chart larger with the Plotly mode bar enabled for zoom/pan.
 */
export default function ChartModal({ data, layout, onClose }) {
  // Close on Escape key
  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [onClose]);

  // Prevent body scroll when modal is open
  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "";
    };
  }, []);

  // Expanded layout — bigger fonts, more margin, mode bar visible
  const expandedLayout = {
    ...layout,
    margin: { l: 70, r: 70, t: 60, b: 50 },
    title: layout.title
      ? { ...layout.title, font: { ...layout.title.font, size: 18 } }
      : undefined,
    xaxis: {
      ...layout.xaxis,
      title: layout.xaxis?.title
        ? { ...layout.xaxis.title, font: { ...layout.xaxis.title.font, size: 13 } }
        : undefined,
      tickfont: { ...layout.xaxis?.tickfont, size: 11 },
    },
    yaxis: {
      ...layout.yaxis,
      title: layout.yaxis?.title
        ? { ...layout.yaxis.title, font: { ...layout.yaxis.title.font, size: 13 } }
        : undefined,
      tickfont: { ...layout.yaxis?.tickfont, size: 11 },
    },
    ...(layout.yaxis2
      ? {
          yaxis2: {
            ...layout.yaxis2,
            title: layout.yaxis2.title
              ? { ...layout.yaxis2.title, font: { ...layout.yaxis2.title.font, size: 13 } }
              : undefined,
            tickfont: { ...layout.yaxis2.tickfont, size: 11 },
          },
        }
      : {}),
    legend: {
      ...layout.legend,
      font: { ...layout.legend?.font, size: 12 },
    },
  };

  const expandedConfig = {
    responsive: true,
    displayModeBar: true,
    scrollZoom: true,
    modeBarButtonsToRemove: ["lasso2d", "select2d"],
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-6xl bg-brand-charcoal rounded-xl border border-brand-gray shadow-2xl"
        onClick={(e) => e.stopPropagation()}
        style={{ height: "80vh" }}
      >
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-3 right-3 z-10 w-8 h-8 flex items-center justify-center rounded-full bg-brand-dark hover:bg-brand-gray text-brand-light hover:text-brand-white transition-colors"
          aria-label="Close"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Expanded chart */}
        <div className="w-full h-full p-4">
          <Plot
            data={data}
            layout={expandedLayout}
            config={expandedConfig}
            useResizeHandler
            style={{ width: "100%", height: "100%" }}
          />
        </div>
      </div>
    </div>
  );
}
