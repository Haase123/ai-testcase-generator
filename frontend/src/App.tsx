import { useEffect, useState } from "react";

import {
  generateRequirement,
  getRequirements,
  exportTestCases,
} from "./services/api";

import type {
  Requirement,
  RequirementDetails as RequirementDetailsType,
  ApiResponse,
  StatusResponse,
} from "./types/api";

import AnalysisResult from "./components/AnalysisResult";
import TestCaseList from "./components/TestCaseList";
import HistoryList from "./components/HistoryList";
import RequirementForm from "./components/RequirementForm";
import RequirementDetails from "./components/RequirementDetails";
import SystemStatus from "./components/SystemStatus";

export default function App() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [history, setHistory] = useState<Requirement[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [systemStatus, setSystemStatus] = useState<StatusResponse | null>(null);
  const [selectedRequirement, setSelectedRequirement] =
    useState<RequirementDetailsType | null>(null);

  async function loadHistory() {
    const data = await getRequirements();
    setHistory(data);
  }

  async function loadSystemStatus() {
    try {
      const response = await fetch("http://127.0.0.1:8000/status");

      if (!response.ok) {
        throw new Error("Status request failed");
      }

      const data = await response.json();
      setSystemStatus(data);
    } catch (error) {
      console.error("Could not load system status:", error);
      setSystemStatus(null);
    }
  }

  useEffect(() => {
    loadHistory();
    loadSystemStatus();
  }, []);

  async function loadRequirement(id: number) {
    try {
      setError(null);

      const response = await fetch(
        `http://127.0.0.1:8000/requirements/${id}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Failed to load requirement."
        );
      }

      setSelectedRequirement(data);

    } catch (error) {
      console.error("Failed to load requirement:", error);

      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Failed to load requirement.");
      }
    }
  }

  async function generate() {
    setError(null);

    if (!title.trim() || !description.trim()) {
      setError("Please provide a title and description.");
      return;
    }

    setLoading(true);

    try {
      const data = await generateRequirement(title, description);
      setResult(data);

      await loadSystemStatus();
      await loadHistory();

      setTitle("");
      setDescription("");

    } catch (error) {
      console.error("Generation failed:", error);

      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("An unexpected error occurred.");
      }

    } finally {
      setLoading(false);
    }
  }

  async function handleExport(format: "json" | "csv") {
    if (!result) {
      return;
    }

    try {
      const blob = await exportTestCases(format, result);

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = `test-cases.${format}`;

      document.body.appendChild(link);
      link.click();

      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Export failed:", error);
    }
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <div className="mx-auto max-w-6xl p-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold">AI Test Case Generator</h1>
          <p className="mt-2 text-slate-400">
            AI-powered requirement analysis, risk assessment and automated QA planning
          </p>
        </div>

        <SystemStatus status={systemStatus} />

        <div className="grid gap-8 lg:grid-cols-3">
          <RequirementForm
            title={title}
            description={description}
            loading={loading}
            error={error}
            onTitleChange={setTitle}
            onDescriptionChange={setDescription}
            onGenerate={generate}
          />

          <HistoryList history={history} onSelect={loadRequirement} />
        </div>

        {selectedRequirement && (
          <RequirementDetails
            requirement={selectedRequirement}
            onClose={() => setSelectedRequirement(null)}
          />
        )}

        {result && (
          <div className="mt-8 space-y-6">
            <AnalysisResult
              result={result}
              onExport={handleExport}
            />

            <TestCaseList
              testCases={result.test_cases}
            />
          </div>
        )}
      </div>
    </div>
  );
}