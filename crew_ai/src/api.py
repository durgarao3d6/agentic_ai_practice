from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from src.crew_setup import ResearchCrew  # Import your CrewSetup class

router = APIRouter()

class ResearchRequest(BaseModel):
    topic: str = "AI trends"  # Default topic

@router.post("/run-research")
async def run_research(request: ResearchRequest):
    """API endpoint to trigger research"""
    try:
        crew_instance = ResearchCrew(request.topic)
        result = crew_instance.crew().kickoff()
        return {"topic": request.topic, "summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
