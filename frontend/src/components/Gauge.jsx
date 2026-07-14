import useCountUp from "../lib/useCountUp";

export default function Gauge({ score, leftLabel = "Human", rightLabel = "AI" }) {
  const animatedScore = useCountUp(score, 800);
  const angle = -90 + (animatedScore / 100) * 180;
  const isAi = score >= 50;

  return (
    <div className="flex flex-col items-center">
      <svg viewBox="0 0 200 120" className="w-44 sm:w-56 h-28 sm:h-36">
        <path d="M 20 100 A 80 80 0 0 1 100 20" fill="none" stroke="#fbbf24" strokeWidth="10" strokeLinecap="round" />
        <path d="M 100 20 A 80 80 0 0 1 180 100" fill="none" stroke="#22d3ee" strokeWidth="10" strokeLinecap="round" />
        <g
          style={{
            transform: `rotate(${angle}deg)`,
            transformOrigin: "100px 100px",
            transition: "transform 0.15s linear",
          }}
        >
          <line x1="100" y1="100" x2="100" y2="34" stroke="#f4f4f5" strokeWidth="3" strokeLinecap="round" />
        </g>
        <circle cx="100" cy="100" r="6" fill="#f4f4f5" />
      </svg>
      <div className="flex justify-between w-44 sm:w-56 -mt-2 px-1 text-xs font-mono tracking-wide">
        <span className="text-amber-400">{leftLabel.toUpperCase()}</span>
        <span className="text-cyan-400">{rightLabel.toUpperCase()}</span>
      </div>
      <div className={`mt-3 text-3xl font-serif italic tabular-nums ${isAi ? "text-cyan-300" : "text-amber-300"}`}>
        {isAi ? `${animatedScore}% AI-leaning` : `${100 - animatedScore}% Human-leaning`}
      </div>
    </div>
  );
}
