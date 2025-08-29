# 🏥 HealthPilot: AI-Powered Lab Report Analysis

## 📋 **Project Overview**

HealthPilot is a personal project born from my own frustration with medical lab reports. Like many people, I found myself staring at pages of complex medical terminology, unclear reference ranges, and results that left me wondering: "Should I be worried? What does this actually mean for my health?"

This project is my solution to that problem. I built HealthPilot to translate those confusing lab reports into clear, understandable insights that actually help people make informed decisions about their health.

## 🎯 **The Problem I'm Solving**

I created this because I, like many others, have struggled with:
- **Complex medical jargon** that makes lab reports feel like reading a foreign language
- **Unclear reference ranges** that don't explain what "normal" actually means for me
- **Lack of context** - results without explanations of what they indicate about my health
- **Anxiety and uncertainty** about whether I should be concerned or not

HealthPilot transforms this confusion into clarity by providing:
- **Plain-English explanations** of what each result actually means
- **Personalized risk assessments** (LOW/MODERATE/HIGH) so you know what to focus on
- **Actionable recommendations** based on your specific results
- **Professional PDF reports** you can share with healthcare providers

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Services   │
│ (Next.js/React) |◄──►│   (FastAPI)     │◄──►│   (Ollama)      │
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
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Terminal 4: Start Frontend**
```bash
cd healthpilot-frontend
npm run dev
```

### **5. Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

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

## ⚠️ **Known Issues**

### **Current Status**
- ⚠️ **File Upload**: CORS and endpoint issues need debugging
- ✅ **Authentication**: Working with Supabase
- ✅ **Dashboard**: Loading and displaying data
- ✅ **Email**: Modal-based email functionality
- ✅ **Download**: PDF report generation

### **Deployment**
- **Frontend**: https://healthpilot-frontend-d89nr9jv3-aakashs-projects-9460ac97.vercel.app
- **Backend**: Running locally with ngrok tunnel
- **Status**: ✅ Deployed, ⚠️ File upload needs debugging

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

I'm a second-year McMaster Software Engineering student who built this project because I genuinely needed it. After getting my own lab results and feeling completely lost trying to understand them, I decided to create something that would help not just me, but anyone who's ever felt overwhelmed by medical jargon.

This project represents my journey into full-stack development, AI integration, and building solutions for real problems that affect real people. It's not just a portfolio piece - it's something I actually use and want to share with others who face the same challenges I did.

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
