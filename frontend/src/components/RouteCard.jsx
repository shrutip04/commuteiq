import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import {
  Clock, Users, AlertTriangle, Shield, Train, Bus,
  Footprints, Car, ChevronDown, ChevronUp, ArrowRight,
  Repeat, Navigation, MapPin, Info, Zap, TrendingUp, TrendingDown
} from 'lucide-react';
import TrustBadge from './TrustBadge';

function CrowdingBar({ pct }) {
  const color = pct < 35 ? '#10b981' : pct < 65 ? '#f59e0b' : '#ef4444';
  const label = pct < 35 ? 'Low' : pct < 65 ? 'Moderate' : 'High';
  return (
    <div>
      <div className="flex justify-between items-center mb-1">
        <span className="text-[10px] text-white/40 uppercase tracking-wider">Crowding</span>
        <span className="text-[10px] font-semibold" style={{ color }}>{label} · {Math.round(pct)}%</span>
      </div>
      <div className="h-1.5 bg-white/[0.08] rounded-full overflow-hidden">
        <motion.div className="h-full rounded-full" style={{ backgroundColor: color }}
          initial={{ width: 0 }} animate={{ width: `${pct}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }} />
      </div>
    </div>
  );
}

function ConfidenceBar({ score }) {
  const pct = Math.round(score * 100);
  return (
    <div>
      <div className="flex justify-between items-center mb-1">
        <span className="text-[10px] text-white/40 uppercase tracking-wider">
          <Shield size={9} className="inline mr-0.5" />Confidence
        </span>
        <span className="text-[10px] font-semibold text-violet-300">{pct}%</span>
      </div>
      <div className="h-1.5 bg-white/[0.08] rounded-full overflow-hidden">
        <motion.div className="h-full rounded-full bg-gradient-to-r from-violet-500 to-violet-400"
          initial={{ width: 0 }} animate={{ width: `${pct}%` }}
          transition={{ duration: 0.8, delay: 0.1, ease: 'easeOut' }} />
      </div>
    </div>
  );
}

const MODE_ICONS = {
  'Local Train': <Train size={11} />,
  'Metro': <Train size={11} />,
  'Bus': <Bus size={11} />,
  'Walk': <Footprints size={11} />,
  'Transfer': <Repeat size={11} />,
  'Auto/Cab': <Car size={11} />,
};

const MODE_COLORS = {
  'Local Train': '#ef4444',
  'Metro': '#06b6d4',
  'Bus': '#10b981',
  'Walk': '#94a3b8',
  'Transfer': '#94a3b8',
  'Auto/Cab': '#f59e0b',
};

function StepCard({ step, isLast }) {
  const color = step.color || MODE_COLORS[step.mode] || '#6366f1';
  const isTransfer = step.mode === 'Transfer';
  const isCab = step.mode === 'Auto/Cab';

  return (
    <div className="relative">
      {/* Vertical connector line */}
      {!isLast && (
        <div className="absolute left-[18px] top-[36px] bottom-0 w-0.5 bg-white/[0.08]" style={{ height: 'calc(100% - 8px)' }} />
      )}

      <div className={`flex gap-3 mb-3 ${isTransfer ? 'opacity-60' : ''}`}>
        {/* Mode icon circle */}
        <div className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 z-10"
          style={{ backgroundColor: `${color}20`, border: `1.5px solid ${color}40` }}>
          <span style={{ color }}>{MODE_ICONS[step.mode] || <Train size={14} />}</span>
        </div>

        <div className="flex-1 min-w-0 pb-1">
          {/* Line name + badge */}
          <div className="flex items-center gap-1.5 flex-wrap mb-1">
            <span className="text-white font-semibold text-xs">{step.line}</span>
            {step.is_fast && (
              <span className="flex items-center gap-0.5 bg-yellow-500/20 border border-yellow-500/30 text-yellow-400 text-[9px] font-bold rounded-full px-1.5 py-0.5">
                <Zap size={8} />FAST
              </span>
            )}
            {step.train_type && !isTransfer && (
              <span className="bg-white/[0.07] text-white/40 text-[9px] rounded-full px-1.5 py-0.5">
                {step.train_type}
              </span>
            )}
          </div>

          {/* From → To */}
          {!isTransfer && (
            <div className="flex items-center gap-1 text-[10px] text-white/50 mb-1.5">
              <MapPin size={9} className="text-green-400 flex-shrink-0" />
              <span className="font-medium text-white/70">{step.from}</span>
              <ArrowRight size={8} className="flex-shrink-0 text-white/30" />
              <MapPin size={9} className="flex-shrink-0" style={{ color: step.color }} />
              <span className="font-medium text-white/70">{step.to}</span>
            </div>
          )}

          {/* Stats row */}
          {step.stops > 0 && (
            <div className="flex items-center gap-3 mb-1.5">
              <span className="text-[9px] text-white/30 flex items-center gap-0.5">
                <Navigation size={8} />{step.stops} stops
              </span>
              {step.freq_min > 0 && (
                <span className="text-[9px] text-white/30 flex items-center gap-0.5">
                  <Clock size={8} />every {step.freq_min} min
                </span>
              )}
              {step.fare && (
                <span className="text-[9px] text-white/30">₹{step.fare}</span>
              )}
              {step.journey_min && (
                <span className="text-[9px] text-white/30">~{step.journey_min} min ride</span>
              )}
            </div>
          )}

          {/* Direction pill — M-Indicator style */}
          {step.direction && !isTransfer && (
            <div className="flex items-center gap-1 mb-1.5">
              <span className="text-[9px] text-white/30">Towards</span>
              <span className="bg-white/[0.08] border border-white/10 text-white/60 text-[9px] font-semibold rounded-full px-2 py-0.5">
                → {step.direction}
              </span>
            </div>
          )}

          {/* Platform badge */}
          {step.platform && step.platform !== '—' && (
            <div className="flex items-center gap-1.5 mb-1.5">
              <span className="bg-blue-500/20 border border-blue-500/30 text-blue-300 text-[9px] font-bold rounded-lg px-2 py-0.5">
                Platform {step.platform}
              </span>
            </div>
          )}

          {/* Bus stops via */}
          {step.via && step.via.length > 0 && (
            <div className="mb-1.5">
              <div className="text-[9px] text-white/30 mb-0.5">Key stops:</div>
              <div className="flex flex-wrap gap-1">
                {step.via.map((v, i) => (
                  <span key={i} className="bg-white/[0.04] border border-white/[0.08] text-white/40 text-[9px] rounded-md px-1.5 py-0.5">
                    {v}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Boarding tip — highlighted box */}
          {step.boarding_tip && (
            <div className="bg-green-500/10 border border-green-500/20 rounded-xl px-2.5 py-2 mb-1">
              <div className="flex items-start gap-1.5">
                <Info size={10} className="text-green-400 flex-shrink-0 mt-0.5" />
                <span className="text-[10px] text-green-300 leading-relaxed">{step.boarding_tip}</span>
              </div>
            </div>
          )}

          {/* Alight tip */}
          {step.alight_tip && step.alight_tip !== '' && (
            <div className="bg-violet-500/10 border border-violet-500/20 rounded-xl px-2.5 py-2">
              <div className="flex items-start gap-1.5">
                <MapPin size={10} className="text-violet-400 flex-shrink-0 mt-0.5" />
                <span className="text-[10px] text-violet-300 leading-relaxed">{step.alight_tip}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function RouteCard({ route, selected, index, onClick }) {
  const [showSteps, setShowSteps] = useState(false);
  const isDisrupted = route.disrupted;
  const steps = (route.steps || []).filter(s => s.mode !== 'Walk' || s.boarding_tip);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.08 }}
      onClick={onClick}
      className={`relative cursor-pointer rounded-2xl p-4 border transition-all ${
        selected
          ? 'bg-violet-600/15 border-violet-500/50 shadow-lg shadow-violet-900/20'
          : 'bg-white/[0.03] border-white/[0.07] hover:bg-white/[0.05] hover:border-white/[0.12]'
      } ${isDisrupted ? 'border-orange-500/40' : ''}`}
    >
      {isDisrupted && (
        <div className="absolute top-3 right-3 flex items-center gap-1 bg-orange-500/20 border border-orange-500/30 rounded-full px-2 py-0.5">
          <AlertTriangle size={9} className="text-orange-400" />
          <span className="text-orange-400 text-[9px] font-bold uppercase">Disrupted</span>
        </div>
      )}
      {selected && !isDisrupted && (
        <div className="absolute top-3 right-3 w-2 h-2 rounded-full bg-violet-400" />
      )}

      {/* Header */}
      <div className="flex items-start gap-3 mb-3" onClick={onClick}>
        <div className="w-3 h-3 rounded-full mt-0.5 flex-shrink-0"
          style={{ backgroundColor: route.color, boxShadow: `0 0 8px ${route.color}60` }} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-white font-semibold text-sm">{route.name}</span>
            {index === 0 && !isDisrupted && (
              <span className="bg-[#c6f135]/15 border border-[#c6f135]/25 text-[#c6f135] text-[9px] font-bold uppercase tracking-wider rounded-full px-1.5 py-0.5">
                Best
              </span>
            )}
            {route.transfers > 0 && (
              <span className="flex items-center gap-0.5 bg-white/[0.07] text-white/40 text-[9px] rounded-full px-1.5 py-0.5">
                <Repeat size={8} />{route.transfers} change
              </span>
            )}
          </div>

          <div className="flex items-center gap-1 mt-1.5 flex-wrap">
            {route.modes?.map((mode, i) => (
              <span key={i} className="flex items-center gap-0.5 text-[10px] rounded-md px-1.5 py-0.5 font-medium"
                style={{
                  backgroundColor: `${MODE_COLORS[mode] || '#6366f1'}20`,
                  color: MODE_COLORS[mode] || '#6366f1',
                  border: `1px solid ${MODE_COLORS[mode] || '#6366f1'}30`
                }}>
                {MODE_ICONS[mode] || <Train size={11} />}{mode}
              </span>
            ))}
            {route.frequency_min > 0 && (
              <span className="text-[9px] text-white/25 ml-1">every {route.frequency_min} min</span>
            )}
          </div>
        </div>
        {/* Trust Badge */}
        {route.trust_score !== undefined && (
          <TrustBadge score={route.trust_score} size="sm" />
        )}
      </div>

      {/* Risk mini indicator */}
      {route.risk && (
        <div className="flex items-center gap-2 mb-3 bg-white/[0.03] border border-white/[0.06] rounded-xl px-3 py-2">
          <span className="text-[9px] text-white/30 uppercase tracking-wider">Risk</span>
          <div className="flex items-center gap-1.5 flex-1">
            <span className="text-[10px] font-bold" style={{
              color: route.risk.current_pct < 30 ? '#10b981' : route.risk.current_pct < 60 ? '#f59e0b' : '#ef4444'
            }}>{route.risk.current_pct}%</span>
            {route.risk.trend === 'up' && <TrendingUp size={10} className="text-red-400" />}
            {route.risk.trend === 'down' && <TrendingDown size={10} className="text-green-400" />}
            <span className="text-[9px] text-white/30">now →</span>
            <span className="text-[10px] font-bold" style={{
              color: route.risk.future_pct < 30 ? '#10b981' : route.risk.future_pct < 60 ? '#f59e0b' : '#ef4444'
            }}>{route.risk.future_pct}% in ~15min</span>
          </div>
        </div>
      )}

      {/* Metrics */}
      <div className="grid grid-cols-3 gap-2 mb-3">
        <div className="bg-white/[0.04] rounded-xl p-2 text-center">
          <Clock size={12} className="text-white/30 mx-auto mb-0.5" />
          <div className="text-white font-bold text-sm">{route.travel_time}</div>
          <div className="text-white/30 text-[9px]">min</div>
        </div>
        <div className="bg-white/[0.04] rounded-xl p-2 text-center">
          <AlertTriangle size={12} className="text-white/30 mx-auto mb-0.5" />
          <div className="text-white font-bold text-sm">{route.delay_minutes}</div>
          <div className="text-white/30 text-[9px]">delay min</div>
        </div>
        <div className="bg-white/[0.04] rounded-xl p-2 text-center">
          <Users size={12} className="text-white/30 mx-auto mb-0.5" />
          <div className="text-white font-bold text-sm">{route.num_stops}</div>
          <div className="text-white/30 text-[9px]">stops</div>
        </div>
      </div>

      <div className="space-y-2 mb-3">
        <CrowdingBar pct={route.crowding_pct} />
        <ConfidenceBar score={route.confidence_score} />
      </div>

      {/* Step-by-step toggle */}
      {steps.length > 0 && (
        <div>
          <button
            onClick={(e) => { e.stopPropagation(); setShowSteps(v => !v); }}
            className="w-full flex items-center justify-between px-3 py-2 rounded-xl bg-white/[0.05] hover:bg-white/[0.09] transition-colors text-white/50 hover:text-white/80 text-[10px] font-semibold border border-white/[0.07]"
          >
            <span className="flex items-center gap-1.5">
              <Navigation size={11} />
              How to travel — Step by step
            </span>
            {showSteps ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
          </button>

          <AnimatePresence>
            {showSteps && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-3 overflow-hidden"
              >
                {steps.map((step, si) => (
                  <StepCard key={si} step={step} isLast={si === steps.length - 1} />
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}
    </motion.div>
  );
}

// Note: TrustBadge and RiskIndicator are imported and used in the RouteCard below.
// The existing export default RouteCard already handles trust_score and risk via props.