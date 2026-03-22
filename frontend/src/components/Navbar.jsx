/**
 * Navbar.jsx — With Emotional Safety Mode that actually changes routing.
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Train, Zap, LogOut, User, Bell, ChevronDown } from 'lucide-react';
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';

const USER_MODES = [
  {
    value: 'normal',
    label: 'Normal',
    emoji: '😊',
    description: 'Balanced routing',
    color: '#10b981',
  },
  {
    value: 'anxious',
    label: 'Anxious',
    emoji: '😰',
    description: 'Avoids crowds, prefers safe routes',
    color: '#f59e0b',
  },
  {
    value: 'alone_night',
    label: 'Alone at Night',
    emoji: '🌙',
    description: 'Prioritises busy, well-lit transport',
    color: '#8b5cf6',
  },
  {
    value: 'late',
    label: 'Running Late',
    emoji: '🏃',
    description: 'Speed-first, minimal stops',
    color: '#ef4444',
  },
];

export default function Navbar({ onToggleHeatmap, heatmapActive, userMode, onUserModeChange }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [modeOpen, setModeOpen] = useState(false);

  const current = USER_MODES.find(m => m.value === userMode) || USER_MODES[0];

  return (
    <motion.nav
      initial={{ y: -60, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="h-14 bg-[#07071f]/90 backdrop-blur-xl border-b border-white/[0.07] flex items-center px-5 gap-3 z-50 relative"
    >
      {/* Logo */}
      <div className="flex items-center gap-2.5 flex-shrink-0">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-600 to-violet-900 flex items-center justify-center shadow-md shadow-violet-900/50">
          <Train size={15} className="text-white" />
        </div>
        <div className="leading-none">
          <span className="text-white font-bold text-base tracking-tight">CommuteIQ</span>
          <div className="flex items-center gap-1 mt-0.5">
            <Zap size={8} className="text-[#c6f135]" />
            <span className="text-[9px] text-[#c6f135] font-mono uppercase tracking-widest">AI Safety</span>
          </div>
        </div>
      </div>

      <div className="flex-1" />

      {/* Live badge */}
      <div className="hidden sm:flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/20 rounded-full px-3 py-1">
        <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
        <span className="text-emerald-400 text-xs font-medium">Live</span>
      </div>

      {/* Emotional Safety Mode Dropdown */}
      <div className="relative">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.97 }}
          onClick={() => setModeOpen(v => !v)}
          className="flex items-center gap-2 px-3 py-1.5 rounded-xl border transition-all"
          style={{
            backgroundColor: `${current.color}18`,
            borderColor: `${current.color}40`,
          }}
        >
          <span className="text-base leading-none">{current.emoji}</span>
          <div className="text-left hidden sm:block">
            <div className="text-[11px] font-bold leading-none" style={{ color: current.color }}>
              {current.label}
            </div>
            <div className="text-[9px] text-white/30 leading-none mt-0.5">Safety Mode</div>
          </div>
          <ChevronDown size={12} className="text-white/30" style={{
            transform: modeOpen ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 0.2s',
          }} />
        </motion.button>

        <AnimatePresence>
          {modeOpen && (
            <motion.div
              initial={{ opacity: 0, y: -8, scale: 0.96 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -8, scale: 0.96 }}
              transition={{ duration: 0.15 }}
              className="absolute right-0 top-full mt-2 w-64 bg-[#0d0d35] border border-white/10 rounded-2xl overflow-hidden shadow-2xl z-50"
            >
              <div className="px-3 py-2 border-b border-white/[0.06]">
                <div className="text-[9px] font-bold text-white/30 uppercase tracking-widest">
                  How do you feel right now?
                </div>
              </div>
              {USER_MODES.map(mode => (
                <motion.button
                  key={mode.value}
                  whileHover={{ backgroundColor: `${mode.color}12` }}
                  onClick={() => {
                    onUserModeChange && onUserModeChange(mode.value);
                    setModeOpen(false);
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-3 transition-all text-left ${
                    userMode === mode.value ? 'border-l-2' : 'border-l-2 border-transparent'
                  }`}
                  style={userMode === mode.value ? {
                    borderColor: mode.color,
                    backgroundColor: `${mode.color}15`,
                  } : {}}
                >
                  <span className="text-xl leading-none">{mode.emoji}</span>
                  <div className="flex-1">
                    <div className="font-semibold text-sm" style={{
                      color: userMode === mode.value ? mode.color : 'rgba(255,255,255,0.75)'
                    }}>
                      {mode.label}
                    </div>
                    <div className="text-[10px] text-white/35 mt-0.5">{mode.description}</div>
                  </div>
                  {userMode === mode.value && (
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: mode.color }} />
                  )}
                </motion.button>
              ))}
              <div className="px-4 py-2.5 border-t border-white/[0.06] bg-white/[0.02]">
                <p className="text-[9px] text-white/25 leading-relaxed">
                  Your safety mode re-weights route scores and reorders recommendations
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Heatmap Toggle */}
      <motion.button
        whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}
        onClick={onToggleHeatmap}
        className={`hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all border ${
          heatmapActive
            ? 'bg-orange-500/20 border-orange-500/30 text-orange-300'
            : 'bg-white/[0.05] border-white/10 text-white/50 hover:text-white/80'
        }`}
      >
        <div className={`w-2 h-2 rounded-full ${heatmapActive ? 'bg-orange-400' : 'bg-white/30'}`} />
        Heat
      </motion.button>

      {/* Bell */}
      <button className="w-8 h-8 rounded-lg bg-white/[0.05] border border-white/[0.08] flex items-center justify-center text-white/40 hover:text-white/70 transition-colors">
        <Bell size={14} />
      </button>

      {/* User */}
      <div className="flex items-center gap-2 bg-white/[0.04] border border-white/[0.08] rounded-xl px-3 py-1.5">
        <div className="w-6 h-6 rounded-full bg-gradient-to-br from-violet-500 to-violet-700 flex items-center justify-center">
          <User size={12} className="text-white" />
        </div>
        <span className="text-white/70 text-xs font-medium hidden sm:block">{user?.username || 'User'}</span>
      </div>

      {/* Logout */}
      <motion.button
        whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
        onClick={() => { logout(); navigate('/login'); }}
        className="w-8 h-8 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400 hover:bg-red-500/20 transition-all"
      >
        <LogOut size={14} />
      </motion.button>
    </motion.nav>
  );
}