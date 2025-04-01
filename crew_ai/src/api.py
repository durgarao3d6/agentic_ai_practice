import json
from fastapi import APIRouter, Body
from pydantic import BaseModel

# Import your function
from src.crews.qa_crew import generate_qa  

router = APIRouter()

# Define response model
class QAResponse(BaseModel):
    success: bool
    data: dict | None = None  # Ensure it's a dict, not a string
    error: str | None = None

# Request model
class QAGenerateRequest(BaseModel):
    topic: str
    num_questions: int = 5

@router.post("/generate-qa", response_model=QAResponse)
async def generate_qa_endpoint(request: QAGenerateRequest = Body(...)):
    try:
        result = generate_qa(request.topic, request.num_questions)

        # Ensure 'result' is a dictionary, not a string
        if isinstance(result, str):
            try:
                result = json.loads(result)  # Convert JSON string to dictionary
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format returned from generate_qa")

        return QAResponse(success=True, data=result)
    
    except ValueError as e:
        return QAResponse(success=False, error=str(e))
