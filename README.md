# 🧠 **Obsessive Compulsive Defender (OCD Agent)**

### *A safe space for intrusive thoughts*

A multi-agent system built with Google ADK to help users reflect on intrusive thoughts with grounding, consent-based logging, and structured insights.

---

## 🌍 **Competition Track**

This project is submitted under the **Agents for Good** track.
It aims to support mental well-being in a safe, ethical, and non-clinical way.

---

## 🌱 **Problem Statement**

Intrusive thoughts and compulsive urges are far more common than many people realize. But for individuals struggling with OCD, these thoughts can feel overwhelming and mentally exhausting. Many people don’t feel comfortable expressing these thoughts openly. Others simply don’t have a structured way to notice patterns, understand triggers, or communicate what they experience to a therapist.

I wanted to create a small, supportive space where users can express intrusive thoughts safely, receive grounding techniques, and optionally track these thoughts over time. The goal is not to diagnose or treat anything. It is to offer clarity, structure, and a gentle conversation partner that doesn’t judge or shame.

This project is personally meaningful to me. I experienced religious OCD when I was younger, and I know firsthand how confusing and frightening intrusive thoughts can be. I built something I wish I had back then.

---

## 🤖 **Why Agents?**

While designing the system, it became clear that a single model cannot handle the different cognitive tasks required here.
Understanding emotions, extracting structured metadata, providing grounding exercises, and generating meaningful summaries are all **different skills**.

Agents allow these tasks to be divided logically:

• The **Conversation Agent** focuses on empathy and safety.
• The **Classifier Agent** specializes in JSON-structured interpretation.
• The **Logger Tool** ensures nothing is logged without consent.
• The **Summarizer Agent** provides meaningful insights.

Because each agent does only one job, the system becomes:

• easier to debug
• easier to test
• much safer
• predictable and structured
• and better aligned with ADK’s strengths

---

## 🧩 **Architecture**

The entire system is created using the **Google Agent Development Kit (ADK)** and orchestrated through **ADK Web**.
The Conversation Agent sits at the center and decides which specialized agent or tool to call based on the user’s message.

Here is the visual agent graph generated directly in ADK Web:

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F7148592%2F4e2d197fa0768688fe4f66f6b85197b2%2FAgent%20Architecture.png?generation=1764601289198221\&alt=media)

### Conversation Agent

Handles all user interaction.
It stays warm, supportive, and non-clinical. It offers grounding, acknowledges distress, and never attempts therapy. When the user expresses an intrusive thought, it calls the Classification Agent. When the user wants insights, it calls the Summarizer Agent. With explicit consent, it triggers the Logger Tool.

### Classification Agent

Takes a raw user message and returns **exactly one JSON object** with theme, emotion, intensity, anonymized note, and recommended logging behavior. This JSON is used internally and never shown directly to the user.

### Logger Tool

Stores the classified intrusive-thought data, but only after explicit consent.
Entries are always anonymized and limited to short summaries.

### Summarizer Agent

Helps users reflect on logged thoughts by identifying trends, repeated themes, and changes in intensity over time.

---

## 🚀 **Setup & Installation**

### Clone the repository

```
git clone https://github.com/YOUR_USERNAME/ocd-defender.git
cd ocd-defender
```

### Create a virtual environment

```
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.\.venv\Scripts\activate     # Windows
```

### Install dependencies

```
pip install --upgrade pip
pip install google-adk
```

### Create your `.env` file

This file stores your Gemini API key.
Do **not** commit this file.

```
GOOGLE_API_KEY=your_api_key_here
MODEL_NAME=gemini-2.5-flash
```

### Running the Agent

```
adk web
```

This command launches the Google ADK Web interface in your browser. From there, you can interact with your Conversation Agent, test messages, view the agent graph, and observe how your multi-agent system routes calls between the Classification Agent, Summarizer Agent, and Logger Tool.

---

## 🎥 **Demo Interaction**

User
“I feel like if I don’t tap the doorknob seven times something terrible will happen.”

Agent
“That sounds like a very stressful intrusive thought to experience. Would you like me to track this thought so you can understand its pattern better? (yes or no)”

If the user says yes, the system stages and logs the entry.
If the user declines, the system simply continues the conversation.

Users can also say:

- show entries
- summarize my thoughts
- give me a grounding technique

---

## 🛠 **The Build**

This project uses:

- Google ADK Web for agent chaining and orchestration
- Gemini models for conversation, classification, and summarization
- A custom Logger Tool with explicit user consent
- A strict JSON schema for reliable classification
- A session-based consent system
- VS Code and GitHub for development
- ChatGPT and Gemini for brainstorming and debugging

The multi-agent structure gives each component one clear responsibility, which made the system easier to build, maintain, and validate for safety.

---

## 🌟 **If I Had More Time**

There are several enhancements I plan to explore next:

- A simple web interface with a calming visual design
- Encrypted local storage for saved logs
- Weekly email or PDF summaries
- A more advanced analytics view, maybe even with charts
- Automatic anonymization checks before export
- Personalized grounding suggestions based on the user’s common thought themes
- Optional connection to clinician dashboards (still fully user-controlled)

---

## 🔒 **Safety Statement**

This system is not a therapist and does not diagnose, treat, or replace any professional mental-health service.
It exists solely to provide supportive grounding and optional structured journaling, always with explicit user consent.

---
