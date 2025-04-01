
import os
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel,DuckDuckGoSearchTool

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the agent with OpenAI Server Model
agent = CodeAgent(tools=[DuckDuckGoSearchTool()],model=OpenAIServerModel(model_id="gpt-4-turbo", api_key=api_key))

# Run the agent with a prompt
response = agent.run("List the top AI breakthroughs of 2024.")
print(response)
