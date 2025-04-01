import os
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel
import datetime

# Load OpenAI API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI model
model = OpenAIServerModel(model_id="gpt-4-turbo", api_key=api_key)

# Create agent with OpenAI
agent = CodeAgent(tools=[], model=model, additional_authorized_imports=['datetime'])

# Run the agent with a time calculation task
response = agent.run(
    """
    Alfred needs to prepare for the party. Here are the tasks:
    1. Prepare the drinks - 30 minutes
    2. Decorate the mansion - 60 minutes
    3. Set up the menu - 45 minutes
    4. Prepare the music and playlist - 45 minutes

    If we start right now, at what time will the party be ready?
    """
)

print(response)


