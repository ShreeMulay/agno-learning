#!/bin/bash
# Start Agno Learning Dashboard (Backend + Frontend)

cd "$(dirname "$0")"
source .venv/bin/activate
export PYTHONPATH=.

# Kill any existing processes on these ports
pkill -f "uvicorn main:app.*8001" 2>/dev/null
pkill -f "next-server.*3001" 2>/dev/null
sleep 1

echo "🚀 Starting Agno Learning Dashboard..."
echo ""

# Start backend in background
echo "📡 Starting backend on http://localhost:8001"
(cd gui/backend && uvicorn main:app --reload --port 8001) &
BACKEND_PID=$!

sleep 2

# Start frontend in background
echo "🎨 Starting frontend on http://localhost:3001"
(cd gui/frontend && bun run dev -- -p 3001) &
FRONTEND_PID=$!

echo ""
echo "✅ Dashboard running!"
echo "   Open: http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
