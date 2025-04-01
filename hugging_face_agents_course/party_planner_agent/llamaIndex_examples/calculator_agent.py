import os
import asyncio
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent

# Load the .env file
load_dotenv()

# Retrieve OpenAI API Key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI LLM
llm = OpenAI(
    model="gpt-4-turbo",
    temperature=0.7,
    max_tokens=100,
    api_key=openai_api_key
)

# Define some tools
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

# Dummy query engine tool (replace with actual implementation)
def query_engine_tool(query: str) -> str:
    """Simulates a query engine tool for information lookup."""
    return f"Simulated response for query: {query}"

# Create agent configs
calculator_agent = ReActAgent(
    name="calculator",
    description="Performs basic arithmetic operations",
    system_prompt="You are a calculator assistant. Use your tools for any math operation.",
    tools=[add, subtract],
    llm=llm,
)

query_agent = ReActAgent(
    name="info_lookup",
    description="Looks up information about XYZ",
    system_prompt="Use your tool to query a RAG system to answer information about XYZ",
    tools=[query_engine_tool],
    llm=llm
)

# Create the workflow
agent_workflow = AgentWorkflow(
    agents=[calculator_agent, query_agent], root_agent="calculator"
)

# Function to run the async function properly
def run_agent():
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(agent_workflow.run(user_msg="Can you add 5 and 3?"))
    print(response)

# Execute
run_agent()
