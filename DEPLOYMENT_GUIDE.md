# Deployment checklist

## 1. GitHub

Upload the complete folder to a new repository.

Do NOT upload:
- `.streamlit/secrets.toml`
- `.env`
- OAuth tokens
- database files

## 2. Streamlit Community Cloud

Create app:
- Repository: your GitHub repo
- Branch: main
- Main file: app.py
- Python: 3.12

Secrets:

```toml
GROQ_API_KEY = "your-groq-key"
GROQ_MODEL = "openai/gpt-oss-120b"
```

## 3. First test

Open:
- ✨ Create Content
- Enter company
- Enter website
- Enter phone / WhatsApp / email if required
- Select country/language
- Select LinkedIn/Instagram
- Generate
- Verify contact values are not changed
- Verify no credentials appear in the post

## 4. Production OAuth

Implement one connector at a time:
1. LinkedIn
2. Meta/Instagram
3. YouTube
4. TikTok
5. X

Use OAuth authorization. Never collect platform passwords.

## 5. Safe publishing

Recommended default:
Generate → QA → Human approval → Schedule → Publish.

Do not enable fully autonomous publishing until connector scopes, token handling, retries, rate limits and audit logs have been tested.
