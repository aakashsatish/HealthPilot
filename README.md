# HealthPilot 🏥

*A comprehensive lab report analysis platform that translates complex medical information into understandable insights*

## The Problem I Wanted to Solve

As a second-year Software Engineering student at McMaster University, I noticed that many people around me (including myself) struggled to understand their medical lab reports. These reports are filled with complex medical terminology, reference ranges, and values that most people can't interpret on their own. This creates a significant barrier to understanding one's own health status. 

**The Challenge**: Lab reports contain crucial health information, but they're written in complex medical terms that is  inaccessible to the average person. This leads to:
- Confusion and anxiety about health status
- Difficulty making informed health decisions
- Reliance on healthcare providers for basic interpretation
- Missed opportunities for proactive health management

## My Solution: HealthPilot

HealthPilot is a full-stack web application that uses AI to analyze lab reports and provide clear, understandable explanations. It's designed to bridge the gap between complex medical data and everyday health understanding.

### Key Features:
- **AI-Powered Analysis**: Uses local LLM (Llama 3.1) to interpret lab results
- **Smart OCR**: Extracts data from uploaded lab report images
- **Comprehensive Explanations**: Provides context, normal ranges, and health implications
- **Email Reports**: Sends detailed analysis directly to users
- **User-Friendly Interface**: Clean, modern UI that anyone can use

## Technologies & Skills I Learned

### Backend Development (Python/FastAPI)
- **FastAPI Framework**: Built a robust REST API with automatic documentation
- **Database Integration**: Implemented Supabase for user management and data storage
- **AI/ML Integration**: Integrated local Ollama server with Llama 3.1 model
- **OCR Processing**: Used Tesseract for extracting text from lab report images
- **Background Jobs**: Implemented Redis + RQ for asynchronous processing
- **Email Services**: Set up SMTP integration for report delivery

### Frontend Development (Next.js/React)
- **Modern React**: Built with Next.js 14 and App Router
- **TypeScript**: Implemented type safety throughout the application
- **Tailwind CSS**: Created responsive, modern UI components
- **Authentication**: Integrated Supabase Auth for user management
- **File Upload**: Built drag-and-drop file upload with progress tracking
- **State Management**: Used React Context for global state management

### DevOps & Infrastructure
- **Environment Management**: Set up virtual environments and dependency management
- **API Documentation**: Auto-generated OpenAPI docs with FastAPI
- **Error Handling**: Implemented comprehensive error handling and logging
- **Security**: Added input validation and secure file handling

### Real-World Problem Solving
- **Requirements Analysis**: Identified user needs and pain points
- **System Design**: Architected a scalable solution
- **Testing**: Implemented unit tests and integration testing
- **Documentation**: Created comprehensive setup and usage guides

## Project Structure

```
HealthPilot/
├── healthpilot-backend/     # FastAPI backend service
│   ├── app/
│   │   ├── ai_analysis_service.py    # AI analysis logic
│   │   ├── ocr_service.py           # Image text extraction
│   │   ├── email_service.py         # Email delivery
│   │   └── database.py              # Database operations
│   └── requirements/
├── healthpilot-frontend/    # Next.js frontend application
│   ├── src/
│   │   ├── app/             # Next.js app router
│   │   ├── components/      # Reusable UI components
│   │   └── lib/             # Utility functions
│   └── public/
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Redis server
- Ollama (for local AI processing)

### Backend Setup
```bash
cd healthpilot-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/requirements.txt
```

### Frontend Setup
```bash
cd healthpilot-frontend
npm install
npm run dev
```

### Start Services
```bash
# Start Ollama server
ollama serve

# Start Redis
redis-server

# Start backend
cd healthpilot-backend
source venv/bin/activate
uvicorn app.main:app --reload

# Start frontend
cd healthpilot-frontend
npm run dev
```

## What I Learned

This project taught me so much about real-world software development:

### Technical Skills
- **Full-Stack Development**: Building both frontend and backend from scratch
- **AI Integration**: Working with local LLMs and understanding AI capabilities
- **API Design**: Creating RESTful APIs with proper documentation
- **Database Design**: Understanding data relationships and storage
- **Security**: Implementing authentication and secure file handling

### Soft Skills
- **Problem Solving**: Breaking down complex problems into manageable pieces
- **User-Centered Design**: Thinking about how real people will use the application
- **Documentation**: Writing clear, comprehensive documentation
- **Testing**: Ensuring code quality and reliability
- **Project Management**: Organizing code and managing dependencies

### Real-World Impact
This project showed me how software engineering can directly improve people's lives. By making medical information more accessible, we can help people:
- Better understand their health
- Make more informed decisions
- Reduce anxiety about medical results
- Take a more proactive approach to health

## Future Enhancements

As I continue learning, I plan to add:
- **Mobile App**: React Native version for iOS/Android
- **Multi-language Support**: Support for different lab report formats
- **Advanced Analytics**: Trend analysis and health insights
- **Integration**: Connect with health tracking devices
- **Machine Learning**: Improve accuracy with more training data

## About Me

I'm a second-year Software Engineering student at McMaster University passionate about using technology to solve real-world problems. This project represents my journey from learning basic programming concepts to building a full-stack application that can actually help people.

**Skills Demonstrated:**
- Full-stack web development
- AI/ML integration
- Database design and management
- API development and documentation
- User interface design
- Problem-solving and critical thinking

---

*This project was created as part of my learning journey in software engineering. It's designed to tackle a real-world problem that affects many people - the difficulty of understanding medical lab reports. By combining modern web technologies with AI capabilities, I've created a solution that makes health information more accessible and understandable.*
