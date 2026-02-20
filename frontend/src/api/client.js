const API_BASE = "/api";

async function fetchJSON(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${res.statusText}`);
  }
  return res.json();
}

export async function getCPIData() {
  return fetchJSON("/cpi");
}

export async function getSectorCharts(sector) {
  return fetchJSON(`/charts/${encodeURIComponent(sector)}`);
}

export async function getHealth() {
  return fetchJSON("/health");
}

export function getDownloadURL() {
  return `${API_BASE}/download/excel`;
}
