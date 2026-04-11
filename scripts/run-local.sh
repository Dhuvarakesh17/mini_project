#!/bin/bash
# Local deployment - runs both frontend dev and backend server

echo "🚀 Starting Heart Risk Intelligence App Locally"
echo ""

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to cleanup on exit
cleanup() {
    echo -e "${BLUE}Shutting down...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Done!${NC}"
}
trap cleanup EXIT

# Start backend
echo -e "${BLUE}Starting FastAPI backend...${NC}"
cd "$(dirname "$0")/.."
source venv/bin/activate 2>/dev/null || echo "⚠️ Virtual env not activated"
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo -e "${GREEN}Backend running on http://localhost:8000${NC}"

# Wait for backend to start
sleep 3

# Start frontend
echo -e "${BLUE}Starting React frontend...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend running on http://localhost:5173${NC}"

echo ""
echo -e "${GREEN}✅ App is ready!${NC}"
echo -e "  Frontend: ${BLUE}http://localhost:5173${NC}"
echo -e "  Backend:  ${BLUE}http://localhost:8000${NC}"
echo -e "  API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "Press Ctrl+C to stop"

# Wait for processes
wait
