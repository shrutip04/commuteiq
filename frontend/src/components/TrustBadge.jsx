/**
 * TrustBadge.jsx — Circular trust score badge with color coding.
 */

import { motion } from 'framer-motion';

export default function TrustBadge({ score, size = 'md' }) {
  const color  = score >= 75 ? '#10b981' : score >= 50 ? '#f59e0b' : '#ef4444';
  const label  = score >= 75 ? 'High Trust' : score >= 50 ? 'Moderate' : 'Low Trust';
  const dim    = size === 'sm' ? 44 : 56;
  const r      = size === 'sm' ? 18 : 22;
  const stroke = size === 'sm' ? 3 : 4;
  const circ   = 2 * Math.PI * r;
  const offset = circ - (score / 100) * circ;

  return (
    <div className="flex flex-col items-center gap-0.5">
      <div className="relative" style={{ width: dim, height: dim }}>
        <svg width={dim} height={dim} style={{ transform: 'rotate(-90deg)' }}>
          {/* Track */}
          <circle cx={dim/2} cy={dim/2} r={r} fill="none"
            stroke="rgba(255,255,255,0.08)" strokeWidth={stroke} />
          {/* Progress */}
          <motion.circle
            cx={dim/2} cy={dim/2} r={r} fill="none"
            stroke={color} strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={circ}
            initial={{ strokeDashoffset: circ }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1, ease: 'easeOut', delay: 0.2 }}
            style={{ filter: `drop-shadow(0 0 4px ${color}80)` }}
          />
        </svg>
        {/* Score text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="font-bold leading-none" style={{
            color,
            fontSize: size === 'sm' ? '11px' : '13px',
          }}>
            {score}
          </span>
        </div>
      </div>
      <span className="text-[8px] font-semibold uppercase tracking-wider"
        style={{ color: `${color}90` }}>
        {label}
      </span>
    </div>
  );
}