import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from crewai import Agent, Task, Crew
from crewai.tasks.output_format import OutputFormat

# Define Task Output Model (Based on TaskOutput structure)
class QAOutputModel(BaseModel):
    """Structured Output Model for QA Task."""
    
    topic: str = Field(description="Topic of the generated questions")
    questions: List[str] = Field(description="List of generated questions")
    answers: List[str] = Field(description="List of generated answers")

    @field_validator("questions", "answers", mode="before")
    def validate_non_empty(cls, value):
        if not value or not isinstance(value, list):
            raise ValueError(f"{cls.__name__} must have a non-empty list.")
        return value

# Extend TaskOutput for consistency
class QATaskOutput(QAOutputModel):
    """Extended Task Output including metadata."""
    
    description: str = Field(description="Description of the task")
    summary: Optional[str] = Field(description="Summary of the task", default=None)
    raw: str = Field(description="Raw output of the task", default="")
    json_dict: Optional[Dict[str, Any]] = Field(description="JSON dictionary of task", default=None)
    agent: str = Field(description="Agent that executed the task")
    output_format: OutputFormat = Field(description="Output format of the task", default=OutputFormat.RAW)

    @model_validator(mode="after")
    def set_summary(self):
        """Generate a summary based on the description."""
        excerpt = " ".join(self.description.split(" ")[:10])
        self.summary = f"{excerpt}..."
        return self

    @property
    def json(self) -> str:
        """Return JSON output if format is correct."""
        if self.output_format != OutputFormat.JSON:
            raise ValueError("Invalid output format requested. Please set output_format to JSON.")
        return json.dumps(self.json_dict or {})

    def to_dict(self) -> Dict[str, Any]:
        """Convert structured output to a dictionary."""
        return self.model_dump()

# Define Agents
question_agent = Agent(
    role="Question Generator",
    goal="Generate relevant and insightful questions for a given topic.",
    backstory="An AI research assistant trained to formulate structured and meaningful questions.",
    verbose=True
)

answer_agent = Agent(
    role="Answer Generator",
    goal="Provide clear and accurate answers based on the generated questions.",
    backstory="An AI-powered knowledge expert capable of answering diverse queries concisely.",
    verbose=True
)

# Define Tasks with Pydantic Output
def expected_output(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Dynamically generate expected output."""
    return {
        "topic": inputs["topic"],
        "questions": [f"Generated question {i+1}" for i in range(inputs["num_questions"])],
        "answers": [f"Answer to question {i+1}" for i in range(inputs["num_questions"])]
    }

qa_task = Task(
    description="Generate {num_questions} questions for the topic: {topic}, then provide detailed answers.",
    agent=question_agent,
    output_pydantic=QATaskOutput,
    expected_output=json.dumps(expected_output({"topic": "Example", "num_questions": 5}))  # Ensure string format
)

# Define Crew
qa_crew = Crew(
    agents=[question_agent, answer_agent],
    tasks=[qa_task],
    process="sequential"
)

# Function to Execute Crew & Return Structured JSON
def generate_qa(topic: str, num_questions: int = 5):
    if not topic:
        raise ValueError("Missing required parameter: topic")

    if not (1 <= num_questions <= 20):
        raise ValueError("Number of questions must be between 1 and 20.")

    # Execute the crew with inputs
    result = qa_crew.kickoff(inputs={"topic": topic, "num_questions": num_questions})

    # Ensure the result is in structured format
    if isinstance(result, QATaskOutput):
        return result.to_dict()  # Ensures consistent output

    # 🔹 Fix: Convert `raw` to a dict if it's a stringified JSON
    if hasattr(result, "raw") and isinstance(result.raw, str):
        try:
            return json.loads(result.raw)  # Convert raw JSON string to dict
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in raw output"}

    return {}  # Default return for unknown cases

# Example Execution
if __name__ == "__main__":
    topic = "Artificial Intelligence"
    num_questions = 3
    output = generate_qa(topic, num_questions)
    print(json.dumps(output, indent=4))
