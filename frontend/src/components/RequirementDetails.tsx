import type { RequirementDetails as RequirementDetailsType } from "../types/api";

type RequirementDetailsProps = {
  requirement: RequirementDetailsType;
  onClose: () => void;
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

export default function RequirementDetails({
  requirement,
  onClose,
}: RequirementDetailsProps) {
  return (
    <div className="mt-8 rounded-2xl bg-slate-800 p-6 shadow-xl">

      {/* Header */}
      <div className="mb-6 flex items-center justify-between gap-4">
        <div>
          <div className="text-sm text-slate-400">
            Requirement #{requirement.id}
          </div>

          <h2 className="mt-1 text-2xl font-semibold">
            {requirement.title}
          </h2>
        </div>

        <button
          onClick={onClose}
          className="rounded-lg bg-slate-700 px-4 py-2 text-sm hover:bg-slate-600"
        >
          Close
        </button>
      </div>

      {/* Description */}
      <div className="mb-6 rounded-xl bg-slate-900 p-4">
        <div className="mb-2 text-sm font-medium text-slate-400">
          Description
        </div>

        <p className="text-slate-200">
          {requirement.description}
        </p>
      </div>

      {/* Generator + Priority */}
      <div className="mb-6 flex flex-wrap items-center gap-3">

        {requirement.generator_mode === "openai" ? (
          <span className="rounded-full bg-purple-600 px-3 py-1 text-sm font-medium">
            🧠 AI Enhanced
          </span>
        ) : (
          <span className="rounded-full bg-slate-600 px-3 py-1 text-sm font-medium">
            ⚙️ Local Engine
          </span>
        )}

        <span
          className={`rounded-full px-3 py-1 text-sm font-medium ${badgeColor(
            requirement.analysis.priority
          )}`}
        >
          {requirement.analysis.priority}
        </span>
      </div>

      {/* Analysis */}
      <div className="mb-8">
        <h3 className="mb-4 text-xl font-semibold">
          Analysis
        </h3>

        <div className="grid gap-4 md:grid-cols-3">

          {/* Risk Level */}
          <div className="rounded-xl bg-slate-900 p-4">
            <div className="text-sm text-slate-400">
              Risk Level
            </div>

            <div className="mt-2 text-xl font-semibold">
              {requirement.analysis.risk_level}
            </div>
          </div>

          {/* Quality Score */}
          <div className="rounded-xl bg-slate-900 p-4">
            <div className="text-sm text-slate-400">
              Quality Score
            </div>

            <div className="mt-2 text-xl font-semibold">
              {requirement.analysis.quality_score}/100
            </div>
          </div>

          {/* Automation */}
          <div className="rounded-xl bg-slate-900 p-4">
            <div className="text-sm text-slate-400">
              Automation Recommendations
            </div>

            <div className="mt-2 text-xl font-semibold">
              {requirement.analysis.recommended_automation?.length ?? 0}
            </div>
          </div>

        </div>
      </div>

      {/* Test Cases */}
      <div>
        <h3 className="mb-4 text-xl font-semibold">
          Generated Test Cases
        </h3>

        <div className="grid gap-6 md:grid-cols-2">

          {Object.entries(requirement.test_cases).map(
            ([category, cases]) => (
              <div
                key={category}
                className="rounded-xl bg-slate-900 p-5"
              >
                <h4 className="mb-3 font-semibold capitalize">
                  {category.replace("_", " ")}
                </h4>

                <ul className="space-y-2 text-sm text-slate-300">
                  {cases.map((testCase) => (
                    <li
                      key={testCase}
                      className="flex gap-2"
                    >
                      <span className="mt-1 text-blue-400">
                        •
                      </span>

                      <span>{testCase}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )
          )}

        </div>
      </div>

    </div>
  );
}