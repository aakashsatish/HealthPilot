# 🌐 **Vercel Frontend + Local Backend Deployment**

This guide will help you deploy your frontend to Vercel while keeping your backend local.

## 🎯 **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Local AI      │
│   (Vercel)      │◄──►│   (Local)       │◄──►│   (Ollama)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 **Step 1: Prepare Your Repository**

### **1.1 Push to GitHub**
```bash
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### **1.2 Get Your Local IP Address**
```bash
# On macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# On Windows
ipconfig | findstr "IPv4"
```

**Your local IP**: `192.168.2.211`

## 🎨 **Step 2: Deploy Frontend to Vercel**

### **2.1 Create Vercel Account**
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"

### **2.2 Import Your Repository**
1. Select your GitHub repository
2. Configure the project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `healthpilot-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### **2.3 Set Environment Variables**
Add these in your Vercel project settings:

```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_API_URL=http://192.168.2.211:8000
```

### **2.4 Deploy**
Click "Deploy" and wait for the build to complete.

## 🔧 **Step 3: Configure Local Backend**

### **3.1 Update CORS Settings**
In `healthpilot-backend/app/main.py`, update the CORS configuration:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://your-vercel-domain.vercel.app",  # Add your Vercel domain
        "https://your-custom-domain.com"          # If you have a custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **3.2 Start Your Local Services**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Redis
redis-server

# Terminal 3: Start Backend
cd healthpilot-backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🌐 **Step 4: Test the Connection**

### **4.1 Check Backend is Accessible**
```bash
# Test from your local machine
curl http://192.168.2.211:8000/health

# Should return:
# {"status": "healthy", "timestamp": "...", "service": "healthpilot-api"}
```

### **4.2 Test from Vercel**
Your Vercel frontend should now be able to connect to your local backend at `http://192.168.2.211:8000`.

## 🔒 **Step 5: Security Considerations**

### **5.1 Network Security**
- Your backend will be accessible on your local network
- Only devices on your network can access it
- Consider using a VPN if accessing from outside

### **5.2 Firewall Settings**
Make sure port 8000 is accessible on your local network:
```bash
# macOS: Allow incoming connections
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
```

## 🎯 **Step 6: Production Considerations**

### **6.1 Dynamic IP Address**
If your local IP changes, you'll need to update the Vercel environment variable:
1. Go to your Vercel project settings
2. Update `NEXT_PUBLIC_API_URL` with the new IP
3. Redeploy

### **6.2 Alternative: Use a Tunnel**
For more reliability, you can use a tunnel service:

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from ngrok.com

# Create tunnel to your backend
ngrok http 8000

# Use the ngrok URL in your Vercel environment variables
# NEXT_PUBLIC_API_URL=https://your-ngrok-url.ngrok.io
```

## 🚀 **Step 7: Access Your Application**

### **Your URLs:**
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `http://192.168.2.211:8000`
- **API Docs**: `http://192.168.2.211:8000/docs`

### **Testing:**
1. Visit your Vercel frontend
2. Try uploading a file
3. Check if it connects to your local backend
4. Verify AI analysis works

## 🔧 **Troubleshooting**

### **CORS Errors**
```
Error: CORS policy violation
Solution: Update CORS settings in backend to include your Vercel domain
```

### **Connection Refused**
```
Error: Failed to fetch
Solution: Check if backend is running and accessible at the correct IP
```

### **IP Address Changed**
```
Error: API calls failing
Solution: Update NEXT_PUBLIC_API_URL in Vercel environment variables
```

## 💰 **Cost Benefits**

### **Free Tier Limits:**
- **Vercel**: 100GB bandwidth, 100 serverless function executions
- **Local Backend**: $0 (your computer)
- **Ollama**: $0 (local AI)
- **Supabase**: $0 (free tier)

### **Total Cost: $0/month!**

## 🎉 **Benefits of This Setup**

### **✅ Advantages:**
- **Professional frontend**: Vercel's global CDN
- **Zero backend costs**: Everything runs locally
- **Full control**: Your data stays on your machine
- **Easy updates**: Frontend deploys automatically
- **Scalable**: Can handle many frontend users

### **⚠️ Considerations:**
- **Backend must be running**: Your computer needs to be on
- **Network dependent**: Only works when you're on the same network
- **IP changes**: Need to update environment variables if IP changes

## 🚀 **Quick Start Commands**

```bash
# 1. Start local services
./start.sh

# 2. Start backend
cd healthpilot-backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 3. Deploy frontend to Vercel
# (Follow the steps above)

# 4. Access your app
# Frontend: https://your-app.vercel.app
# Backend: http://192.168.2.211:8000
```

This setup gives you the best of both worlds: a professional frontend deployment with zero backend costs! 🎯 