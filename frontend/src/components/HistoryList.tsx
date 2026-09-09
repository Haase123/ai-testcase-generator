import type { Requirement } from "../types/api";

type HistoryListProps = {
  history: Requirement[];
  onSelect: (id: number) => void;
};

export default function HistoryList({
  history,
  onSelect,
}: HistoryListProps) {
  return (
    <div className="rounded-2xl bg-slate-800 p-6 shadow-xl">
      <h2 className="mb-4 text-xl font-semibold">
        Recent Requirements
      </h2>

      <div className="space-y-3">
        {history.slice(-5).reverse().map((item) => (
          <button
            key={item.id}
            onClick={() => onSelect(item.id)}
            className="w-full rounded-lg bg-slate-900 p-3 text-left transition hover:bg-slate-700"
          >
            <div className="flex items-center justify-between gap-3">
              <div className="font-medium">{item.title}</div>
              <span className="text-xs text-slate-500">#{item.id}</span>
            </div>

            <div className="mt-1 text-sm text-slate-400 line-clamp-2">
              {item.description}
            </div>

            <div className="mt-2 text-left text-xs text-blue-400">
              View details →
            </div>
          </button>
        ))}

        {history.length === 0 && (
          <div className="text-sm text-slate-500">
            No requirements yet
          </div>
        )}
      </div>
    </div>
  );
}