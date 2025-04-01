
from smolagents import CodeAgent, OpenAIServerModel, DuckDuckGoSearchTool, tool, Tool

# Let's pretend we have a function that fetches the highest-rated catering services.
@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.

    Args:
        query: A search term for finding catering services.
    """
    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }

    # Find the highest-rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)

    return best_service

# Set up the agent using OpenAIServerModel for OpenAI interaction
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(), catering_service_tool],  # Add both DuckDuckGo search and the catering service tool
    model=OpenAIServerModel(model_id="gpt-3.5-turbo")  # Using the latest supported OpenAI model
)

# Run the agent to find the best catering service
result = agent.run(
    "Can you give me the name of the highest-rated catering service in Gotham City?"
)

# Output the result from OpenAI via the agent
print(result)  # Expected output: "Gotham Catering Co."
