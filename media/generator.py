from __future__ import annotations

import io
import os
import re
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HD_SIZES = {
    "Landscape 16:9": (1920, 1080),
    "Portrait 4:5": (1080, 1350),
    "Story/Reel 9:16": (1080, 1920),
    "Square 1:1": (1080, 1080),
}


def _font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _safe_filename(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip())
    return value[:60] or "social_asset"


def _gradient(size, top=(10, 16, 30), bottom=(25, 70, 90)):
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        c = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img


def _wrap(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render_hd_image(payload: dict, post: dict, output_dir: str, aspect: str = "Landscape 16:9") -> str:
    size = HD_SIZES.get(aspect, HD_SIZES["Landscape 16:9"])
    company = payload.get("company") or "Your Brand"
    topic = payload.get("topic") or "A better future"
    content = post.get("content", "")
    # Keep the visual headline short even if the social post is longer.
    headline = topic.strip()
    if len(headline) > 72:
        headline = headline[:69].rsplit(" ", 1)[0] + "..."

    img = _gradient(size)
    draw = ImageDraw.Draw(img)
    w, h = size
    margin = int(w * 0.08)

    # Decorative high-resolution shapes.
    draw.ellipse((w * 0.70, -h * 0.15, w * 1.10, h * 0.25), fill=(34, 197, 184))
    draw.ellipse((-w * 0.16, h * 0.76, w * 0.18, h * 1.10), fill=(37, 99, 235))
    draw.rounded_rectangle((margin, margin, w - margin, h - margin), radius=36, outline=(120, 210, 220), width=3)

    brand_font = _font(max(30, int(w * 0.025)), bold=True)
    title_font = _font(max(54, int(w * 0.062)), bold=True)
    small_font = _font(max(24, int(w * 0.022)))

    draw.text((margin * 1.4, margin * 1.3), company[:48], font=brand_font, fill="white")
    y = int(h * 0.31)
    for line in _wrap(draw, headline, title_font, int(w * 0.72))[:3]:
        draw.text((margin * 1.4, y), line, font=title_font, fill="white")
        y += int(title_font.size * 1.18)

    # Short value line from the post, without overcrowding the artwork.
    cleaned = " ".join(content.replace("\n", " ").split())
    value = cleaned[:150] + ("..." if len(cleaned) > 150 else "")
    draw.text((margin * 1.4, int(h * 0.67)), "• " + value, font=small_font, fill=(225, 240, 245))

    cta = payload.get("custom_cta") or "Learn more"
    draw.rounded_rectangle((margin * 1.4, int(h * 0.82), min(w - margin, margin * 1.4 + 430), int(h * 0.90)), radius=20, fill=(34, 197, 184))
    draw.text((margin * 1.65, int(h * 0.835)), cta[:34], font=small_font, fill=(5, 20, 28))

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{_safe_filename(company)}_{_safe_filename(post.get('platform', 'social'))}_{_safe_filename(aspect)}.png"
    img.save(path, format="PNG", optimize=True)
    return str(path)


def render_hd_video(payload: dict, post: dict, output_dir: str, aspect: str = "Landscape 16:9", seconds: int = 8) -> str:
    """Render a lightweight HD MP4 from branded visual frames.

    This is intentionally local/offline: it does not pretend to be a diffusion video model.
    The result is a real downloadable MP4 suitable for an MVP/demo and can later be replaced
    by a connected video-generation provider without changing the UI contract.
    """
    import imageio.v2 as imageio

    size = HD_SIZES.get(aspect, HD_SIZES["Landscape 16:9"])
    company = payload.get("company") or "Your Brand"
    topic = payload.get("topic") or "Your next big idea"
    content = " ".join(post.get("content", "").split())
    frames = []
    fps = 8
    total = max(1, int(seconds * fps))
    stage_text = [
        topic[:80],
        "Why it matters: " + content[:110],
        "Make the next move.",
        (payload.get("custom_cta") or "Learn more")[:70],
    ]
    for i in range(total):
        stage = min(len(stage_text) - 1, i * len(stage_text) // total)
        img = _gradient(size, top=(7 + stage * 5, 12 + stage * 8, 25 + stage * 10), bottom=(18, 68 + stage * 8, 82 + stage * 8))
        draw = ImageDraw.Draw(img)
        w, h = size
        title_font = _font(max(52, int(w * 0.058)), bold=True)
        brand_font = _font(max(28, int(w * 0.023)), bold=True)
        small_font = _font(max(24, int(w * 0.021)))
        draw.text((w * 0.08, h * 0.10), company[:48], font=brand_font, fill="white")
        y = h * 0.34
        for line in _wrap(draw, stage_text[stage], title_font, int(w * 0.76))[:4]:
            draw.text((w * 0.08, y), line, font=title_font, fill="white")
            y += title_font.size * 1.18
        draw.text((w * 0.08, h * 0.84), f"{company}  •  AI Social Studio", font=small_font, fill=(220, 240, 245))
        frames.append(img)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{_safe_filename(company)}_{_safe_filename(post.get('platform', 'social'))}_HD.mp4"
    writer = imageio.get_writer(str(path), fps=fps, codec="libx264", quality=7, macro_block_size=1)
    try:
        for frame in frames:
            writer.append_data(__import__("numpy").array(frame))
    finally:
        writer.close()
    return str(path)
