"""CrewAI role registry.

The MVP keeps actual text generation in the official Groq Python SDK.
This avoids coupling the app's critical generation path to CrewAI's provider
adapter/LiteLLM behavior. CrewAI still defines the multi-agent roles and can
be activated as the orchestration layer in a later production backend.
"""
try:
    from crewai import Agent
    CREWAI_AVAILABLE = True
except Exception:
    Agent = None
    CREWAI_AVAILABLE = False

ROLE_DATA = [
    ("Brand Intelligence Agent", "Ground content in approved brand facts and contact details."),
    ("Strategy Agent", "Choose a useful platform, audience and campaign angle."),
    ("Content Creator Agent", "Write natural, platform-specific social content."),
    ("Localization Agent", "Adapt language, country and regional style."),
    ("QA & Contact Guard Agent", "Check factual grounding, CTA and contact placement."),
]

def get_agent_registry():
    agents = []
    if CREWAI_AVAILABLE:
        for role, goal in ROLE_DATA:
            agents.append(Agent(role=role, goal=goal, backstory="Specialized AI social-media team member.", allow_delegation=False))
    return {"available": CREWAI_AVAILABLE, "objects": agents, "names": [r[0] for r in ROLE_DATA]}
