import type { 
    Requirement,
    ApiResponse,
 } from "../types/api";

const API_URL = "http://127.0.0.1:8000";

export async function generateRequirement(
  title: string,
  description: string
): Promise<ApiResponse> {
  const response = await fetch(`${API_URL}/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title,
      description,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to generate test cases");
  }

  return response.json();
}


export async function getRequirements(): Promise<Requirement[]> {
  const response = await fetch(`${API_URL}/requirements`);

  if (!response.ok) {
    throw new Error("Failed to load requirements");
  }

  return response.json();
}


export async function exportTestCases(
  format: "json" | "csv",
  data: unknown
) {
  const response = await fetch(`${API_URL}/export/${format}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`Failed to export test cases as ${format}`);
  }

  return response.blob();
}