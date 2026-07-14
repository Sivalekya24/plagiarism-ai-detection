/* =====================================================================
   Plain-text report generation + download for result screens.
   No external libraries — Blob + a throwaway <a download> element.
===================================================================== */

export function triggerTextDownload(filename, content) {
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function timestamp() {
  return new Date().toISOString().replace(/[:.]/g, "-");
}

// ---------------------------------------------------------------------
// Plagiarism reports (Document + Code)
// ---------------------------------------------------------------------

export function buildPlagiarismReportText({ kind, mode, overall, matches }) {
  const lines = [
    `Verity ${kind} Plagiarism Report`,
    `Generated: ${new Date().toLocaleString()}`,
    `Mode: ${mode === "two" ? "Two-item compare" : "Single-item check (vs. archive)"}`,
    "",
    `Overall similarity: ${overall}%`,
    "",
    "Matches:",
  ];

  if (!matches || matches.length === 0) {
    lines.push("  (no matches above threshold)");
  } else {
    matches.forEach((m, i) => {
      lines.push(`  ${i + 1}. Source: ${m.source}`);
      lines.push(`     Similarity: ${m.similarity}%`);
      if (m.snippet) lines.push(`     Snippet: "${m.snippet}"`);
      lines.push("");
    });
  }

  return lines.join("\n");
}

export function downloadPlagiarismReport({ kind, mode, overall, matches }) {
  const text = buildPlagiarismReportText({ kind, mode, overall, matches });
  triggerTextDownload(`verity-${kind.toLowerCase()}-plagiarism-${timestamp()}.txt`, text);
}

// ---------------------------------------------------------------------
// AI detection reports (Text + Code)
// ---------------------------------------------------------------------

export function buildAiDetectionReportText({ kind, result }) {
  const lines = [
    `Verity ${kind} AI Detection Report`,
    `Generated: ${new Date().toLocaleString()}`,
  ];

  if (result.language) lines.push(`Language: ${result.language}`);
  if (result.model) lines.push(`Model: ${result.model}`);

  lines.push(
    "",
    `Verdict: ${result.label === "ai" ? "Likely AI-generated" : "Likely human-written"}`,
    `Confidence: ${result.confidence}%`,
    `Score: ${result.score}`,
    "",
    "Features:"
  );

  (result.features || []).forEach((f) => {
    lines.push(`  - ${f.name}: ${f.value}${f.note ? ` (${f.note})` : ""}`);
  });

  return lines.join("\n");
}

export function downloadAiDetectionReport({ kind, result }) {
  const text = buildAiDetectionReportText({ kind, result });
  triggerTextDownload(`verity-${kind.toLowerCase()}-ai-detection-${timestamp()}.txt`, text);
}
