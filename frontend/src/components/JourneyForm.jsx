/**
 * JourneyForm.jsx — Left panel form for entering journey parameters.
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MapPin, Clock, Sliders, ArrowRight, Navigation, RotateCcw } from 'lucide-react';

const MUMBAI_LOCATIONS = [
  // SOUTH MUMBAI
  'CST', 'CSMT', 'Chhatrapati Shivaji Terminus', 'Victoria Terminus',
  'Churchgate', 'Marine Lines', 'Charni Road', 'Grant Road',
  'Mumbai Central', 'Mahalaxmi', 'Lower Parel', 'Prabhadevi',
  'Elphinstone', 'Parel', 'Currey Road', 'Chinchpokli',
  'Byculla', 'Sandhurst Road', 'Masjid',

  // CENTRAL LINE
  'Dadar', 'Matunga', 'Sion', 'Kurla', 'Vidyavihar',
  'Ghatkopar', 'Vikhroli', 'Kanjurmarg', 'Bhandup',
  'Nahur', 'Mulund', 'Thane',

  // CENTRAL EXTENSION
  'Kalwa', 'Mumbra', 'Diva', 'Kopar',
  'Dombivli', 'Thakurli', 'Kalyan',

  // WESTERN LINE
  'Dadar West', 'Matunga Road', 'Mahim',
  'Bandra', 'Bandra West', 'Bandra East',
  'Khar', 'Santacruz', 'Vile Parle',
  'Andheri', 'Andheri West', 'Andheri East',
  'Jogeshwari', 'Goregaon', 'Malad',
  'Kandivali', 'Borivali', 'Dahisar',
  'Mira Road', 'Bhayandar', 'Naigaon',
  'Vasai Road', 'Virar',

  // HARBOUR LINE
  'Dockyard Road', 'Reay Road', 'Cotton Green',
  'Sewri', 'Wadala Road', 'GTB Nagar',
  'Guru Tegh Bahadur Nagar', 'Chunabhatti',
  'Tilak Nagar', 'Chembur', 'Govandi',
  'Mankhurd', 'Vashi',

  // NAVI MUMBAI
  'Sanpada', 'Juinagar', 'Nerul',
  'Seawoods', 'Seawoods Darave',
  'Belapur', 'CBD Belapur',
  'Kharghar', 'Mansarovar',
  'Khandeshwar', 'Panvel',

  // TRANS HARBOUR
  'Airoli', 'Rabale', 'Ghansoli',
  'Koparkhairane', 'Turbhe',

  // COMMON AREAS / LANDMARKS (for better UX search)
  'Colaba', 'Nariman Point', 'Fort',
  'Worli', 'Prabhadevi', 'Dharavi',
  'BKC', 'Bandra Kurla Complex',
  'Powai', 'Juhu', 'Versova',
  'Lokhandwala', 'Oshiwara',
  'Film City', 'Andheri MIDC',

  // NAVI MUMBAI GENERIC
  'Navi Mumbai'
];

const PREFERENCES = [
  { value: 'fastest', label: 'Fastest Route', icon: '⚡' },
  { value: 'least_crowded', label: 'Least Crowded', icon: '🌿' },
  { value: 'balanced', label: 'Balanced', icon: '⚖️' },
];

export default function JourneyForm({ onSubmit, loading }) {
  const [form, setForm] = useState({
    source: '',
    destination: '',
    time: new Date().toTimeString().slice(0, 5),
    preference: 'balanced',
  });
  const [srcSuggestions, setSrcSuggestions] = useState(false);
  const [dstSuggestions, setDstSuggestions] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (form.source && form.destination) onSubmit(form);
  };

  const swap = () => setForm({ ...form, source: form.destination, destination: form.source });

  const getFilteredSuggestions = (field) => {
    const val = form[field].toLowerCase().trim();
    if (!val) return MUMBAI_LOCATIONS.slice(0, 8);
    return MUMBAI_LOCATIONS.filter(l =>
      l.toLowerCase().includes(val)
    ).slice(0, 8);
  };

  const LocationInput = ({ field, label, icon, showSuggestions, onFocus, onBlur }) => {
    const suggestions = getFilteredSuggestions(field);

    return (
      <div className="relative">
        <label className="block text-[10px] font-semibold text-white/40 uppercase tracking-widest mb-1.5">
          {label}
        </label>
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30">{icon}</span>
          <input
            type="text"
            name={field}
            value={form[field]}
            onChange={handleChange}
            onFocus={onFocus}
            onBlur={() => setTimeout(onBlur, 200)}
            placeholder={`Type station name…`}
            autoComplete="off"
            spellCheck="false"
            className="w-full bg-white/[0.05] border border-white/10 rounded-xl pl-9 pr-4 py-2.5 text-white placeholder:text-white/20 text-sm focus:outline-none focus:border-violet-500/60 focus:bg-white/[0.08] transition-all"
          />
        </div>

        <AnimatePresence>
          {showSuggestions && suggestions.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: -4, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -4, scale: 0.98 }}
              transition={{ duration: 0.15 }}
              className="absolute top-full left-0 right-0 mt-1 bg-[#0d0d30] border border-white/10 rounded-xl overflow-hidden z-50 shadow-2xl"
            >
              {suggestions.map(loc => (
                <button
                  key={loc}
                  type="button"
                  onMouseDown={(e) => {
                    e.preventDefault();
                    setForm(f => ({ ...f, [field]: loc }));
                    onBlur();
                  }}
                  className="w-full text-left px-3 py-2 text-sm text-white/70 hover:bg-violet-500/20 hover:text-white transition-colors flex items-center gap-2"
                >
                  <MapPin size={11} className="text-violet-400 flex-shrink-0" />
                  <span>{loc}</span>
                </button>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
      className="h-full flex flex-col"
    >
      <div className="mb-5">
        <h2 className="text-white font-bold text-base">Plan Journey</h2>
        <p className="text-white/30 text-xs mt-0.5">AI-powered route optimization</p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4 flex-1">

        <LocationInput
          field="source"
          label="From"
          icon={<Navigation size={14} />}
          showSuggestions={srcSuggestions}
          onFocus={() => setSrcSuggestions(true)}
          onBlur={() => setSrcSuggestions(false)}
        />

        <div className="flex justify-center">
          <motion.button
            type="button"
            onClick={swap}
            whileHover={{ scale: 1.1, rotate: 180 }}
            whileTap={{ scale: 0.9 }}
            transition={{ duration: 0.3 }}
            className="w-7 h-7 rounded-full bg-white/[0.07] border border-white/10 flex items-center justify-center text-white/40 hover:text-white/70 hover:bg-white/10 transition-colors -my-1"
          >
            <RotateCcw size={13} />
          </motion.button>
        </div>

        <LocationInput
          field="destination"
          label="To"
          icon={<MapPin size={14} />}
          showSuggestions={dstSuggestions}
          onFocus={() => setDstSuggestions(true)}
          onBlur={() => setDstSuggestions(false)}
        />

        <div>
          <label className="block text-[10px] font-semibold text-white/40 uppercase tracking-widest mb-1.5">
            Departure Time
          </label>
          <div className="relative">
            <Clock size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30" />
            <input
              type="time"
              name="time"
              value={form.time}
              onChange={handleChange}
              className="w-full bg-white/[0.05] border border-white/10 rounded-xl pl-9 pr-4 py-2.5 text-white text-sm focus:outline-none focus:border-violet-500/60 transition-all [color-scheme:dark]"
            />
          </div>
        </div>

        <div>
          <label className="block text-[10px] font-semibold text-white/40 uppercase tracking-widest mb-2">
            <Sliders size={10} className="inline mr-1" />
            Preference
          </label>
          <div className="grid grid-cols-3 gap-1.5">
            {PREFERENCES.map(pref => (
              <motion.button
                key={pref.value}
                type="button"
                onClick={() => setForm({ ...form, preference: pref.value })}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.97 }}
                className={`py-2 px-1 rounded-xl text-center transition-all border ${
                  form.preference === pref.value
                    ? 'bg-violet-600/30 border-violet-500/50 text-violet-300'
                    : 'bg-white/[0.04] border-white/[0.08] text-white/40 hover:text-white/60 hover:bg-white/[0.07]'
                }`}
              >
                <div className="text-base leading-none mb-0.5">{pref.icon}</div>
                <div className="text-[10px] font-medium leading-tight">{pref.label}</div>
              </motion.button>
            ))}
          </div>
        </div>

        <div className="flex-1" />

        <motion.button
          type="submit"
          disabled={loading || !form.source || !form.destination}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.97 }}
          className="w-full bg-gradient-to-r from-violet-600 to-violet-700 hover:from-violet-500 hover:to-violet-600 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-violet-900/40 text-sm"
        >
          {loading ? (
            <>
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Optimizing…
            </>
          ) : (
            <>
              Find Best Routes
              <ArrowRight size={15} />
            </>
          )}
        </motion.button>
      </form>
    </motion.div>
  );
}