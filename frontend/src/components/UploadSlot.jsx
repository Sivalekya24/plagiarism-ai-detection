import { useRef, useState } from "react";
import { Upload, X } from "lucide-react";
import FileBadge from "./FileBadge";

export default function UploadSlot({ label, value, onChange, fileName, onFileName, accept, small, onSubmit, onFile }) {
  const fileRef = useRef(null);
  const [dragOver, setDragOver] = useState(false);
  const [justDropped, setJustDropped] = useState(false);

  function readFile(file) {
    if (!file) return;
    onFile?.(file); // expose the raw File so callers can send real multipart uploads
    if (/\.(pdf|docx?)$/i.test(file.name)) {
      // Real backend accepts these as multipart/form-data uploads and
      // extracts text server-side. Here we just record the name for preview.
      onFileName(file.name);
      onChange(`[${file.name} — binary content, parsed server-side]`);
    } else {
      const reader = new FileReader();
      reader.onload = (e) => {
        onChange(String(e.target.result || ""));
        onFileName(file.name);
      };
      reader.readAsText(file);
    }
    setJustDropped(true);
    setTimeout(() => setJustDropped(false), 400);
  }

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragOver(false);
        readFile(e.dataTransfer.files?.[0]);
      }}
      className={`verity-slot bg-slate-900 border rounded-lg overflow-hidden transition-colors ${
        dragOver ? "border-amber-400/70 bg-amber-400/5" : "border-slate-800"
      } ${justDropped ? "ring-2 ring-amber-400/40" : ""}`}
      style={{ transition: "border-color 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease" }}
    >
      <div className="flex items-center justify-between px-3 py-2 border-b border-slate-800 bg-slate-900/60">
        <div className="flex items-center gap-2 text-slate-400 text-xs font-mono tracking-wide">
          {label}
          {fileName && <FileBadge name={fileName} />}
        </div>
        <div className="flex items-center gap-2">
          {fileName && (
            <button
              onClick={() => {
                onFileName("");
                onChange("");
                onFile?.(null);
              }}
              className="text-slate-500 hover:text-slate-300 transition-colors"
            >
              <X size={13} />
            </button>
          )}
          <button
            onClick={() => fileRef.current?.click()}
            className="verity-btn flex items-center gap-1 text-[11px] font-medium text-slate-300 hover:text-amber-300 border border-slate-700 hover:border-amber-400/50 rounded px-2 py-1"
          >
            <Upload size={11} /> Upload
          </button>
          <input ref={fileRef} type="file" accept={accept} onChange={(e) => readFile(e.target.files?.[0])} className="hidden" />
        </div>
      </div>
      <textarea
        value={value}
        onChange={(e) => {
          onChange(e.target.value);
          onFileName("");
          onFile?.(null);
        }}
        onKeyDown={(e) => {
          if (onSubmit && (e.metaKey || e.ctrlKey) && e.key === "Enter") onSubmit();
        }}
        placeholder={dragOver ? "Drop file to upload…" : "Paste content, or drag a file here… (⌘/Ctrl + Enter to run)"}
        className={`w-full ${small ? "h-32" : "h-48"} bg-transparent p-3 text-sm text-slate-100 placeholder-slate-600 focus:outline-none resize-none font-mono leading-relaxed`}
        spellCheck={false}
      />
    </div>
  );
}
