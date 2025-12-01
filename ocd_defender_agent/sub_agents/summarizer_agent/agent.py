# Add parent directory so local modules (e.g., summarizer_agent/) can be imported.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# ADK import: Only LlmAgent is used here, so all other unused imports were removed.
from google.adk.agents.llm_agent import LlmAgent

# Local project import: instruction text for the summarizer agent.
from summarizer_agent.prompt import Summarizer_instruction_prompt as prompt


# Create the Summarizer Agent.
# - This agent takes anonymized recent logs and produces summaries, themes, and insights.
Summarizer_Agent = LlmAgent(
    model='gemini-2.5-flash',    # LLM model to use
    name="summarizer_agent",     # Unique name for this agent
    description=(
        "Summarize recent anonymized log entries and surface "
        "common themes, counts, trends, and short insights."
    ),
    instruction=prompt,           # System-style instruction for behavior
    output_key="summarizer_result",  # Where the agent's output will be stored
)
