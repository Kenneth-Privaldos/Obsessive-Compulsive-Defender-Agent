# Audited file: removed unused imports and added comments for clarity

# Standard library
import datetime  # used for timestamps
import os
import sys

# Ensure parent directory is on sys.path so local packages (e.g., Conversation_Agent, sub_agents) can be imported.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# ADK / Google imports (only the ones actually referenced in this file)
# LlmAgent is used to create the conversation agent.
from google.adk.agents import LlmAgent
# ToolContext is used for typing and runtime access to the agent's state in logger_tool.
from google.adk.tools.tool_context import ToolContext
# AgentTool wraps sub-agents so they are usable as tools by the LlmAgent.
from google.adk.tools.agent_tool import AgentTool

# typing
from typing import Dict, Any

# Local project import: instruction text for the conversation agent.
from Conversation_Agent.prompt import Conversation_agent_instruction as instruction

print("✅ ADK components imported successfully.")

def logger_tool(theme: str, confidence: int, emotion: str, intensity: int, note: str, raw_message: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Saves a consented log entry with its classified metadata to a persistent store (in-memory here).

    Args:
        theme: The main theme of the user's message.
        confidence: Confidence (e.g., classifier confidence) for the theme classification.
        emotion: The dominant emotion expressed.
        intensity: The emotional intensity (1-10).
        note: A short summary of the message content.
        raw_message: The original user input for context.
        tool_context: ADK-provided context object that contains runtime state.

    Returns:
        A dict with a "result" message. (Runtimes may expect additional keys such as "stateDelta".)
    """

    # Build a structured log entry. Use isoformat() to create a human-readable timestamp.
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),  # local time ISO timestamp
        "theme": theme,
        "theme classification confidence": confidence,
        "emotion": emotion,
        "intensity": intensity,
        "note": note,
        "user_message": raw_message
    }

    # ----------------------------
    # 2. STATE LOGIC (In-Memory Memory)
    # ----------------------------
    # Defensive check: ensure the state dict exists before indexing into it.
    # The ADK's ToolContext typically provides a .state mapping for persisting small pieces of state.
    if "recent_logs" not in tool_context.state:
        # Initialize as a list if missing.
        tool_context.state["recent_logs"] = []

    recent_logs = tool_context.state["recent_logs"]

    # Here we're checking the full dict `log_entry` for membership. This avoids exact-duplicate dict entries.
    # Note: If you only want to dedupe based on theme or timestamp, adjust this comparison accordingly.
    if log_entry not in recent_logs:
        recent_logs.append(log_entry)
        tool_context.state["recent_logs"] = recent_logs

    # Return payload — ADK runtimes sometimes expect a stateDelta key as well.
    # If you find state is not persisting, return something like:
    # {"result": ..., "stateDelta": {"recent_logs": [log_entry]}}
    return {
        "result": f"Log entry for '{theme}' successfully saved."
    }

# Sub-agent imports (these wrap smaller agent behaviors into tools).
# These imports reference local modules under sub_agents/.
from sub_agents.classifier_agent.agent import Classification_Agent
from sub_agents.summarizer_agent.agent import Summarizer_Agent

# Wrap the sub-agents in AgentTool so the LLM agent can call them like tools.
classification_tool = AgentTool(agent=Classification_Agent)
summarizer_tool = AgentTool(agent=Summarizer_Agent)

# Create the conversation agent.
# - model: the model id used for the agent's LLM.
# - instruction: the system/prompt instruction for the agent's behavior.
# - tools: provides the agent access to the classification and summarizer sub-agents, plus the logger_tool.
Conversation_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='Conversation_Agent',
    description="The user-facing agent. Friendly, supportive, and non-judgmental.",
    instruction=instruction,
    output_key="response",
    tools=[classification_tool, summarizer_tool, logger_tool],
)

# Expose the root agent variable for the rest of the application to use.
root_agent = Conversation_agent
