
def build_image_prompt(payload):
    return (
        f"Premium {payload['platforms'][0] if payload['platforms'] else 'social media'} visual for "
        f"{payload['company']} about {payload['topic']}. Audience: {payload['audience']}. "
        f"Country context: {payload['country']}. Style: {payload['tone']}, clean corporate design, "
        "strong visual hierarchy, realistic details, no fake logos, no invented statistics, "
        "leave safe space for headline text."
    )

def build_video_script(payload):
    return (
        f"0-3s HOOK: {payload['topic']}\n"
        f"3-10s PROBLEM: Explain why the topic matters to {payload['audience']}.\n"
        "10-25s VALUE: Give 2-3 useful, factual points grounded in the brand context.\n"
        "25-35s CTA: Invite the audience to learn more or contact the company using only supplied details."
    )
