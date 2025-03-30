import uuid
import os
import asyncio
import json
import logging
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from crewai.flow.flow import Flow, listen, start
from crewai import LLM
from src.crews.content_crew.content_crew import ContentCrew
import concurrent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Define Models
class Section(BaseModel):
    title: str
    description: str

class GuideOutline(BaseModel):
    title: str
    introduction: str
    target_audience: str
    sections: List[Section]
    conclusion: str

class GuideRequest(BaseModel):
    topic: str
    audience_level: str

class GuideResponse(BaseModel):
    message: str
    guide_path: str

OUTPUT_DIR = "output"
# Store task statuses and results
tasks = {}  # {task_id: "processing" | "completed" | "failed"}
task_results = {}  # {task_id: "file_path"}

def load_existing_guides():
    """Load previously saved guides and their metadata on startup."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".md"):
            task_id = filename.replace(".md", "")
            task_results[task_id] = os.path.join(OUTPUT_DIR, filename)
            tasks[task_id] = "completed"

            # Load title from metadata JSON file
            metadata_path = os.path.join(OUTPUT_DIR, f"{task_id}.json")
            if os.path.exists(metadata_path):
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    task_titles[task_id] = metadata.get("title", "Untitled Guide")  # Store title
            else:
                task_titles[task_id] = "Untitled Guide"  # Fallback if metadata is missing

# Call this function at startup
task_titles = {}  # Store task_id -> title mapping
load_existing_guides()


# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Guide Flow Definition
class GuideCreatorState(BaseModel):
    topic: str = ""
    audience_level: str = ""
    guide_outline: Optional[GuideOutline] = None
    sections_content: Dict[str, str] = {}

class GuideCreatorFlow(Flow[GuideCreatorState]):
    """Flow for creating a guide"""

    @start()
    def get_user_input(self):
        """Initialize flow with user input"""
        return self.state

    @listen(get_user_input)
    def create_guide_outline(self, state):
        """Generate guide outline using LLM"""
        llm = LLM(model="openai/gpt-4o-mini", response_format=GuideOutline)

        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"""
            Create a detailed outline for a guide on "{state.topic}" for {state.audience_level} learners.
            """}
        ]

        response = llm.call(messages=messages)

        try:
            outline_dict = json.loads(response)
            self.state.guide_outline = GuideOutline(**outline_dict)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from LLM: {response}, error: {str(e)}")
            raise ValueError("Invalid response from LLM")

        return self.state.guide_outline

    @listen(create_guide_outline)
    async def write_and_compile_guide(self, outline):
        """Generate complete guide content"""
        sections_content = {}

        async def process_section(section):
            """Async processing of sections"""
            try:
                result = await asyncio.to_thread(ContentCrew().crew().kickoff, {
                    "section_title": section.title,
                    "section_description": section.description,
                    "audience_level": self.state.audience_level,
                    "draft_content": "",
                    "previous_sections": "No previous sections", 
                })
                return section.title, result.raw
            except Exception as e:
                logger.error(f"Error processing section '{section.title}': {str(e)}")
                return section.title, f"Error generating content: {str(e)}"

        section_tasks = [process_section(section) for section in outline.sections]
        results = await asyncio.gather(*section_tasks)

        for title, content in results:
            sections_content[title] = content

        guide_content = f"# {outline.title}\n\n## Introduction\n\n{outline.introduction}\n\n"
        for section in outline.sections:
            guide_content += f"## {section.title}\n\n{sections_content.get(section.title, '')}\n\n"
        guide_content += f"## Conclusion\n\n{outline.conclusion}\n\n"

        return guide_content  # Return guide content instead of writing file here

import json

# async def kickoff_guide(request: GuideRequest, task_id: str):
#     """Kick off guide creation process and store metadata with title"""
#     flow = GuideCreatorFlow()
#     flow.state.topic = request.topic
#     flow.state.audience_level = request.audience_level

#     try:
#         # Run flow.kickoff() in a separate process
#         loop = asyncio.get_running_loop()
#         with concurrent.futures.ThreadPoolExecutor() as pool:
#             guide_content = await loop.run_in_executor(pool, flow.kickoff)

#         # Save guide content to file
#         guide_path = os.path.join(OUTPUT_DIR, f"{task_id}.md")
#         with open(guide_path, "w", encoding="utf-8") as f:
#             f.write(guide_content)

#         # Extract title from first line of content
#         title = guide_content.split("\n")[0].replace("# ", "").strip() or "Untitled Guide"

#         # Save metadata with title
#         metadata_path = os.path.join(OUTPUT_DIR, f"{task_id}.json")
#         metadata = {"task_id": task_id, "title": title}

#         with open(metadata_path, "w", encoding="utf-8") as f:
#             json.dump(metadata, f)

#         logger.info(f"Metadata saved: {metadata_path} -> {metadata}")

#         # Update task tracking
#         tasks[task_id] = "completed"
#         task_results[task_id] = guide_path  # Store the guide path
#     except Exception as e:
#         tasks[task_id] = "failed"
#         logger.error(f"Error in kickoff_guide: {str(e)}")

async def kickoff_guide(request: GuideRequest, task_id: str):
    """Kick off guide creation process and store metadata with title"""
    flow = GuideCreatorFlow()
    flow.state.topic = request.topic
    flow.state.audience_level = request.audience_level

    try:
        # Run flow.kickoff() in a separate thread
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            guide_content = await loop.run_in_executor(pool, flow.kickoff)

        # Save guide content to file
        guide_path = os.path.join(OUTPUT_DIR, f"{task_id}.md")
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(guide_content)

        # Extract title from first line of content
        title = guide_content.split("\n")[0].replace("# ", "").strip() or "Untitled Guide"

        # Save metadata with title
        metadata_path = os.path.join(OUTPUT_DIR, f"{task_id}.json")
        metadata = {
            "task_id": task_id,
            "title": title,
            "topic": request.topic,
            "audience_level": request.audience_level,
        }

        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f)

        logger.info(f"Metadata saved: {metadata_path} -> {metadata}")

        # Update tracking dictionaries
        tasks[task_id] = "completed"
        task_results[task_id] = guide_path  # Store the guide path
        task_titles[task_id] = title  # Store the guide title

    except Exception as e:
        tasks[task_id] = "failed"
        logger.error(f"Error in kickoff_guide: {str(e)}")

@router.post("/create_guide/", response_model=Dict[str, str])
async def create_guide(request: GuideRequest, background_tasks: BackgroundTasks):
    """Start the guide creation and return a task ID"""
    task_id = str(uuid.uuid4())  # Generate unique task ID
    tasks[task_id] = "processing"

    background_tasks.add_task(kickoff_guide, request, task_id)

    return {"message": "Guide creation started", "task_id": task_id}

@router.get("/task_status/{task_id}", response_model=Dict[str, str])
async def get_task_status(task_id: str):
    """Check the status of the guide creation process"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task ID not found")
    return {"task_id": task_id, "status": tasks[task_id]}

@router.get("/download/{task_id}")
async def download_guide(task_id: str):
    """Download the completed guide"""
    if task_id not in task_results:
        raise HTTPException(status_code=404, detail="Guide not found or still processing")
    guide_path = task_results[task_id]
    if not os.path.exists(guide_path):
        raise HTTPException(status_code=500, detail="Guide file missing")
    return FileResponse(guide_path, filename=f"{task_id}.md", media_type="text/markdown")

@router.get("/list_guides", response_model=List[Dict[str, str]])
async def list_guides():
    """List all completed guides with their titles."""
    guide_list = []
    logger.info(f"Task Titles Updated: {json.dumps(task_titles, indent=2)}")
    for task_id, file_path in task_results.items():
        guide_list.append({
            "task_id": task_id,
            "title": task_titles.get(task_id, "Untitled Guide"),  # Get title from metadata
            "file": os.path.basename(file_path),
        })

    return guide_list

@router.get("/guide_content/{task_id}", response_model=Dict[str, str])
async def get_guide_content(task_id: str):
    """Fetch the guide content as plain text"""
    if task_id not in task_results:
        raise HTTPException(status_code=404, detail="Guide not found or still processing")

    guide_path = task_results[task_id]
    if not os.path.exists(guide_path):
        raise HTTPException(status_code=500, detail="Guide file missing")

    with open(guide_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {"task_id": task_id, "content": content}

