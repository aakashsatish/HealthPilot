# 🏥 HealthPilot: AI-Powered Lab Report Analysis

## 📋 **Project Overview**

HealthPilot is a comprehensive lab report analysis platform that uses AI to translate complex medical information into understandable insights. Built as a full-stack application, it helps users understand their lab results through intelligent analysis and clear explanations.

## 🎯 **Problem Solved**

Many people struggle to understand their lab reports due to:
- **Complex medical terminology**
- **Unclear reference ranges**
- **Lack of context for results**
- **Difficulty identifying important findings**

HealthPilot addresses these issues by providing:
- **AI-powered analysis** of lab results
- **Clear, plain-English explanations**
- **Risk level assessment**
- **Personalized recommendations**
- **Professional PDF reports**

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Services   │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Ollama)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Supabase      │    │     Redis       │    │   Tesseract     │
│   (Database)    │    │   (Queue)       │    │    (OCR)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ **Technologies Used**

### **Frontend**
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **Supabase Auth** - User authentication
- **React Hook Form** - Form handling
- **Lucide React** - Modern icons

### **Backend**
- **FastAPI** - Modern Python web framework
- **Python 3.11+** - Backend language
- **Supabase** - Database and authentication
- **Redis + RQ** - Background job processing
- **ReportLab** - PDF generation
- **Tesseract OCR** - Text extraction from images

### **AI & Processing**
- **Ollama** - Local LLM for AI analysis
- **Tesseract** - OCR for text extraction
- **SMTP** - Email notifications
- **Background Jobs** - Asynchronous processing

## 🚀 **Getting Started**

### **Prerequisites**
- Node.js 18+ and npm
- Python 3.11+
- Ollama (for local AI)
- Redis (for background jobs)
- ngrok (for hybrid deployment)

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/healthpilot.git
cd healthpilot
```

### **2. Set Up Backend**
```bash
cd healthpilot-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Supabase credentials
```

### **3. Set Up Frontend**
```bash
cd healthpilot-frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your Supabase credentials
```

### **4. Start Services**

**Terminal 1: Start Ollama**
```bash
ollama serve
ollama pull llama3.1
```

**Terminal 2: Start Redis**
```bash
redis-server
```

**Terminal 3: Start Backend**
```bash
cd healthpilot-backend
source venv/bin/activate
python -m app.main
```

**Terminal 4: Start ngrok (for hybrid deployment)**
```bash
ngrok http 8000
```

**Terminal 5: Start Frontend (local development)**
```bash
cd healthpilot-frontend
npm run dev
```

### **5. Access the Application**

#### **Local Development**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

#### **Hybrid Deployment (Current)**
- **Frontend**: https://healthpilot-frontend-d89nr9jv3-aakashs-projects-9460ac97.vercel.app
- **Backend**: Running locally with ngrok tunnel
- **Status**: ✅ Deployed, ⚠️ File upload needs debugging

## 🚀 **Quick Start**

### **Using the Start Script**
For easy setup, use the provided start script:
```bash
chmod +x start.sh
./start.sh
```

This script will:
- Check prerequisites (Node.js, Python, Ollama, Redis)
- Set up virtual environment
- Install dependencies
- Start Ollama and Redis
- Provide instructions for starting backend and frontend

## 📁 **Project Structure**

```
HealthPilot/
├── healthpilot-frontend/          # Next.js frontend
│   ├── src/
│   │   ├── app/                   # App Router pages
│   │   ├── components/            # React components
│   │   ├── contexts/              # React contexts
│   │   ├── lib/                   # Utilities
│   │   └── types/                 # TypeScript types
│   ├── public/                    # Static assets
│   └── package.json
├── healthpilot-backend/           # FastAPI backend
│   ├── app/
│   │   ├── main.py               # FastAPI application
│   │   ├── models.py             # Data models
│   │   ├── database.py           # Database service
│   │   ├── auth.py               # Authentication
│   │   ├── upload_service.py     # File upload handling
│   │   ├── ai_analysis_service.py # AI analysis
│   │   ├── email_service.py      # Email notifications
│   │   └── worker.py             # Background jobs
│   ├── requirements/
│   │   └── requirements.txt      # Python dependencies
│   └── uploads/                  # File storage
├── start.sh                      # Quick start script
├── README.md                     # This file
├── .gitignore                    # Git ignore rules
└── deploy.sh                     # Deployment script
```

## 🎯 **Key Features**

### **🔐 Authentication**
- User registration and login
- Secure session management
- Profile management

### **📁 File Upload**
- Support for multiple file formats (PDF, JPG, PNG)
- OCR text extraction
- File validation and processing

### **🤖 AI Analysis**
- Intelligent lab result interpretation
- Risk level assessment (LOW/MODERATE/HIGH)
- Plain-English explanations
- Personalized recommendations

### **📊 Report Management**
- View analysis history
- Download PDF reports
- Email report sharing
- Delete reports

### **📧 Email Integration**
- Send reports via email
- Professional email templates
- PDF attachments

### **⚡ Background Processing**
- Asynchronous file processing
- Job status tracking
- Error handling and retries

## 🚀 **Deployment**

### **Current Deployment**
The application is currently deployed using a hybrid approach:
- **Frontend**: Hosted on Vercel (free tier)
- **Backend**: Running locally with ngrok tunnel
- **Database**: Supabase (free tier)
- **AI**: Ollama (local, free)

### **Deployment URLs**
- **Production Frontend**: https://healthpilot-frontend-d89nr9jv3-aakashs-projects-9460ac97.vercel.app
- **Backend Tunnel**: https://dac0ce69ae25.ngrok-free.app

### **Known Issues**
- ⚠️ **File Upload**: CORS and endpoint issues need debugging
- ✅ **Authentication**: Working with Supabase
- ✅ **Dashboard**: Loading and displaying data
- ✅ **Email**: Modal-based email functionality
- ✅ **Download**: PDF report generation

## 🧪 **Testing**

### **Backend Tests**
```bash
cd healthpilot-backend
python -m pytest tests/
```

### **Frontend Tests**
```bash
cd healthpilot-frontend
npm test
```

## 🚀 **Development**

### **Adding New Features**
1. **Backend**: Add endpoints in `app/main.py`
2. **Frontend**: Add pages in `src/app/`
3. **Components**: Create reusable components in `src/components/`
4. **Styling**: Use Tailwind CSS classes

### **Database Changes**
1. Create migration in `supabase/migrations/`
2. Update models in `app/models.py`
3. Test with sample data

### **AI Improvements**
1. Modify prompts in `app/ai_analysis_service.py`
2. Test with different lab report formats
3. Optimize for accuracy and speed

## 📚 **Learning Outcomes**

### **Technical Skills Gained**
- **Full-Stack Development**: End-to-end application building
- **AI Integration**: Practical ML/AI implementation
- **Database Design**: Schema design and optimization
- **API Development**: RESTful API design
- **File Processing**: Multi-format file handling
- **Background Jobs**: Asynchronous processing
- **Real-time Features**: WebSocket implementation
- **Security**: Authentication and authorization

### **Soft Skills Developed**
- **Problem Solving**: Identifying and solving real user needs
- **User Experience**: Designing intuitive interfaces
- **Documentation**: Writing clear technical documentation
- **Testing**: Error handling and edge cases
- **Project Management**: Organizing complex features

## 🎓 **About the Developer**

This project was developed by a second-year McMaster Software Engineering student as a comprehensive learning experience in modern web development. The goal was to create a practical application that solves real-world problems while demonstrating proficiency in current technologies and best practices.

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 **Support**

For questions or support, please open an issue on GitHub or contact the developer.

---

**Built with ❤️ by a McMaster Software Engineering student**
