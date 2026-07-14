import { useState } from "react";
import { AlertCircle, CheckCircle2 } from "lucide-react";
import AnimatedBar from "./AnimatedBar";

export default function SimilarityReport({ overall, matches, highlightSnippets }) {
  const [copied, setCopied] = useState(false);

  function copyReport() {
    const lines = [
      `Verity similarity report — ${overall}% overlap`,
      ...matches.map((m) => `- ${m.source}: ${m.similarity}%${m.snippet ? ` — "${m.snippet}"` : ""}`),
    ];
    navigator.clipboard?.writeText(lines.join("\n")).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    });
  }

  return (
    <div className="flex-1 flex flex-col">
      <div className="flex items-center gap-3 mb-4">
        {overall > 30 ? <AlertCircle className="text-amber-400" size={22} /> : <CheckCircle2 className="text-cyan-400" size={22} />}
        <div>
          <div className="text-2xl font-serif italic">{overall}% overlap found</div>
          <div className="text-xs text-slate-500">Against indexed sources</div>
        </div>
      </div>
      <div className="flex-1 space-y-3">
        {matches.length === 0 && <div className="text-slate-500 text-sm">No significant matches found.</div>}
        {matches.map((m) => (
          <div key={m.source} className="border-b border-slate-800/70 pb-3 last:border-0">
            <div className="flex items-center justify-between text-sm mb-1">
              <span className="text-slate-300 font-mono truncate pr-3">{m.source}</span>
              <span className="text-slate-400 font-mono">{m.similarity}%</span>
            </div>
            <AnimatedBar pct={m.similarity} className="h-full bg-amber-400/80" />
            {highlightSnippets && m.snippet && (
              <p className="text-xs text-slate-400 italic bg-amber-400/10 border-l-2 border-amber-400/50 pl-2 py-1">
                “{m.snippet}”
              </p>
            )}
          </div>
        ))}
      </div>
      <button
        onClick={copyReport}
        className="verity-btn mt-4 self-start text-xs font-medium text-slate-300 hover:text-amber-300 border border-slate-700 hover:border-amber-400/50 rounded px-3 py-1.5"
      >
        {copied ? "Copied ✓" : "Copy report"}
      </button>
    </div>
  );
}
