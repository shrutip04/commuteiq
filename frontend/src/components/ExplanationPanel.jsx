/**
 * ExplanationPanel.jsx — Intelligence panel with AI bullets, risk, what-if, guardian.
 */

import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Zap, AlertTriangle, RefreshCw, ChevronRight, CheckCircle } from 'lucide-react';
import RiskIndicator from './RiskIndicator';
import WhatIfPanel from './WhatIfPanel';
import GuardianMode from './GuardianMode';

function SkeletonLine({ width = 'w-full' }) {
  return <div className={`h-3 bg-white/[0.07] rounded animate-pulse ${width}`} />;
}

export default function ExplanationPanel({
  explanation, loadingExplanation,
  onSimulate, loadingSimulation,
  disruption, selectedRoute, userMode,
}) {
  const bullets = explanation?.bullets || [];

  return (
    <div className="flex flex-col gap-4">

      {/* AI Explanation */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-2xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-6 h-6 rounded-lg bg-violet-600/30 border border-violet-500/20 flex items-center justify-center">
            <Sparkles size={12} className="text-violet-400" />
          </div>
          <span className="text-white/60 text-xs font-semibold uppercase tracking-wider">AI Analysis</span>
        </div>

        <AnimatePresence mode="wait">
          {loadingExplanation ? (
            <motion.div key="load" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="space-y-2">
              <SkeletonLine /><SkeletonLine width="w-5/6" /><SkeletonLine width="w-4/5" />
            </motion.div>
          ) : bullets.length > 0 ? (
            <motion.div key="bullets" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="space-y-2">
              {bullets.map((b, i) => (
                <motion.div key={i} initial={{ opacity: 0, x: -6 }} animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }} className="flex items-start gap-2">
                  <CheckCircle size={11} className="text-violet-400 flex-shrink-0 mt-0.5" />
                  <p className="text-white/60 text-[11px] leading-relaxed">{b}</p>
                </motion.div>
              ))}
            </motion.div>
          ) : (
            <p className="text-white/25 text-sm italic">Select a route to see AI analysis.</p>
          )}
        </AnimatePresence>
      </div>

      {/* Risk Indicator */}
      <AnimatePresence>
        {selectedRoute?.risk && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}>
            <RiskIndicator risk={selectedRoute.risk} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Disruption Simulator */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-2xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <div className="w-6 h-6 rounded-lg bg-orange-600/30 border border-orange-500/20 flex items-center justify-center">
            <Zap size={12} className="text-orange-400" />
          </div>
          <span className="text-white/60 text-xs font-semibold uppercase tracking-wider">Disruption Sim</span>
        </div>
        <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
          onClick={onSimulate}
          disabled={loadingSimulation || !selectedRoute}
          className="w-full bg-orange-600/20 hover:bg-orange-600/35 border border-orange-500/25 hover:border-orange-500/50 disabled:opacity-40 disabled:cursor-not-allowed text-orange-300 font-semibold py-2.5 rounded-xl flex items-center justify-center gap-2 transition-all text-sm"
        >
          {loadingSimulation
            ? <><RefreshCw size={14} className="animate-spin" />Simulating…</>
            : <><AlertTriangle size={14} />Simulate Disruption<ChevronRight size={14} /></>
          }
        </motion.button>
      </div>

      <AnimatePresence>
        {disruption && (
          <motion.div key="dis" initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            className={`rounded-2xl p-4 border ${disruption.severity === 'HIGH' ? 'bg-red-500/10 border-red-500/30' : 'bg-orange-500/10 border-orange-500/30'}`}>
            <div className="flex items-start gap-2.5">
              <span className="text-xl">{disruption.icon}</span>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-white font-semibold text-sm">{disruption.label}</span>
                  <span className={`text-[9px] font-bold uppercase px-1.5 py-0.5 rounded-full border ${disruption.severity === 'HIGH' ? 'bg-red-500/20 border-red-500/30 text-red-400' : 'bg-orange-500/20 border-orange-500/30 text-orange-400'}`}>{disruption.severity}</span>
                </div>
                <p className="text-white/50 text-xs">{disruption.message}</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* What-If Engine */}
      <WhatIfPanel selectedRoute={selectedRoute} userMode={userMode} />

      {/* Guardian Mode */}
      <div>
        <div className="text-[10px] font-bold text-white/30 uppercase tracking-widest mb-3">
          🛡️ Guardian Mode
        </div>
        <GuardianMode selectedRoute={selectedRoute} userMode={userMode} />
      </div>
    </div>
  );
}