from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.routers import detection, auth, sessions
from app.core.config import settings
from app.core.database import init_supabase
from app.services.pose_estimator import PoseEstimator
from app.services.muscle_classifier import MuscleClassifier

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting MuscleVision Backend...")
    
    # Initialize Supabase connection
    await init_supabase()
    
    # Initialize CV models
    app.state.pose_estimator = PoseEstimator()
    app.state.muscle_classifier = MuscleClassifier()
    
    print("✅ Backend initialized successfully!")
    yield
    
    # Shutdown
    print("🛑 Shutting down MuscleVision Backend...")

app = FastAPI(
    title="MuscleVision API",
    description="Computer vision backend for muscle detection and form analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://musclevision.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for session outputs
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(detection.router, prefix="/api/detection", tags=["Detection"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])

@app.get("/")
async def root():
    return {
        "message": "MuscleVision API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": ["pose_estimation", "muscle_classification", "supabase"]}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 