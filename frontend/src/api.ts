const API_BASE_URL = "http://127.0.0.1:8000";

async function apiFetch(endpoint: string) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);

  if (!response.ok) {
    throw new Error(`API request failed: ${endpoint}`);
  }

  return response.json();
}

export async function fetchRisk() {
  return apiFetch("/api/risk");
}

export async function fetchSuppliers() {
  return apiFetch("/api/suppliers");
}

export async function fetchWebShield() {
  return apiFetch("/api/webshield");
}

export async function fetchMarket() {
  return apiFetch("/api/market");
}

export async function fetchScraperHealth() {
  return apiFetch("/api/scraper-health");
}

export async function fetchSystemStatus() {
  return apiFetch("/api/system-status");
}

export async function fetchScraperSources() {
  return apiFetch("/api/scraper-sources");
}