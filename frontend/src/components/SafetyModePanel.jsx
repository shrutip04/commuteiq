/**
 * SafetyModePanel.jsx — Shows exactly what the active safety mode changed
 * and includes a gender selector that affects route scoring.
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { User, ChevronDown, Info } from 'lucide-react';
import { prefsAPI } from '../services/api';

const MODE_INFO = {
  normal: {
    emoji: '😊', label: 'Normal Mode', color: '#10b981',
    description: 'Balanced routing. No safety adjustments.',
    rules: [],
  },
  anxious: {
    emoji: '😰', label: 'Anxious Mode', color: '#f59e0b',
    description: 'Avoids crowds. Prefers predictable, monitored transport.',
    rules: [
      '👥 High-crowd routes penalised −18 pts',
      '🚗 Auto/Cab penalised −12 pts (less predictable)',
      '🚇 Train & Metro boosted +5 pts',
      '🔀 Routes sorted by safety score, not speed',
    ],
  },
  alone_night: {
    emoji: '🌙', label: 'Alone at Night', color: '#8b5cf6',
    description: 'Prioritises busy, well-lit, monitored transport.',
    rules: [
      '🚇 Train & Metro boosted +15 pts (lit, monitored)',
      '🚗 Auto/Cab penalised −18 pts (risky alone at night)',
      '👻 Very low-crowd routes penalised (isolated = dangerous)',
      '🔀 Routes sorted by safety, not speed',
    ],
  },
  late: {
    emoji: '🏃', label: 'Running Late', color: '#ef4444',
    description: 'Speed-first routing. Fastest route always wins.',
    rules: [
      '⚡ Delay weighted 50% — top priority',
      '🏎️ Auto/Cab boosted +8 pts (fastest door-to-door)',
      '⏱️ Routes under 25 min get +12 pts bonus',
      '🔀 Routes sorted by travel time (fastest first)',
    ],
  },
};

const GENDER_OPTIONS = [
  { value: 'prefer_not_to_say', label: 'Prefer not to say', icon: '🔒' },
  { value: 'female',  label: 'Female',  icon: '👩' },
  { value: 'male',    label: 'Male',    icon: '👨' },
  { value: 'other',   label: 'Other',   icon: '🧑' },
];

export default function SafetyModePanel({ userMode, routes, gender, onGenderChange }) {
  const info = MODE_INFO[userMode] || MODE_INFO.normal;
  const [showGender, setShowGender] = useState(false);
  const [saving, setSaving]         = useState(false);
  const [saved, setSaved]           = useState(false);

  const currentGender = GENDER_OPTIONS.find(g => g.value === gender) || GENDER_OPTIONS[0];

  const handleGenderChange = async (val) => {
    setShowGender(false);
    onGenderChange && onGenderChange(val);
    setSaving(true);
    try {
      await prefsAPI.save({ gender: val, user_mode: userMode, preference: 'balanced' });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (e) { console.error(e); }
    finally { setSaving(false); }
  };

  const isFemaleNight = gender === 'female' && (userMode === 'alone_night' || userMode === 'anxious');

  return (
    <div className="mb-4 space-y-2">

      {/* Gender Selector — always visible */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <User size={12} className="text-white/30" />
            <span className="text-[10px] text-white/40 uppercase tracking-wider">Your Profile</span>
            {saved && <span className="text-[9px] text-green-400 font-semibold">✓ Saved</span>}
          </div>
          <div className="relative">
            <motion.button
              whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
              onClick={() => setShowGender(v => !v)}
              className="flex items-center gap-1.5 bg-white/[0.05] border border-white/10 rounded-lg px-2.5 py-1.5 text-[10px] text-white/60 hover:text-white/80 transition-colors"
            >
              <span>{currentGender.icon}</span>
              <span>{currentGender.label}</span>
              <ChevronDown size={10} style={{ transform: showGender ? 'rotate(180deg)' : '', transition: 'transform 0.2s' }} />
            </motion.button>

            <AnimatePresence>
              {showGender && (
                <motion.div
                  initial={{ opacity: 0, y: -6, scale: 0.96 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -6 }}
                  className="absolute right-0 top-full mt-1 w-48 bg-[#0d0d35] border border-white/10 rounded-xl overflow-hidden shadow-2xl z-50"
                >
                  <div className="px-3 py-2 border-b border-white/[0.06]">
                    <div className="text-[9px] text-white/30 uppercase tracking-wider">
                      Affects night safety scoring
                    </div>
                  </div>
                  {GENDER_OPTIONS.map(opt => (
                    <motion.button
                      key={opt.value}
                      whileHover={{ backgroundColor: 'rgba(124,58,237,0.15)' }}
                      onClick={() => handleGenderChange(opt.value)}
                      className={`w-full flex items-center gap-2.5 px-3 py-2.5 text-left transition-colors ${
                        gender === opt.value ? 'bg-violet-500/15' : ''
                      }`}
                    >
                      <span className="text-base">{opt.icon}</span>
                      <span className="text-[11px] font-medium text-white/70">{opt.label}</span>
                      {gender === opt.value && (
                        <div className="ml-auto w-1.5 h-1.5 rounded-full bg-violet-400" />
                      )}
                    </motion.button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Female night safety note */}
        <AnimatePresence>
          {isFemaleNight && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-2 flex items-start gap-1.5 bg-purple-500/10 border border-purple-500/20 rounded-lg px-2.5 py-2"
            >
              <Info size={10} className="text-purple-400 flex-shrink-0 mt-0.5" />
              <p className="text-[10px] text-purple-300 leading-relaxed">
                Female safety profile active: Auto/Cab penalised extra −10 pts,
                trains boosted +8 pts, isolated routes heavily penalised.
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Safety Mode Impact — only when non-normal mode active */}
      <AnimatePresence>
        {userMode !== 'normal' && (
          <motion.div
            key={userMode}
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            className="rounded-xl p-3 border"
            style={{
              background: `${info.color}10`,
              borderColor: `${info.color}30`,
            }}
          >
            <div className="flex items-center gap-2 mb-2">
              <span className="text-base leading-none">{info.emoji}</span>
              <div>
                <div className="font-bold text-[11px]" style={{ color: info.color }}>{info.label} Active</div>
                <div className="text-[9px] text-white/35 mt-0.5">{info.description}</div>
              </div>
            </div>

            {info.rules.length > 0 && (
              <div className="space-y-1 mt-2">
                {info.rules.map((rule, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -4 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.06 }}
                    className="text-[10px] text-white/50 flex items-start gap-1.5"
                  >
                    <span className="flex-shrink-0">{rule.split(' ')[0]}</span>
                    <span>{rule.split(' ').slice(1).join(' ')}</span>
                  </motion.div>
                ))}
              </div>
            )}

            {/* Route ranking after mode */}
            {routes && routes.length > 0 && (
              <div className="mt-3 pt-2.5 border-t border-white/[0.07]">
                <div className="text-[9px] text-white/25 uppercase tracking-wider mb-1.5">
                  Route ranking after {info.label}
                </div>
                {routes.slice(0, 4).map((r, i) => (
                  <div key={r.route_id} className="flex items-center gap-2 mb-1 last:mb-0">
                    <div className="w-4 h-4 rounded-full flex items-center justify-center text-[8px] font-black text-white flex-shrink-0"
                      style={{ backgroundColor: r.color }}>
                      {i + 1}
                    </div>
                    <span className="text-[10px] text-white/55 flex-1 truncate">{r.name}</span>
                    <div className="flex items-center gap-1">
                      <span className="text-[9px] font-bold" style={{
                        color: r.trust_score >= 75 ? '#10b981' : r.trust_score >= 50 ? '#f59e0b' : '#ef4444'
                      }}>
                        {r.trust_score}
                      </span>
                      {r.trust_delta !== undefined && r.trust_delta !== 0 && (
                        <span className="text-[8px]" style={{
                          color: r.trust_delta > 0 ? '#10b981' : '#ef4444'
                        }}>
                          ({r.trust_delta > 0 ? '+' : ''}{r.trust_delta})
                        </span>
                      )}
                    </div>
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