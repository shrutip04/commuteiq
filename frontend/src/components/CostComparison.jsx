/**
 * CostComparison.jsx — Multi-modal commute cost comparison engine.
 * Shows all transport options with cost, time, and segment breakdowns.
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { IndianRupee, Clock, Repeat, Trophy, Zap, Lightbulb, Filter, ChevronDown, ChevronUp, TrendingDown } from 'lucide-react';
import { costAPI } from '../services/api';

// ── Label config ──────────────────────────────────────────────────────────────
const LABEL_CONFIG = {
  cheapest:   { icon: <Trophy size={10} />,    text: 'Cheapest',   bg: 'bg-green-500/20',  border: 'border-green-500/30',  color: 'text-green-400'  },
  fastest:    { icon: <Zap size={10} />,        text: 'Fastest',    bg: 'bg-orange-500/20', border: 'border-orange-500/30', color: 'text-orange-400' },
  best_value: { icon: <Lightbulb size={10} />, text: 'Best Value', bg: 'bg-blue-500/20',   border: 'border-blue-500/30',  color: 'text-blue-400'   },
};

const FILTER_OPTIONS = [
  { value: 'all',       label: 'All' },
  { value: 'cheapest',  label: '🏆 Cheapest' },
  { value: 'fastest',   label: '⚡ Fastest' },
  { value: 'single',    label: 'Direct' },
  { value: 'multi',     label: 'Multi-modal' },
];

// ── Single card ───────────────────────────────────────────────────────────────
function CostCard({ option, isHighlighted, index }) {
  const [expanded, setExpanded] = useState(false);
  const isMulti = option.transfers > 0;

  const cardBorder = option.labels.includes('cheapest')
    ? 'border-green-500/40'
    : option.labels.includes('fastest')
    ? 'border-orange-500/40'
    : option.labels.includes('best_value')
    ? 'border-blue-500/40'
    : 'border-white/[0.07]';

  const cardBg = option.labels.includes('cheapest')
    ? 'bg-green-500/5'
    : option.labels.includes('fastest')
    ? 'bg-orange-500/5'
    : option.labels.includes('best_value')
    ? 'bg-blue-500/5'
    : 'bg-white/[0.02]';

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay: index * 0.04, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ scale: 1.01, transition: { duration: 0.15 } }}
      className={`rounded-2xl border cursor-pointer transition-all ${cardBorder} ${cardBg}`}
      onClick={() => setExpanded(v => !v)}
    >
      <div className="p-3">
        {/* Header row */}
        <div className="flex items-start justify-between gap-2 mb-2">
          <div className="flex-1 min-w-0">
            {/* Mode name */}
            <div className="flex items-center gap-1.5 flex-wrap">
              <span className="text-sm leading-none">{option.icon}</span>
              <span className="text-white font-semibold text-sm truncate">{option.mode}</span>
              {isMulti && (
                <span className="flex items-center gap-0.5 bg-white/[0.07] text-white/35 text-[9px] rounded-full px-1.5 py-0.5">
                  <Repeat size={8} />1 change
                </span>
              )}
            </div>
            {/* Label badges */}
            {option.labels.length > 0 && (
              <div className="flex gap-1 mt-1.5 flex-wrap">
                {option.labels.map(lbl => {
                  const cfg = LABEL_CONFIG[lbl];
                  return cfg ? (
                    <span key={lbl} className={`flex items-center gap-1 text-[9px] font-bold rounded-full px-2 py-0.5 border ${cfg.bg} ${cfg.border} ${cfg.color}`}>
                      {cfg.icon}{cfg.text}
                    </span>
                  ) : null;
                })}
              </div>
            )}
          </div>

          {/* Cost + time */}
          <div className="text-right flex-shrink-0">
            <div className="flex items-center gap-0.5 justify-end">
              <IndianRupee size={14} className="text-white/80" />
              <span className="text-white font-black text-lg leading-none">{option.total_cost}</span>
            </div>
            <div className="flex items-center gap-1 justify-end mt-1">
              <Clock size={9} className="text-white/30" />
              <span className="text-white/40 text-[10px]">{option.total_time} min</span>
            </div>
          </div>
        </div>

        {/* Segment mini-bar */}
        <div className="flex gap-1 mb-2">
          {option.segments.map((seg, i) => (
            <div
              key={i}
              className="h-1 rounded-full flex-1"
              style={{ backgroundColor: seg.color, opacity: 0.7 }}
            />
          ))}
        </div>

        {/* Segment quick summary */}
        <div className="flex items-center gap-2 flex-wrap">
          {option.segments.map((seg, i) => (
            <span key={i} className="text-[10px] text-white/40 flex items-center gap-1">
              <span>{seg.icon}</span>
              <span style={{ color: seg.color }}>₹{seg.cost}</span>
              {i < option.segments.length - 1 && <span className="text-white/20">+</span>}
            </span>
          ))}
          <span className="ml-auto text-[9px] text-white/20">
            {option.segments.length > 1 ? 'tap for breakdown' : ''}
          </span>
        </div>
      </div>

      {/* Expanded breakdown */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
          >
            <div className="px-3 pb-3 pt-1 border-t border-white/[0.06] space-y-2">
              {option.segments.map((seg, i) => (
                <div key={i} className="flex items-center gap-3 bg-white/[0.03] rounded-xl px-3 py-2">
                  <span className="text-base leading-none">{seg.icon}</span>
                  <div className="flex-1">
                    <div className="text-[11px] font-semibold text-white/70">{seg.label}</div>
                    <div className="text-[9px] text-white/30 mt-0.5">{seg.distance} km · {seg.time} min</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold" style={{ color: seg.color }}>₹{seg.cost}</div>
                  </div>
                </div>
              ))}

              {/* Total row */}
              <div className="flex items-center justify-between px-3 py-2 bg-white/[0.05] rounded-xl border border-white/[0.08]">
                <span className="text-[11px] font-bold text-white/60">Total</span>
                <div className="flex items-center gap-3">
                  <span className="text-[10px] text-white/40">{option.total_time} min</span>
                  <span className="text-sm font-black text-white">₹{option.total_cost}</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────
export default function CostComparison({ selectedRoute, routes }) {
  const [data, setData]         = useState(null);
  const [loading, setLoading]   = useState(false);
  const [filter, setFilter]     = useState('all');
  const [sortBy, setSortBy]     = useState('cost'); // cost | time
  const [error, setError]       = useState(null);

  const source      = selectedRoute?.source?.name || routes?.[0]?.source?.name;
  const destination = selectedRoute?.destination?.name || routes?.[0]?.destination?.name;
  const distance    = selectedRoute?.distance_km || routes?.[0]?.distance_km || 10;

  useEffect(() => {
    if (!source || !destination || !distance) return;
    setLoading(true);
    setError(null);
    costAPI.getCostOptions(source, destination, distance)
      .then(res => setData(res.data))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [source, destination, distance]);

  if (!source || !destination) return null;

  // Filter options
  const filteredOptions = () => {
    if (!data?.options) return [];
    let opts = [...data.options];

    if (filter === 'cheapest') opts = opts.filter(o => o.labels.includes('cheapest'));
    else if (filter === 'fastest') opts = opts.filter(o => o.labels.includes('fastest'));
    else if (filter === 'single')  opts = opts.filter(o => o.transfers === 0);
    else if (filter === 'multi')   opts = opts.filter(o => o.transfers > 0);

    if (sortBy === 'cost') opts.sort((a, b) => a.total_cost - b.total_cost);
    else opts.sort((a, b) => a.total_time - b.total_time);

    return opts;
  };

  return (
    <div className="mt-4">
      {/* Section header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <IndianRupee size={13} className="text-violet-400" />
          <span className="text-[10px] font-bold text-white/30 uppercase tracking-widest">
            Cost Comparison
          </span>
          {data && (
            <span className="text-[9px] text-white/20 bg-white/[0.05] rounded-full px-2 py-0.5">
              {data.options.length} options
            </span>
          )}
        </div>
        {/* Sort toggle */}
        {data && (
          <div className="flex gap-1">
            {[{ v: 'cost', l: '₹' }, { v: 'time', l: '⏱' }].map(s => (
              <button
                key={s.v}
                onClick={() => setSortBy(s.v)}
                className={`text-[10px] px-2 py-1 rounded-lg border transition-all ${
                  sortBy === s.v
                    ? 'bg-violet-600/30 border-violet-500/40 text-violet-300'
                    : 'bg-white/[0.04] border-white/10 text-white/30 hover:text-white/60'
                }`}
              >
                {s.l}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Filter pills */}
      {data && (
        <div className="flex gap-1.5 mb-3 flex-wrap">
          {FILTER_OPTIONS.map(f => (
            <button
              key={f.value}
              onClick={() => setFilter(f.value)}
              className={`text-[10px] px-2.5 py-1 rounded-full border transition-all ${
                filter === f.value
                  ? 'bg-violet-600/30 border-violet-500/40 text-violet-300'
                  : 'bg-white/[0.03] border-white/[0.07] text-white/30 hover:text-white/60'
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      )}

      {/* Savings insight */}
      <AnimatePresence>
        {data?.savings_insight && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-3 bg-green-500/10 border border-green-500/20 rounded-xl px-3 py-2.5 flex items-center gap-2"
          >
            <TrendingDown size={13} className="text-green-400 flex-shrink-0" />
            <span className="text-[11px] text-green-300 font-medium">{data.savings_insight}</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Loading */}
      {loading && (
        <div className="space-y-2">
          {[0,1,2].map(i => (
            <div key={i} className="h-16 rounded-2xl bg-white/[0.04] animate-pulse"
              style={{ animationDelay: `${i * 0.1}s` }} />
          ))}
        </div>
      )}

      {/* Error */}
      {error && !loading && (
        <div className="text-center text-white/30 text-xs py-4">
          Could not load cost data
        </div>
      )}

      {/* Cards */}
      {!loading && data && (
        <div className="space-y-2">
          {filteredOptions().map((option, i) => (
            <CostCard
              key={option.id}
              option={option}
              index={i}
              isHighlighted={option.labels.length > 0}
            />
          ))}
          {filteredOptions().length === 0 && (
            <div className="text-center text-white/25 text-xs py-4">
              No options match this filter
            </div>
          )}
        </div>
      )}

      {/* Distance note */}
      {data && (
        <p className="text-[9px] text-white/15 text-center mt-3">
          Based on {data.distance_km} km journey · Fares are estimates
        </p>
      )}
    </div>
  );
}