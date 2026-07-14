import { useState } from "react";
import { ChevronRight, Download, Gauge as GaugeIcon } from "lucide-react";
import UploadSlot from "../components/UploadSlot";
import EmptyState from "../components/EmptyState";
import LoadingState from "../components/LoadingState";
import Gauge from "../components/Gauge";
import FeatureRow from "../components/FeatureRow";
import FadeIn from "../components/FadeIn";
import { detectText, words } from "../lib/api";
import { downloadAiDetectionReport } from "../lib/downloadReport";

export default function TextAiDetection() {
  const [text, setText] = useState("");
  const [fileName, setFileName] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function run() {
    setLoading(true);
    setResult(null);
    const r = await detectText({ file, text: file ? undefined : text });
    setResult(r);
    setLoading(false);
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <UploadSlot
          label="TEXT"
          value={text}
          onChange={setText}
          fileName={fileName}
          onFileName={setFileName}
          onFile={setFile}
          accept=".txt,.pdf,.docx"
          onSubmit={run}
        />
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mt-3">
          <span className="text-xs text-slate-600 font-mono">{text.trim() ? `${words(text).length} words` : "no input yet"}</span>
          <button
            onClick={run}
            disabled={(!text.trim() && !file) || loading}
            className="verity-btn flex items-center gap-1.5 bg-amber-400 hover:bg-amber-300 disabled:bg-slate-800 disabled:text-slate-600 text-slate-950 disabled:cursor-not-allowed font-semibold text-sm px-4 py-2 rounded"
          >
            {loading ? "Analyzing…" : "Analyze"} <ChevronRight size={15} />
          </button>
        </div>
      </div>
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 sm:p-5 flex flex-col min-h-[16rem] md:min-h-[19rem]">
        {!result && !loading && <EmptyState icon={GaugeIcon} text="Results will appear here." />}
        {loading && <LoadingState text="Reading signal…" />}
        {result && (
          <FadeIn className="flex-1 flex flex-col">
            <div className="flex justify-end mb-1">
              <button
                onClick={() => downloadAiDetectionReport({ kind: "Text", result })}
                className="verity-btn flex items-center gap-1.5 text-xs text-slate-400 hover:text-amber-300 border border-slate-700 hover:border-amber-400/50 rounded px-2.5 py-1.5"
              >
                <Download size={13} /> Download report
              </button>
            </div>
            <Gauge score={result.score} />
            <div className="mt-2 border-t border-slate-800 pt-2">
              {result.features.map((f) => (
                <FeatureRow key={f.name} f={f} />
              ))}
            </div>
          </FadeIn>
        )}
      </div>
    </div>
  );
}
