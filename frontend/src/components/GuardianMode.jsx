/**
 * GuardianMode.jsx — Live safety simulation with dramatic, visible alerts.
 */

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, ShieldAlert, MapPin, Phone, Activity, X, Navigation, Clock, CheckCircle, AlertTriangle, Siren } from 'lucide-react';

const TOKEN = () => localStorage.getItem('commuteiq_token');

function simulateMovement(waypoints, progress) {
  if (!waypoints || waypoints.length < 2) return null;
  const idx = Math.min(Math.floor(progress * (waypoints.length - 1)), waypoints.length - 2);
  const t = (progress * (waypoints.length - 1)) - idx;
  const a = waypoints[idx], b = waypoints[idx + 1];
  return { lat: a[0] + (b[0] - a[0]) * t, lng: a[1] + (b[1] - a[1]) * t };
}

// Scripted demo — fires at exact tick counts
const SCRIPT = [
  {
    at: 5,
    type: 'status',
    icon: '✅',
    color: '#10b981',
    title: 'Journey Started',
    body: 'Guardian is monitoring your route. GPS locked. Stay safe!',
    level: 'OK',
  },
  {
    at: 14,
    type: 'inactive',
    icon: '⚠️',
    color: '#f59e0b',
    title: 'You stopped moving!',
    body: "You've been inactive for 2 minutes. Are you okay? Tap 'I'm Safe' to confirm.",
    level: 'WARNING',
    action: 'CONFIRM',
    contactAlert: null,
  },
  {
    at: 26,
    type: 'deviation',
    icon: '🗺️',
    color: '#f97316',
    title: 'Route Deviation Detected',
    body: "You've moved off the recommended safe path. Recalculating a safer route back.",
    level: 'WARNING',
    action: null,
    contactAlert: null,
  },
  {
    at: 38,
    type: 'risk_spike',
    icon: '🚨',
    color: '#ef4444',
    title: 'Safety Alert — High Risk Ahead',
    body: 'Area ahead has elevated risk right now. An alternate route has been found — only 4 min longer but significantly safer.',
    level: 'DANGER',
    action: 'REROUTE',
    contactAlert: '📱 Alerting trusted contact: Mom',
  },
  {
    at: 52,
    type: 'status',
    icon: '✅',
    color: '#10b981',
    title: 'Back on Safe Route',
    body: 'You are back on the safe path. All clear ahead.',
    level: 'OK',
    contactAlert: null,
  },
];

export default function GuardianMode({ selectedRoute, userMode }) {
  const [active, setActive]             = useState(false);
  const [progress, setProgress]         = useState(0);
  const [tick, setTick]                 = useState(0);
  const [currentAlert, setCurrentAlert] = useState(null);
  const [log, setLog]                   = useState([]);
  const [contactMsg, setContactMsg]     = useState(null);
  const [confirmed, setConfirmed]       = useState(false);
  const [done, setDone]                 = useState(false);

  const intervalRef = useRef(null);
  const scriptIdx   = useRef(0);
  const waypoints   = selectedRoute?.waypoints || [];

  const start = () => {
    setActive(true); setProgress(0); setTick(0);
    setCurrentAlert(null); setLog([]); setContactMsg(null);
    setConfirmed(false); setDone(false);
    scriptIdx.current = 0;

    intervalRef.current = setInterval(() => {
      setTick(t => {
        const next = t + 1;
        setProgress(p => Math.min(p + 0.016, 1));

        // Fire scripted event?
        const ev = SCRIPT[scriptIdx.current];
        if (ev && next >= ev.at) {
          setCurrentAlert(ev);
          setConfirmed(false);
          setLog(l => [{ ...ev, time: new Date().toLocaleTimeString() }, ...l.slice(0, 6)]);
          if (ev.contactAlert) {
            setContactMsg(ev.contactAlert);
            setTimeout(() => setContactMsg(null), 5000);
          }
          scriptIdx.current += 1;
        }

        if (next >= 65) {
          clearInterval(intervalRef.current);
          setActive(false); setDone(true);
        }
        return next;
      });
    }, 900);
  };

  const stop = () => {
    clearInterval(intervalRef.current);
    setActive(false); setProgress(0); setTick(0);
    setCurrentAlert(null); scriptIdx.current = 0;
  };

  useEffect(() => () => clearInterval(intervalRef.current), []);

  const glowColor = currentAlert?.color || (active ? '#10b981' : '#7c3aed');
  const isDanger  = currentAlert?.level === 'DANGER';
  const isWarning = currentAlert?.level === 'WARNING';

  return (
    <div className="flex flex-col gap-3">

      {/* ── FULL-SCREEN DANGER OVERLAY ──────────────────────────────── */}
      <AnimatePresence>
        {isDanger && !confirmed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[9999] flex items-center justify-center p-6"
            style={{ background: 'rgba(5,5,26,0.92)', backdropFilter: 'blur(8px)' }}
          >
            <motion.div
              initial={{ scale: 0.85, y: 30 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.85, y: 30 }}
              className="w-full max-w-sm rounded-3xl p-6 border-2 border-red-500/60"
              style={{
                background: 'linear-gradient(135deg, #1a0505 0%, #0f0f35 100%)',
                boxShadow: '0 0 60px rgba(239,68,68,0.4)',
              }}
            >
              {/* Flashing siren */}
              <motion.div
                animate={{ scale: [1, 1.1, 1], opacity: [1, 0.7, 1] }}
                transition={{ repeat: Infinity, duration: 0.8 }}
                className="w-16 h-16 rounded-full bg-red-500/20 border-2 border-red-500/50 flex items-center justify-center mx-auto mb-4"
              >
                <span className="text-4xl">🚨</span>
              </motion.div>

              <h2 className="text-red-400 font-black text-xl text-center mb-2">
                {currentAlert.title}
              </h2>
              <p className="text-white/60 text-sm text-center leading-relaxed mb-5">
                {currentAlert.body}
              </p>

              {contactMsg && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-blue-500/15 border border-blue-500/30 rounded-xl px-4 py-2.5 flex items-center gap-2 mb-4"
                >
                  <Phone size={14} className="text-blue-400" />
                  <span className="text-blue-300 text-sm font-semibold">{contactMsg}</span>
                </motion.div>
              )}

              <div className="flex gap-3">
                <motion.button
                  whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.96 }}
                  onClick={() => { setConfirmed(true); setCurrentAlert(null); }}
                  className="flex-1 bg-red-500/20 border border-red-500/40 text-red-300 font-bold py-3 rounded-2xl text-sm"
                >
                  Take Alternate Route
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.96 }}
                  onClick={() => { setConfirmed(true); setCurrentAlert(null); }}
                  className="flex-1 bg-white/[0.06] border border-white/10 text-white/60 font-bold py-3 rounded-2xl text-sm"
                >
                  Stay on Route
                </motion.button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── WARNING BANNER ───────────────────────────────────────────── */}
      <AnimatePresence>
        {isWarning && !confirmed && (
          <motion.div
            initial={{ opacity: 0, y: -12, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -12 }}
            className="rounded-2xl p-4 border-2"
            style={{
              background: `${currentAlert.color}12`,
              borderColor: `${currentAlert.color}50`,
              boxShadow: `0 0 24px ${currentAlert.color}25`,
            }}
          >
            <div className="flex items-start gap-3">
              <motion.span
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ repeat: 4, duration: 0.5 }}
                className="text-2xl leading-none"
              >
                {currentAlert.icon}
              </motion.span>
              <div className="flex-1">
                <div className="font-bold text-white text-sm mb-1">{currentAlert.title}</div>
                <p className="text-white/55 text-[11px] leading-relaxed">{currentAlert.body}</p>
                {currentAlert.action === 'CONFIRM' && (
                  <motion.button
                    whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.96 }}
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 }}
                    onClick={() => { setConfirmed(true); setCurrentAlert(null); }}
                    className="mt-2.5 flex items-center gap-1.5 bg-green-500/20 border border-green-500/35 text-green-300 text-xs font-bold px-4 py-2 rounded-xl"
                  >
                    <CheckCircle size={12} /> I'm Safe — Continue
                  </motion.button>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── CONTACT NOTIFICATION (outside overlay) ──────────────────── */}
      <AnimatePresence>
        {contactMsg && !isDanger && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="bg-blue-500/15 border border-blue-500/30 rounded-xl px-3 py-2.5 flex items-center gap-2"
          >
            <Phone size={13} className="text-blue-400 flex-shrink-0" />
            <span className="text-blue-300 text-[11px] font-semibold">{contactMsg}</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── MAIN GUARDIAN CARD ──────────────────────────────────────── */}
      <motion.div
        animate={{
          borderColor: active
            ? isDanger ? '#ef444460' : isWarning ? '#f59e0b50' : '#10b98140'
            : 'rgba(255,255,255,0.07)',
          backgroundColor: active
            ? isDanger ? 'rgba(239,68,68,0.06)' : isWarning ? 'rgba(245,158,11,0.05)' : 'rgba(16,185,129,0.05)'
            : 'rgba(255,255,255,0.03)',
        }}
        className="rounded-2xl p-4 border transition-colors duration-700"
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2.5">
            <motion.div
              animate={active ? { scale: [1, 1.12, 1] } : {}}
              transition={{ repeat: Infinity, duration: 2 }}
              className="w-8 h-8 rounded-xl flex items-center justify-center"
              style={{
                background: `${glowColor}20`,
                border: `1.5px solid ${glowColor}45`,
                boxShadow: active ? `0 0 14px ${glowColor}30` : 'none',
              }}
            >
              {isDanger
                ? <ShieldAlert size={16} className="text-red-400" />
                : <Shield size={16} style={{ color: glowColor }} />
              }
            </motion.div>
            <div>
              <div className="text-white font-bold text-sm leading-tight">Guardian Mode</div>
              <div className="text-[9px] text-white/30 uppercase tracking-wider">AI Safety Monitor</div>
            </div>
          </div>
          {active && (
            <div className="flex items-center gap-1.5 bg-green-500/15 border border-green-500/25 rounded-full px-2.5 py-1">
              <motion.div
                animate={{ opacity: [1, 0.2, 1] }}
                transition={{ repeat: Infinity, duration: 1 }}
                className="w-1.5 h-1.5 rounded-full bg-green-400"
              />
              <span className="text-[9px] text-green-400 font-bold">MONITORING</span>
            </div>
          )}
        </div>

        {/* What Guardian does — shown before starting */}
        {!active && !done && (
          <div className="mb-3 space-y-1.5">
            {[
              { icon: '📍', text: 'Tracks your live simulated GPS location' },
              { icon: '😴', text: 'Alerts if you stop moving for 2+ minutes' },
              { icon: '🗺️', text: 'Detects if you leave the safe route' },
              { icon: '🚨', text: 'Warns of risk spikes with alternate route' },
              { icon: '📱', text: 'Notifies trusted contact in emergencies' },
            ].map((item, i) => (
              <div key={i} className="flex items-center gap-2 text-[10px] text-white/40">
                <span>{item.icon}</span>
                <span>{item.text}</span>
              </div>
            ))}
          </div>
        )}

        {/* Progress bar — shown when active */}
        {active && (
          <div className="mb-3">
            <div className="flex justify-between text-[9px] text-white/30 mb-1.5">
              <span className="flex items-center gap-1">
                <Navigation size={8} />{selectedRoute?.source?.name || 'Start'}
              </span>
              <span className="font-semibold" style={{ color: glowColor }}>
                {Math.round(progress * 100)}%
              </span>
              <span className="flex items-center gap-1">
                <MapPin size={8} />{selectedRoute?.destination?.name || 'End'}
              </span>
            </div>
            <div className="relative h-2.5 bg-white/[0.06] rounded-full overflow-visible">
              <motion.div
                className="h-full rounded-full"
                style={{ width: `${progress * 100}%`, backgroundColor: glowColor, boxShadow: `0 0 8px ${glowColor}60` }}
              />
              {/* Moving dot */}
              <motion.div
                className="absolute top-1/2 -translate-y-1/2 w-4 h-4 rounded-full border-2 border-white shadow-lg"
                style={{ left: `calc(${progress * 100}% - 8px)`, backgroundColor: glowColor, boxShadow: `0 0 12px ${glowColor}` }}
              />
            </div>
            <div className="flex items-center gap-3 mt-2">
              <div className="flex items-center gap-1 text-[9px] text-white/30">
                <Clock size={9} />{tick}s elapsed
              </div>
              <div className="flex items-center gap-1 text-[9px] text-white/30">
                <Activity size={9} />
                {simulateMovement(waypoints, progress)
                  ? `${simulateMovement(waypoints, progress).lat.toFixed(4)}, ${simulateMovement(waypoints, progress).lng.toFixed(4)}`
                  : 'GPS tracking...'}
              </div>
            </div>
          </div>
        )}

        {/* Done state */}
        {done && (
          <div className="mb-3 bg-green-500/10 border border-green-500/25 rounded-xl px-3 py-2.5 flex items-center gap-2">
            <CheckCircle size={14} className="text-green-400" />
            <span className="text-green-300 text-sm font-semibold">Journey Complete — You arrived safely! 🎉</span>
          </div>
        )}

        {/* Start / Stop Button */}
        <motion.button
          whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
          onClick={active ? stop : start}
          disabled={!selectedRoute}
          className="w-full font-bold py-3 rounded-xl flex items-center justify-center gap-2 text-sm border transition-all disabled:opacity-40 disabled:cursor-not-allowed"
          style={active ? {
            background: 'rgba(239,68,68,0.15)',
            borderColor: 'rgba(239,68,68,0.35)',
            color: '#fca5a5',
          } : {
            background: 'linear-gradient(135deg, rgba(124,58,237,0.35), rgba(109,40,217,0.35))',
            borderColor: 'rgba(124,58,237,0.5)',
            color: '#c4b5fd',
            boxShadow: '0 0 20px rgba(124,58,237,0.2)',
          }}
        >
          {active
            ? <><X size={14} />End Journey</>
            : <><Shield size={14} />Start Safe Journey</>
          }
        </motion.button>
      </motion.div>

      {/* ── JOURNEY LOG ─────────────────────────────────────────────── */}
      <AnimatePresence>
        {log.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="bg-white/[0.02] border border-white/[0.06] rounded-2xl p-3 overflow-hidden"
          >
            <div className="text-[9px] font-bold text-white/25 uppercase tracking-widest mb-2">Journey Log</div>
            <div className="space-y-2">
              {log.map((entry, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-start gap-2 pb-2 border-b border-white/[0.04] last:border-0 last:pb-0"
                >
                  <span className="text-base leading-none mt-0.5">{entry.icon}</span>
                  <div className="flex-1 min-w-0">
                    <div className="text-[10px] font-semibold text-white/70">{entry.title}</div>
                    <div className="text-[9px] text-white/30 mt-0.5 truncate">{entry.body}</div>
                  </div>
                  <span className="text-[8px] text-white/20 flex-shrink-0">{entry.time}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}