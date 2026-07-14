import { useMemo, useState } from "react";
import { ChevronRight, Download, Gauge as GaugeIcon, Sparkles } from "lucide-react";
import UploadSlot from "../components/UploadSlot";
import EmptyState from "../components/EmptyState";
import LoadingState from "../components/LoadingState";
import Gauge from "../components/Gauge";
import FeatureRow from "../components/FeatureRow";
import FadeIn from "../components/FadeIn";
import { detectCode, detectLanguage } from "../lib/api";
import { downloadAiDetectionReport } from "../lib/downloadReport";

export default function CodeAiDetection() {
  const [code, setCode] = useState("");
  const [fileName, setFileName] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const liveLang = useMemo(() => (code.trim() ? detectLanguage(code) : null), [code]);

  async function run() {
    setLoading(true);
    setResult(null);
    const r = await detectCode({ file, code: file ? undefined : code });
    setResult(r);
    setLoading(false);
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <UploadSlot
          label="CODE"
          value={code}
          onChange={setCode}
          fileName={fileName}
          onFileName={setFileName}
          onFile={setFile}
          accept=".py,.js,.java,.c,.cpp,.cs,.go,.rb,.php"
          onSubmit={run}
        />
        <div className="flex items-center justify-between mt-3">
          <span className="text-xs font-mono">
            {liveLang ? (
              <span className="inline-flex items-center gap-1 text-emerald-300 bg-emerald-500/10 border border-emerald-500/30 rounded px-1.5 py-0.5">
                <Sparkles size={11} /> Detected: {liveLang}
              </span>
            ) : (
              <span className="text-slate-600">no input yet</span>
            )}
          </span>
          <button
            onClick={run}
            disabled={(!code.trim() && !file) || loading}
            className="verity-btn flex items-center gap-1.5 bg-amber-400 hover:bg-amber-300 disabled:bg-slate-800 disabled:text-slate-600 text-slate-950 disabled:cursor-not-allowed font-semibold text-sm px-4 py-2 rounded"
          >
            {loading ? "Analyzing…" : "Analyze"} <ChevronRight size={15} />
          </button>
        </div>
      </div>
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 sm:p-5 flex flex-col min-h-[16rem] md:min-h-[19rem]">
        {!result && !loading && <EmptyState icon={GaugeIcon} text="Results will appear here." />}
        {loading && <LoadingState text="Running XGBoost inference…" />}
        {result && (
          <FadeIn className="flex-1 flex flex-col">
            <div className="flex items-center justify-between mb-1">
              <div className="flex gap-2">
                <span className="text-[11px] font-mono text-slate-500 border border-slate-700 rounded px-1.5 py-0.5">{result.language}</span>
                <span className="text-[11px] font-mono text-amber-300/80 border border-amber-500/30 rounded px-1.5 py-0.5">model: {result.model}</span>
              </div>
              <button
                onClick={() => downloadAiDetectionReport({ kind: "Code", result })}
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
