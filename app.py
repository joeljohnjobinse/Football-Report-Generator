import streamlit as st
import os
from dotenv import load_dotenv
from fetch_data import get_recent_matches
from process_data import extract_match_stats
from report_generator import generate_report

load_dotenv()

st.set_page_config(
    page_title="MatchReport AI",
    page_icon="⚽",
    layout="centered"
)

# ── INJECT ALL STYLES ──────────────────────────────────────────────
st.markdown("""
<style>
/* Hide Streamlit default chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 780px; }

/* ── Top bar ── */
.topbar {
    background: #cc0000;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: -1rem -1rem 0;
    border-radius: 0;
}
.topbar-logo {
    font-size: 22px;
    font-weight: 900;
    color: #fff;
    letter-spacing: -0.5px;
    font-family: system-ui, sans-serif;
}
.topbar-sub {
    font-size: 12px;
    color: rgba(255,255,255,0.65);
    font-weight: 500;
    margin-top: 1px;
    font-family: system-ui, sans-serif;
}

/* ── Hero band ── */
.hero-band {
    background: #111111;
    padding: 32px 24px 28px;
    margin: 0 -1rem;
}
.hero-eyebrow {
    font-size: 11px;
    font-weight: 800;
    color: #cc0000;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 10px;
    font-family: system-ui, sans-serif;
}
.hero-title {
    font-size: 34px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 8px;
    font-family: system-ui, sans-serif;
}
.hero-sub {
    font-size: 15px;
    color: #777;
    font-family: system-ui, sans-serif;
}

/* ── Section labels ── */
.sec-label {
    font-size: 11px;
    font-weight: 800;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 28px 0 10px;
    font-family: system-ui, sans-serif;
}

/* ── Match hero card ── */
.match-hero {
    background: #fff;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #e0e0e0;
    margin: 20px 0 0;
}
.match-hero-top {
    background: #111;
    padding: 11px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.league-pill {
    background: #cc0000;
    color: #fff;
    font-size: 10px;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-family: system-ui, sans-serif;
}
.match-date-tag {
    font-size: 12px;
    color: #777;
    font-family: system-ui, sans-serif;
}

/* ── Scoreboard ── */
.scoreboard {
    padding: 28px 24px 20px;
    display: grid;
    grid-template-columns: 1fr 100px 1fr;
    align-items: center;
    gap: 12px;
    background: #fff;
}
.team-side { display: flex; flex-direction: column; gap: 8px; }
.team-side.right { align-items: flex-end; }
.team-crest {
    width: 56px; height: 56px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; font-weight: 900;
    font-family: system-ui, sans-serif;
}
.home-crest { background: #fff8e1; color: #b8860b; border: 1px solid #ffe082; }
.away-crest { background: #e3f2fd; color: #1565c0; border: 1px solid #90caf9; }
.team-fullname {
    font-size: 16px; font-weight: 800; color: #111; line-height: 1.15;
    font-family: system-ui, sans-serif;
}
.team-tag {
    font-size: 10px; color: #aaa;
    text-transform: uppercase; letter-spacing: 0.07em; font-weight: 700;
    font-family: system-ui, sans-serif;
}
.score-col { text-align: center; }
.score-big {
    font-size: 48px; font-weight: 900; color: #111;
    line-height: 1; letter-spacing: -2px;
    font-family: system-ui, sans-serif;
}
.score-dash { font-size: 28px; color: #ddd; font-weight: 300; }
.ft-label {
    font-size: 10px; font-weight: 800; color: #cc0000;
    text-transform: uppercase; letter-spacing: 0.1em; margin-top: 6px;
    font-family: system-ui, sans-serif;
}

/* ── Winner bar ── */
.winner-bar {
    background: #111;
    padding: 11px 18px;
    display: flex; align-items: center; gap: 10px;
    border-top: 2px solid #cc0000;
}
.w-dot {
    width: 20px; height: 20px; background: #cc0000;
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 10px; color: #fff;
    font-weight: 900; flex-shrink: 0;
}
.winner-bar span {
    font-size: 13px; font-weight: 700; color: #fff;
    font-family: system-ui, sans-serif;
}

/* ── Stats grid ── */
.stats-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 12px; margin: 14px 0 0;
}
.stat-card {
    background: #fff; border-radius: 10px;
    padding: 16px 18px; border: 1px solid #e5e5e5;
}
.stat-card-head {
    font-size: 10px; font-weight: 800; color: #555;
    text-transform: uppercase; letter-spacing: 0.09em;
    margin-bottom: 12px; display: flex; align-items: center; gap: 7px;
    font-family: system-ui, sans-serif;
}
.stat-dot { width: 7px; height: 7px; border-radius: 50%; background: #cc0000; flex-shrink: 0; }
.stat-item {
    font-size: 14px; color: #222; padding: 6px 0;
    border-bottom: 1px solid #f2f2f2; font-weight: 500;
    font-family: system-ui, sans-serif;
}
.stat-item:last-child { border-bottom: none; }
.stat-empty { font-size: 13px; color: #bbb; font-style: italic; font-family: system-ui, sans-serif; }

/* ── Tone pills ── */
.tone-pills { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
.tone-pill {
    padding: 9px 20px; border-radius: 4px;
    font-size: 12px; font-weight: 800; border: 1.5px solid #ddd;
    color: #666; background: #fff; cursor: pointer;
    text-transform: uppercase; letter-spacing: 0.05em;
    font-family: system-ui, sans-serif;
}
.tone-pill.active { background: #cc0000; color: #fff; border-color: #cc0000; }

/* ── Generate button ── */
.gen-btn-wrap { margin: 24px 0 0; }

/* ── Report card ── */
.report-card {
    background: #fff; border-radius: 10px;
    border: 1px solid #e0e0e0; overflow: hidden;
    margin: 18px 0 0;
}
.report-card-head {
    background: #111; padding: 14px 20px;
    display: flex; justify-content: space-between; align-items: center;
}
.r-label {
    font-size: 12px; font-weight: 800; color: #fff;
    text-transform: uppercase; letter-spacing: 0.09em;
    font-family: system-ui, sans-serif;
}
.ai-badge {
    background: #cc0000; color: #fff;
    font-size: 10px; font-weight: 800;
    padding: 4px 12px; border-radius: 3px;
    text-transform: uppercase; letter-spacing: 0.05em;
    font-family: system-ui, sans-serif;
}
.report-match-line {
    background: #f7f7f7; padding: 10px 20px;
    font-size: 13px; font-weight: 700; color: #444;
    border-bottom: 1px solid #eee;
    font-family: system-ui, sans-serif;
}
.report-body {
    padding: 24px 22px;
}
.report-body p {
    font-size: 16px; color: #1a1a1a; line-height: 1.85;
    margin-bottom: 18px; font-family: Georgia, 'Times New Roman', serif;
}
.report-body p:last-child { margin-bottom: 0; }
</style>
""", unsafe_allow_html=True)


# ── TOP BAR ───────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div>
    <div class="topbar-logo">⚽ MATCHREPORT</div>
    <div class="topbar-sub">AI-Powered Football Journalism</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── HERO BAND ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero-band">
  <div class="hero-eyebrow">Live Match Reports</div>
  <div class="hero-title">Football Match<br>Report Generator</div>
  <div class="hero-sub">Pick a match. Get a journalist-quality report in seconds.</div>
</div>
""", unsafe_allow_html=True)


# ── SELECTORS ─────────────────────────────────────────────────────
competitions = {
    "Premier League": "PL",
    "Champions League": "CL",
    "La Liga": "PD",
    "Bundesliga": "BL1",
    "Serie A": "SA"
}

st.markdown('<div class="sec-label">Select match</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    selected_comp = st.selectbox(
        "Competition",
        list(competitions.keys()),
        label_visibility="collapsed"
    )

with col2:
    @st.cache_data(ttl=300)
    def fetch(code):
        return get_recent_matches(code, limit=10)

    with st.spinner("Loading matches..."):
        raw_matches = fetch(competitions[selected_comp])

    if not raw_matches:
        st.warning("No finished matches found. Try another competition.")
        st.stop()

    def make_label(m):
        h = m["homeTeam"]["name"]
        a = m["awayTeam"]["name"]
        hs = m["score"]["fullTime"].get("home", "?")
        as_ = m["score"]["fullTime"].get("away", "?")
        d = m["utcDate"][:10]
        return f"{d}  |  {h} {hs}–{as_} {a}"

    labels = [make_label(m) for m in reversed(raw_matches)]
    matches_rev = list(reversed(raw_matches))

    selected_label = st.selectbox(
        "Match",
        labels,
        label_visibility="collapsed"
    )

idx = labels.index(selected_label)
clean = extract_match_stats(matches_rev[idx])


# ── MATCH HERO CARD ───────────────────────────────────────────────
home_init = "".join(w[0] for w in clean["home_team"].split()[:3]).upper()
away_init = "".join(w[0] for w in clean["away_team"].split()[:3]).upper()

if clean["result"] == "Draw":
    winner_text = "Draw — points shared"
else:
    winner_text = f"{clean['result']} · {clean['competition']}"

st.markdown(f"""
<div class="match-hero">
  <div class="match-hero-top">
    <span class="league-pill">{clean['competition']}</span>
    <span class="match-date-tag">📅 {clean['date']} · Full Time</span>
  </div>
  <div class="scoreboard">
    <div class="team-side">
      <div class="team-crest home-crest">{home_init}</div>
      <div class="team-fullname">{clean['home_team']}</div>
      <div class="team-tag">Home</div>
    </div>
    <div class="score-col">
      <div class="score-big">{clean['home_score']}<span class="score-dash"> – </span>{clean['away_score']}</div>
      <div class="ft-label">Full Time</div>
    </div>
    <div class="team-side right">
      <div class="team-crest away-crest">{away_init}</div>
      <div class="team-fullname">{clean['away_team']}</div>
      <div class="team-tag">Away</div>
    </div>
  </div>
  <div class="winner-bar">
    <div class="w-dot">✓</div>
    <span>{winner_text}</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ── STATS GRID ────────────────────────────────────────────────────
goals_html = ""
if clean["goals"]:
    for g in clean["goals"]:
        suffix = " (OG)" if g["type"] == "OWN" else " (pen)" if g["type"] == "PENALTY" else ""
        goals_html += f'<div class="stat-item">⚽ {g["minute"]}\' — {g["scorer"]} ({g["team"]}){suffix}</div>'
else:
    goals_html = '<div class="stat-empty">No goal data available</div>'

bookings_html = ""
if clean["bookings"]:
    for b in clean["bookings"]:
        icon = "🟡" if b["card"] == "YELLOW" else "🔴"
        bookings_html += f'<div class="stat-item">{icon} {b["minute"]}\' — {b["player"]} ({b["team"]})</div>'
else:
    bookings_html = '<div class="stat-empty">No bookings data available</div>'

st.markdown(f"""
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-card-head"><div class="stat-dot"></div>Goals</div>
    {goals_html}
  </div>
  <div class="stat-card">
    <div class="stat-card-head"><div class="stat-dot"></div>Bookings</div>
    {bookings_html}
  </div>
</div>
""", unsafe_allow_html=True)


# ── TONE SELECTOR ─────────────────────────────────────────────────
st.markdown('<div class="sec-label">Report tone</div>', unsafe_allow_html=True)

tones = ["Broadsheet", "Pundit", "Match Programme"]
if "tone" not in st.session_state:
    st.session_state["tone"] = "Broadsheet"

tcols = st.columns(len(tones))
for i, tone in enumerate(tones):
    with tcols[i]:
        is_active = st.session_state["tone"] == tone
        if st.button(
            tone,
            key=f"tone_{tone}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state["tone"] = tone
            st.rerun()


# ── GENERATE BUTTON ───────────────────────────────────────────────
st.markdown('<div class="gen-btn-wrap">', unsafe_allow_html=True)
if st.button("📝 Generate Match Report", type="primary", use_container_width=True):
    with st.spinner("Writing your match report..."):
        report = generate_report(clean, tone=st.session_state["tone"])
        st.session_state["report"] = report
        st.session_state["report_label"] = selected_label
st.markdown('</div>', unsafe_allow_html=True)


# ── REPORT DISPLAY ────────────────────────────────────────────────
if "report" in st.session_state:
    paras = st.session_state["report"].strip().split("\n\n")
    paras_html = "".join(f"<p>{p.strip()}</p>" for p in paras if p.strip())
    match_line = st.session_state.get("report_label", "")

    st.markdown(f"""
    <div class="report-card">
      <div class="report-card-head">
        <span class="r-label">Match Report</span>
        <span class="ai-badge">AI Generated</span>
      </div>
      <div class="report-match-line">{match_line}</div>
      <div class="report-body">{paras_html}</div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Download report as .txt",
        data=st.session_state["report"],
        file_name="match_report.txt",
        mime="text/plain",
        use_container_width=True
    )