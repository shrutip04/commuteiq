/**
 * Dashboard.jsx — 3-column layout with tabbed right panel to avoid scrolling.
 */

import { useState, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MapPin, IndianRupee, Brain, ChevronRight } from 'lucide-react';
import Navbar from '../components/Navbar';
import JourneyForm from '../components/JourneyForm';
import MapView from '../components/MapView';
import RouteList from '../components/RouteList';
import ExplanationPanel from '../components/ExplanationPanel';
import SafetyModePanel from '../components/SafetyModePanel';
import CostComparison from '../components/CostComparison';
import { journeyAPI, prefsAPI } from '../services/api';

// ── Tab config ────────────────────────────────────────────────────────────────
const TABS = [
  { id: 'routes',  label: 'Routes',      icon: <MapPin size={12} /> },
  { id: 'cost',    label: 'Cost',         icon: <IndianRupee size={12} /> },
  { id: 'intel',   label: 'Intelligence', icon: <Brain size={12} /> },
];

export default function Dashboard() {
  const [routes, setRoutes]               = useState([]);
  const [selectedRoute, setSelectedRoute] = useState(null);
  const [explanation, setExplanation]     = useState(null);
  const [disruption, setDisruption]       = useState(null);
  const [heatmapData, setHeatmapData]     = useState([]);
  const [showHeatmap, setShowHeatmap]     = useState(false);
  const [userMode, setUserMode]           = useState('normal');
  const [gender, setGender]               = useState('prefer_not_to_say');
  const [activeTab, setActiveTab]         = useState('routes');

  const [loadingRoutes, setLoadingRoutes]           = useState(false);
  const [loadingExplanation, setLoadingExplanation] = useState(false);
  const [loadingSimulation, setLoadingSimulation]   = useState(false);

  // Load saved gender + mode on mount
  useEffect(() => {
    prefsAPI.get()
      .then(res => {
        if (res.data?.gender)    setGender(res.data.gender);
        if (res.data?.user_mode) setUserMode(res.data.user_mode);
      })
      .catch(() => {});
  }, []);

  const handlePlanJourney = async (form) => {
    setLoadingRoutes(true);
    setDisruption(null); setExplanation(null); setSelectedRoute(null);
    setActiveTab('routes');
    try {
      const res = await journeyAPI.planJourney(
        form.source, form.destination, form.time, form.preference, userMode
      );
      const newRoutes = res.data.routes;
      setRoutes(newRoutes);
      if (newRoutes.length > 0) handleSelectRoute(newRoutes[0], newRoutes.slice(1));
    } catch (err) {
      console.error('Journey error:', err);
    } finally {
      setLoadingRoutes(false);
    }
  };

  const handleSelectRoute = useCallback(async (route, alts) => {
    setSelectedRoute(route);
    const alternatives = alts || routes.filter(r => r.route_id !== route.route_id);
    setLoadingExplanation(true);
    try {
      const res = await journeyAPI.getExplanation(route, alternatives);
      setExplanation(res.data);
    } catch {
      setExplanation({ bullets: [], summary: 'Unable to generate explanation.' });
    } finally {
      setLoadingExplanation(false);
    }
  }, [routes]);

  const handleSimulate = async () => {
    if (!routes.length) return;
    setLoadingSimulation(true);
    try {
      const res = await journeyAPI.simulateAlert(routes);
      const { updated_routes, disruption: info } = res.data;
      setRoutes(updated_routes);
      setDisruption(info);
      if (updated_routes.length > 0)
        handleSelectRoute(updated_routes[0], updated_routes.slice(1));
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingSimulation(false);
    }
  };

  const handleToggleHeatmap = async () => {
    if (!showHeatmap && heatmapData.length === 0) {
      try {
        const src = routes[0]?.source;
        const dst = routes[0]?.destination;
        const res = await journeyAPI.getHeatmap(src?.lat, src?.lng, dst?.lat, dst?.lng);
        setHeatmapData(res.data.points);
      } catch (err) { console.error(err); }
    }
    setShowHeatmap(v => !v);
  };

  return (
    <div className="min-h-screen bg-[#05051a] flex flex-col font-body">
      {/* Background grid */}
      <div className="fixed inset-0 pointer-events-none opacity-40" style={{
        backgroundImage: 'linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px)',
        backgroundSize: '40px 40px',
      }} />
      <div className="fixed top-1/4 left-1/3 w-96 h-96 rounded-full pointer-events-none opacity-[0.06]"
        style={{ background: 'radial-gradient(circle, #7c3aed, transparent 70%)', filter: 'blur(40px)' }}
      />

      <Navbar
        onToggleHeatmap={handleToggleHeatmap}
        heatmapActive={showHeatmap}
        userMode={userMode}
        onUserModeChange={setUserMode}
      />

      <div className="flex-1 flex overflow-hidden relative z-10">

        {/* ── Left: Journey Form ──────────────────────────────────────────── */}
        <motion.aside
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.4 }}
          className="w-64 flex-shrink-0 border-r border-white/[0.06] p-4 overflow-y-auto"
        >
          <JourneyForm
            onSubmit={handlePlanJourney}
            loading={loadingRoutes}
            userMode={userMode}
          />
        </motion.aside>

        {/* ── Center: Map ─────────────────────────────────────────────────── */}
        <motion.main
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="flex-1 p-3"
        >
          <MapView
            routes={routes}
            selectedRouteId={selectedRoute?.route_id}
            heatmapData={heatmapData}
            showHeatmap={showHeatmap}
          />
        </motion.main>

        {/* ── Right: Tabbed Panel ─────────────────────────────────────────── */}
        <motion.aside
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.4 }}
          className="flex-shrink-0 border-l border-white/[0.06] flex flex-col"
          style={{ width: '308px' }}
        >
          {/* Tab bar — fixed at top */}
          <div className="flex border-b border-white/[0.07] bg-[#07071f]/60 flex-shrink-0">
            {TABS.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 flex items-center justify-center gap-1.5 py-3 text-[10px] font-bold uppercase tracking-wider transition-all relative ${
                  activeTab === tab.id
                    ? 'text-violet-300'
                    : 'text-white/25 hover:text-white/50'
                }`}
              >
                {tab.icon}
                <span className="hidden sm:inline">{tab.label}</span>
                {/* Active underline */}
                {activeTab === tab.id && (
                  <motion.div
                    layoutId="tab-underline"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-violet-500 rounded-full"
                  />
                )}
                {/* Badge for routes tab */}
                {tab.id === 'routes' && routes.length > 0 && (
                  <span className="ml-0.5 w-4 h-4 rounded-full bg-violet-600/50 border border-violet-500/40 text-[8px] font-black text-violet-300 flex items-center justify-center">
                    {routes.length}
                  </span>
                )}
              </button>
            ))}
          </div>

          {/* Tab content — scrollable */}
          <div className="flex-1 overflow-y-auto">
            <AnimatePresence mode="wait">

              {/* ── Tab: Routes ─────────────────────────────────────────── */}
              {activeTab === 'routes' && (
                <motion.div
                  key="routes"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  transition={{ duration: 0.2 }}
                  className="p-4"
                >
                  <SafetyModePanel
                    userMode={userMode}
                    routes={routes}
                    gender={gender}
                    onGenderChange={setGender}
                  />
                  <RouteList
                    routes={routes}
                    selectedRouteId={selectedRoute?.route_id}
                    onSelectRoute={route => handleSelectRoute(route)}
                    loading={loadingRoutes}
                  />
                  {/* Nudge to cost tab after routes load */}
                  {routes.length > 0 && (
                    <button
                      onClick={() => setActiveTab('cost')}
                      className="mt-3 w-full flex items-center justify-center gap-2 py-2 bg-white/[0.03] border border-white/[0.07] rounded-xl text-white/30 text-[10px] hover:text-white/60 hover:bg-white/[0.05] transition-all"
                    >
                      <IndianRupee size={10} />
                      View cost breakdown
                      <ChevronRight size={10} />
                    </button>
                  )}
                </motion.div>
              )}

              {/* ── Tab: Cost ───────────────────────────────────────────── */}
              {activeTab === 'cost' && (
                <motion.div
                  key="cost"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  transition={{ duration: 0.2 }}
                  className="p-4"
                >
                  {routes.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-48 gap-3">
                      <IndianRupee size={28} className="text-white/10" />
                      <p className="text-white/25 text-xs text-center leading-relaxed">
                        Plan a journey first to see<br />cost comparison
                      </p>
                    </div>
                  ) : (
                    <CostComparison
                      selectedRoute={selectedRoute}
                      routes={routes}
                    />
                  )}
                </motion.div>
              )}

              {/* ── Tab: Intelligence ────────────────────────────────────── */}
              {activeTab === 'intel' && (
                <motion.div
                  key="intel"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  transition={{ duration: 0.2 }}
                  className="p-4"
                >
                  <ExplanationPanel
                    explanation={explanation}
                    loadingExplanation={loadingExplanation}
                    onSimulate={handleSimulate}
                    loadingSimulation={loadingSimulation}
                    disruption={disruption}
                    selectedRoute={selectedRoute}
                    userMode={userMode}
                  />
                </motion.div>
              )}

            </AnimatePresence>
          </div>
        </motion.aside>
      </div>
    </div>
  );
}