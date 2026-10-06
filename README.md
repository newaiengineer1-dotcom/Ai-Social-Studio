# 🤖 AI Social Studio

A modular Streamlit MVP for multilingual, humanized social-media content generation using a CrewAI role layer, Groq generation, lightweight RAG, contact-aware CTA generation, calendar drafts and secure OAuth connector scaffolds.

## Included

- Company website, phone/call, WhatsApp, email, contact URL and address inputs.
- Optional contact insertion: CTA only, compact line, footer-style or AI decision.
- English, Arabic and Urdu.
- UAE, Pakistan, Saudi Arabia and Global localization profiles.
- LinkedIn, Instagram, Facebook, TikTok, YouTube and X content targets.
- Image-generation prompts and short-video storyboard generation.
- Five-agent CrewAI role registry.
- Lightweight local TF-IDF RAG to reduce dependencies.
- SQLite campaign/calendar storage.
- Human approval before publishing.
- OAuth connector scaffolds; no social passwords.
- Dark premium Streamlit UI.
- GitHub + Streamlit Community Cloud deployment files.

## Important architecture note

The critical generation call uses the official Groq Python SDK. CrewAI is used as the multi-agent role/orchestration layer but is not forced through a provider-specific LiteLLM adapter in this MVP. This deliberately reduces the provider/model compatibility problems common in small Streamlit deployments.

## Local run

Python 3.12 is recommended.

```bash
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

For macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Groq key

Preferred:

```text
.streamlit/secrets.toml
```

with:

```toml
GROQ_API_KEY = "your-key"
GROQ_MODEL = "openai/gpt-oss-120b"
```

Do not commit secrets.

## GitHub / Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload all project files.
3. In Streamlit Community Cloud, create an app from the repository.
4. Select Python 3.12 in Advanced settings.
5. Add `GROQ_API_KEY` in Secrets.
6. Deploy `app.py`.

## Social publishing security

This MVP intentionally does NOT ask for social-media passwords and does NOT pretend that OAuth publishing is configured. Production publishing must use each platform's official OAuth/API flow, token storage and platform-specific app review/permissions.

## MVP limitation

The calendar is a local draft calendar. Actual automatic posting is intentionally separated behind connectors. This makes the hackathon version safer and easier to validate. Add production OAuth credentials only after platform app approval.
