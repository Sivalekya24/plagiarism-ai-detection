import { useEffect, useState } from "react";

export default function AnimatedBar({ pct, className }) {
  const [w, setW] = useState(0);

  useEffect(() => {
    const t = setTimeout(() => setW(pct), 30);
    return () => clearTimeout(t);
  }, [pct]);

  return (
    <div className="h-1 bg-slate-800 rounded overflow-hidden mb-1.5">
      <div className={className} style={{ width: `${w}%`, transition: "width 0.6s cubic-bezier(.22,1,.36,1)" }} />
    </div>
  );
}
