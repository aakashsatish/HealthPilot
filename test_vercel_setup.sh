#!/bin/bash

echo "🌐 Testing Vercel + Local Backend Setup"
echo "========================================"

# Get local IP
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
echo "📍 Your local IP: $LOCAL_IP"

# Test backend accessibility
echo ""
echo "🔍 Testing backend accessibility..."
if curl -s "http://$LOCAL_IP:8000/health" > /dev/null; then
    echo "✅ Backend is accessible from network"
else
    echo "❌ Backend is not accessible from network"
    echo "   Make sure backend is running with:"
    echo "   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
fi

# Test Ollama
echo ""
echo "🤖 Testing Ollama..."
if curl -s "http://localhost:11434/api/tags" > /dev/null; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not running"
    echo "   Start with: ollama serve"
fi

# Test Redis
echo ""
echo "🔴 Testing Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is running"
else
    echo "❌ Redis is not running"
    echo "   Start with: redis-server"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Deploy frontend to Vercel with:"
echo "   NEXT_PUBLIC_API_URL=http://$LOCAL_IP:8000"
echo ""
echo "2. Your URLs will be:"
echo "   Frontend: https://your-app.vercel.app"
echo "   Backend:  http://$LOCAL_IP:8000"
echo ""
echo "3. Test the connection from Vercel to your local backend"
echo ""
echo "📖 See VERCEL_DEPLOYMENT.md for detailed instructions" 