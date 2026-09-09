import type { ApiResponse } from "../types/api";

type AnalysisResultProps = {
  result: ApiResponse;
  onExport: (format: "json" | "csv") => void;
};

function badgeColor(priority: string) {
  switch (priority) {
    case "CRITICAL":
      return "bg-red-600";

    case "HIGH":
      return "bg-orange-500";

    case "MEDIUM":
      return "bg-yellow-500 text-black";

    default:
      return "bg-green-600";
  }
}

export default function AnalysisResult({
  result,
  onExport,
}: AnalysisResultProps) {
  return (
    <div className="rounded-2xl bg-slate-800 p-6 shadow-xl">
      <div className="mb-4 flex items-center justify-between flex-wrap gap-3">

        {/* Title + Generator Mode */}
        <div className="flex items-center gap-3">
          <h2 className="text-2xl font-semibold">
            Analysis Result
          </h2>

          {result.generator_mode === "openai" ? (
            <span className="rounded-full bg-purple-600 px-3 py-1 text-sm font-medium">
              🧠 AI Enhanced
            </span>
          ) : (
            <span className="rounded-full bg-slate-600 px-3 py-1 text-sm font-medium">
              ⚙️ Local Engine
            </span>
          )}
        </div>

        {/* Export Buttons */}
        <div className="flex gap-3">
          <button
            onClick={() => onExport("json")}
            className="rounded-lg bg-slate-700 px-4 py-2 text-white hover:bg-slate-600"
          >
            Export JSON
          </button>

          <button
            onClick={() => onExport("csv")}
            className="rounded-lg bg-slate-700 px-4 py-2 text-white hover:bg-slate-600"
          >
            Export CSV
          </button>
        </div>

        {/* Priority */}
        <span
          className={`rounded-full px-3 py-1 text-sm font-medium ${badgeColor(
            result.analysis.priority
          )}`}
        >
          {result.analysis.priority}
        </span>
      </div>

      {/* Analysis Cards */}
      <div className="grid gap-4 md:grid-cols-3">

        {/* Risk Level */}
        <div className="rounded-xl bg-slate-900 p-4">
          <div className="text-sm text-slate-400">
            Risk Level
          </div>

          <div className="mt-2 text-xl font-semibold">
            {result.analysis.risk_level}
          </div>
        </div>

        {/* Quality Score */}
        <div className="rounded-xl bg-slate-900 p-4">
          <div className="text-sm text-slate-400">
            Quality Score
          </div>

          <div className="mt-2 text-xl font-semibold">
            {result.analysis.quality_score}/100
          </div>
        </div>

        {/* Automation Recommendations */}
        <div className="rounded-xl bg-slate-900 p-4">
          <div className="text-sm text-slate-400">
            Automation Recommendations
          </div>

          <div className="mt-2 text-xl font-semibold">
            {result.analysis.recommended_automation.length}
          </div>
        </div>

      </div>
    </div>
  );
}