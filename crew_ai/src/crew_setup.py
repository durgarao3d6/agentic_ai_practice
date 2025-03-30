import os
import sys
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()



class ResearchCrew:
    """A crew for research tasks on a specific topic."""

    def __init__(self, topic: str):
        self.topic = topic
        self.serper_tool = SerperDevTool()

    def researcher(self) -> Agent:
        """The researcher agent."""
        return Agent(
            name="Researcher",
            role="AI Researcher",
            goal=f"Find the latest updates on {self.topic} using web search.",
            backstory="A dedicated researcher with expertise in AI and technology.",
            tools=[self.serper_tool],  # Ensure tool is passed correctly
            verbose=True,
        )

    def reporting_analyst(self) -> Agent:
        """The reporting analyst agent."""
        return Agent(
            name="Reporting Analyst",
            role="Data Analyst",
            goal=f"Analyze the research findings on {self.topic} and generate insights.",
            backstory="An analytical expert experienced in summarizing research trends.",
            verbose=True,
        )

    def research_task(self, researcher: Agent) -> Task:
        """Task for the researcher"""
        return Task(
            description=f"Find the top 5 recent developments in {self.topic}.",
            expected_output=f"A structured list of the latest news, trends, and articles on {self.topic}.",
            agent=researcher,
        )

    def analysis_task(self, analyst: Agent) -> Task:
        """Task for the reporting analyst"""
        return Task(
            description=f"Analyze the research findings on {self.topic} and provide a structured report.",
            expected_output=f"A detailed report summarizing key insights, trends, and takeaways on {self.topic}.",
            agent=analyst,
        )

    def crew(self) -> Crew:
        """Creates and runs the crew"""
        researcher = self.researcher()
        analyst = self.reporting_analyst()

        return Crew(
            agents=[researcher, analyst],
            tasks=[self.research_task(researcher), self.analysis_task(analyst)],
            process=Process.sequential,
            verbose=True,
        )


if __name__ == "__main__":
    crew_instance = ResearchCrew()
    result = crew_instance.crew().kickoff()
    print("\nFinal Research Summary:\n", result)
