from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import FreelancerProfile, ProposalRequest, ProposalResponse
from .rag_system import SmartProposalSystem
from typing import List, Dict, Any
import os

app = FastAPI(title="Swiftme Mini - Job Proposal Generator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the system
proposal_system = SmartProposalSystem()

@app.get("/")
async def root():
    return {"message": "Swiftme Mini Job Proposal Generator API"}

@app.post("/api/profile/setup")
async def setup_profile(profile: FreelancerProfile):
    """Setup freelancer profile"""
    try:
        profile_data = profile.dict()
        profile_id = proposal_system.setup_profile(profile_data)
        return {
            "message": "Profile setup successfully",
            "profile_id": profile_id,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile setup failed: {str(e)}")

@app.post("/api/proposal/generate", response_model=ProposalResponse)
async def generate_proposal(request: ProposalRequest):
    """Generate proposal for job posting"""
    try:
        response = proposal_system.generate_proposal(
            job_posting=request.job_posting,
            tone=request.tone or "professional"
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proposal generation failed: {str(e)}")

@app.get("/api/proposal/history")
async def get_proposal_history():
    """Get last 5 generated proposals"""
    try:
        history = proposal_system.get_proposal_history()
        return {
            "proposals": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Swiftme Mini API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)