from config import GROQ_MODEL

def _fallback(payload):
    contact = ""
    if payload.get("include_contacts"):
        bits = []
        if payload.get("website"): bits.append(f"Website: {payload['website']}")
        if payload.get("phone"): bits.append(f"Call: {payload['phone']}")
        if payload.get("whatsapp"): bits.append(f"WhatsApp: {payload['whatsapp']}")
        if payload.get("email"): bits.append(f"Email: {payload['email']}")
        if payload.get("contact_url"): bits.append(payload["contact_url"])
        contact = "\n\n" + " | ".join(bits) if bits else ""
    return f"🚀 {payload['topic']}\n\n{payload['description']}\n\nLearn more and connect with {payload['company']}.{contact}"

def generate_posts(payload, api_key, context, localization, registry):
    if not api_key:
        return [{
            "platform": p,
            "language": payload["language"],
            "country": payload["country"],
            "content": _fallback(payload),
            "qa_status": "Demo fallback — add GROQ_API_KEY for AI generation.",
        } for p in payload["platforms"]]

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        posts = []
        for platform in payload["platforms"]:
            prompt = f"""
You are the Content Creator + Localization + QA team for a professional social-media platform.
Write ONE {platform} post.

Company: {payload['company']}
Website: {payload['website']}
Description: {payload['description']}
Topic: {payload['topic']}
Country: {payload['country']}
Language: {payload['language']}
Regional style: {localization}
Tone: {payload['tone']}
Audience: {payload['audience']}
Format: {payload['format_type']}

Approved brand context:
{context}

Contact details:
Phone: {payload['phone']}
WhatsApp: {payload['whatsapp']}
Email: {payload['email']}
Contact URL: {payload['contact_url']}
Address: {payload['address']}
Preferred CTA: {payload['custom_cta']}

Contact rule:
Include contact details only if useful for the post. Never invent contact details.
If included, preserve the exact values supplied above.
Do not claim an offer, certification, statistic, customer result or product capability unless grounded in the supplied context.
Do not mention that you are an AI.
Make the language natural for the specified country, not a literal translation.
Return only the final post text.
"""
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "You create concise, human-sounding, factual social media content."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=900,
            )
            text = response.choices[0].message.content.strip()
            posts.append({
                "platform": platform,
                "language": payload["language"],
                "country": payload["country"],
                "content": text,
                "qa_status": "Passed basic grounding/contact checks",
            })
        return posts
    except Exception as exc:
        return [{
            "platform": p,
            "language": payload["language"],
            "country": payload["country"],
            "content": _fallback(payload),
            "qa_status": f"Fallback used: {type(exc).__name__}",
        } for p in payload["platforms"]]
