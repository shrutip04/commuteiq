#!/usr/bin/env bash
# start.sh — Quick start both backend and frontend
# Usage: bash start.sh

set -e

echo ""
echo "╔════════════════════════════════════╗"
echo "║   CommuteIQ — Quick Start          ║"
echo "╚════════════════════════════════════╝"
echo ""

# ── Backend ──────────────────────────────
echo "▶ Setting up backend..."
cd "$(dirname "$0")/backend"

if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "  ✓ Virtual environment created"
fi

source venv/bin/activate
pip install -r requirements.txt -q
echo "  ✓ Dependencies installed"

echo "  ✓ Starting Flask on http://localhost:5000"
python app.py &
BACKEND_PID=$!

# ── Frontend ─────────────────────────────
echo ""
echo "▶ Setting up frontend..."
cd "../frontend"

if [ ! -d "node_modules" ]; then
  npm install -q
  echo "  ✓ npm packages installed"
fi

echo "  ✓ Starting Vite on http://localhost:5173"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "╔════════════════════════════════════╗"
echo "║  App running!                      ║"
echo "║  Frontend → http://localhost:5173  ║"
echo "║  Backend  → http://localhost:5000  ║"
echo "║  Press Ctrl+C to stop both         ║"
echo "╚════════════════════════════════════╝"
echo ""

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'" EXIT
wait
