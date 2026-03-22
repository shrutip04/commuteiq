/**
 * LiveMonitor.jsx — Live journey monitoring with real-time alerts.
 */

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, Square, Bell, CheckCircle, AlertTriangle } from 'lucide-react';

export default function LiveMonitor({ selectedRoute }) {
  const [active, setActive]   = useState(false);
  const [alert, setAlert]     = useState(null);
  const [checks, setChecks]   = useState(0);
  const intervalRef           = useRef(null);
  const token = localStorage.getItem('commuteiq_token');

  const startMonitor = () => {
    setActive(true);
    setAlert(null);
    setChecks(0);
    intervalRef.current = setInterval(async () => {
      try {
        const res = await fetch('http://localhost:5000/api/live_monitor', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const json = await res.json();
        setAlert(json.data);
        setChecks(c => c + 1);
      } catch (e) {
        console.error(e);
      }
    }, 6000);
  };

  const stopMonitor = () => {
    setActive(false);
    clearInterval(intervalRef.current);
    setAlert(null);
    setChecks(0);
  };

  useEffect(() => () => clearInterval(intervalRef.current), []);

  return (
    <div className="bg-white/[0.03] border border-white/[0.07] rounded-2xl p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className={`w-6 h-6 rounded-lg flex items-center justify-center border ${
            active
              ? 'bg-green-500/20 border-green-500/30'
              : 'bg-white/[0.05] border-white/10'
          }`}>
            <Bell size={12} className={active ? 'text-green-400' : 'text-white/30'} />
          </div>
          <span className="text-white/60 text-xs font-semibold uppercase tracking-wider">
            Live Monitor
          </span>
          {active && (
            <div className="flex items-center gap-1">
              <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
              <span className="text-[9px] text-green-400 font-medium">LIVE</span>
            </div>
          )}
        </div>
        {checks > 0 && (
          <span className="text-[9px] text-white/20">{checks} check{checks > 1 ? 's' : ''}</span>
        )}
      </div>

      <p className="text-white/30 text-[10px] mb-3 leading-relaxed">
        Monitor your journey in real-time. Get instant alerts if conditions change.
      </p>

      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.97 }}
        onClick={active ? stopMonitor : startMonitor}
        disabled={!selectedRoute}
        className={`w-full font-semibold py-2.5 rounded-xl flex items-center justify-center gap-2 transition-all text-sm border disabled:opacity-40 disabled:cursor-not-allowed ${
          active
            ? 'bg-red-500/20 border-red-500/30 text-red-300 hover:bg-red-500/30'
            : 'bg-green-500/20 border-green-500/30 text-green-300 hover:bg-green-500/30'
        }`}
      >
        {active
          ? <><Square size={13} />Stop Monitoring</>
          : <><Play size={13} />Start Journey</>
        }
      </motion.button>

      <AnimatePresence>
        {alert && (
          <motion.div
            key={alert.message}
            initial={{ opacity: 0, y: 8, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.97 }}
            className={`mt-3 rounded-xl p-3 border ${
              alert.alert
                ? 'bg-orange-500/10 border-orange-500/25'
                : 'bg-green-500/10 border-green-500/25'
            }`}
          >
            <div className="flex items-start gap-2">
              {alert.alert
                ? <AlertTriangle size={13} className="text-orange-400 flex-shrink-0 mt-0.5" />
                : <CheckCircle size={13} className="text-green-400 flex-shrink-0 mt-0.5" />
              }
              <div>
                <p className={`text-[11px] font-medium leading-relaxed ${
                  alert.alert ? 'text-orange-300' : 'text-green-300'
                }`}>
                  {alert.message}
                </p>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`text-[9px] font-bold uppercase px-1.5 py-0.5 rounded-full border ${
                    alert.risk_level === 'HIGH'
                      ? 'bg-red-500/20 border-red-500/30 text-red-400'
                      : alert.risk_level === 'MEDIUM'
                      ? 'bg-orange-500/20 border-orange-500/30 text-orange-400'
                      : 'bg-green-500/20 border-green-500/30 text-green-400'
                  }`}>
                    {alert.risk_level}
                  </span>
                  <span className="text-[9px] text-white/20">
                    {new Date(alert.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}