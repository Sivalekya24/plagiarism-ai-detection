import { FileType } from "lucide-react";

function fileBadgeColor(ext) {
  if (ext === "pdf") return "bg-rose-500/15 text-rose-300 border-rose-500/30";
  if (ext === "docx" || ext === "doc") return "bg-blue-500/15 text-blue-300 border-blue-500/30";
  if (ext === "txt") return "bg-slate-500/15 text-slate-300 border-slate-500/30";
  return "bg-emerald-500/15 text-emerald-300 border-emerald-500/30";
}

export default function FileBadge({ name }) {
  if (!name) return null;
  const ext = name.split(".").pop().toLowerCase();
  return (
    <span className={`inline-flex items-center gap-1 text-[11px] font-mono border rounded px-1.5 py-0.5 ${fileBadgeColor(ext)}`}>
      <FileType size={11} /> {ext.toUpperCase()}
    </span>
  );
}
