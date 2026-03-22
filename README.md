<div align="center">

<br/>

```
  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗██╗   ██╗████████╗███████╗    ██╗ ██████╗
 ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██║   ██║╚══██╔══╝██╔════╝    ██║██╔═══██╗
 ██║     ██║   ██║██╔████╔██║██╔████╔██║██║   ██║   ██║   █████╗      ██║██║   ██║
 ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██║   ██║   ██║   ██╔══╝      ██║██║▄▄ ██║
 ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║╚██████╔╝   ██║   ███████╗    ██║╚██████╔╝
  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝ ╚═════╝    ╚═╝   ╚══════╝    ╚═╝ ╚══▀▀═╝
```

### **AI-Powered Smart Commute Optimization for Mumbai**
*Predictive · Human-Aware · Safety-First*

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Framer](https://img.shields.io/badge/Framer_Motion-11-0055FF?style=for-the-badge&logo=framer&logoColor=white)](https://framer.com/motion)
[![License](https://img.shields.io/badge/License-MIT-c6f135?style=for-the-badge)](LICENSE)

<br/>

> *"This could actually save someone."*

<br/>

---

</div>

## 🗺️ What is CommuteIQ?

CommuteIQ is a full-stack AI commute assistant built for Mumbai — the city with **8 million daily train passengers** and one of the world's most complex transit networks. It goes far beyond route planning.

CommuteIQ combines **machine learning predictions**, **real Mumbai transit data**, **emotional safety scoring**, and a live **Guardian Mode** that monitors your journey in real-time — notifying trusted contacts if something goes wrong.

<br/>

---

## ✨ Features at a Glance

<table>
<tr>
<td width="50%">

### 🚦 Smart Route Planning
- Real Mumbai train network (WR, CR, Harbour, Trans-Harbour, Metro 1/2A/7)
- **Exact platform numbers** and boarding tips per station
- Fast/Slow local distinction with train direction
- OSRM real road geometry for buses & cabs
- **Rail track geometry** — routes follow actual train corridors, not roads
- NMMT + BEST bus routes for Navi Mumbai

</td>
<td width="50%">

### 🤖 ML Predictions
- RandomForest model trained on synthetic commute data
- Predicts **crowding %** and **delay minutes** per route
- Peak / off-peak hour awareness
- Day-of-week patterns
- Falls back gracefully to rule-based logic

</td>
</tr>
<tr>
<td>

### 🛡️ Trust Score System
- Every route gets a **0–100 Trust Score**
- Circular animated badge (🟢 green / 🟡 yellow / 🔴 red)
- Factors: confidence × crowding × delay × time-of-day
- Night hour penalty, peak hour penalty

</td>
<td>

### 🔮 Future Risk Prediction
- Predicts conditions **15 minutes ahead**
- Shows `22% now → 61% in ~15min ↑`
- Trend arrows: rising / falling / stable
- Mini bar chart comparison
- Simulates peak-hour transitions

</td>
</tr>
<tr>
<td>

### 😰 Emotional Safety Mode
Four modes that **actually re-rank routes**:

| Mode | What changes |
|------|-------------|
| 😊 Normal | Balanced routing |
| 😰 Anxious | −18pts for crowded routes, trains boosted |
| 🌙 Alone at Night | Auto/Cab −18pts, trains +15pts |
| 🏃 Running Late | Sorted by speed, delay weight 50% |

**Female profile** adds an extra safety layer: Auto/Cab −10pts extra, trains +8pts extra, isolated routes heavily penalised.

</td>
<td>

### 🚨 Guardian Mode
Live journey simulation with scripted alerts:

- **Tick 14s** → `⚠️ You stopped moving` — "I'm Safe" button
- **Tick 26s** → `🗺️ Route deviation detected`
- **Tick 38s** → Full-screen `🚨 Safety Alert` overlay with action buttons
- **Auto-notifies** trusted contact (`📱 Alerting Mom`)
- GPS dot moves along route progress bar
- Journey log with timestamps

</td>
</tr>
<tr>
<td>

### 🎮 What-If Engine
Interactive scenario simulator:
- ⏰ Delay slider (0–20 min)
- 🌧️ Weather (Clear / Rain / Heavy Rain)
- 🌙 Night mode toggle
- Shows exact Before → After trust score
- e.g. *"Safety drops from 82 → 54 (−28 pts)"*
- *"Rain increases accident risk by ~23%"*

</td>
<td>

### 💸 Multi-Modal Cost Engine
12 transport options calculated for every journey:

**Single:** Auto · Cab · Bus · Local Train

**Hybrid:** Train+Auto · Bus+Train · Train+Bus · Auto+Bus · and more

Each shows cost breakdown per segment, travel time, and badges:
- 🏆 Cheapest · ⚡ Fastest · 💡 Best Value
- *"Taking train instead of cab saves ₹146"*

</td>
</tr>
<tr>
<td>

### 🔥 Congestion Heatmap
- City-wide heat overlay on Leaflet map
- 🔴 Red = high congestion (CST, Dadar, Andheri)
- 🟠 Orange = moderate
- 🟢 Green = low
- Zoom-aware blob radius
- Redraws correctly as map pans/zooms

</td>
<td>

### 🧠 AI Explanation Engine
Consistent 3-bullet analysis per route:
1. **Performance** — speed vs alternatives
2. **Trust reasoning** — *why* the score is what it is, including safety mode penalties
3. **Risk outlook** — current vs predicted conditions

No more contradictions — if safety mode penalised a route, the AI explains exactly why.

</td>
</tr>
</table>

<br/>

---

## 🏗️ Architecture

```
commuteiq/
├── backend/                        # Flask + Python
│   ├── app.py                      # Entry point, global CORS handler
│   ├── routes.py                   # 14 API endpoints
│   ├── utils.py                    # Geocoding + OSRM routing + heatmap
│   ├── ml_engine.py                # RandomForest + trust score + future risk
│   ├── safety_engine.py            # Emotional safety mode scoring
│   ├── cost_engine.py              # Multi-modal fare calculator
│   ├── explain.py                  # AI explanation generator
│   ├── mumbai_transit.py           # Full Mumbai transit DB (WR/CR/HL/THL/Metro)
│   ├── rail_geometry.py            # GPS coords for every Mumbai station
│   ├── simulate_alert.py           # Disruption simulation
│   ├── simulate_scenario.py        # What-if scenario engine
│   ├── database.py                 # SQLite schema (users + preferences + gender)
│   └── auth.py                     # bcrypt + JWT
│
└── frontend/                       # React + Vite + Tailwind
    └── src/
        ├── pages/
        │   ├── Dashboard.jsx       # 3-column layout with tabbed right panel
        │   ├── Login.jsx
        │   └── Signup.jsx
        ├── components/
        │   ├── MapView.jsx         # Leaflet dark map + rail routes + heatmap
        │   ├── RouteCard.jsx       # M-Indicator style step-by-step directions
        │   ├── RouteList.jsx       # Route cards with grid/list toggle
        │   ├── GuardianMode.jsx    # Live safety simulation
        │   ├── WhatIfPanel.jsx     # What-if scenario controls
        │   ├── CostComparison.jsx  # Multi-modal cost breakdown
        │   ├── SafetyModePanel.jsx # Gender selector + mode impact display
        │   ├── ExplanationPanel.jsx
        │   ├── TrustBadge.jsx      # Circular animated trust score
        │   ├── RiskIndicator.jsx   # Current vs future risk bars
        │   ├── LiveMonitor.jsx     # Real-time journey monitoring
        │   └── Navbar.jsx          # Safety mode dropdown
        └── services/
            └── api.js              # authAPI · journeyAPI · costAPI · prefsAPI
```

<br/>

---

## 🚇 Mumbai Transit Coverage

| Line | Stations | Platforms | Fast/Slow |
|------|----------|-----------|-----------|
| Western Railway (WR) | Churchgate → Virar (27 stations) | ✅ Per station | ✅ |
| Central Railway (CR) | CSMT → Kalyan (26 stations) | ✅ Per station | ✅ |
| Harbour Line (HL) | CSMT → Panvel (25 stations) | ✅ Per station | — |
| Trans-Harbour (THL) | Thane → Nerul (8 stations) | ✅ Per station | — |
| Metro Line 1 | Versova → Ghatkopar (8 stations) | ✅ | — |
| Metro Line 2A | Dahisar E → DN Nagar (8 stations) | ✅ | — |
| Metro Line 7 | Dahisar E → Andheri E (5 stations) | ✅ | — |
| BEST Bus | 16 routes across Mumbai | — | — |
| NMMT Bus | 10 routes across Navi Mumbai | — | — |

**Cross-network interchanges handled:** WR↔HL via CSMT, CR↔HL via Kurla, Metro↔CR via Ghatkopar, Metro↔WR via Andheri, THL↔HL via Nerul

<br/>

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/signup` | Register user |
| `POST` | `/api/login` | Login → JWT token |
| `GET`  | `/api/me` | Current user profile |
| `POST` | `/api/plan_journey` | Plan route with ML predictions + safety scoring |
| `POST` | `/api/simulate_alert` | Trigger disruption simulation |
| `POST` | `/api/route_explanation` | AI explanation for selected route |
| `GET`  | `/api/heatmap_data` | Congestion heatmap points |
| `POST` | `/api/simulate_scenario` | What-if: delay / rain / night |
| `GET`  | `/api/live_monitor` | Real-time safety check |
| `POST` | `/api/guardian_check` | Guardian mode event processor |
| `POST` | `/api/guardian_scenario` | What-if with impact analysis |
| `POST` | `/api/cost_options` | Multi-modal cost breakdown |
| `GET`  | `/api/user_preferences` | Load saved preferences |
| `POST` | `/api/user_preferences` | Save preferences + gender |

<br/>

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend

```powershell
cd commuteiq/backend
pip install flask flask-cors bcrypt PyJWT pandas scikit-learn numpy
python app.py
```

Verify: `http://localhost:5000/health` → `{"status": "ok"}`

### Frontend

```powershell
cd commuteiq/frontend
npm install
npm run dev
```

Open: `http://localhost:5173`

### Default credentials
Register a new account on the signup page — or use any email/password (min 6 chars).

<br/>

---

## 🧠 How the ML Works

```
User searches: Kharghar → Vashi at 09:00

1. Geocode source + destination (Mumbai lookup table → Nominatim fallback)
2. Get transit options from Mumbai transit DB
3. For each option:
   a. RandomForest predicts crowding_pct + delay_minutes
   b. compute_trust_score() → 0–100 based on confidence × crowding × delay × hour
   c. predict_future_risk() → simulates conditions +1 hour ahead
   d. apply_safety_scoring() → re-weights scores based on user mode + gender
4. Routes re-sorted by safety profile
5. AI explanation generated with consistent trust + risk reasoning
```

**No retraining needed for safety modes** — the ML predicts raw crowding/delay, and the safety engine applies multipliers on top.

<br/>

---

## 🎯 Key Design Decisions

**Why not retrain the model for safety modes?**
The ML model predicts objective conditions (crowding %, delay mins). Safety preferences are subjective — they belong in the scoring layer, not the model. This means safety modes work instantly with no data collection required.

**Why rail track geometry instead of OSRM for trains?**
OSRM routes along roads. Train routes should follow actual rail corridors. `rail_geometry.py` stores exact GPS coordinates for every Mumbai station and interpolates waypoints between them — giving routes that visually follow the correct tracks on the map.

**Why SQLite?**
Hackathon-appropriate. The schema is clean enough to migrate to PostgreSQL with no code changes beyond the connection string.

<br/>

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend framework | React 18 + Vite |
| Styling | Tailwind CSS |
| Animations | Framer Motion |
| Maps | Leaflet.js + CartoDB dark tiles |
| Road routing | OSRM public API |
| Backend | Flask 3.0 |
| ML | scikit-learn RandomForest |
| Database | SQLite |
| Auth | bcrypt + PyJWT |
| Geocoding | Custom Mumbai lookup + Nominatim |

<br/>

---

## 👩‍💻 Built By

**Shruti** — Full-stack development, ML integration, Mumbai transit data, UI/UX design

*Built for hackathon — March 2026*

<br/>

---

<div align="center">

**CommuteIQ** — *Because your commute should be smart, safe, and stress-free.*

⭐ Star this repo if you found it useful

</div>
