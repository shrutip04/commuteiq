/**
 * RouteList.jsx — Right panel: scrollable list of route cards + comparison mode.
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { LayoutGrid, Columns, ChevronDown, ChevronUp, Clock, Users, Shield } from 'lucide-react';
import RouteCard from './RouteCard';

function ComparisonView({ routes }) {
  if (routes.length < 2) return null;
  const [a, b] = routes;
  const metrics = [
    { key: 'travel_time', label: 'Travel Time', unit: 'min', icon: Clock, lower: true },
    { key: 'crowding_pct', label: 'Crowding', unit: '%', icon: Users, lower: true },
    { key: 'delay_minutes', label: 'Delay', unit: 'min', icon: Clock, lower: true },
    { key: 'confidence_score', label: 'Confidence', unit: '%', icon: Shield, lower: false,
      format: v => Math.round(v * 100) },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/[0.03] border border-white/[0.07] rounded-2xl overflow-hidden"
    >
      {/* Header */}
      <div className="grid grid-cols-3 bg-white/[0.04] border-b border-white/[0.07]">
        <div className="p-2.5 text-white/30 text-[10px] font-semibold uppercase tracking-wider">Metric</div>
        {[a, b].map((r, i) => (
          <div key={i} className="p-2.5 flex items-center gap-1.5 border-l border-white/[0.07]">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: r.color }} />
            <span className="text-white/70 text-[10px] font-semibold truncate">{r.name}</span>
          </div>
        ))}
      </div>

      {/* Rows */}
      {metrics.map((m, i) => {
        const va = m.format ? m.format(a[m.key]) : a[m.key];
        const vb = m.format ? m.format(b[m.key]) : b[m.key];
        const aWins = m.lower ? va <= vb : va >= vb;
        const bWins = m.lower ? vb <= va : vb >= va;

        return (
          <div key={m.key} className={`grid grid-cols-3 ${i % 2 === 0 ? '' : 'bg-white/[0.02]'}`}>
            <div className="p-2.5 text-white/30 text-[10px] flex items-center gap-1">
              <m.icon size={10} />
              {m.label}
            </div>
            {[{ v: va, wins: aWins }, { v: vb, wins: bWins }].map((item, j) => (
              <div key={j} className={`p-2.5 border-l border-white/[0.07] flex items-center gap-1 ${item.wins ? 'text-[#c6f135]' : 'text-white/50'}`}>
                <span className="text-sm font-bold">{item.v}</span>
                <span className="text-[9px]">{m.unit}</span>
                {item.wins && <span className="text-[9px] bg-[#c6f135]/10 rounded px-1">✓ Better</span>}
              </div>
            ))}
          </div>
        );
      })}
    </motion.div>
  );
}

export default function RouteList({ routes, selectedRouteId, onSelectRoute, loading }) {
  const [compareMode, setCompareMode] = useState(false);
  const [compareRoutes, setCompareRoutes] = useState([]);

  const toggleCompare = (route) => {
    setCompareRoutes(prev => {
      if (prev.find(r => r.route_id === route.route_id)) {
        return prev.filter(r => r.route_id !== route.route_id);
      }
      if (prev.length >= 2) return [prev[1], route];
      return [...prev, route];
    });
  };

  if (loading) {
    return (
      <div className="flex flex-col gap-3">
        {[0, 1, 2].map(i => (
          <div key={i} className="h-40 rounded-2xl bg-white/[0.04] animate-pulse" style={{ animationDelay: `${i * 0.1}s` }} />
        ))}
      </div>
    );
  }

  if (!routes?.length) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex flex-col items-center justify-center py-12 text-center"
      >
        <div className="text-4xl mb-3">🗺️</div>
        <p className="text-white/30 text-sm">Enter a journey to see route options</p>
      </motion.div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Controls */}
      <div className="flex items-center justify-between">
        <span className="text-white/50 text-xs">{routes.length} routes found</span>
        <div className="flex gap-1.5">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => { setCompareMode(false); setCompareRoutes([]); }}
            className={`p-1.5 rounded-lg border transition-all ${!compareMode ? 'bg-violet-600/20 border-violet-500/40 text-violet-300' : 'bg-white/[0.04] border-white/10 text-white/30 hover:text-white/60'}`}
          >
            <LayoutGrid size={13} />
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setCompareMode(true)}
            className={`p-1.5 rounded-lg border transition-all ${compareMode ? 'bg-violet-600/20 border-violet-500/40 text-violet-300' : 'bg-white/[0.04] border-white/10 text-white/30 hover:text-white/60'}`}
          >
            <Columns size={13} />
          </motion.button>
        </div>
      </div>

      {/* Route Cards */}
      <div className="flex flex-col gap-2.5">
        {routes.map((route, i) => (
          <div key={route.route_id} className="relative">
            <RouteCard
              route={route}
              index={i}
              selected={selectedRouteId === route.route_id}
              onClick={() => onSelectRoute(route)}
            />
            {compareMode && (
              <motion.button
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                whileHover={{ scale: 1.1 }}
                onClick={() => toggleCompare(route)}
                className={`absolute top-3 left-3 w-5 h-5 rounded flex items-center justify-center border text-[10px] font-bold transition-all ${
                  compareRoutes.find(r => r.route_id === route.route_id)
                    ? 'bg-violet-600 border-violet-500 text-white'
                    : 'bg-white/[0.08] border-white/20 text-white/40 hover:bg-white/15'
                }`}
              >
                {compareRoutes.findIndex(r => r.route_id === route.route_id) + 1 || ''}
              </motion.button>
            )}
          </div>
        ))}
      </div>

      {/* Comparison Table */}
      <AnimatePresence>
        {compareMode && compareRoutes.length === 2 && (
          <motion.div
            key="compare"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <div className="text-[10px] font-semibold text-white/30 uppercase tracking-wider mb-2">Side-by-Side Comparison</div>
            <ComparisonView routes={compareRoutes} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
