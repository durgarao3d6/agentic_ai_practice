import os
from dotenv import load_dotenv
from smolagents import ToolCallingAgent, DuckDuckGoSearchTool, OpenAIServerModel

# Load OpenAI API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API Model
model = OpenAIServerModel(model_id="gpt-4-turbo", api_key=api_key)

# Create the agent with OpenAI's model
agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model
)

# Run the agent with a query
response = agent.run("Search for the best music recommendations for a party at the Wayne's mansion.")

print(response)
