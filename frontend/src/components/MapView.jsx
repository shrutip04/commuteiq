/**
 * MapView.jsx — Leaflet map with real OSRM road-following routes.
 */

import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

export default function MapView({ routes, selectedRouteId, heatmapData, showHeatmap }) {
  const mapRef         = useRef(null);
  const mapInstanceRef = useRef(null);
  const layersRef      = useRef([]);
  const heatLayerRef   = useRef(null);
  const [mapLoaded, setMapLoaded] = useState(false);

  // ── Init map ──────────────────────────────────────────────────────────────
  useEffect(() => {
    if (!mapRef.current || mapInstanceRef.current) return;

    import('leaflet').then(L => {
      // Clear stale Leaflet state from hot-reload
      if (mapRef.current._leaflet_id) {
        delete mapRef.current._leaflet_id;
      }
      while (mapRef.current.firstChild) {
        mapRef.current.removeChild(mapRef.current.firstChild);
      }

      delete L.Icon.Default.prototype._getIconUrl;
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
        iconUrl:       'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        shadowUrl:     'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
      });

      const map = L.map(mapRef.current, {
        center: [20.5937, 78.9629],
        zoom: 5,
        zoomControl: false,
        attributionControl: false,
      });

      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        subdomains: 'abcd',
        maxZoom: 19,
      }).addTo(map);

      L.control.zoom({ position: 'bottomright' }).addTo(map);
      L.control.attribution({ position: 'bottomleft', prefix: '© OpenStreetMap · OSRM' }).addTo(map);

      mapInstanceRef.current = map;
      setMapLoaded(true);
    });

    // Cleanup on unmount — lets hot-reload reinitialise cleanly
    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // ── Draw routes ───────────────────────────────────────────────────────────
  useEffect(() => {
    if (!mapInstanceRef.current || !mapLoaded) return;
    import('leaflet').then(L => {
      const map = mapInstanceRef.current;

      // Remove all old layers
      layersRef.current.forEach(l => { try { map.removeLayer(l); } catch(e){} });
      layersRef.current = [];

      if (!routes?.length) return;

      const allPoints = [];

      // Draw non-selected routes first (behind), selected route on top
      const sorted = [...routes].sort((a, b) => {
        if (a.route_id === selectedRouteId) return 1;
        if (b.route_id === selectedRouteId) return -1;
        return 0;
      });

      sorted.forEach(route => {
        const isSelected = route.route_id === selectedRouteId;
        const waypoints  = route.waypoints || [];
        if (waypoints.length < 2) return;

        // Shadow/glow for selected route
        if (isSelected) {
          const glow = L.polyline(waypoints, {
            color:   route.color,
            weight:  14,
            opacity: 0.15,
          }).addTo(map);
          layersRef.current.push(glow);
        }

        // Main route line
        const line = L.polyline(waypoints, {
          color:     route.color,
          weight:    isSelected ? 6 : 3,
          opacity:   isSelected ? 0.95 : 0.35,
          dashArray: isSelected ? null : '10, 8',
          lineCap:   'round',
          lineJoin:  'round',
        }).addTo(map);

        layersRef.current.push(line);
        allPoints.push(...waypoints);

        // Only show markers for selected route
        if (isSelected) {
          const src = route.source      || {};
          const dst = route.destination || {};

          // Pulsing source marker
          const srcIcon = L.divIcon({
            html: `
              <div style="position:relative;width:20px;height:20px;">
                <div style="position:absolute;inset:0;border-radius:50%;background:#c6f135;opacity:0.3;animation:ping 1.5s cubic-bezier(0,0,0.2,1) infinite;"></div>
                <div style="position:absolute;inset:3px;border-radius:50%;background:#c6f135;border:2px solid #fff;box-shadow:0 0 10px #c6f13590;"></div>
              </div>`,
            className: '',
            iconSize:   [20, 20],
            iconAnchor: [10, 10],
          });

          // Destination marker
          const dstIcon = L.divIcon({
            html: `
              <div style="position:relative;width:20px;height:20px;">
                <div style="position:absolute;inset:0;border-radius:50%;background:${route.color};opacity:0.3;animation:ping 1.5s cubic-bezier(0,0,0.2,1) infinite 0.5s;"></div>
                <div style="position:absolute;inset:3px;border-radius:50%;background:${route.color};border:2px solid #fff;box-shadow:0 0 10px ${route.color}90;"></div>
              </div>`,
            className: '',
            iconSize:   [20, 20],
            iconAnchor: [10, 10],
          });

          if (src.lat && src.lng) {
            const m = L.marker([src.lat, src.lng], { icon: srcIcon, zIndexOffset: 1000 })
              .addTo(map)
              .bindPopup(`
                <div style="font-family:DM Sans,sans-serif;padding:2px 0">
                  <div style="color:#c6f135;font-weight:700;font-size:13px">🟢 ${src.name || 'Origin'}</div>
                  <div style="color:rgba(255,255,255,0.5);font-size:11px;margin-top:2px">${src.lat?.toFixed(4)}, ${src.lng?.toFixed(4)}</div>
                </div>`);
            layersRef.current.push(m);
          }

          if (dst.lat && dst.lng) {
            const m = L.marker([dst.lat, dst.lng], { icon: dstIcon, zIndexOffset: 1000 })
              .addTo(map)
              .bindPopup(`
                <div style="font-family:DM Sans,sans-serif;padding:2px 0">
                  <div style="color:${route.color};font-weight:700;font-size:13px">📍 ${dst.name || 'Destination'}</div>
                  <div style="color:rgba(255,255,255,0.5);font-size:11px;margin-top:2px">${dst.lat?.toFixed(4)}, ${dst.lng?.toFixed(4)}</div>
                </div>`);
            layersRef.current.push(m);
          }
        }
      });

      // Auto-zoom to fit all route points
      if (allPoints.length > 1) {
        const bounds = L.latLngBounds(allPoints);
        map.fitBounds(bounds, { padding: [60, 60], maxZoom: 15, animate: true });
      }
    });
  }, [routes, selectedRouteId, mapLoaded]);

  // ── Heatmap ───────────────────────────────────────────────────────────────
  useEffect(() => {
    if (!mapInstanceRef.current || !mapLoaded) return;
    import('leaflet').then(L => {
      const map = mapInstanceRef.current;
      if (heatLayerRef.current) { try { map.removeLayer(heatLayerRef.current); } catch(e){} heatLayerRef.current = null; }
      if (!showHeatmap || !heatmapData?.length) return;

      const CanvasLayer = L.Layer.extend({
        onAdd(map) {
          this._map = map;
          this._canvas = L.DomUtil.create('canvas', 'leaflet-heatmap');
          this._resize();
          Object.assign(this._canvas.style, {
            position: 'absolute', top: '0', left: '0',
            pointerEvents: 'none', zIndex: '300',
          });
          map.getPanes().overlayPane.appendChild(this._canvas);
          map.on('moveend zoomend viewreset resize', this._redraw, this);
          this._redraw();
        },
        onRemove(map) {
          map.getPanes().overlayPane.removeChild(this._canvas);
          map.off('moveend zoomend viewreset resize', this._redraw, this);
        },
        _resize() {
          const sz = this._map.getSize();
          this._canvas.width  = sz.x;
          this._canvas.height = sz.y;
        },
        _redraw() {
          const map    = this._map;
          const canvas = this._canvas;
          this._resize();

          // Align canvas with current map viewport
          const topLeft = map.containerPointToLayerPoint([0, 0]);
          L.DomUtil.setPosition(canvas, topLeft);

          const ctx  = canvas.getContext('2d');
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Zoom-scaled radius — blobs visible at any zoom level
          const zoom  = map.getZoom();
          const baseR = Math.max(25, Math.min(80, zoom * 4));

          heatmapData.forEach(pt => {
            const cp = map.latLngToContainerPoint([pt.lat, pt.lng]);
            const x  = cp.x;
            const y  = cp.y;
            const r  = baseR * pt.intensity;

            // Skip off-screen points
            if (x + r < 0 || x - r > canvas.width || y + r < 0 || y - r > canvas.height) return;

            const grad  = ctx.createRadialGradient(x, y, 0, x, y, r);
            const alpha = Math.min(0.88, pt.intensity * 0.8);

            if (pt.intensity >= 0.70) {
              // 🔴 High congestion — red/orange
              grad.addColorStop(0,   `rgba(239,68,68,${alpha})`);
              grad.addColorStop(0.35,`rgba(239,68,68,${alpha * 0.8})`);
              grad.addColorStop(0.70,`rgba(245,158,11,${alpha * 0.4})`);
            } else if (pt.intensity >= 0.40) {
              // 🟠 Medium congestion — orange/yellow
              grad.addColorStop(0,   `rgba(245,158,11,${alpha})`);
              grad.addColorStop(0.40,`rgba(245,158,11,${alpha * 0.7})`);
              grad.addColorStop(0.75,`rgba(250,204,21,${alpha * 0.3})`);
            } else {
              // 🟢 Low congestion — green
              grad.addColorStop(0,   `rgba(34,197,94,${alpha})`);
              grad.addColorStop(0.40,`rgba(34,197,94,${alpha * 0.6})`);
              grad.addColorStop(0.75,`rgba(16,185,129,${alpha * 0.2})`);
            }
            grad.addColorStop(1, 'rgba(0,0,0,0)');

            ctx.beginPath();
            ctx.fillStyle = grad;
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.fill();
          });
        },
      });
      heatLayerRef.current = new CanvasLayer().addTo(map);
    });
  }, [showHeatmap, heatmapData, mapLoaded]);

  const selectedRoute = routes?.find(r => r.route_id === selectedRouteId);

  return (
    <div className="relative w-full h-full rounded-2xl overflow-hidden border border-white/[0.07]">
      <div ref={mapRef} className="w-full h-full" />

      {/* Ping animation CSS */}
      <style>{`
        @keyframes ping {
          75%, 100% { transform: scale(2); opacity: 0; }
        }
        .leaflet-popup-content-wrapper {
          background: #0f0f35 !important;
          border: 1px solid rgba(255,255,255,0.12) !important;
          border-radius: 14px !important;
          color: white !important;
          box-shadow: 0 8px 32px rgba(0,0,0,0.6) !important;
          padding: 4px !important;
        }
        .leaflet-popup-content { margin: 10px 14px !important; }
        .leaflet-popup-tip { background: #0f0f35 !important; }
        .leaflet-control-zoom { border-radius: 12px !important; overflow: hidden; border: 1px solid rgba(255,255,255,0.1) !important; }
        .leaflet-control-zoom-in, .leaflet-control-zoom-out {
          background: rgba(10,10,40,0.9) !important; color: rgba(255,255,255,0.6) !important;
          border: none !important; width: 30px !important; height: 30px !important; line-height: 30px !important;
        }
        .leaflet-control-zoom-in:hover, .leaflet-control-zoom-out:hover {
          background: rgba(124,58,237,0.4) !important; color: white !important;
        }
        .leaflet-control-attribution { background: rgba(5,5,26,0.7) !important; color: rgba(255,255,255,0.25) !important; font-size: 9px !important; border-radius: 8px 0 0 0 !important; }
        .leaflet-control-attribution a { color: rgba(124,58,237,0.7) !important; }
      `}</style>

      {/* Loading */}
      {!mapLoaded && (
        <div className="absolute inset-0 bg-[#07071f] flex items-center justify-center z-10">
          <div className="flex flex-col items-center gap-3">
            <div className="w-8 h-8 border-2 border-violet-500/30 border-t-violet-500 rounded-full animate-spin" />
            <span className="text-white/30 text-xs">Loading map…</span>
          </div>
        </div>
      )}

      {/* Route legend */}
      {routes?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-md border border-white/10 rounded-xl p-3 z-[400] min-w-[160px]"
        >
          <div className="text-[9px] font-bold text-white/30 uppercase tracking-widest mb-2">Routes</div>
          {routes.map(r => (
            <div key={r.route_id} className={`flex items-center gap-2 mb-1.5 last:mb-0 transition-opacity ${selectedRouteId === r.route_id ? 'opacity-100' : 'opacity-50'}`}>
              <div className="w-4 h-1 rounded-full" style={{ backgroundColor: r.color }} />
              <span className="text-[10px] text-white/70 font-medium">{r.name}</span>
              <span className="text-[9px] text-white/30 ml-auto">{r.distance_km}km</span>
            </div>
          ))}
        </motion.div>
      )}

      {/* Selected route info pill */}
      {selectedRoute && (
        <motion.div
          key={selectedRoute.route_id}
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute top-4 left-4 bg-black/70 backdrop-blur-md border border-white/10 rounded-xl px-3 py-2 z-[400] flex items-center gap-3"
        >
          <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: selectedRoute.color }} />
          <span className="text-white/80 text-xs font-semibold">{selectedRoute.name}</span>
          <span className="text-white/30 text-[10px]">{selectedRoute.distance_km} km · {selectedRoute.travel_time} min</span>
        </motion.div>
      )}

      {/* Heatmap badge */}
      {showHeatmap && (
        <motion.div
          initial={{ opacity: 0, x: 8 }}
          animate={{ opacity: 1, x: 0 }}
          className="absolute top-4 right-4 bg-orange-500/20 border border-orange-500/30 backdrop-blur-sm rounded-xl px-3 py-1.5 z-[400]"
        >
          <span className="text-orange-300 text-[10px] font-semibold">🔥 Congestion Heatmap</span>
        </motion.div>
      )}
    </div>
  );
}