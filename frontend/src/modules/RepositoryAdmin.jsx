import { useEffect, useState } from "react";
import { Database, Search, Trash2, Upload, ShieldAlert, FileText, Code2 } from "lucide-react";
import toast from "react-hot-toast";
import LoadingState from "../components/LoadingState";
import FadeIn from "../components/FadeIn";
import {
  listRepositoryDocuments,
  getRepositoryStatistics,
  deleteRepositoryDocument,
  searchRepository,
  uploadToRepository,
  listCodeArchive,
  getCodeArchiveStatistics,
  deleteCodeArchiveDocument,
} from "../lib/api";

function StatCard({ label, value }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-3">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="text-xl font-serif italic text-slate-100 mt-0.5">{value}</div>
    </div>
  );
}

/**
 * ADMIN ONLY. This manages the archive that user-facing single-document /
 * single-file checks are compared against. Access to this whole module
 * should be gated server-side (auth check on every underlying call) —
 * hiding the tab in the UI is not real access control by itself.
 */
export default function RepositoryAdmin() {
  const [archive, setArchive] = useState("documents"); // documents | code
  const [stats, setStats] = useState(null);
  const [documents, setDocuments] = useState(null);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  async function refresh() {
    setLoading(true);
    if (archive === "documents") {
      const [statsRes, docsRes] = await Promise.all([getRepositoryStatistics(), listRepositoryDocuments()]);
      setStats(statsRes);
      setDocuments(docsRes.documents);
    } else {
      const [statsRes, docsRes] = await Promise.all([getCodeArchiveStatistics(), listCodeArchive()]);
      setStats(statsRes);
      setDocuments(docsRes.documents);
    }
    setLoading(false);
  }

  useEffect(() => {
    // Standard fetch-on-dependency-change pattern; refresh() sets loading/data
    // state, which is the whole point of this effect.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [archive]);

  function switchArchive(id) {
    setQuery("");
    setArchive(id);
  }

  async function handleSearch(e) {
    e.preventDefault();
    if (archive !== "documents") return; // no search endpoint confirmed for code archive yet
    if (!query.trim()) return refresh();
    setLoading(true);
    const res = await searchRepository(query);
    setDocuments(res.documents);
    setLoading(false);
  }

  async function handleDelete(filename) {
    setDocuments((docs) => docs.filter((d) => d.filename !== filename));
    if (archive === "documents") {
      await deleteRepositoryDocument(filename);
    } else {
      await deleteCodeArchiveDocument(filename);
    }
    toast.success(`Deleted ${filename}`);
    refresh();
  }

  async function handleUpload(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    await uploadToRepository(file); // document archive only — see note below for code
    toast.success(`Added ${file.name} to the archive`);
    setUploading(false);
    refresh();
    e.target.value = "";
  }

  return (
    <div>

      <div className="flex items-start gap-2 bg-amber-400/10 border border-amber-500/30 rounded-lg px-3 py-2.5 mb-6 text-xs text-amber-200">
        <ShieldAlert size={15} className="mt-0.5 shrink-0" />
        <span>
          Admin only. This manages the archive that user-facing single-document/single-file checks are compared
          against. Gate access to this panel server-side (auth check on every underlying call), not just by hiding
          the tab in the UI.
        </span>
      </div>

      <div className="flex flex-wrap gap-2 mb-5">
        {[
          ["documents", "Document Archive", FileText],
          ["code", "Code Archive", Code2],
        ].map(([id, label, Icon]) => (
          <button
            key={id}
            onClick={() => switchArchive(id)}
            className={`flex items-center gap-1.5 text-xs font-medium px-4 py-2 rounded-full border whitespace-nowrap ${
              archive === id ? "bg-amber-400 text-slate-950 border-amber-400" : "text-slate-400 border-slate-700 hover:border-slate-500"
            }`}
          >
            <Icon size={13} /> {label}
          </button>
        ))}
      </div>

      {archive === "code" && (
        <p className="text-xs text-slate-500 mb-4">
          Note: no dedicated "add to archive" endpoint is confirmed for code yet — entries here are assumed to come
          from <code>/code/upload</code> / <code>/code/paste</code> checks. Confirm with your backend and adjust if
          there's a separate admin upload route.
        </p>
      )}

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-6">
        <StatCard label="Files stored" value={stats ? stats.totalDocuments : "—"} />
        <StatCard label="Total size" value={stats ? `${stats.totalSizeKb} KB` : "—"} />
        <StatCard label="Last updated" value={stats ? stats.lastUpdated : "—"} />
      </div>

      <div className="flex flex-col sm:flex-row gap-3 mb-4">
        <form onSubmit={handleSearch} className="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 flex-1">
          <Search size={14} className="text-slate-500 shrink-0" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={archive === "documents" ? "Search stored documents…" : "Search not available for code archive yet"}
            disabled={archive !== "documents"}
            className="flex-1 bg-transparent text-sm text-slate-100 placeholder-slate-600 focus:outline-none min-w-0 disabled:cursor-not-allowed"
          />
        </form>
        {archive === "documents" && (
          <label className="verity-btn flex items-center justify-center gap-1.5 bg-amber-400 hover:bg-amber-300 text-slate-950 font-semibold text-sm px-4 py-2 rounded cursor-pointer shrink-0">
            <Upload size={15} /> {uploading ? "Adding…" : "Add to archive"}
            <input type="file" className="hidden" onChange={handleUpload} disabled={uploading} />
          </label>
        )}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 sm:p-5 min-h-[16rem]">
        {loading && <LoadingState text="Loading archive…" />}
        {!loading && documents && documents.length === 0 && (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-600 text-sm gap-2 py-10">
            <Database size={26} className="opacity-40" /> No files match.
          </div>
        )}
        {!loading && documents && documents.length > 0 && (
          <FadeIn>
            <div className="overflow-x-auto -mx-1">
              <table className="w-full text-sm min-w-[26rem]">
                <thead>
                  <tr className="text-left text-xs text-slate-500 border-b border-slate-800">
                    <th className="font-medium pb-2 px-1">Filename</th>
                    <th className="font-medium pb-2 px-1">Uploaded</th>
                    <th className="font-medium pb-2 px-1 text-right">Size</th>
                    <th className="font-medium pb-2 px-1 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {documents.map((d) => (
                    <tr key={d.filename} className="border-b border-slate-800/60 last:border-0">
                      <td className="py-2 px-1 font-mono text-slate-300 truncate max-w-[14rem]">{d.filename}</td>
                      <td className="py-2 px-1 text-slate-500 font-mono text-xs">{d.uploadedAt}</td>
                      <td className="py-2 px-1 text-right text-slate-400 font-mono text-xs">{d.sizeKb} KB</td>
                      <td className="py-2 px-1 text-right">
                        <button
                          onClick={() => handleDelete(d.filename)}
                          className="verity-btn text-rose-400 hover:text-rose-300 inline-flex items-center gap-1 text-xs border border-rose-500/30 hover:border-rose-400/60 rounded px-2 py-1"
                        >
                          <Trash2 size={12} /> Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </FadeIn>
        )}
      </div>
    </div>
  );
}
