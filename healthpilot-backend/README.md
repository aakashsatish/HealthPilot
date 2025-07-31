# HealthPilot Backend

Blood test report analysis API service.

## Setup

1. Create virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements/requirements.txt`
4. Run: `uvicorn app.main:app --reload`

## Endpoints

- `GET /health` - Health check
- `GET /` - Root endpoint
- `GET /docs` - API documentation