export default function EmptyState({ icon: Icon, text }) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center text-slate-600 text-sm gap-2">
      <Icon size={26} className="opacity-40" /> {text}
    </div>
  );
}
