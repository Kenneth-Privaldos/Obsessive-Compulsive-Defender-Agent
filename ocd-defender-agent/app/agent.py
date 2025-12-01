# Standard library
import datetime  # used for timestamps

# ADK / Google imports (only the ones actually referenced in this file)
from google.adk.agents import LlmAgent  # used to create the Conversation agent
from google.adk.tools.function_tool import FunctionTool  # wraps consent_approval as a tool
from google.adk.tools.tool_context import ToolContext  # typing / runtime ToolContext object

# typing
from typing import Any, Dict

print("✅ ADK components imported successfully.")


def consent_approval(
    user_message: str, tool_context: ToolContext
) -> dict:
    """
    Ask the user for data gathering consent to be used for dashboard insights.

    NOTE: This function is synchronous and returns a small dict describing
    whether the user's message contains a 'yes' style consent.
    """

    # ------------------------------------------
    # Helper: Detect if the user gave consent
    # ------------------------------------------
    def user_gave_consent(user_message) -> bool:
        # Normalize the message to lowercase for simple keyword matching
        message = user_message.lower()

        # Common "yes" variations — this is intentionally simple keyword matching.
        # Consider more robust NLP or stricter matching if false positives matter.
        consent_words = ["yes", "yep", "yeah", "sure", "ok", "okay", "sounds good"]

        # Return True if any of the consent tokens appear anywhere in the message.
        return any(word in message for word in consent_words)

    # ------------------------------------------
    # Evaluate user response
    # ------------------------------------------
    if user_gave_consent(user_message):
        # Return a clear structure the orchestrator can interpret.
        return {
            "consent": True,
            "status": "granted",
            "message": "User granted consent for data collection."
        }
    else:
        return {
            "consent": False,
            "status": "not_granted",
            "message": "User did not grant consent for data collection."
        }


def logger_tool(theme: str, emotion: str, intensity: int, note: str, raw_message: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Saves a consented log entry with its classified metadata to a persistent store.

    Args:
        theme: The main theme of the user's message.
        emotion: The dominant emotion expressed.
        intensity: The emotional intensity (1-10).
        note: A short summary of the message content.
        raw_message: The original user input for context.

    IMPORTANT NOTES (kept as comments — logic not changed):
      - This implementation stores full log entries in tool_context.state["recent_logs"].
        That means recent_logs is a list of dicts (not a list of theme strings).
      - If the orchestrator expects "recent_logs" to be a list of theme strings,
        membership checks (`if log_entry not in recent_logs`) will behave differently.
      - Consider storing unique themes separately (e.g., a `recent_themes` list) if needed.
      - Also consider limiting the size of recent_logs to avoid unbounded growth.
    """
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),  # local time ISO timestamp
        "theme": theme,
        "emotion": emotion,
        "intensity": intensity,
        "note": note,
        "user_message": raw_message
    }

    # 2. STATE LOGIC (In-Memory Memory)
    # Defensive check: ensure the state dict exists before indexing into it.
    
    if "recent_logs" not in tool_context.state:
        # Initialize as a list if missing
        tool_context.state["recent_logs"] = []

    recent_logs = tool_context.state["recent_logs"]

    # Here you're checking the full dict `log_entry` for membership. This works
    # if recent_logs is a list of dicts and you want to avoid exact-duplicate entries.
    # If recent_logs holds different shapes, this check may not dedupe as you expect.
    if log_entry not in recent_logs:
        recent_logs.append(log_entry)
        tool_context.state["recent_logs"] = recent_logs

    # Return payload — ADK runtimes sometimes expect a stateDelta key as well.
    # If you find state is not persisting, return {"result":..., "stateDelta": {...}}
    return {
        "result": f"Log entry for '{theme}' successfully saved."
    }


# Long instruction block used as the LLM instruction 
Conversation_agent_instruction = """
You are a supportive, non-clinical assistant for people experiencing intrusive or obsessive thoughts.

Rules (must follow exactly):

1) You are NOT a therapist. Do not diagnose, provide therapy exercises, or give exposure plans. You first message and should ALWAYS include a clear disclaimer: "I am an AI assistant, not a doctor or therapist. I cannot provide diagnoses, treatment plans, or medical advice. If you are in crisis, please call your local emergency services."
You also should ask the user's well-being . If the user's first message is just a greeting, respond with the disclaimer and ask how you can help with their thoughts. If the user's first message is about the intrusive thoughts, respond with the disclaimer and a brief supportive message.
2) If the user expresses imminent harm or intent to self-harm, immediately produce a crisis response and include local emergency instructions; do NOT log, stage, or reassure.
3) Limit reassurance; never repeatedly reassure. Prefer brief validation and grounding exercises (1-2 sentences).
4) ASK the user for data consent approval, use the consent_approval tool. Send the result of consent_approval to the logger_tool for classification.

- If not logging, set "log_entry": false and include a helpful "reply".
- If logging is proposed ("log_entry": true), the "reply" should include a short consent prompt (e.g., "Would you like me to track this thought for patterns? (yes/no)").
- Use the logger_tool to classify and log only AFTER receiving explicit user consent.
- After using the logger_tool, check if Log entry for '' successfully saved." was returned. Don't show to the user the JSON format. Continue the conversation naturally.
- Remember recently logged entries are stored in tool_context.state["recent_logs"].
5) Always ask for explicit consent before any staging or persistence in this session. Do NOT call any logging tool directly — return the JSON only. The orchestrator will handle staging and approval.
6) Keep "note" anonymized and <= 200 chars. Remove names, locations, or identifiable details.
7) Provide 2-3 short examples (few-shot) in your instruction so the model learns format exactly.

Example 1:
User: [General Greetings: Hi, Hello, Hey there]
Output:
Refer to rule 1 above.

Example 2:
User: "I think if I don't tap the door 7 times my family will be harmed."
Output:
That sounds distressing. Would you like me to track this thought for patterns? (yes/no)


"""

# Create the conversation agent.
# Note: the LlmAgent object is created with two tools: the consent_approval wrapper (FunctionTool) and logger_tool.

Conversation_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='Conversation_Agent',
    description="The user-facing agent. Friendly, supportive, and non-judgmental.",
    instruction=Conversation_agent_instruction,
    tools=[FunctionTool(func=consent_approval), logger_tool],
)

# Root agent points to the conversation agent
root_agent = Conversation_agent
