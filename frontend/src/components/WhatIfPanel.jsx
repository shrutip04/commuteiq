/**
 * WhatIfPanel.jsx — What-If scenario engine with real impact analysis.
 * Shows exactly how delay/rain/night changes safety scores.
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Sliders, CloudRain, Moon, Sun, Clock, Zap,
  TrendingDown, TrendingUp, AlertTriangle, RefreshCw
} from 'lucide-react';

const TOKEN = () => localStorage.getItem('commuteiq_token');

export default function WhatIfPanel({ selectedRoute, userMode }) {
  const [delay, setDelay]     = useState(0);
  const [weather, setWeather] = useState('clear');
  const [isNight, setIsNight] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult]   = useState(null);

  const WEATHER = [
    { value: 'clear',      label: 'Clear',       icon: <Sun size={12} />,       color: '#f59e0b' },
    { value: 'rain',       label: 'Rain',         icon: <CloudRain size={12} />, color: '#60a5fa' },
    { value: 'heavy_rain', label: 'Heavy Rain',   icon: <CloudRain size={12} />, color: '#3b82f6' },
  ];

  const handleSimulate = async () => {
    if (!selectedRoute) return;
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/api/guardian_scenario', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${TOKEN()}`,
        },
        body: JSON.stringify({
          route: selectedRoute,
          delay_added: delay,
          weather,
          is_night: isNight,
          user_mode: userMode,
        }),
      });
      const json = await res.json();
      setResult(json.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const trustColor = s => s >= 75 ? '#10b981' : s >= 50 ? '#f59e0b' : '#ef4444';

  return (
    <div className="bg-white/[0.03] border border-white/[0.07] rounded-2xl p-4">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-6 h-6 rounded-lg bg-violet-500/20 border border-violet-500/30 flex items-center justify-center">
          <Sliders size={12} className="text-violet-400" />
        </div>
        <span className="text-white/60 text-xs font-semibold uppercase tracking-wider">What-If Engine</span>
      </div>

      {/* Delay Slider */}
      <div className="mb-4">
        <div className="flex justify-between mb-1.5">
          <div className="flex items-center gap-1.5 text-[10px] text-white/40 uppercase tracking-wider">
            <Clock size={10} />Delay
          </div>
          <span className="text-[11px] font-bold text-white/80">
            {delay === 0 ? 'No delay' : `+${delay} min`}
          </span>
        </div>
        <input
          type="range" min="0" max="20" step="1" value={delay}
          onChange={e => setDelay(Number(e.target.value))}
          className="w-full h-1.5 rounded-full appearance-none cursor-pointer"
          style={{
            background: `linear-gradient(to right, #7c3aed ${delay * 5}%, rgba(255,255,255,0.08) ${delay * 5}%)`,
          }}
        />
        <div className="flex justify-between text-[9px] text-white/15 mt-1">
          <span>0</span><span>5</span><span>10</span><span>15</span><span>20</span>
        </div>
      </div>

      {/* Weather */}
      <div className="mb-4">
        <div className="text-[10px] text-white/40 uppercase tracking-wider mb-2">Weather Condition</div>
        <div className="flex gap-1.5">
          {WEATHER.map(w => (
            <motion.button
              key={w.value}
              whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.96 }}
              onClick={() => setWeather(w.value)}
              className="flex-1 flex items-center justify-center gap-1 py-2 rounded-xl text-[10px] font-semibold border transition-all"
              style={weather === w.value ? {
                backgroundColor: `${w.color}20`,
                borderColor: `${w.color}50`,
                color: w.color,
              } : {
                backgroundColor: 'rgba(255,255,255,0.03)',
                borderColor: 'rgba(255,255,255,0.08)',
                color: 'rgba(255,255,255,0.3)',
              }}
            >
              {w.icon}{w.label}
            </motion.button>
          ))}
        </div>
      </div>

      {/* Night Toggle */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Moon size={13} className={isNight ? 'text-violet-400' : 'text-white/25'} />
          <span className="text-[10px] text-white/40 uppercase tracking-wider">Night Mode</span>
        </div>
        <motion.button
          onClick={() => setIsNight(v => !v)}
          className="w-11 h-6 rounded-full relative transition-colors"
          style={{ backgroundColor: isNight ? '#7c3aed' : 'rgba(255,255,255,0.08)' }}
        >
          <motion.div
            className="absolute top-1 w-4 h-4 rounded-full bg-white shadow"
            animate={{ left: isNight ? '26px' : '4px' }}
            transition={{ type: 'spring', stiffness: 500, damping: 30 }}
          />
        </motion.button>
      </div>

      {/* Run Button */}
      <motion.button
        whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
        onClick={handleSimulate}
        disabled={loading || !selectedRoute}
        className="w-full bg-violet-600/25 hover:bg-violet-600/45 border border-violet-500/30 disabled:opacity-40 disabled:cursor-not-allowed text-violet-200 font-bold py-2.5 rounded-xl flex items-center justify-center gap-2 transition-all text-sm"
      >
        {loading
          ? <><RefreshCw size={13} className="animate-spin" />Analysing…</>
          : <><Zap size={13} />Simulate Impact</>
        }
      </motion.button>

      {/* Impact Result */}
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 overflow-hidden"
          >
            {/* Before / After */}
            <div className="flex items-center gap-3 mb-3">
              <div className="flex-1 bg-white/[0.04] border border-white/[0.07] rounded-xl p-3 text-center">
                <div className="text-[9px] text-white/30 uppercase tracking-wider mb-1">Before</div>
                <div className="text-xl font-black" style={{ color: trustColor(result.original.trust_score) }}>
                  {result.original.trust_score}
                </div>
                <div className="text-[9px] text-white/30">trust score</div>
              </div>

              <div className="flex flex-col items-center">
                {result.trust_delta < -5
                  ? <TrendingDown size={20} className="text-red-400" />
                  : result.trust_delta > 5
                  ? <TrendingUp size={20} className="text-green-400" />
                  : <span className="text-white/30 text-lg">→</span>
                }
                <span className="text-[10px] font-bold mt-0.5"
                  style={{ color: result.trust_delta < 0 ? '#ef4444' : '#10b981' }}>
                  {result.trust_delta > 0 ? '+' : ''}{result.trust_delta}
                </span>
              </div>

              <div className="flex-1 bg-white/[0.04] border border-white/[0.07] rounded-xl p-3 text-center">
                <div className="text-[9px] text-white/30 uppercase tracking-wider mb-1">After</div>
                <div className="text-xl font-black" style={{ color: trustColor(result.simulated.trust_score) }}>
                  {result.simulated.trust_score}
                </div>
                <div className="text-[9px] text-white/30">trust score</div>
              </div>
            </div>

            {/* Impact bullets */}
            <div className="space-y-1.5">
              {result.impacts.map((impact, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -6 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.08 }}
                  className="bg-white/[0.03] border border-white/[0.06] rounded-xl px-3 py-2"
                >
                  <p className="text-[11px] text-white/65 leading-relaxed">{impact}</p>
                </motion.div>
              ))}
            </div>

            {/* Warnings */}
            {result.warnings?.length > 0 && (
              <div className="mt-2 space-y-1">
                {result.warnings.map((w, i) => (
                  <div key={i} className="flex items-center gap-1.5">
                    <AlertTriangle size={10} className="text-orange-400 flex-shrink-0" />
                    <span className="text-[10px] text-orange-300">{w}</span>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}