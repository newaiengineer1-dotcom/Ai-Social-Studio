import tempfile
from datetime import datetime, date, time
from pathlib import Path

import streamlit as st

from config import APP_NAME, get_groq_key
from agents.pipeline import run_content_pipeline
from database.db import init_db, save_campaign
from localization.profiles import LANGUAGES, COUNTRIES, PLATFORM_OPTIONS
from rag.retriever import BrandRAG
from connectors.registry import connector_status
from scheduler.calendar_store import save_calendar_item, list_calendar_items
from media.generator import render_hd_image, render_hd_video
from media.prompts import build_image_prompt, build_video_script
from ui.theme import inject_theme
from ui.components import metric_card, card, activity, fake_chart, network_panel, status_badge

st.set_page_config(page_title=APP_NAME, page_icon="✦", layout="wide", initial_sidebar_state="expanded")
inject_theme()
init_db()

if "rag" not in st.session_state:
    st.session_state.rag = BrandRAG()
if "generated" not in st.session_state:
    st.session_state.generated = None
if "nav" not in st.session_state:
    st.session_state.nav = "Dashboard"

NAV = [
    ("⌂", "Dashboard"), ("▣", "Content Hub"), ("✦", "AI Studio"),
    ("◈", "Campaigns"), ("□", "Calendar"), ("⌁", "Analytics"),
    ("♙", "Leads"), ("⌘", "Integrations"), ("⚙", "Settings"),
]

with st.sidebar:
    st.markdown('''<div class="brand"><div class="brand-mark">✦</div><div><div class="brand-name">AI Social Studio</div><div class="brand-sub">Digital Marketing OS</div></div></div>''', unsafe_allow_html=True)
    current = st.session_state.nav
    for icon, label in NAV:
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.nav = label
            st.rerun()
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.markdown('''<div class="card card-tight"><div class="card-title">✦ AI Assistant</div><div class="card-muted" style="margin:6px 0 10px">Turn one idea into platform-ready posts, HD visuals and short videos.</div></div>''', unsafe_allow_html=True)
    if st.button("↗  Create Content", use_container_width=True, type="primary"):
        st.session_state.nav = "AI Studio"
        st.rerun()
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    api_key = st.text_input("Groq API key", value=get_groq_key(), type="password", help="Or configure GROQ_API_KEY in Streamlit Secrets.")
    if api_key:
        st.session_state.api_key = api_key
    st.caption("No social-media passwords are requested. Production connections use OAuth.")

page = st.session_state.nav

# Header
col1, col2 = st.columns([4, 1.5])
with col1:
    st.markdown('<div class="eyebrow">AI SOCIAL STUDIO / WORKSPACE</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Welcome back, your AI marketing team is ready ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Create short, high-impact content and turn it into HD images, videos and scheduled campaigns.</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    if st.button("＋ Create Content", type="primary", use_container_width=True, key="top_create"):
        st.session_state.nav = "AI Studio"
        st.rerun()

if page == "Dashboard":
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1: metric_card("TOTAL REACH", "128.7K", "↗ 18.6% this period", "◌")
    with m2: metric_card("ENGAGEMENT", "9.46K", "↗ 24.1% this period", "♡")
    with m3: metric_card("CONTENT PUBLISHED", "24", "↗ 26.3% this month", "▣")
    with m4: metric_card("AI ASSETS", "58", "↗ 31 HD visuals", "✦")

    left, right = st.columns([1.75, 1])
    with left:
        st.markdown('<div class="section-title">✦ AI Marketing Hub</div>', unsafe_allow_html=True)
        network_panel()
    with right:
        st.markdown('<div class="section-title">⌁ Performance Overview</div>', unsafe_allow_html=True)
        card("This Week", '<div class="card-muted">Channel activity and content output</div>')
        fake_chart([32,44,38,56,48,73,66,81,76,91,84,96], ["M","T","W","T","F","S","S"])
        c1, c2 = st.columns(2)
        with c1: metric_card("CONVERSIONS", "2.38K", "↗ 16.3%", "◎")
        with c2: metric_card("SCHEDULED", "7", "3 today", "◷")

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.25, .9])
    with left:
        st.markdown('<div class="section-title">✦ AI Insights</div>', unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a: st.markdown('<div class="insight"><b>↗ Best channel</b><p>LinkedIn is currently your strongest channel for professional content.</p></div>', unsafe_allow_html=True)
        with b: st.markdown('<div class="insight"><b>◷ Best timing</b><p>Your calendar has 7 scheduled posts. Keep a consistent weekly rhythm.</p></div>', unsafe_allow_html=True)
        with c: st.markdown('<div class="insight"><b>✦ Repurpose</b><p>Turn high-performing posts into Reels, Shorts and carousel visuals.</p></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section-title">◷ Recent Activity</div>', unsafe_allow_html=True)
        card("Latest workspace activity", "")
        activity("✦", "AI campaign generated", "3 post variants + 2 HD assets", "Ready")
        activity("◎", "Instagram visual prepared", "Short-form creative", "Draft")
        activity("in", "LinkedIn post scheduled", "Tomorrow · 10:00 AM", "Scheduled")
        activity("✓", "Brand knowledge updated", "RAG context refreshed")

elif page == "AI Studio":
    st.markdown('<div class="eyebrow">AI STUDIO</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Create content that gets remembered.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">One campaign idea → short impact post → HD image → HD video → review → schedule.</div>', unsafe_allow_html=True)

    setup, preview = st.columns([1.12, .88])
    with setup:
        with st.container(border=True):
            st.markdown('<div class="section-title">Campaign setup</div>', unsafe_allow_html=True)
            company = st.text_input("Company / Brand", "Your Company")
            website = st.text_input("Company website", "https://example.com")
            description = st.text_area("Brand / product description", "Describe your company, product, service or campaign.", height=80)
            topic = st.text_area("Campaign idea", "Create an educational post about our new service.", height=80)
            c1, c2, c3 = st.columns(3)
            with c1: country = st.selectbox("Country", list(COUNTRIES.keys()))
            with c2: language = st.selectbox("Language", list(LANGUAGES.keys()))
            with c3: tone = st.selectbox("Tone", ["Professional","Friendly","Executive","Educational","Sales","Casual"])
            audience = st.text_input("Target audience", "Business decision-makers")
            dialect = st.text_input("Humanized regional style", COUNTRIES[country]["style"])
            platforms = st.multiselect("Platforms", PLATFORM_OPTIONS, default=["LinkedIn", "Instagram"])
            format_type = st.selectbox("Content format", ["Campaign Pack", "Text Post", "Image + Post", "Carousel", "HD Video + Post"])
            c1, c2 = st.columns(2)
            with c1: make_hd_image = st.checkbox("🖼 Generate HD image", True)
            with c2: make_hd_video = st.checkbox("🎬 Generate HD MP4", True)
            aspect = st.selectbox("Visual format", ["Landscape 16:9", "Portrait 4:5", "Story/Reel 9:16", "Square 1:1"])
            st.markdown('<div class="card-muted">Copy is intentionally short: strong hook + one valuable idea + clear CTA. The QA layer is designed to remove filler and unsupported claims.</div>', unsafe_allow_html=True)
            generate_count = st.slider("Variants", 1, 5, 1)
            generate = st.button("✦ Generate AI Campaign", type="primary", use_container_width=True)
            if generate:
                if not topic.strip():
                    st.error("Enter a campaign idea.")
                else:
                    payload = {"company":company,"website":website,"description":description,"topic":topic,"phone":"","whatsapp":"","email":"","contact_url":"","address":"","custom_cta":"","include_contacts":True,"contact_style":"Let AI decide","country":country,"language":language,"tone":tone,"audience":audience,"dialect":dialect,"platforms":platforms,"format_type":format_type,"generate_count":generate_count,"make_hd_image":make_hd_image,"make_hd_video":make_hd_video,"aspect":aspect}
                    key = api_key or st.session_state.get("api_key") or get_groq_key()
                    with st.spinner("AI team is creating your campaign…"):
                        result = run_content_pipeline(payload, key, st.session_state.rag)
                    media_dir = tempfile.mkdtemp(prefix="ai_social_studio_media_")
                    for item in result["posts"]:
                        if make_hd_image:
                            try: item["hd_image_path"] = render_hd_image(payload, item, media_dir, aspect)
                            except Exception: item["hd_image_error"] = "Image render failed"
                        if make_hd_video:
                            try: item["hd_video_path"] = render_hd_video(payload, item, media_dir, aspect)
                            except Exception: item["hd_video_error"] = "Video render failed"
                    st.session_state.generated = result
                    save_campaign(payload, result)
                    st.success("Campaign generated. Review the media and copy before publishing.")
    with preview:
        st.markdown('<div class="section-title">Live campaign preview</div>', unsafe_allow_html=True)
        if st.session_state.generated:
            for i, item in enumerate(st.session_state.generated["posts"]):
                st.markdown(f'<div class="preview"><div class="preview-head"><span>{item.get("platform","Platform")}</span><span>{status_badge("AI READY","green")}</span></div><div class="preview-copy">{item.get("content","")}</div></div>', unsafe_allow_html=True)
                if item.get("hd_image_path"):
                    st.image(item["hd_image_path"], use_container_width=True)
                    with open(item["hd_image_path"], "rb") as f:
                        st.download_button("⬇ Download HD image", f.read(), file_name=f"ai_social_{i+1}.png", mime="image/png", key=f"dli_{i}")
                if item.get("hd_video_path"):
                    st.video(item["hd_video_path"])
                    with open(item["hd_video_path"], "rb") as f:
                        st.download_button("⬇ Download HD MP4", f.read(), file_name=f"ai_social_{i+1}.mp4", mime="video/mp4", key=f"dlv_{i}")
                st.download_button("⬇ Download post copy", item.get("content", ""), file_name=f"ai_social_{i+1}.txt", mime="text/plain", key=f"dlt_{i}")
        else:
            st.markdown('<div class="card" style="min-height:380px;display:flex;align-items:center;justify-content:center;text-align:center"><div><div style="font-size:42px">✦</div><div class="card-title" style="font-size:18px">Your campaign will appear here</div><div class="card-muted" style="margin-top:8px">Generate a campaign to preview the short post, HD image and MP4 video.</div></div></div>', unsafe_allow_html=True)

elif page == "Content Hub":
    st.markdown('<div class="eyebrow">CONTENT HUB</div><div class="hero-title">Your content library</div>', unsafe_allow_html=True)
    if not st.session_state.generated:
        card("No generated campaign in this session", '<div class="card-muted">Open AI Studio to create your first short-form campaign with HD media.</div>')
    else:
        for i, item in enumerate(st.session_state.generated["posts"]):
            with st.container(border=True):
                c1, c2 = st.columns([1.6,1])
                with c1:
                    st.markdown(f"**{item.get('platform','Platform')}**  {status_badge('READY','green')}", unsafe_allow_html=True)
                    st.write(item.get("content",""))
                with c2:
                    if item.get("hd_image_path"): st.image(item["hd_image_path"], use_container_width=True)

elif page == "Campaigns":
    st.markdown('<div class="eyebrow">CAMPAIGNS</div><div class="hero-title">Campaign control center</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: metric_card("ACTIVE", "03", "2 ready for approval", "◈")
    with c2: metric_card("DRAFTS", "08", "4 with HD media", "□")
    with c3: metric_card("APPROVED", "12", "Ready to schedule", "✓")
    card("Workflow", '<div class="card-muted">Generate → QA → Human approval → Schedule → Publish. Real publishing remains connector/OAuth dependent.</div>')

elif page == "Calendar":
    st.markdown('<div class="eyebrow">CALENDAR</div><div class="hero-title">Plan your publishing rhythm</div>', unsafe_allow_html=True)
    left,right=st.columns([1.3,.8])
    with left:
        items=list_calendar_items()
        if items:
            for x in items:
                st.markdown(f'<div class="card card-tight" style="margin-bottom:8px"><b>{x["scheduled_at"]}</b> · {x["platform"]} {status_badge(x["status"],"yellow" if x["status"]=="Draft" else "green")}<br><span class="card-muted">{x["title"]}</span></div>', unsafe_allow_html=True)
        else: card("No scheduled content", '<div class="card-muted">Add your first campaign to the calendar.</div>')
    with right:
        with st.form("calendar_form"):
            platform=st.selectbox("Platform", PLATFORM_OPTIONS); title=st.text_input("Title","Campaign post"); d=st.date_input("Date",date.today()); t=st.time_input("Time",time(10,0))
            if st.form_submit_button("＋ Add to calendar"):
                save_calendar_item(platform,title,datetime.combine(d,t).isoformat(),"Draft"); st.success("Added to calendar."); st.rerun()

elif page == "Analytics":
    st.markdown('<div class="eyebrow">ANALYTICS</div><div class="hero-title">Performance overview</div>', unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: metric_card("REACH","128.7K","↗ 18.6%","↗")
    with c2: metric_card("ENGAGEMENT","9.46K","↗ 24.1%","♡")
    with c3: metric_card("CONVERSIONS","2.38K","↗ 16.3%","◎")
    with c4: metric_card("CONTENT","24","↗ 26.3%","▣")
    l,r=st.columns([1.5,1])
    with l:
        card("Engagement trend", '<div class="card-muted">Illustrative workspace analytics — connect platform APIs for live metrics.</div>'); fake_chart([35,45,39,54,51,67,63,79,72,87,83,94], ["Jan","Feb","Mar","Apr","May","Jun"])
    with r:
        card("Content status", '<div style="margin-top:15px"><b>Published</b><div class="progress"><span style="width:58%"></span></div><div class="card-muted">58%</div><br><b>Scheduled</b><div class="progress"><span style="width:27%"></span></div><div class="card-muted">27%</div><br><b>Drafting</b><div class="progress"><span style="width:15%"></span></div><div class="card-muted">15%</div></div>')

elif page == "Leads":
    st.markdown('<div class="eyebrow">LEADS</div><div class="hero-title">Lead-ready content signals</div>', unsafe_allow_html=True)
    card("Lead automation", '<div class="card-muted">This MVP provides the workspace layer. Connect CRM/lead APIs later for real lead capture and qualification.</div>')
    c1,c2,c3=st.columns(3)
    with c1: metric_card("NEW SIGNALS","18","This week","◎")
    with c2: metric_card("QUALIFIED","7","Awaiting follow-up","✓")
    with c3: metric_card("CTA CLICKS","142","Campaign-linked","↗")

elif page == "Integrations":
    st.markdown('<div class="eyebrow">INTEGRATIONS</div><div class="hero-title">Connect your channels safely</div>', unsafe_allow_html=True)
    st.warning("Never enter social-media passwords. Production publishing must use official OAuth authorization and encrypted token storage.")
    for name,status in connector_status().items():
        card(name, f'<div class="card-muted">{status_badge(status,"yellow" if "scaffold" in status.lower() else "green")} Official OAuth connector architecture can be enabled here.</div>')

elif page == "Settings":
    st.markdown('<div class="eyebrow">SETTINGS</div><div class="hero-title">AI Social Studio configuration</div>', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        card("AI Engine", f'<div class="card-muted">Groq model</div><b>{st.session_state.get("api_key") and "API key configured" or "Use Streamlit Secrets"}</b>')
        card("Safety", '<div class="card-muted">Human approval is required before publishing. Contact information is only inserted when enabled and contextually appropriate.</div>')
    with c2:
        card("Deployment", '<div class="card-muted">Python 3.12 · Streamlit 1.65 · Groq SDK · CrewAI · local TF-IDF RAG</div>')
        card("Media", '<div class="card-muted">HD PNG and MP4 demo rendering is enabled. Dedicated AI image/video providers can be connected later.</div>')

st.markdown('<div style="height:24px"></div><div style="text-align:center;color:#4e6579;font-size:10px">AI Social Studio · Generate → Visualize → Approve → Schedule · No social passwords stored</div>', unsafe_allow_html=True)
