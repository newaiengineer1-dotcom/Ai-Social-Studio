import streamlit as st

CSS = r'''
<style>
:root {
  --bg:#050b17; --panel:#0a1322; --panel2:#0d192b; --line:#1c3047;
  --text:#edf6ff; --muted:#8fa3b8; --cyan:#19e6c2; --blue:#3b82f6;
  --purple:#8b5cf6; --amber:#f5b72d; --green:#22c55e; --red:#fb5b5b;
}
.stApp { background:
 radial-gradient(circle at 72% 6%, rgba(25,230,194,.08), transparent 28%),
 radial-gradient(circle at 18% 90%, rgba(59,130,246,.08), transparent 28%), #050b17; color:var(--text); }
.block-container { max-width:1540px; padding:1.2rem 1.5rem 3rem; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#07101d,#050a13); border-right:1px solid #13263b; }
[data-testid="stSidebar"] > div:first-child { padding:1rem .75rem; }
[data-testid="stSidebar"] .stButton button { border:1px solid transparent; background:transparent; color:#91a6ba; text-align:left; justify-content:flex-start; border-radius:10px; min-height:40px; }
[data-testid="stSidebar"] .stButton button:hover { background:#0d1b2c; color:#eafcff; border-color:#17334a; }
[data-testid="stSidebar"] .stRadio label { color:#9db0c4 !important; }
[data-testid="stSidebar"] [role="radiogroup"] { gap:2px; }
[data-testid="stSidebar"] [role="radiogroup"] label { padding:7px 10px; border-radius:9px; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background:#0d1b2c; }
[data-testid="stSidebar"] .stCaption { color:#70879d; }

/* Remove the default white/grey surfaces from tabs and inputs. */
.stTabs [data-baseweb="tab-list"] { gap:6px; background:transparent; }
.stTabs [data-baseweb="tab"] { background:#091423; border:1px solid #172b40; border-radius:10px; color:#91a6ba; padding:8px 14px; }
.stTabs [aria-selected="true"] { color:#eafffb !important; border-color:#1d6f69 !important; background:#0b2026 !important; }
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"] > div,.stMultiSelect div[data-baseweb="select"] > div { background:#081321 !important; color:#eaf4ff !important; border-color:#1a3045 !important; }
.stTextInput label,.stTextArea label,.stSelectbox label,.stMultiSelect label,.stSlider label,.stCheckbox label { color:#a8b9ca !important; }
.stButton button[kind="primary"] { background:linear-gradient(135deg,#19e6c2,#11b8dc); color:#031014; border:0; font-weight:800; box-shadow:0 0 25px rgba(25,230,194,.16); }
.stButton button { border-color:#1b3349; background:#0a1625; color:#dcecff; }
.stDownloadButton button { background:#0b1c2a; border-color:#17475a; color:#9ffbea; }

.brand { display:flex; align-items:center; gap:10px; padding:7px 10px 18px; }
.brand-mark { width:34px;height:34px;border-radius:11px;display:grid;place-items:center;background:radial-gradient(circle,#35ffe0,#0e9e92 55%,#09272a); box-shadow:0 0 24px rgba(25,230,194,.25); font-size:18px; }
.brand-name { font-size:18px; font-weight:800; letter-spacing:-.3px; color:#f2fbff; }
.brand-sub { font-size:9px; color:#6f879e; letter-spacing:.7px; text-transform:uppercase; }

.eyebrow { color:#6f879e; font-size:11px; letter-spacing:1.4px; text-transform:uppercase; font-weight:700; }
.hero-title { font-size:34px; line-height:1.1; font-weight:800; letter-spacing:-1.2px; margin:4px 0; }
.hero-sub { color:#8196aa; font-size:14px; }
.topbar { display:flex; justify-content:space-between; align-items:center; margin-bottom:18px; }
.topbar-right { color:#8ba1b5; font-size:12px; }

.card { background:linear-gradient(145deg,rgba(12,25,41,.96),rgba(7,17,29,.96)); border:1px solid #183047; border-radius:15px; padding:17px; box-shadow:inset 0 1px 0 rgba(255,255,255,.025),0 14px 40px rgba(0,0,0,.16); }
.card-tight { padding:13px 15px; }
.card-title { font-size:13px; font-weight:750; color:#dcecff; }
.card-muted { color:#70869c; font-size:11px; }
.metric { min-height:112px; }
.metric-value { font-size:27px; font-weight:800; margin-top:9px; color:#f1f8ff; }
.metric-change { font-size:11px; color:#2ee6a6; margin-top:5px; }
.metric-label { color:#7f95aa; font-size:11px; }

.network { position:relative; min-height:420px; overflow:hidden; border:1px solid #183047; border-radius:16px; background:radial-gradient(circle at center,rgba(17,71,82,.25),transparent 33%), linear-gradient(145deg,#071423,#07101d); }
.network-grid { position:absolute; inset:0; opacity:.22; background-image:linear-gradient(rgba(62,115,145,.13) 1px,transparent 1px),linear-gradient(90deg,rgba(62,115,145,.13) 1px,transparent 1px); background-size:28px 28px; mask-image:radial-gradient(circle at center,black,transparent 72%); }
.network-ring { position:absolute; border:1px dashed rgba(49,226,202,.2); border-radius:50%; left:50%;top:50%; transform:translate(-50%,-50%); }
.ring1 { width:240px;height:240px; } .ring2 { width:350px;height:350px; border-color:rgba(63,128,210,.18); }
.network-center { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:145px;height:145px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center; text-align:center; background:radial-gradient(circle,#12353b,#07151f 65%); border:1px solid rgba(25,230,194,.55); box-shadow:0 0 0 12px rgba(25,230,194,.035),0 0 50px rgba(25,230,194,.24); }
.network-center .core-icon { font-size:30px; color:#2df2d1; } .network-center b { font-size:18px; } .network-center span { font-size:9px;color:#5fe4cf; }
.node { position:absolute; min-width:126px; padding:9px 11px; border:1px solid #1d3a50; border-radius:12px; background:rgba(8,20,33,.94); box-shadow:0 12px 25px rgba(0,0,0,.18); }
.node b { font-size:11px; } .node small { display:block; color:#70879d; margin-top:3px; font-size:9px; }
.node .dot { display:inline-block; width:7px;height:7px;border-radius:50%; background:#20d9a8; box-shadow:0 0 10px #20d9a8; margin-right:5px; }
.node1{left:7%;top:15%}.node2{left:35%;top:5%}.node3{right:7%;top:17%}.node4{right:6%;top:54%}.node5{left:8%;bottom:14%}.node6{left:36%;bottom:5%}
.network-line { position:absolute; height:1px; background:linear-gradient(90deg,transparent,#1edabf,transparent); opacity:.55; transform-origin:left center; }
.line1{width:170px;left:25%;top:32%;transform:rotate(12deg)}.line2{width:145px;left:51%;top:31%;transform:rotate(-18deg)}.line3{width:170px;left:57%;top:52%;transform:rotate(18deg)}.line4{width:155px;left:25%;top:58%;transform:rotate(-17deg)}

.section-title { font-size:14px; font-weight:800; margin:2px 0 10px; }
.badge { display:inline-flex; align-items:center; gap:5px; padding:4px 8px; border-radius:999px; border:1px solid #25425a; background:#0a1928; color:#9bb1c5; font-size:9px; }
.badge-green { color:#62f0c2; border-color:#185a50; background:#09251f; } .badge-yellow { color:#f5ca55; border-color:#5a4a19; background:#211c09; } .badge-blue { color:#78b7ff; border-color:#204a72; background:#091d31; }
.activity { display:flex; gap:10px; align-items:flex-start; padding:10px 0; border-bottom:1px solid #122638; }
.activity:last-child { border-bottom:0; } .activity-icon { width:29px;height:29px;border-radius:9px;display:grid;place-items:center;background:#0d2734;color:#65eacb; }
.activity-title { font-size:11px; color:#d9e7f3; } .activity-sub { font-size:9px;color:#71879b; margin-top:2px; }
.insight { height:100%; border:1px solid #18354a; border-radius:12px; padding:12px; background:rgba(8,20,33,.7); }
.insight b { font-size:10px; } .insight p { margin:5px 0 0; color:#8499ac; font-size:9px; line-height:1.5; }

.chart { height:150px; display:flex; align-items:flex-end; gap:5px; padding:15px 4px 5px; }
.bar { flex:1; border-radius:4px 4px 1px 1px; background:linear-gradient(180deg,#1ee0c2,#0d6b76); opacity:.85; min-height:8px; }
.chart-labels { display:flex; justify-content:space-between; color:#566f84; font-size:9px; }
.progress { height:6px; background:#101f30;border-radius:999px;overflow:hidden;margin-top:8px; } .progress > span { display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,#19e6c2,#3b82f6); }

.preview { border:1px solid #1a354a;border-radius:13px;overflow:hidden;background:#060d16; }
.preview-head { padding:10px 12px;display:flex;justify-content:space-between;border-bottom:1px solid #14283a;color:#8498aa;font-size:10px; }
.preview-copy { padding:15px;color:#dceaf6;font-size:13px;line-height:1.55;min-height:115px; }

@media (max-width: 900px) { .hero-title{font-size:27px}.network{min-height:520px}.node1{left:2%}.node3{right:2%}.node4{right:2%}.node5{left:2%}.node2,.node6{left:34%} }
</style>
'''

def inject_theme():
    st.markdown(CSS, unsafe_allow_html=True)
