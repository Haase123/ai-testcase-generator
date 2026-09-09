import type { TestCases } from "../types/api";

type TestCaseListProps = {
  testCases: TestCases;
};

export default function TestCaseList({
  testCases,
}: TestCaseListProps) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      {Object.entries(testCases).map(([category, cases]) => (
        <div
          key={category}
          className="rounded-2xl bg-slate-800 p-6 shadow-xl"
        >
          <h3 className="mb-4 text-lg font-semibold capitalize">
            {category.replace("_", " ")}
          </h3>

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
      ))}
    </div>
  );
}