/**
 * EmergencyButton.jsx — Always-visible floating SOS button.
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import EmergencyModal from './EmergencyModal';

export default function EmergencyButton({ selectedRoute, userMode }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Floating SOS button */}
      <motion.button
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 1, type: 'spring', stiffness: 400, damping: 25 }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.92 }}
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-[9998] w-14 h-14 rounded-full flex items-center justify-center shadow-2xl"
        style={{
          background: 'linear-gradient(135deg, #ef4444, #dc2626)',
          boxShadow: '0 0 0 0 rgba(239,68,68,0.4)',
          animation: 'sos-pulse 2.5s infinite',
        }}
        title="SOS Emergency"
      >
        <span className="text-2xl leading-none select-none">🆘</span>
      </motion.button>

      <style>{`
        @keyframes sos-pulse {
          0%   { box-shadow: 0 0 0 0 rgba(239,68,68,0.5); }
          70%  { box-shadow: 0 0 0 16px rgba(239,68,68,0); }
          100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
        }
      `}</style>

      <AnimatePresence>
        {open && (
          <EmergencyModal
            onClose={() => setOpen(false)}
            selectedRoute={selectedRoute}
            userMode={userMode}
          />
        )}
      </AnimatePresence>
    </>
  );
}