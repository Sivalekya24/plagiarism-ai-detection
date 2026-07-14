import { Loader2 } from "lucide-react";

export default function LoadingState({ text }) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center text-slate-500 text-sm gap-3">
      <Loader2 size={20} className="animate-spin text-amber-400" /> {text}
    </div>
  );
}
