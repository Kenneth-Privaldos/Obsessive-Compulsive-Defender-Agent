# Add parent directory to Python path so local modules (e.g., classifier_agent/) can be imported.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# ADK import: Only LlmAgent is required here.
from google.adk.agents.llm_agent import LlmAgent

# Local project import: instruction text for the classifier agent.
from classifier_agent.prompt import Classification_agent_instruction as prompt


# Create the Classification Agent.
# - This agent categorizes intrusive thoughts into predefined theme labels.
Classification_Agent = LlmAgent(
    model='gemini-2.5-flash',     # LLM model to use
    name="classification_agent",  # Unique agent ID ph
    description="Classify intrusive thought into a discrete theme.",
    instruction=prompt,           # System/prompt instruction for agent behavior
    output_key="classification_result",  # Key where the agent's output will be placed
)
