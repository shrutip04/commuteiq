/**
 * SafetyMonitor.jsx — Automatic background safety check with countdown auto-trigger.
 * Polls /live_safety_check every 8s during active journey.
 * If alert fires and user doesn't respond in 10s → auto-triggers emergency.
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, ShieldAlert, CheckCircle, AlertTriangle, Loader } from 'lucide-react';

const TOKEN   = () => localStorage.getItem('commuteiq_token');
const BASE    = 'http://localhost:5000/api';
const POLL_MS = 8000;   // Check every 8 seconds
const AUTO_TRIGGER_SECS = 10;

async function apiGet(path) {
  const res = await fetch(BASE + path, {
    headers: { Authorization: `Bearer ${TOKEN()}` },
  });
  return res.json();
}
async function apiPost(path, body) {
  const res = await fetch(BASE + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${TOKEN()}` },
    body: JSON.stringify(body),
  });
  return res.json();
}

export default function SafetyMonitor({ active, selectedRoute, userMode, riskScore }) {
  const [alert, setAlert]           = useState(null);
  const [countdown, setCountdown]   = useState(null);
  const [triggered, setTriggered]   = useState(false);
  const [dismissed, setDismissed]   = useState(false);
  const [triggering, setTriggering] = useState(false);

  const pollRef      = useRef(null);
  const countdownRef = useRef(null);
  const alertRef     = useRef(null);

  // ── Trigger emergency ─────────────────────────────────────────────────────
  const triggerEmergency = useCallback(async (reason) => {
    if (triggered || triggering) return;
    setTriggering(true);
    clearInterval(countdownRef.current);
    const location = selectedRoute
      ? { lat: selectedRoute.source?.lat || 19.076, lng: selectedRoute.source?.lng || 72.877 }
      : { lat: 19.076, lng: 72.877 };
    try {
      await apiPost('/trigger_emergency', {
        location,
        risk_score: riskScore || 0.8,
        reason,
      });
      setTriggered(true);
      setCountdown(null);
    } catch (e) {
      console.error('[SafetyMonitor]', e);
    } finally {
      setTriggering(false);
    }
  }, [triggered, triggering, selectedRoute, riskScore]);

  // ── Start countdown → auto-trigger ────────────────────────────────────────
  const startCountdown = useCallback((reason) => {
    setCountdown(AUTO_TRIGGER_SECS);
    let secs = AUTO_TRIGGER_SECS;
    countdownRef.current = setInterval(() => {
      secs -= 1;
      setCountdown(secs);
      if (secs <= 0) {
        clearInterval(countdownRef.current);
        triggerEmergency(reason);
      }
    }, 1000);
  }, [triggerEmergency]);

  // ── Poll live_safety_check ─────────────────────────────────────────────────
  const poll = useCallback(async () => {
    if (alertRef.current) return;  // Don't poll while alert is showing
    try {
      const r = await apiGet(
        `/live_safety_check?user_mode=${userMode}&risk_score=${riskScore || ''}`
      );
      const data = r.data;
      if (data?.alert) {
        alertRef.current = data;
        setAlert(data);
        setDismissed(false);
        startCountdown(data.reason);
      }
    } catch (e) {}
  }, [userMode, riskScore, startCountdown]);

  // ── Start/stop polling based on active state ──────────────────────────────
  useEffect(() => {
    if (active) {
      pollRef.current = setInterval(poll, POLL_MS);
      return () => {
        clearInterval(pollRef.current);
        clearInterval(countdownRef.current);
      };
    } else {
      clearInterval(pollRef.current);
      clearInterval(countdownRef.current);
      setAlert(null);
      setCountdown(null);
      setTriggered(false);
      setDismissed(false);
      alertRef.current = null;
    }
  }, [active, poll]);

  const handleSafe = () => {
    clearInterval(countdownRef.current);
    setAlert(null);
    setCountdown(null);
    setDismissed(true);
    alertRef.current = null;
    setTimeout(() => setDismissed(false), 3000);
  };

  const handleNeedHelp = () => {
    clearInterval(countdownRef.current);
    triggerEmergency(alert?.reason || 'User requested help');
  };

  if (!active) return null;

  return (
    <>
      {/* ── Status badge (always shown when monitoring) ──────────────────── */}
      <AnimatePresence>
        {!alert && !triggered && (
          <motion.div
            initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
            className="fixed bottom-24 right-6 z-[9990] flex items-center gap-2 bg-black/70 backdrop-blur-md border border-green-500/25 rounded-full px-3 py-1.5 pointer-events-none"
          >
            <motion.div animate={{ opacity: [1, 0.3, 1] }} transition={{ repeat: Infinity, duration: 1.5 }}
              className="w-1.5 h-1.5 rounded-full bg-green-400" />
            <Shield size={11} className="text-green-400" />
            <span className="text-green-400 text-[10px] font-semibold">Monitoring active</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── "You're safe" confirmation ───────────────────────────────────── */}
      <AnimatePresence>
        {dismissed && (
          <motion.div
            initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
            className="fixed bottom-24 right-6 z-[9990] flex items-center gap-2 bg-green-500/15 border border-green-500/30 rounded-full px-3 py-1.5 pointer-events-none"
          >
            <CheckCircle size={11} className="text-green-400" />
            <span className="text-green-300 text-[10px] font-semibold">Stay safe! ✅</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── ALERT POPUP ─────────────────────────────────────────────────────── */}
      <AnimatePresence>
        {alert && !triggered && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[9995] flex items-center justify-center p-6"
            style={{ background: 'rgba(5,5,26,0.85)', backdropFilter: 'blur(8px)' }}
          >
            <motion.div
              initial={{ scale: 0.88, y: 24 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.88 }}
              className="w-full max-w-xs rounded-3xl overflow-hidden shadow-2xl"
              style={{
                background: 'linear-gradient(160deg, #1a0a0a 0%, #0f0f35 100%)',
                border: `1px solid ${alert.severity === 'HIGH' ? 'rgba(239,68,68,0.5)' : 'rgba(245,158,11,0.4)'}`,
                boxShadow: `0 0 40px ${alert.severity === 'HIGH' ? 'rgba(239,68,68,0.2)' : 'rgba(245,158,11,0.15)'}`,
              }}
            >
              {/* Warning icon */}
              <div className="flex flex-col items-center pt-7 pb-4 px-5">
                <motion.div
                  animate={{ scale: [1, 1.12, 1] }}
                  transition={{ repeat: Infinity, duration: 1 }}
                  className="w-16 h-16 rounded-full flex items-center justify-center mb-3"
                  style={{
                    background: alert.severity === 'HIGH' ? 'rgba(239,68,68,0.15)' : 'rgba(245,158,11,0.15)',
                    border: `2px solid ${alert.severity === 'HIGH' ? 'rgba(239,68,68,0.4)' : 'rgba(245,158,11,0.4)'}`,
                  }}
                >
                  <AlertTriangle size={30} style={{
                    color: alert.severity === 'HIGH' ? '#ef4444' : '#f59e0b'
                  }} />
                </motion.div>

                <h2 className="text-white font-black text-lg text-center mb-1">
                  Are you safe?
                </h2>
                <p className="text-white/50 text-xs text-center leading-relaxed mb-1">
                  {alert.message}
                </p>

                {/* Countdown bar */}
                {countdown !== null && (
                  <div className="w-full mt-3">
                    <div className="flex justify-between text-[9px] text-white/30 mb-1">
                      <span>Auto-alerting contacts in…</span>
                      <span className="font-bold text-red-400">{countdown}s</span>
                    </div>
                    <div className="h-1 bg-white/[0.08] rounded-full overflow-hidden">
                      <motion.div
                        className="h-full bg-red-500 rounded-full"
                        style={{ width: `${(countdown / AUTO_TRIGGER_SECS) * 100}%` }}
                        transition={{ duration: 0.9 }}
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* Action buttons */}
              <div className="grid grid-cols-2 gap-2 px-5 pb-5">
                <motion.button
                  whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.96 }}
                  onClick={handleSafe}
                  className="py-3 rounded-2xl font-bold text-sm text-green-300 border border-green-500/30 bg-green-500/15 hover:bg-green-500/25 transition-all"
                >
                  ✅ I'm Safe
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.96 }}
                  onClick={handleNeedHelp}
                  disabled={triggering}
                  className="py-3 rounded-2xl font-bold text-sm text-red-200 border border-red-500/40 bg-red-500/20 hover:bg-red-500/30 transition-all disabled:opacity-60 flex items-center justify-center gap-1.5"
                >
                  {triggering
                    ? <><Loader size={12} className="animate-spin" />Sending…</>
                    : '🆘 Need Help'
                  }
                </motion.button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── TRIGGERED SUCCESS TOAST ──────────────────────────────────────────── */}
      <AnimatePresence>
        {triggered && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="fixed bottom-24 right-6 z-[9990] bg-red-500/15 border border-red-500/30 rounded-2xl p-3 max-w-[200px]"
          >
            <div className="flex items-center gap-2 mb-1">
              <motion.div animate={{ opacity: [1, 0.2, 1] }} transition={{ repeat: Infinity, duration: 0.8 }}
                className="w-2 h-2 rounded-full bg-red-400" />
              <span className="text-red-300 text-[11px] font-bold">SOS ACTIVE</span>
            </div>
            <p className="text-white/40 text-[10px]">Contacts alerted · Location shared · Recording on</p>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}