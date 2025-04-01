from fastapi import APIRouter, Body
from pydantic import BaseModel

# Import your generate_qa function
from src.crews.qa_crew import generate_qa  # Replace with your actual module name

router = APIRouter()

# Request model
class QAGenerateRequest(BaseModel):
    topic: str
    num_questions: int = 5

@router.post("/generate-qa")
async def generate_qa_endpoint(request: QAGenerateRequest = Body(...)):  # ✅ Add Body(...)
    try:
        # Call the function with request data
        result = generate_qa(request.topic, request.num_questions)
        return {"success": True, "data": result}
    except ValueError as e:
        return {"success": False, "error": str(e)}
