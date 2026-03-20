#!/bin/bash
echo "Starting Thumbtack AI Matchmaker Backend..."
cd backend
source venv/bin/activate
# Replace this with your actual key before running!
export GROQ_API_KEY="your-api-key-here" 
nohup uvicorn main:app --reload > backend.log 2>&1 &
cd ..

echo "Starting Thumbtack AI Matchmaker Frontend..."
cd frontend
nohup npm run dev > frontend.log 2>&1 &
cd ..

echo ""
echo "✅ Services started!"
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:3000"
echo "To stop the servers later, you can run: pkill -f uvicorn && pkill -f 'npm run dev'"
