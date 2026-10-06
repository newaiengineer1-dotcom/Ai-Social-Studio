def build_image_prompt(payload):
    return (
        f"HD 1920x1080 social media visual for {payload['company']} about {payload['topic']}. "
        f"Audience: {payload['audience']}. Country: {payload['country']}. Tone: {payload['tone']}. "
        "Premium realistic campaign photography/design, strong focal subject, clean composition, "
        "high contrast, mobile-readable, authentic regional context, no fake logos, no invented statistics, "
        "no excessive text, safe space for a short headline, commercial-quality lighting."
    )


def build_video_script(payload):
    return (
        "HD short-form video, 8-15 seconds, fast professional pacing.\n"
        f"0-2s HOOK: One sharp visual statement about {payload['topic']}.\n"
        f"2-6s VALUE: One or two concrete points relevant to {payload['audience']}.\n"
        f"6-10s PROOF/INSIGHT: Use only supplied brand facts; never invent claims.\n"
        f"10-15s CTA: {payload.get('custom_cta') or 'Learn more'} using only supplied contact details.\n"
        "Visual style: premium, realistic, cinematic, platform-native, captions readable on mobile."
    )
