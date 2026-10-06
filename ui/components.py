import html
import streamlit as st


def card(title, body, extra_class=""):
    st.markdown(f'<div class="card {extra_class}"><div class="card-title">{title}</div>{body}</div>', unsafe_allow_html=True)


def metric_card(label, value, change="", icon="✦"):
    st.markdown(f'''
    <div class="card metric">
      <div style="display:flex;justify-content:space-between;align-items:center"><span class="metric-label">{label}</span><span class="badge">{icon}</span></div>
      <div class="metric-value">{value}</div>
      <div class="metric-change">{change}</div>
    </div>''', unsafe_allow_html=True)


def status_badge(text, kind="green"):
    return f'<span class="badge badge-{kind}">● {html.escape(text)}</span>'


def activity(icon, title, subtitle, status=""):
    badge = status_badge(status) if status else ""
    st.markdown(f'''
    <div class="activity"><div class="activity-icon">{icon}</div><div style="flex:1"><div class="activity-title">{html.escape(title)} {badge}</div><div class="activity-sub">{html.escape(subtitle)}</div></div></div>''', unsafe_allow_html=True)


def fake_chart(values, labels=None):
    vals = [max(5, min(100, int(v))) for v in values]
    bars = "".join([f'<div class="bar" style="height:{v}%;"></div>' for v in vals])
    st.markdown(f'<div class="chart">{bars}</div>', unsafe_allow_html=True)
    if labels:
        st.markdown('<div class="chart-labels">' + ''.join(f'<span>{html.escape(x)}</span>' for x in labels) + '</div>', unsafe_allow_html=True)


def network_panel():
    st.markdown('''
    <div class="network">
      <div class="network-grid"></div><div class="network-ring ring1"></div><div class="network-ring ring2"></div>
      <div class="network-line line1"></div><div class="network-line line2"></div><div class="network-line line3"></div><div class="network-line line4"></div>
      <div class="node node1"><b>● LinkedIn</b><small>Published · 8 posts</small></div>
      <div class="node node2"><b>▣ Content Hub</b><small>24 assets generated</small></div>
      <div class="node node3"><b>◎ Instagram</b><small>Scheduled · 6 posts</small></div>
      <div class="node node4"><b>▶ YouTube</b><small>Drafting · 3 videos</small></div>
      <div class="node node5"><b>𝕏 X</b><small>Drafting · 4 posts</small></div>
      <div class="node node6"><b>◉ Facebook</b><small>Published · 5 posts</small></div>
      <div class="network-center"><div class="core-icon">✦</div><b>AI Social Studio</b><span>AI-POWERED MARKETING HUB</span></div>
    </div>''', unsafe_allow_html=True)
