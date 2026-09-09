type RequirementFormProps = {
  title: string;
  description: string;
  loading: boolean;
  onTitleChange: (value: string) => void;
  onDescriptionChange: (value: string) => void;
  onGenerate: () => void;
  error: string | null;
};

export default function RequirementForm({
  title,
  description,
  loading,
  onTitleChange,
  onDescriptionChange,
  onGenerate,
  error,
}: RequirementFormProps) {
  return (
    <div className="lg:col-span-2 rounded-2xl bg-slate-800 p-6 shadow-xl">
      <h2 className="mb-4 text-xl font-semibold">
        New Requirement
      </h2>

      <div className="space-y-4">
        <input
          value={title}
          onChange={(e) => onTitleChange(e.target.value)}
          placeholder="Requirement title"
          className="w-full rounded-lg border border-slate-700 bg-slate-900 p-3 text-white outline-none focus:border-blue-500"
        />

        <textarea
          value={description}
          onChange={(e) => onDescriptionChange(e.target.value)}
          rows={6}
          placeholder="Describe the requirement..."
          className="w-full rounded-lg border border-slate-700 bg-slate-900 p-3 text-white outline-none focus:border-blue-500"
        />

        <button
          onClick={onGenerate}
          disabled={loading}
          className="rounded-lg bg-blue-600 px-6 py-3 font-medium transition hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Generating..." : "Generate Test Cases"}
        </button>

        {error && (
          <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
            <div className="font-semibold">Something went wrong</div>
            <div className="mt-1 whitespace-pre-line">{error}</div>
          </div>
        )}
      </div>
    </div>
  );
}