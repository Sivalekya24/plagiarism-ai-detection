/* =====================================================================
   API layer for Verity — mapped to the confirmed real backend endpoints.

   DOCUMENT PLAGIARISM (user-facing)
     POST /document/compare   { docA, docB }    -> two-document similarity report
     POST /document/upload    FormData(file)    -> single-document check (file)
     POST /document/paste     { text }          -> single-document check (pasted text)

   CODE PLAGIARISM (user-facing)
     POST /code/compare  { snippetA, snippetB }
     POST /code/upload   FormData(file)
     POST /code/paste    { code }

   AI DETECTION (user-facing)
     GET  /ai/health
     POST /ai/text          { text }          -> { label, confidence, score, features }
     POST /ai/text/upload   FormData(file)    -> same shape
     POST /ai/code          { code }          -> { language, label, confidence, score, model, features }
     POST /ai/code/upload   FormData(file)    -> same shape

   REPOSITORY — DOCUMENT ARCHIVE (admin only)
     POST   /repository/upload              FormData(file) -> add a document to the archive
     GET    /repository/documents           -> list stored documents
     GET    /repository/statistics          -> archive stats
     DELETE /repository/document/{filename} -> remove a stored document
     GET    /repository/search?q=...        -> search the archive

   CODE ARCHIVE (admin only)
     GET    /code/documents            -> list stored code files
     GET    /code/statistics           -> archive stats
     DELETE /code/document/{filename}  -> remove a stored code file
     NOTE: unlike documents, there's no separate "/code/repository/upload"
     admin-only endpoint visible in the API docs — /code/upload and
     /code/paste (the same ones used for checking) appear to be what
     populates this archive. Confirm this against your actual backend
     handler code; if there IS a dedicated admin upload endpoint, swap
     it in below in uploadToCodeArchive().

   Every function has the real fetch() written and commented out, with
   a demo fallback directly beneath so the app stays interactive before
   the backend is wired up. Delete the demo line once fetch() ships.
===================================================================== */
const API_BASE = "plagiarism-ai-detection-production.up.railway.app"; // "http://localhost:8000" for local dev
import { getAdminToken, setAdminToken, clearAdminToken } from "./auth";

const DEMO_LATENCY = 600;

async function demoDelay() {
  await new Promise((r) => setTimeout(r, DEMO_LATENCY));
}

// ---------------------------------------------------------------------
// Admin auth
// ---------------------------------------------------------------------

// Real login call. The backend validates credentials and returns a token
// that every subsequent /repository/* and /code/documents|statistics|
// document/* call must send back as `Authorization: Bearer <token>`.
export async function adminLogin(username, password) {
  const res = await fetch(`${API_BASE}/admin/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) {
    throw new Error(res.status === 401 ? "Invalid username or password." : "Login failed.");
  }
  const data = await res.json();
  setAdminToken(data.token);
  return data;
}
// Wraps fetch() for every admin-only archive endpoint: attaches the
// Bearer token, and on a 401/403 clears the stale token and forces the
// admin back to the login screen instead of silently failing.
async function adminFetch(path, options = {}) {
  const token = getAdminToken();
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    },
  });
  if (res.status === 401 || res.status === 403) {
    clearAdminToken();
    window.location.reload();
    throw new Error("Admin session expired — please sign in again.");
  }
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }
  return res.json();
}
export function words(text) {
  return text.toLowerCase().match(/[^\W\d_]+/gu) || [];
}

export function detectLanguage(code) {
  if (/\bdef\s+\w+\(.*\):/.test(code) || /^\s*import\s+\w+/m.test(code)) return "Python";
  if (/\bfunction\s+\w+\(|=>\s*{|const\s+\w+\s*=/.test(code)) return "JavaScript";
  if (/\bpublic\s+class\s+\w+|System\.out\.println/.test(code)) return "Java";
  if (/#include\s*<.*>|std::/.test(code)) return "C++";
  if (/\bfunc\s+\w+\(/.test(code) && /package\s+main/.test(code)) return "Go";
  if (/<\?php/.test(code)) return "PHP";
  return "Unknown";
}

// ---------------------------------------------------------------------
// Document Plagiarism
// ---------------------------------------------------------------------

export async function compareDocuments(docA, docB) {
  // return (await fetch("/document/compare", {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ docA, docB }),
  // })).json();

  await demoDelay();
  return demoSimilarityReport(docA.length + docB.length, {
    aName: "cs-dept-archive.edu/assignments/2023",
    bName: "openlibrary-essays.org/education",
  });
}

export async function checkSingleDocument({ file, text }) {
  // if (file) {
  //   const formData = new FormData();
  //   formData.append("file", file);
  //   return (await fetch("/document/upload", { method: "POST", body: formData })).json();
  // }
  // return (await fetch("/document/paste", {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ text }),
  // })).json();

  await demoDelay();
  const len = (file?.name?.length || 0) + (text?.length || 0);
  return demoSimilarityReport(len, {
    aName: "cs-dept-archive.edu/assignments/2023",
    bName: "openlibrary-essays.org/education",
  });
}

// ---------------------------------------------------------------------
// Code Plagiarism
// ---------------------------------------------------------------------

export async function compareCode(snippetA, snippetB) {
  // return (await fetch("/code/compare", {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ snippetA, snippetB }),
  // })).json();

  await demoDelay();
  return demoSimilarityReport(snippetA.length + snippetB.length, {
    aName: "github.com/example/utils.py#L44-L61",
    bName: "StackOverflow answer #291840",
  });
}

export async function checkSingleCode({ file, code }) {
  // if (file) {
  //   const formData = new FormData();
  //   formData.append("file", file);
  //   return (await fetch("/code/upload", { method: "POST", body: formData })).json();
  // }
  // return (await fetch("/code/paste", {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ code }),
  // })).json();

  await demoDelay();
  const len = (file?.name?.length || 0) + (code?.length || 0);
  return demoSimilarityReport(len, {
    aName: "github.com/example/utils.py#L44-L61",
    bName: "StackOverflow answer #291840",
  });
}

function demoSimilarityReport(seedLen, { aName, bName }) {
  const seed = seedLen % 11;
  const overall = Math.max(3, Math.min(82, 10 + seed * 7));
  return {
    overall,
    matches: [
      { source: aName, similarity: Math.min(overall, 41), snippet: "the primary determinants of long-term retention are spaced repetition" },
      { source: bName, similarity: Math.max(0, overall - 24), snippet: "students who engage in active recall outperform passive review methods" },
    ].filter((m) => m.similarity > 3),
  };
}

// ---------------------------------------------------------------------
// AI Detection
// ---------------------------------------------------------------------

export async function detectText({ file, text }) {
  // if (file) {
  //   const formData = new FormData();
  //   formData.append("file", file);
  //   return (await fetch("/ai/text/upload", { method: "POST", body: formData })).json();
  // }
  // return (await fetch("/ai/text", {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ text }),
  // })).json();

  await demoDelay();
  const len = (file?.name?.length || 0) + (text?.length || 0);
  const seed = len % 11;
  const score = Math.max(4, Math.min(96, 30 + seed * 6));
  return {
    label: score >= 50 ? "ai" : "human",
    confidence: score >= 50 ? score : 100 - score,
    score,
    features: [
      { name: "Burstiness", value: (1.1 - seed * 0.06).toFixed(2), note: "Sentence-length variation." },
      { name: "Lexical diversity", value: (0.45 + seed * 0.02).toFixed(2), note: "Unique words ÷ total words." },
      { name: "Perplexity", value: Math.round(80 + seed * 12), note: "Predictability under reference model." },
      { name: "Repeated phrasing", value: `${seed * 2}%`, note: "Reused two-word phrases." },
    ],
  };
}

export async function detectCode({ file, code }) {
  // if (file) {
  //   const formData = new FormData();
  //   formData.append("file", file);
  //   return (await fetch("/ai/code/upload", { method: "POST", body: formData })).json();
  // }
  // return (await fetch("/ai/code", {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ code }),
  // })).json();

  await demoDelay();
  const len = (file?.name?.length || 0) + (code?.length || 0);
  const seed = len % 11;
  const score = Math.max(4, Math.min(96, 25 + seed * 7));
  return {
    language: detectLanguage(code || ""),
    label: score >= 50 ? "ai" : "human",
    confidence: score >= 50 ? score : 100 - score,
    score,
    model: "XGBoost",
    features: [
      { name: "Comment density", value: `${seed * 3}%`, note: "AI code tends to over-document." },
      { name: "Identifier length (avg)", value: (4 + seed * 0.7).toFixed(1), note: "Descriptive names lean AI." },
      { name: "Naming consistency", value: `${70 + seed * 2}%`, note: "Uniform convention lean AI." },
      { name: "Cyclomatic complexity", value: 2 + (seed % 5), note: "Decision-point count." },
    ],
  };
}

export async function checkAiHealth() {
  // return (await fetch("/ai/health")).json();
  await demoDelay();
  return { status: "ok" };
}

// ---------------------------------------------------------------------
// Repository — Document Archive (ADMIN ONLY)
// ---------------------------------------------------------------------

export async function uploadToRepository(file) {
  const formData = new FormData();
  formData.append("file", file);
  return adminFetch("/repository/upload", { method: "POST", body: formData });
}

export async function listRepositoryDocuments() {
  return adminFetch("/repository/documents");
}

export async function getRepositoryStatistics() {
  return adminFetch("/repository/statistics");
}

export async function deleteRepositoryDocument(filename) {
  return adminFetch(`/repository/document/${encodeURIComponent(filename)}`, { method: "DELETE" });
}

export async function searchRepository(query) {
  return adminFetch(`/repository/search?q=${encodeURIComponent(query)}`);
}

// ---------------------------------------------------------------------
// Code Archive (ADMIN ONLY)
// ---------------------------------------------------------------------

export async function listCodeArchive() {
  return adminFetch("/code/documents");
}

export async function getCodeArchiveStatistics() {
  return adminFetch("/code/statistics");
}

export async function deleteCodeArchiveDocument(filename) {
  return adminFetch(`/code/document/${encodeURIComponent(filename)}`, { method: "DELETE" });
}
