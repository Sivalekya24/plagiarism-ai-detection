import { useState } from "react";
import { LogOut } from "lucide-react";
import { isAdminAuthenticated, clearAdminToken } from "./lib/auth";
import { adminLogin } from "./lib/api";
import RepositoryAdmin from "./modules/RepositoryAdmin";

function AdminLogin({ onSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await adminLogin(username, password);
      onSuccess();
    } catch (err) {
      setError(err.message || "Sign in failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center px-4">
      <form onSubmit={handleSubmit} className="w-full max-w-sm bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h1 className="text-xl font-serif italic mb-1">Admin sign in</h1>
        <p className="text-xs text-slate-500 mb-5">Repository archive management.</p>

        <label className="block text-xs text-slate-400 mb-1">Username</label>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          autoFocus
          className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm mb-3 focus:outline-none focus:border-amber-400/50"
        />

        <label className="block text-xs text-slate-400 mb-1">Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm mb-4 focus:outline-none focus:border-amber-400/50"
        />

        {error && <p className="text-rose-400 text-xs mb-3">{error}</p>}

        <button
          type="submit"
          disabled={loading || !username || !password}
          className="verity-btn w-full bg-amber-400 hover:bg-amber-300 disabled:bg-slate-800 disabled:text-slate-600 text-slate-950 font-semibold text-sm px-4 py-2 rounded"
        >
          {loading ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}

// Mounted only when the URL is /admin (see main.jsx) — regular users never
// load this bundle path in the UI nav. Real access control still lives in
// the backend: every /repository/* and /code/documents|statistics|document/*
// handler must verify the Bearer token itself, since a client-side gate can
// always be bypassed by someone hitting the API directly.
export default function AdminApp() {
  const [authed, setAuthed] = useState(isAdminAuthenticated());

  if (!authed) {
    return <AdminLogin onSuccess={() => setAuthed(true)} />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800/80">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-5 flex items-center justify-between">
          <h1 className="text-lg font-serif italic">Repository Admin</h1>
          <button
            onClick={() => {
              clearAdminToken();
              setAuthed(false);
            }}
            className="verity-btn flex items-center gap-1.5 text-xs text-slate-400 hover:text-rose-300 border border-slate-700 hover:border-rose-400/50 rounded px-3 py-1.5"
          >
            <LogOut size={13} /> Sign out
          </button>
        </div>
      </header>
      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
        <RepositoryAdmin />
      </main>
    </div>
  );
}
