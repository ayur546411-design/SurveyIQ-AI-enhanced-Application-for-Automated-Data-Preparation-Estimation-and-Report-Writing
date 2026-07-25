from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from APIs.survey_routes import router as survey_router

app = FastAPI(title="SurveyIQ API", description="Backend for SurveyIQ Application")

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Vite default port
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure reports directory exists
REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

# Mount static reports directory so frontend can download files
app.mount("/reports", StaticFiles(directory=REPORTS_DIR), name="reports")

# Include the API router
app.include_router(survey_router, prefix="/api", tags=["survey"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the SurveyIQ API"}
