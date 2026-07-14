import { useState } from "react";
import { Code2, FileText, Lock } from "lucide-react";
import DocumentPlagiarism from "./modules/DocumentPlagiarism";
import CodePlagiarism from "./modules/CodePlagiarism";
import TextAiDetection from "./modules/TextAiDetection";
import CodeAiDetection from "./modules/CodeAiDetection";
import companyLogo from "./assets/images/company_logo.jpg";

const CATEGORIES = [
  {
    id: "plagiarism",
    label: "Plagiarism",
    modules: [
      {
        id: "document",
        label: "Document",
        icon: FileText,
        desc: "Compare two documents, or check a single document — automatically checked against the archive.",
        Comp: DocumentPlagiarism,
      },
      {
        id: "code",
        label: "Code",
        icon: Code2,
        desc: "Compare two code files, or check a single file — automatically checked against the archive.",
        Comp: CodePlagiarism,
      },
    ],
  },
  {
    id: "ai",
    label: "AI Detection",
    modules: [
      {
        id: "text",
        label: "Text",
        icon: FileText,
        desc: "Detect whether written content is AI-generated or human-written.",
        Comp: TextAiDetection,
      },
      {
        id: "code",
        label: "Code",
        icon: Code2,
        desc: "Detect AI-generated code logic using a trained XGBoost classifier.",
        Comp: CodeAiDetection,
      },
    ],
  },
];

export default function App() {
  const [category, setCategory] = useState("plagiarism");
  const [moduleId, setModuleId] = useState("document");

  const activeCategory = CATEGORIES.find((c) => c.id === category);
  const activeModule = activeCategory.modules.find((m) => m.id === moduleId) || activeCategory.modules[0];
  const ActiveComp = activeModule.Comp;

  function switchCategory(id) {
    setCategory(id);
    setModuleId(CATEGORIES.find((c) => c.id === id).modules[0].id);
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100" style={{ fontFamily: "Times New Roman, serif" }}>
      <header className="border-b border-slate-800/80">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-6 flex flex-col sm:flex-row sm:items-end justify-between gap-2">
          <div>
            <div className="flex items-baseline gap-2.5">
              <img src={companyLogo} alt="Company Logo" className="w-10 h-10" />
              <h1 className="text-[50px] font-serif italic tracking-wider">Shnoor International LLC</h1>
            </div>
            <p className="text-[22px] text-slate-400 font-medium mt-2">Plagiarism &amp; AI-provenance instrument.</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden sm:block text-right text-xs text-slate-600 font-mono">v1.1 · XGBoost + self-trained models</div>
            <a
              href="/admin"
              title="Admin"
              className="verity-btn flex items-center gap-1 text-[11px] font-mono text-slate-600 hover:text-slate-400 border border-slate-800 hover:border-slate-700 rounded px-2 py-1 shrink-0"
            >
              <Lock size={11} /> Admin
            </a>
          </div>
        </div>

        {/* Category pills */}
        <div className="max-w-5xl mx-auto px-4 sm:px-6 pb-4 flex gap-2 overflow-x-auto">
          {CATEGORIES.map((c) => (
            <button
              key={c.id}
              onClick={() => switchCategory(c.id)}
              className={`text-xl font-semibold px-6 py-2 rounded-full border whitespace-nowrap transition-colors ${
                category === c.id
                  ? "bg-white text-black border-white"
                  : "text-slate-300 border-slate-700 hover:border-slate-500"
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>
      </header>

      {/* Sub-module tabs (only shown when a category has more than one module) */}
      {activeCategory.modules.length > 1 && (
        <nav className="max-w-5xl mx-auto px-4 sm:px-6 pt-6 overflow-x-auto">
          <div className="flex gap-2 border-b border-slate-800 min-w-max">
            {activeCategory.modules.map((m) => {
              const Icon = m.icon;
              const active = m.id === moduleId;
              return (
                <button
                  key={m.id}
                  onClick={() => setModuleId(m.id)}
                  className={`flex items-center gap-3 px-8 py-5 text-xl font-semibold border-b-4 transition-all duration-200 ${
                    active ? "border-amber-400 text-amber-300" : "border-transparent text-slate-400 hover:text-white"
                  }`}
                >
                  <Icon size={15} /> {m.label}
                </button>
              );
            })}
          </div>
        </nav>
      )}

      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
        <p className="text-slate-500 text-lg mb-5">{activeModule.desc}</p>
        <ActiveComp key={`${category}-${moduleId}`} />
        <p className="text-[14px] text-slate-600 mt-8 max-w-2xl">Shnoor International LLC, 2024. All rights reserved.</p>
      </main>
    </div>
  );
}
