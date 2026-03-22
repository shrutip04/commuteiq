/**
 * RiskIndicator.jsx — Current vs future risk display with trend arrow.
 */

import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

export default function RiskIndicator({ risk }) {
  if (!risk) return null;

  const { current_pct = 0, future_pct = 0, trend = 'stable' } = risk;

  const riskColor = (pct) =>
    pct < 30 ? '#10b981' : pct < 60 ? '#f59e0b' : '#ef4444';

  const TrendIcon = trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : Minus;
  const trendColor = trend === 'up' ? '#ef4444' : trend === 'down' ? '#10b981' : '#94a3b8';
  const trendLabel = trend === 'up' ? 'Rising' : trend === 'down' ? 'Falling' : 'Stable';

  return (
    <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
      <div className="text-[9px] text-white/30 uppercase tracking-wider mb-2 font-semibold">
        Risk Forecast
      </div>
      <div className="flex items-center gap-3">
        {/* Current */}
        <div className="flex-1 text-center">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="text-lg font-bold leading-none"
            style={{ color: riskColor(current_pct) }}
          >
            {current_pct}%
          </motion.div>
          <div className="text-[9px] text-white/30 mt-0.5">Now</div>
        </div>

        {/* Arrow */}
        <div className="flex flex-col items-center gap-0.5">
          <TrendIcon size={14} style={{ color: trendColor }} />
          <span className="text-[8px] font-semibold" style={{ color: trendColor }}>
            {trendLabel}
          </span>
        </div>

        {/* Future */}
        <div className="flex-1 text-center">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.15 }}
            className="text-lg font-bold leading-none"
            style={{ color: riskColor(future_pct) }}
          >
            {future_pct}%
          </motion.div>
          <div className="text-[9px] text-white/30 mt-0.5">In ~15 min</div>
        </div>
      </div>

      {/* Mini bar comparison */}
      <div className="mt-2.5 space-y-1">
        {[
          { label: 'Now', pct: current_pct },
          { label: '~15m', pct: future_pct },
        ].map(({ label, pct }) => (
          <div key={label} className="flex items-center gap-2">
            <span className="text-[9px] text-white/30 w-6">{label}</span>
            <div className="flex-1 h-1 bg-white/[0.06] rounded-full overflow-hidden">
              <motion.div
                className="h-full rounded-full"
                style={{ backgroundColor: riskColor(pct) }}
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
              />
            </div>
            <span className="text-[9px] font-semibold w-6 text-right"
              style={{ color: riskColor(pct) }}>{pct}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}