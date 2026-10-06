import os
import streamlit as st

APP_NAME = "AI Social Studio"
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

def get_groq_key():
    try:
        return st.secrets.get("GROQ_API_KEY", "") or os.getenv("GROQ_API_KEY", "")
    except Exception:
        return os.getenv("GROQ_API_KEY", "")
