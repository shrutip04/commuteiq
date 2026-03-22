# 🚇 CommuteIQ — AI-Powered Smart Commute Optimization System

A hackathon-grade full-stack commute intelligence platform with ML-powered routing, AI explanations, live disruption simulation, and a polished React dashboard.

---

## 🗂 Project Structure

```
commuteiq/
├── backend/
│   ├── app.py              # Flask entry point
│   ├── routes.py           # All API endpoints (Blueprint)
│   ├── auth.py             # JWT auth + bcrypt password hashing
│   ├── database.py         # SQLite init & connection
│   ├── ml_engine.py        # RandomForest ML model (crowding + delay)
│   ├── explain.py          # AI route explanation generator
│   ├── simulate_alert.py   # Disruption simulation engine
│   ├── utils.py            # Route generation, heatmap, geocoding
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Navbar.jsx
    │   │   ├── JourneyForm.jsx
    │   │   ├── RouteCard.jsx
    │   │   ├── RouteList.jsx        # + Comparison mode
    │   │   ├── MapView.jsx          # Leaflet map + canvas heatmap
    │   │   └── ExplanationPanel.jsx # AI text + disruption sim
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Signup.jsx
    │   │   └── Dashboard.jsx       # 3-column layout
    │   ├── services/
    │   │   └── api.js              # All API calls
    │   ├── AuthContext.jsx         # Global auth state
    │   ├── App.jsx                 # Router + auth guards
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── vite.config.js
    ├── tailwind.config.js
    └── package.json
```

---

## ⚙️ Setup & Run

### 1. Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
# → Running on http://localhost:5000
```

The ML model trains automatically on first run (takes ~5 seconds).

---

### 2. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# → Running on http://localhost:5173
```

Open **http://localhost:5173** in your browser.

---

## 🔑 Demo Flow

1. **Sign up** at `/signup` with any username/email/password
2. **Log in** at `/login`
3. On the **Dashboard**:
   - Enter source (e.g. `CST`) and destination (e.g. `Andheri`)
   - Select departure time and preference
   - Click **Find Best Routes**
4. Three route cards appear with ML-predicted metrics
5. Click a route → map updates + AI explanation generated
6. Toggle **Heatmap** in the navbar to see congestion overlay
7. Click **Simulate Disruption** to trigger a real-world incident
8. Routes dynamically reroute with updated metrics
9. Use **Compare mode** (columns icon) to compare two routes

---

## 🧠 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/signup` | Register user |
| POST | `/api/login` | Login, returns JWT |
| GET | `/api/me` | Current user info |
| POST | `/api/plan_journey` | Get 3 optimized routes |
| POST | `/api/simulate_alert` | Trigger disruption on routes |
| POST | `/api/route_explanation` | AI explanation for selected route |
| GET | `/api/heatmap_data` | Congestion heatmap points |
| GET | `/api/user_preferences` | Get user preferences |
| POST | `/api/user_preferences` | Save user preferences |

All protected endpoints require: `Authorization: Bearer <jwt_token>`

---

## 🤖 AI Integration (Production)

To plug in a real LLM, edit `backend/explain.py`:

```python
import anthropic
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def generate_explanation(route, alternatives):
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": _build_prompt(route, alternatives)}]
    )
    return message.content[0].text
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python Flask + SQLite |
| ML | scikit-learn RandomForest |
| Auth | bcrypt + JWT |
| Frontend | React 18 + Vite |
| Styling | Tailwind CSS |
| Maps | Leaflet.js (dark tiles) |
| Animations | Framer Motion |
| API | REST/JSON |
