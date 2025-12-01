# 🧠 OCD Thought Support Agent

*A multi-agent system built using the Google Agent Development Kit (ADK) to gently support users experiencing intrusive thoughts through grounding techniques, consent-based logging, and structured insights.*

---

## 🌍 Competition Track

This project is submitted under the **Agents for Good** track.
The goal is to support mental well-being in a safe, ethical, and non-clinical way.

---

## 🌱 Problem Statement

Intrusive thoughts and compulsive urges are far more common than people realize, but for individuals struggling with OCD, these thoughts can feel overwhelming, repetitive, and mentally exhausting. Many people don’t feel comfortable expressing these thoughts openly. Others simply don’t have a reliable way to notice patterns, understand triggers, or communicate what’s happening to their therapist.

I wanted to build a small, supportive space where users can express their intrusive thoughts safely and receive grounding support. At the same time, I wanted to give them the option to track and organize these thoughts over time. The goal isn’t to treat or diagnose anything. The goal is to offer clarity, structure, and a gentle conversation partner that doesn’t judge or shame.

This project is personal to me. I experienced religious OCD when I was younger, and I know how confusing intrusive thoughts can feel. Having a tool like this back then would have helped me understand what was happening instead of feeling controlled by it.

---

## 🤖 Why Agents?

I learned quickly that a single model cannot gracefully balance empathy, structure, safety, and classification. Language understanding is one skill. Emotion handling is another. JSON classification is different. Summarizing patterns over time requires yet another cognitive skill.

Agents let me break these responsibilities into separate, specialized roles.
Each agent focuses on exactly one job. ADK’s orchestration handles the routing, which keeps everything predictable, testable, and safe.

This approach also means the conversation stays warm and human-like, while the classification and logging stay precise and structured.

---

## 🧩 What I Created — Overall Architecture

The system uses the Google Agent Development Kit (ADK), built in ADK Web.
The Conversation Agent is the “human-facing” agent, and it automatically calls specialized sub-agents or tools depending on the user’s needs.

Here is the actual agent graph:

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F7148592%2F4e2d197fa0768688fe4f66f6b85197b2%2FAgent%20Architecture.png?generation=1764601289198221\&alt=media)

### Conversation Agent

This is the agent users interact with directly.
Its job is to respond in a warm, supportive, non-clinical manner. It offers grounding, acknowledges distress without over-reassurance, and never attempts therapy or diagnosis.

Whenever the user mentions an intrusive thought, this agent calls the Classification Agent.
If the user wants insights, it calls the Summarizer Agent.
If the user gives explicit consent, it safely triggers the Logger Tool.

### Classification Agent

This agent performs the structured reasoning.
It takes the raw user message and returns a single JSON object containing:

- theme
- emotion
- intensity
- anonymized note
- whether logging is recommended
- a short reply for the Conversation Agent

The JSON is for internal use only. Users never see it directly.

### Logger Tool

The Logger Tool handles storing intrusive-thought metadata, but only after the user explicitly says yes.
Nothing is ever logged automatically.
Everything is anonymized and kept short.

The easiest way to think of it is a consent-based thought journal with structure and safety built in.

### Summarizer Agent

This agent analyzes saved entries and generates insights.
It helps users identify recurring themes, observe emotional changes, and understand patterns over time.

If the user chooses to share the summary with a licensed professional, it can improve communication — but the agent itself never provides clinical analysis.

---

## 🎥 Demo

A typical interaction might look like this:

**User**
“I feel like if I don’t tap the doorknob seven times something terrible will happen.”

**Conversation Agent**
“That sounds like a very stressful intrusive thought to experience. Would you like me to track this thought so you can understand its pattern better? (yes or no)”

If the user says yes, the Logger Tool stages and saves the entry.
If the user says no, the system respects the decision and continues the conversation normally.

Users may later ask:
- “show entries”
- “summarize my thoughts”
- “give me a grounding technique”

---

## 🛠 The Build

This project uses the Google Agent Development Kit (ADK), which made it easy to create a safe multi-agent architecture. ADK Web gives me a clear visual graph and lets my Conversation Agent call other components as needed.

The system includes:

- ADK Web for agent chaining and visualization
- Gemini models for conversation, classification, and summarization
- A custom Logger Tool that stores entries with explicit user consent
- A strict JSON schema so classification stays predictable
- A session-based consent system to protect user data

Other tools I used:

- Visual Studio Code
- GitHub
- ChatGPT and Gemini for brainstorming, debugging, and polishing ideas

The multi-agent structure keeps each component focused, and made the entire system easier to build and maintain.

---

## 🌟 If I Had More Time

There are several features I plan to explore next:

- A calming, simple web interface
- Encrypted local storage for logged thoughts
- Weekly email or PDF summaries
- More advanced analytics and charts for recurring themes
- Automatic anonymization checks before exporting
- Personalized grounding suggestions based on a user’s most common thought themes
- Optional clinician export mode with privacy filters

