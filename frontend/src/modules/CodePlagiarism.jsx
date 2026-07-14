import { useState } from "react";
import { ChevronRight, Code2, Download } from "lucide-react";
import UploadSlot from "../components/UploadSlot";
import EmptyState from "../components/EmptyState";
import LoadingState from "../components/LoadingState";
import SimilarityReport from "../components/SimilarityReport";
import FadeIn from "../components/FadeIn";
import { compareCode, checkSingleCode } from "../lib/api";
import { downloadPlagiarismReport } from "../lib/downloadReport";

export default function CodePlagiarism() {
  const [mode, setMode] = useState("two"); // two | single
  const [codeA, setCodeA] = useState("");
  const [nameA, setNameA] = useState("");
  const [fileA, setFileA] = useState(null);
  const [codeB, setCodeB] = useState("");
  const [nameB, setNameB] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const ready = mode === "two" ? codeA.trim() && codeB.trim() : codeA.trim();

  async function run() {
    setLoading(true);
    setResult(null);
    const r =
      mode === "two"
        ? await compareCode(codeA, codeB)
        : await checkSingleCode({ file: fileA, code: fileA ? undefined : codeA });
    setResult(r);
    setLoading(false);
  }

  function switchMode(id) {
    setMode(id);
    setResult(null);
    setCodeB("");
    setNameB("");
  }

  return (
    <div>
      <div className="flex flex-wrap gap-2 mb-5">
        {[
          ["two", "Two-File Compare"],
          ["single", "Single-File Check"],
        ].map(([id, label]) => (
          <button
            key={id}
            onClick={() => switchMode(id)}
            className={`text-xs font-medium px-5 py-2 rounded-full border whitespace-nowrap ${
              mode === id ? "bg-amber-400 text-slate-950 border-amber-400" : "text-slate-400 border-slate-700 hover:border-slate-500"
            }`}
          >
            {label}
          </button>
        ))}
      </div>
      {mode === "single" && (
        <p className="text-xs text-slate-500 mb-3">
          Uploaded or pasted code is automatically checked against the stored code archive — no extra step needed.
        </p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-3">
          <UploadSlot
            label={mode === "two" ? "SNIPPET A" : "CODE FILE"}
            value={codeA}
            onChange={setCodeA}
            fileName={nameA}
            onFileName={setNameA}
            onFile={setFileA}
            accept=".py,.js,.java,.c,.cpp,.go,.rb,.php"
            small
            onSubmit={run}
          />
          {mode === "two" && (
            <UploadSlot
              label="SNIPPET B"
              value={codeB}
              onChange={setCodeB}
              fileName={nameB}
              onFileName={setNameB}
              accept=".py,.js,.java,.c,.cpp,.go,.rb,.php"
              small
              onSubmit={run}
            />
          )}
          <div className="flex justify-end">
            <button
              onClick={run}
              disabled={!ready || loading}
              className="verity-btn flex items-center gap-1.5 bg-amber-400 hover:bg-amber-300 disabled:bg-slate-800 disabled:text-slate-600 text-slate-950 disabled:cursor-not-allowed font-semibold text-sm px-4 py-2 rounded w-full sm:w-auto justify-center"
            >
              {loading ? "Checking…" : mode === "two" ? "Compare code" : "Check code"} <ChevronRight size={15} />
            </button>
          </div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 sm:p-5 flex flex-col min-h-[16rem] md:min-h-[19rem]">
          {!result && !loading && (
            <EmptyState
              icon={Code2}
              text={mode === "two" ? "Paste or upload two snippets to check for overlap." : "Paste or upload a file — it's checked against the archive automatically."}
            />
          )}
          {loading && <LoadingState text="Checking against archive…" />}
          {result && (
            <FadeIn>
              <div className="flex justify-end mb-2">
                <button
                  onClick={() => downloadPlagiarismReport({ kind: "Code", mode, overall: result.overall, matches: result.matches })}
                  className="verity-btn flex items-center gap-1.5 text-xs text-slate-400 hover:text-amber-300 border border-slate-700 hover:border-amber-400/50 rounded px-2.5 py-1.5"
                >
                  <Download size={13} /> Download report
                </button>
              </div>
              <SimilarityReport overall={result.overall} matches={result.matches} highlightSnippets />
            </FadeIn>
          )}
        </div>
      </div>
    </div>
  );
}
