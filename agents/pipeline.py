from agents.crewai_registry import get_agent_registry
from agents.content_agent import generate_posts
from localization.profiles import build_localization_context

def run_content_pipeline(payload, api_key, rag):
    context = rag.retrieve(payload["topic"], top_k=5)
    localization = build_localization_context(payload["language"], payload["country"], payload["dialect"])
    registry = get_agent_registry()
    posts = generate_posts(payload, api_key, context, localization, registry)
    return {
        "posts": posts,
        "agent_trace": registry["names"],
        "brand_context_used": context,
        "localization": localization,
    }
