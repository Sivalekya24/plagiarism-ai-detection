export default function FeatureRow({ f }) {
  return (
    <div className="flex items-center justify-between py-2.5 border-b border-slate-800/70 last:border-0">
      <div>
        <div className="text-sm text-slate-200 font-medium">{f.name}</div>
        <div className="text-xs text-slate-500">{f.note}</div>
      </div>
      <div className="font-mono text-sm text-slate-100 bg-slate-800/70 rounded px-2 py-1 min-w-[3.5rem] text-center">
        {f.value}
      </div>
    </div>
  );
}
