import streamlit as st
from datetime import datetime, date, time
from config import APP_NAME, GROQ_MODEL, get_groq_key
from agents.pipeline import run_content_pipeline
from database.db import init_db, save_campaign
from localization.profiles import LANGUAGES, COUNTRIES, PLATFORM_OPTIONS
from rag.retriever import BrandRAG
from connectors.registry import connector_status
from scheduler.calendar_store import save_calendar_item, list_calendar_items
from media.prompts import build_image_prompt, build_video_script

st.set_page_config(page_title=APP_NAME, page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp { background: #070b14; color: #eef2ff; }
.block-container { padding-top: 1.2rem; max-width: 1500px; }
.hero { padding: 28px; border: 1px solid #273149; border-radius: 22px;
        background: linear-gradient(135deg,#101827,#0b1220); margin-bottom: 18px; }
.hero h1 { margin: 0; font-size: 2.2rem; }
.card { padding: 18px; border: 1px solid #263149; border-radius: 16px;
        background: #0d1422; margin-bottom: 12px; }
.badge { display:inline-block; padding:4px 10px; border-radius:999px;
         border:1px solid #334155; margin:2px; font-size:.82rem; }
.small { color:#9aa7bd; font-size:.9rem; }
</style>
""", unsafe_allow_html=True)

init_db()

if "rag" not in st.session_state:
    st.session_state.rag = BrandRAG()
if "generated" not in st.session_state:
    st.session_state.generated = None

with st.sidebar:
    st.markdown("## 🤖 AI Social Studio")
    st.caption("Multilingual multi-agent content workflow")
    api_key = st.text_input("Groq API key", value=get_groq_key(), type="password")
    if api_key:
        st.session_state.api_key = api_key
    st.divider()
    page = st.radio("Workspace", ["✨ Create Content", "📅 AI Calendar", "🔗 Social Accounts", "📚 Brand Knowledge", "🛡️ System Check"])

st.markdown('<div class="hero"><h1>🚀 AI Social Studio</h1><div class="small">Plan → Create → Localize → QA → Approve → Schedule</div></div>', unsafe_allow_html=True)

if page == "✨ Create Content":
    left, right = st.columns([1.1, 0.9])
    with left:
        st.subheader("🎯 Campaign & brand inputs")
        company = st.text_input("Company / Brand name", "Your Company")
        website = st.text_input("🌐 Company website", "https://example.com")
        description = st.text_area("Company / product description", "Describe the company, product, service or campaign.", height=90)
        topic = st.text_area("Campaign topic / post idea", "Create an educational post about our new service.", height=90)

        st.markdown("### 📞 Contact & CTA details")
        c1, c2 = st.columns(2)
        with c1:
            phone = st.text_input("📞 Call / Phone", "")
            whatsapp = st.text_input("💬 WhatsApp", "")
            email = st.text_input("✉️ Email", "")
        with c2:
            contact_url = st.text_input("🔗 Contact / Booking URL", "")
            address = st.text_input("📍 Office / location", "")
            custom_cta = st.text_input("🎯 Preferred CTA", "")

        include_contacts = st.checkbox("Include contact details when contextually appropriate", value=True)
        contact_style = st.selectbox("Contact presentation", ["CTA only", "Compact contact line", "Footer-style", "Let AI decide"])

        st.markdown("### 🌍 Audience & localization")
        c1, c2, c3 = st.columns(3)
        with c1:
            country = st.selectbox("Country", list(COUNTRIES.keys()))
        with c2:
            language = st.selectbox("Language", list(LANGUAGES.keys()))
        with c3:
            tone = st.selectbox("Tone", ["Professional", "Friendly", "Executive", "Educational", "Sales", "Casual"])

        audience = st.text_input("Target audience", "Business decision-makers")
        dialect = st.text_input("Humanized regional style", COUNTRIES[country]["style"])

        st.markdown("### 📱 Platforms & format")
        platforms = st.multiselect("Platforms", PLATFORM_OPTIONS, default=["LinkedIn", "Instagram"])
        format_type = st.selectbox("Content format", ["Text Post", "Image Concept", "Carousel", "Short Video Script", "Campaign Pack"])
        generate_count = st.slider("Posts to generate", 1, 5, 1)

        if st.button("🚀 Generate AI Campaign", type="primary", use_container_width=True):
            if not topic.strip():
                st.error("Enter a campaign topic.")
            else:
                payload = {
                    "company": company, "website": website, "description": description,
                    "topic": topic, "phone": phone, "whatsapp": whatsapp, "email": email,
                    "contact_url": contact_url, "address": address, "custom_cta": custom_cta,
                    "include_contacts": include_contacts, "contact_style": contact_style,
                    "country": country, "language": language, "tone": tone,
                    "audience": audience, "dialect": dialect, "platforms": platforms,
                    "format_type": format_type, "generate_count": generate_count,
                }
                result = run_content_pipeline(payload, api_key, st.session_state.rag)
                st.session_state.generated = result
                save_campaign(payload, result)
                st.success("Campaign generated. Review it before publishing.")
                if format_type in ("Image Concept", "Campaign Pack"):
                    st.markdown("### 🎨 Image prompt")
                    st.code(build_image_prompt(payload))
                if format_type in ("Short Video Script", "Campaign Pack"):
                    st.markdown("### 🎬 Video storyboard")
                    st.code(build_video_script(payload))


    with right:
        st.subheader("🧠 Multi-agent workflow")
        for icon, name, detail in [
            ("📚", "Brand Intelligence", "Uses saved brand facts and contact details"),
            ("🔎", "Research / Strategy", "Builds platform and audience angle"),
            ("✍️", "Content Creator", "Creates humanized platform content"),
            ("🌍", "Localization", "Adapts language, country and regional style"),
            ("🛡️", "QA & Contact Guard", "Checks claims, links and contact placement"),
        ]:
            st.markdown(f'<div class="card"><b>{icon} {name}</b><br><span class="small">{detail}</span></div>', unsafe_allow_html=True)

        if st.session_state.generated:
            st.subheader("✨ Generated content")
            for item in st.session_state.generated["posts"]:
                st.markdown(f"### {item['platform']}")
                st.markdown(item["content"])
                st.caption(f"QA: {item['qa_status']} · {item['language']} · {item['country']}")
                st.download_button(
                    f"⬇️ Download {item['platform']} post",
                    item["content"],
                    file_name=f"{item['platform'].lower()}_post.txt",
                    mime="text/plain",
                    key=f"dl_{item['platform']}_{hash(item['content'])}",
                )

elif page == "📅 AI Calendar":
    st.subheader("📅 AI Content Calendar")
    st.info("MVP calendar stores approved drafts locally. Real social publishing is connector-dependent and intentionally disabled until OAuth is configured.")
    items = list_calendar_items()
    if items:
        for x in items:
            st.markdown(f'<div class="card"><b>{x["scheduled_at"]}</b> · {x["platform"]}<br>{x["title"]}<br><span class="small">{x["status"]}</span></div>', unsafe_allow_html=True)
    else:
        st.write("No scheduled items yet.")
    with st.form("calendar_form"):
        platform = st.selectbox("Platform", PLATFORM_OPTIONS)
        title = st.text_input("Calendar title", "Campaign post")
        d = st.date_input("Date", date.today())
        t = st.time_input("Time", time(10, 0))
        if st.form_submit_button("➕ Add to calendar"):
            save_calendar_item(platform, title, datetime.combine(d, t).isoformat(), "Draft")
            st.success("Added to calendar.")

elif page == "🔗 Social Accounts":
    st.subheader("🔐 Secure social-account connections")
    st.warning("Never enter social-media passwords here. Production connectors must use each platform's OAuth authorization flow.")
    for name, status in connector_status().items():
        st.markdown(f'<div class="card"><b>{name}</b> · <span class="badge">{status}</span><br><span class="small">Connector scaffold is included; credentials are not stored in source code.</span></div>', unsafe_allow_html=True)

elif page == "📚 Brand Knowledge":
    st.subheader("📚 Brand RAG knowledge")
    st.write("Add factual company/product information used to ground generated posts.")
    text = st.text_area("Brand facts", height=220, placeholder="Products, services, approved claims, audience, brand voice, FAQs...")
    if st.button("💾 Save brand knowledge"):
        if text.strip():
            st.session_state.rag.add_text(text)
            st.success("Brand knowledge indexed for this session.")
        else:
            st.warning("Enter some brand facts first.")
    st.caption("The MVP uses lightweight local TF-IDF retrieval to avoid a heavy vector-database dependency.")

else:
    st.subheader("🛡️ System / deployment check")
    checks = {
        "Python target": "3.12",
        "Streamlit": "1.65.0",
        "CrewAI": "1.15.22",
        "Groq SDK": "1.7.0",
        "API key": "Configured" if (st.session_state.get("api_key") or get_groq_key()) else "Not configured",
        "OAuth": "Scaffold / not configured",
        "Publishing": "Human approval required",
    }
    for k, v in checks.items():
        st.markdown(f'<div class="card"><b>{k}</b><br><span class="small">{v}</span></div>', unsafe_allow_html=True)
