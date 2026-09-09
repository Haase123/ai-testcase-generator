import type { StatusResponse } from "../types/api";

type SystemStatusProps = {
  status: StatusResponse | null;
};

function StatusItem({
  name,
  status,
}: {
  name: string;
  status: string;
}) {
  let label = status;
  let color = "bg-yellow-500";

  if (status === "ok") {
    label = "Operational";
    color = "bg-green-500";
  } else if (status === "openai") {
    label = "OpenAI";
    color = "bg-purple-500";
  } else if (status === "fallback") {
    label = "Fallback Mode";
    color = "bg-yellow-500";
  } else if (status === "error") {
    label = "Error";
    color = "bg-red-500";
  } else if (status === "unknown") {
    label = "Not tested";
    color = "bg-slate-500";
  }

  return (
    <div className="rounded-xl bg-slate-900 p-4">
      <div className="text-sm text-slate-400">{name}</div>

      <div className="mt-2 flex items-center gap-2">
        <span className={`h-3 w-3 rounded-full ${color}`} />

        <span className="font-medium">
          {label}
        </span>
      </div>
    </div>
  );
}

export default function SystemStatus({
  status,
}: SystemStatusProps) {
    return (
        <div className="mb-8 rounded-2xl bg-slate-800 p-6 shadow-xl">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold">System Status</h2>
              <p className="text-sm text-slate-400">
                Current status of application services
              </p>
            </div>

            {status && (
              <span className="rounded-full bg-green-600 px-3 py-1 text-sm font-medium">
                ● System Healthy
              </span>
            )}
          </div>

          {status ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <StatusItem
                name="API"
                status={status.services.api}
              />

              <StatusItem
                name="Database"
                status={status.services.database}
              />

              <StatusItem
                name="AI Generator"
                status={status.services.ai_generator}
              />

              <StatusItem
                name="Export"
                status={status.services.export}
              />
            </div>
          ) : (
            <div className="text-sm text-red-400">
              Unable to retrieve system status
            </div>
          )}
        </div>
    );
}