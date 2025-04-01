import os
from huggingface_hub import login
from dotenv import load_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

# Load environment variables from .env file
load_dotenv()

# Retrieve the Hugging Face token
hf_token = os.getenv("HF_TOKEN")

# Login using the token
login(token=hf_token)


agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())

agent.run("Search for the best music recommendations for a party at the Wayne's mansion.")

# publishing agent to hub
# Change to your username and repo name
agent.push_to_hub('sergiopaniego/AlfredAgent')
# Change to your username and repo name
alfred_agent = agent.from_hub('sergiopaniego/AlfredAgent', trust_remote_code=True)

alfred_agent.run("Give me the best playlist for a party at Wayne's mansion. The party idea is a 'villain masquerade' theme")  