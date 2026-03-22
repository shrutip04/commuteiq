/**
 * EmergencyModal.jsx — Emergency response modal with contacts, calls, recording.
 */

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Phone, Mic, MapPin, UserPlus, Trash2, CheckCircle, AlertTriangle, Loader } from 'lucide-react';

const TOKEN = () => localStorage.getItem('commuteiq_token');
const BASE  = 'http://localhost:5000/api';

async function api(method, path, body) {
  const res = await fetch(BASE + path, {
    method,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${TOKEN()}` },
    body: body ? JSON.stringify(body) : undefined,
  });
  return res.json();
}

const SERVICES = [
  { label: 'Police',       icon: '👮', number: '100', color: '#3b82f6' },
  { label: 'Ambulance',    icon: '🚑', number: '102', color: '#10b981' },
  { label: 'Women Helpline', icon: '🛡️', number: '1091', color: '#8b5cf6' },
  { label: 'Emergency',    icon: '🆘', number: '112', color: '#ef4444' },
];

export default function EmergencyModal({ onClose, selectedRoute, userMode }) {
  const [phase, setPhase]           = useState('main');  // main | contacts | triggered
  const [contacts, setContacts]     = useState([]);
  const [recording, setRecording]   = useState(false);
  const [tracking, setTracking]     = useState(false);
  const [sending, setSending]       = useState(false);
  const [result, setResult]         = useState(null);
  const [newName, setNewName]       = useState('');
  const [newPhone, setNewPhone]     = useState('');
  const [addingContact, setAdding]  = useState(false);

  // Load contacts on mount
  useEffect(() => {
    api('GET', '/emergency_contacts').then(r => {
      if (r.data?.contacts) setContacts(r.data.contacts);
    }).catch(() => {});
  }, []);

  const handleTrigger = async () => {
    setSending(true);
    const location = selectedRoute
      ? { lat: selectedRoute.source?.lat || 19.076, lng: selectedRoute.source?.lng || 72.877 }
      : { lat: 19.076, lng: 72.877 };
    try {
      const r = await api('POST', '/trigger_emergency', {
        location,
        risk_score: 0.85,
        reason: 'Manual SOS triggered by user',
      });
      setResult(r.data);
      setRecording(true);
      setTracking(true);
      setPhase('triggered');
    } catch (e) {
      console.error(e);
    } finally {
      setSending(false);
    }
  };

  const handleAddContact = async () => {
    if (!newName.trim() || !newPhone.trim()) return;
    setAdding(true);
    try {
      const r = await api('POST', '/emergency_contacts', {
        name: newName.trim(), phone: newPhone.trim(), type: 'personal'
      });
      if (r.data?.contact) {
        setContacts(c => [...c, r.data.contact]);
        setNewName(''); setNewPhone('');
      }
    } finally { setAdding(false); }
  };

  const handleDeleteContact = async (id) => {
    await api('DELETE', `/emergency_contacts/${id}`);
    setContacts(c => c.filter(x => x.id !== id));
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[9999] flex items-center justify-center p-4"
      style={{ background: 'rgba(5,5,26,0.88)', backdropFilter: 'blur(10px)' }}
      onClick={e => { if (e.target === e.currentTarget) onClose(); }}
    >
      <motion.div
        initial={{ scale: 0.92, y: 24 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.92, y: 24 }}
        className="w-full max-w-sm rounded-3xl overflow-hidden shadow-2xl"
        style={{ background: 'linear-gradient(160deg, #0f0f35 0%, #0a0a28 100%)', border: '1px solid rgba(239,68,68,0.3)' }}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-white/[0.07]">
          <div className="flex items-center gap-2.5">
            <motion.div
              animate={{ scale: [1, 1.15, 1] }}
              transition={{ repeat: Infinity, duration: 1.5 }}
              className="w-8 h-8 rounded-full bg-red-500/20 border border-red-500/40 flex items-center justify-center"
            >
              <span className="text-lg">🆘</span>
            </motion.div>
            <div>
              <div className="text-white font-black text-base">Emergency SOS</div>
              <div className="text-red-400/70 text-[10px] uppercase tracking-wider">Safety Response</div>
            </div>
          </div>
          <button onClick={onClose} className="w-8 h-8 rounded-full bg-white/[0.06] flex items-center justify-center text-white/40 hover:text-white/80 transition-colors">
            <X size={14} />
          </button>
        </div>

        <AnimatePresence mode="wait">

          {/* ── MAIN PHASE ─────────────────────────────────────────── */}
          {phase === 'main' && (
            <motion.div key="main" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="p-5 space-y-4">

              {/* Emergency services grid */}
              <div>
                <p className="text-[10px] text-white/30 uppercase tracking-wider mb-2.5 font-semibold">Call Emergency Services</p>
                <div className="grid grid-cols-2 gap-2">
                  {SERVICES.map(svc => (
                    <motion.a
                      key={svc.number}
                      href={`tel:${svc.number}`}
                      whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.96 }}
                      className="flex items-center gap-2.5 px-3 py-3 rounded-2xl border transition-all"
                      style={{ background: `${svc.color}12`, borderColor: `${svc.color}35` }}
                    >
                      <span className="text-xl leading-none">{svc.icon}</span>
                      <div>
                        <div className="text-white font-semibold text-xs">{svc.label}</div>
                        <div className="font-black text-sm" style={{ color: svc.color }}>{svc.number}</div>
                      </div>
                    </motion.a>
                  ))}
                </div>
              </div>

              {/* Contacts count */}
              <button
                onClick={() => setPhase('contacts')}
                className="w-full flex items-center justify-between px-4 py-3 bg-white/[0.04] border border-white/[0.08] rounded-2xl hover:bg-white/[0.07] transition-all"
              >
                <div className="flex items-center gap-2">
                  <span className="text-lg">👥</span>
                  <span className="text-white/70 text-sm font-medium">Alert My Contacts</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] bg-violet-600/40 border border-violet-500/30 text-violet-300 rounded-full px-2 py-0.5 font-bold">
                    {contacts.length} saved
                  </span>
                  <span className="text-white/20">›</span>
                </div>
              </button>

              {/* SOS button */}
              <motion.button
                whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
                onClick={handleTrigger}
                disabled={sending}
                className="w-full py-4 rounded-2xl font-black text-white text-base flex items-center justify-center gap-2.5 disabled:opacity-60"
                style={{
                  background: 'linear-gradient(135deg, #ef4444, #dc2626)',
                  boxShadow: '0 8px 32px rgba(239,68,68,0.35)',
                }}
              >
                {sending
                  ? <><Loader size={16} className="animate-spin" />Alerting…</>
                  : <><AlertTriangle size={16} />Send SOS Alert Now</>
                }
              </motion.button>

              <p className="text-[10px] text-white/20 text-center leading-relaxed">
                This will alert your saved contacts with your location and start live tracking.
              </p>
            </motion.div>
          )}

          {/* ── CONTACTS PHASE ──────────────────────────────────────── */}
          {phase === 'contacts' && (
            <motion.div key="contacts" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0 }} className="p-5">
              <button onClick={() => setPhase('main')} className="text-white/30 text-xs flex items-center gap-1 mb-4 hover:text-white/60">
                ← Back
              </button>

              <p className="text-[10px] text-white/30 uppercase tracking-wider mb-3 font-semibold">Saved Contacts</p>

              {contacts.length === 0 && (
                <div className="text-center py-4 text-white/20 text-xs">No contacts saved yet</div>
              )}

              <div className="space-y-2 mb-4">
                {contacts.map(c => (
                  <div key={c.id} className="flex items-center gap-3 bg-white/[0.04] border border-white/[0.07] rounded-xl px-3 py-2.5">
                    <span className="text-lg">{c.type === 'personal' ? '👤' : '📞'}</span>
                    <div className="flex-1">
                      <div className="text-white text-sm font-semibold">{c.name}</div>
                      <div className="text-white/40 text-[10px]">{c.phone}</div>
                    </div>
                    <button onClick={() => handleDeleteContact(c.id)}
                      className="w-6 h-6 rounded-lg flex items-center justify-center text-white/20 hover:text-red-400 hover:bg-red-500/10 transition-all">
                      <Trash2 size={11} />
                    </button>
                  </div>
                ))}
              </div>

              {/* Add contact */}
              <div className="border-t border-white/[0.06] pt-3 space-y-2">
                <p className="text-[10px] text-white/30 uppercase tracking-wider font-semibold">Add Contact</p>
                <input value={newName} onChange={e => setNewName(e.target.value)}
                  placeholder="Name (e.g. Mom)"
                  className="w-full bg-white/[0.05] border border-white/[0.09] rounded-xl px-3 py-2 text-white text-sm placeholder-white/20 focus:outline-none focus:border-violet-500/50"
                />
                <input value={newPhone} onChange={e => setNewPhone(e.target.value)}
                  placeholder="Phone number"
                  className="w-full bg-white/[0.05] border border-white/[0.09] rounded-xl px-3 py-2 text-white text-sm placeholder-white/20 focus:outline-none focus:border-violet-500/50"
                />
                <motion.button
                  whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
                  onClick={handleAddContact} disabled={addingContact || !newName || !newPhone}
                  className="w-full bg-violet-600/30 border border-violet-500/30 text-violet-300 font-semibold py-2.5 rounded-xl flex items-center justify-center gap-2 text-sm disabled:opacity-40"
                >
                  {addingContact
                    ? <Loader size={13} className="animate-spin" />
                    : <><UserPlus size={13} />Save Contact</>
                  }
                </motion.button>
              </div>
            </motion.div>
          )}

          {/* ── TRIGGERED PHASE ─────────────────────────────────────── */}
          {phase === 'triggered' && result && (
            <motion.div key="triggered" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              exit={{ opacity: 0 }} className="p-5 space-y-3">

              {/* Success header */}
              <div className="flex items-center gap-3 bg-red-500/10 border border-red-500/25 rounded-2xl px-4 py-3">
                <motion.div animate={{ scale: [1, 1.15, 1] }} transition={{ repeat: 3, duration: 0.5 }}>
                  <CheckCircle size={22} className="text-red-400" />
                </motion.div>
                <div>
                  <div className="text-white font-bold text-sm">SOS Activated</div>
                  <div className="text-red-400/70 text-[10px]">ID: {result.emergency_id}</div>
                </div>
              </div>

              {/* Contacts alerted */}
              <div className="bg-white/[0.03] border border-white/[0.07] rounded-2xl p-3">
                <div className="text-[10px] text-white/30 uppercase tracking-wider mb-2">Contacts Alerted</div>
                {result.contacts_alerted?.length > 0
                  ? result.contacts_alerted.map((c, i) => (
                      <div key={i} className="flex items-center gap-2 text-sm">
                        <div className={`w-1.5 h-1.5 rounded-full ${c.status === 'delivered' ? 'bg-green-400' : 'bg-red-400'}`} />
                        <span className="text-white/60">{c.name}</span>
                        <span className="text-white/25 text-[10px]">{c.status}</span>
                      </div>
                    ))
                  : <p className="text-white/25 text-xs">No personal contacts saved. Add contacts for future emergencies.</p>
                }
              </div>

              {/* Live indicators */}
              <div className="grid grid-cols-2 gap-2">
                <div className="bg-green-500/10 border border-green-500/25 rounded-xl p-3 flex items-center gap-2">
                  <motion.div animate={{ opacity: [1, 0.3, 1] }} transition={{ repeat: Infinity, duration: 1.2 }}
                    className="w-2 h-2 rounded-full bg-green-400" />
                  <div>
                    <div className="text-green-300 text-[11px] font-bold">Live Tracking</div>
                    <div className="text-green-400/50 text-[9px]">Location shared</div>
                  </div>
                </div>
                <div className="bg-red-500/10 border border-red-500/25 rounded-xl p-3 flex items-center gap-2">
                  <motion.div animate={{ scale: [1, 1.3, 1] }} transition={{ repeat: Infinity, duration: 0.8 }}
                    className="w-2 h-2 rounded-full bg-red-400" />
                  <div>
                    <div className="text-red-300 text-[11px] font-bold">🎙️ Recording</div>
                    <div className="text-red-400/50 text-[9px]">Audio active</div>
                  </div>
                </div>
              </div>

              {/* Maps link */}
              <a href={result.maps_url} target="_blank" rel="noreferrer"
                className="flex items-center gap-2 bg-blue-500/10 border border-blue-500/25 rounded-xl px-3 py-2.5 text-blue-300 text-xs font-medium hover:bg-blue-500/20 transition-all">
                <MapPin size={12} />
                View your location on Maps
              </a>

              <motion.button
                whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
                onClick={onClose}
                className="w-full bg-white/[0.06] border border-white/[0.1] text-white/70 font-semibold py-2.5 rounded-xl text-sm"
              >
                Close — Help is on the way
              </motion.button>
            </motion.div>
          )}

        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
}