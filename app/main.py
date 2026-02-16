from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routers import candidates

# The FastAPI instance MUST be named 'app' (this is required)
app = FastAPI(
    title="Resume Management API",
    description="API for managing candidate resumes (In-Memory Storage)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(candidates.router)

# Mount uploads directory
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def root():
    return {
        "message": "Resume Management API",
        "version": "1.0.0",
        "storage": "In-Memory (No Database)",
        "endpoints": {
            "POST /api/candidates": "Upload new candidate with resume",
            "GET /api/candidates": "List candidates with filters",
            "GET /api/candidates/{id}": "Get candidate by ID",
            "PUT /api/candidates/{id}": "Update candidate",
            "DELETE /api/candidates/{id}": "Delete candidate",
            "GET /health": "Health check"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}