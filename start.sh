#!/bin/bash

echo "🚀 Starting HealthPilot Local Development"
echo "========================================"

# Check if required services are installed
echo "🔍 Checking prerequisites..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it first:"
    echo "   https://ollama.ai/download"
    exit 1
fi

# Check if Redis is installed
if ! command -v redis-server &> /dev/null; then
    echo "❌ Redis is not installed. Please install it first:"
    echo "   macOS: brew install redis"
    echo "   Ubuntu: sudo apt-get install redis-server"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install it first:"
    echo "   https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first:"
    echo "   https://python.org/"
    exit 1
fi

echo "✅ All prerequisites are installed!"

# Check if virtual environment exists
if [ ! -d "healthpilot-backend/venv" ]; then
    echo "📦 Setting up Python virtual environment..."
    cd healthpilot-backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements/requirements.txt
    cd ..
fi

# Check if node_modules exists
if [ ! -d "healthpilot-frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd healthpilot-frontend
    npm install
    cd ..
fi

echo ""
echo "🎯 Starting services..."
echo ""

# Check if Ollama is already running
if pgrep -f "ollama serve" > /dev/null; then
    echo "🤖 Ollama is already running!"
else
    echo "🤖 Starting Ollama..."
    ollama serve &
    OLLAMA_PID=$!
    sleep 3
fi

# Pull the model if not already downloaded
echo "📥 Checking for Llama model..."
ollama list | grep -q "llama3.1" || ollama pull llama3.1

# Check if Redis is already running
if pgrep -f "redis-server" > /dev/null; then
    echo "🔴 Redis is already running!"
else
    echo "🔴 Starting Redis..."
    redis-server &
    REDIS_PID=$!
    sleep 2
fi

echo ""
echo "✅ Services started successfully!"
echo ""
echo "🌐 Your application will be available at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 To start the application:"
echo "   1. Terminal 1: cd healthpilot-backend && source venv/bin/activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo "   2. Terminal 2: cd healthpilot-frontend && npm run dev"
echo ""
echo "🛑 To stop all services:"
echo "   pkill -f ollama"
echo "   pkill -f redis-server"
echo ""
echo "🎉 Happy coding!" 