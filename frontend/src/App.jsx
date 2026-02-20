import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import CPIPage from "./pages/CPIPage";
import SignsOfExcessPage from "./pages/SignsOfExcessPage";
import OperatingFundamentalsPage from "./pages/OperatingFundamentalsPage";
import YieldSpreadsPage from "./pages/YieldSpreadsPage";
import GlobalGrowthPage from "./pages/GlobalGrowthPage";
import DownloadPage from "./pages/DownloadPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/cpi" replace />} />
        <Route path="/cpi" element={<CPIPage />} />
        <Route path="/signs-of-excess" element={<SignsOfExcessPage />} />
        <Route path="/operating-fundamentals" element={<OperatingFundamentalsPage />} />
        <Route path="/yield-spreads" element={<YieldSpreadsPage />} />
        <Route path="/global-growth" element={<GlobalGrowthPage />} />
        <Route path="/download" element={<DownloadPage />} />
      </Routes>
    </Layout>
  );
}
