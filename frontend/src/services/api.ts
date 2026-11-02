import type { AnalysisRequest, AnalysisResponse, HealthResponse } from "../types";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/+$/, "");

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: { "Content-Type": "application/json", ...options?.headers },
    });
  } catch {
    throw new Error("Could not connect to FixProof AI. Check your connection and try again.");
  }

  if (!response.ok) {
    let message = `Request failed (${response.status}).`;
    try {
      const body = await response.json();
      if (typeof body.detail === "string") message = body.detail;
    } catch {
      // Keep fallback message for non-JSON error responses.
    }
    if (response.status === 429) message = "You've reached the analysis limit. Please wait a minute and try again.";
    if (response.status === 413) message = "The request is too large. Please reduce the submitted content.";
    if (response.status >= 500 && response.status !== 502) message = "The server is temporarily unavailable. Please try again shortly.";
    throw new Error(message);
  }

  try {
    return await response.json() as T;
  } catch {
    throw new Error("The server returned an unreadable response. Please try again.");
  }
}

export function checkHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}
export function analyzeCode(payload: AnalysisRequest): Promise<AnalysisResponse> {
  return request<AnalysisResponse>("/api/analyze", { method: "POST", body: JSON.stringify(payload) });
}
export async function downloadReport(payload: AnalysisRequest, result: AnalysisResponse): Promise<string> {
  const response = await request<{ report: string }>("/api/report", {
    method: "POST", body: JSON.stringify({ request: payload, result }),
  });
  return response.report;
}
