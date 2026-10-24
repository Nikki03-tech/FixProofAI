import type {
  AnalysisRequest,
  AnalysisResponse,
  HealthResponse,
} from "../types";

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
).replace(/\/+$/, "");

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
  } catch {
    throw new Error(
      "Could not connect to FixProof AI. Check the backend URL and try again."
    );
  }

  if (!response.ok) {
    let message = `Request failed (${response.status}).`;

    try {
      const body = await response.json();
      if (typeof body.detail === "string") {
        message = body.detail;
      }
    } catch {
      // Keep the default error message if the response is not JSON.
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export function checkHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export function analyzeCode(
  payload: AnalysisRequest
): Promise<AnalysisResponse> {
  return request<AnalysisResponse>("/api/analyze", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function downloadReport(
  payload: AnalysisRequest,
  result: AnalysisResponse
): Promise<string> {
  const response = await request<{ report: string }>("/api/report", {
    method: "POST",
    body: JSON.stringify({ request: payload, result }),
  });

  return response.report;
}
