"""
app/streamlit_app.py
---------------------
WBC 2026 Home Run Surge — Interactive Analytics Dashboard
Dark editorial aesthetic, production-grade layout.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from ingestion.ingest_wbc import ingest_all
from transform.run_transforms import run_all

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WBC 2026 | Home Run Surge",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Color palette ──────────────────────────────────────────────────────────
BG       = "#0D0D0D"
CARD_BG  = "#141414"
BORDER   = "#2A2A2A"
ACCENT   = "#E8C547"   # gold
ACCENT2  = "#E05C4B"   # red
TEXT_PRI = "#F0EDE6"
TEXT_SEC = "#8A8A8A"
GRID     = "#1F1F1F"

# ── Global CSS ─────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

  html, body, [class*="css"] {{
    font-family: 'Syne', sans-serif;
    background-color: {BG};
    color: {TEXT_PRI};
  }}
  .stApp {{ background-color: {BG}; }}

  /* Hide Streamlit chrome */
  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding: 2rem 3rem 4rem; max-width: 1400px; }}

  /* Metrics */
  [data-testid="metric-container"] {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
  }}
  [data-testid="metric-container"] label {{
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {TEXT_SEC} !important;
  }}
  [data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: {ACCENT};
  }}
  [data-testid="metric-container"] [data-testid="stMetricDelta"] {{
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
  }}

  /* Section headers */
  .section-label {{
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {ACCENT};
    margin-bottom: 0.25rem;
  }}
  .section-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: {TEXT_PRI};
    margin-bottom: 1.5rem;
    border-bottom: 1px solid {BORDER};
    padding-bottom: 0.75rem;
  }}

  /* Cards */
  .moment-card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-left: 3px solid {ACCENT};
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
  }}
  .moment-card.historic {{
    border-left-color: {ACCENT2};
  }}
  .moment-game {{
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: {TEXT_SEC};
    text-transform: uppercase;
  }}
  .moment-headline {{
    font-size: 0.95rem;
    font-weight: 700;
    color: {TEXT_PRI};
    margin: 0.2rem 0;
  }}
  .moment-note {{
    font-size: 0.78rem;
    color: {TEXT_SEC};
  }}
  .badge {{
    display: inline-block;
    background: {ACCENT2}22;
    color: {ACCENT2};
    border: 1px solid {ACCENT2}55;
    border-radius: 4px;
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    padding: 2px 7px;
    text-transform: uppercase;
    margin-left: 6px;
    vertical-align: middle;
  }}

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
  }}
  .stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: {TEXT_SEC};
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 7px;
    padding: 0.4rem 1rem;
  }}
  .stTabs [aria-selected="true"] {{
    background: {ACCENT} !important;
    color: {BG} !important;
    font-weight: 600;
  }}
  .stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.5rem; }}

  /* Divider */
  hr {{ border-color: {BORDER}; }}

  /* Table */
  .stDataFrame {{ background: {CARD_BG}; border-radius: 10px; }}

  /* Sidebar */
  [data-testid="stSidebar"] {{ background: {CARD_BG}; border-right: 1px solid {BORDER}; }}

  /* Footer */
  .footer-text {{
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: {TEXT_SEC};
    letter-spacing: 0.08em;
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid {BORDER};
  }}
</style>
""", unsafe_allow_html=True)


# ── Data pipeline ──────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_data():
    ingest_all()
    run_all()
    BASE = os.path.join(os.path.dirname(__file__), "..", "data")
    hr_hist  = pd.read_csv(os.path.join(BASE, "marts", "mart_hr_per_game.csv"))
    team_hr  = pd.read_csv(os.path.join(BASE, "marts", "mart_team_hr_2026.csv"))
    multi    = pd.read_csv(os.path.join(BASE, "marts", "mart_multi_hr_games.csv"))
    moments  = pd.read_csv(os.path.join(BASE, "raw",   "wbc_2026_key_moments.csv"))
    return hr_hist, team_hr, multi, moments

hr_hist, team_hr, multi, moments = load_data()


# ── HEADER ─────────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([5, 1])
with col_title:
    st.markdown("""
    <div style="margin-bottom:0.2rem">
      <span style="font-family:'DM Mono',monospace;font-size:0.7rem;
                   letter-spacing:0.18em;color:#E8C547;text-transform:uppercase">
        Baseball Analytics · 2026 World Baseball Classic
      </span>
    </div>
    <h1 style="font-family:'Syne',sans-serif;font-size:2.8rem;font-weight:800;
               color:#F0EDE6;line-height:1.1;margin:0 0 0.3rem 0">
      The Home Run Surge
    </h1>
    <p style="font-size:1rem;color:#8A8A8A;margin:0;max-width:600px">
      Exploring an unusual power pattern in tournament baseball, 
      pool play data, historical context, and key moments.
    </p>
    """, unsafe_allow_html=True)
with col_badge:
    st.markdown("""
    <div style="text-align:right;padding-top:1rem">
      <span style="font-family:'DM Mono',monospace;font-size:0.65rem;
                   letter-spacing:0.12em;color:#8A8A8A;text-transform:uppercase">
        Data source<br>
        <span style="color:#F0EDE6">Baseball Reference<br>MLB.com (public)</span>
      </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)

# ── KPI METRICS ────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total HRs (pool play)", "92", "↑ vs 85 in 2023 record", delta_color="normal")
k2.metric("HR / Game (2026)", "2.88", "↑ 52% vs 2017 avg", delta_color="normal")
k3.metric("Multi-HR Games", "8", "New WBC record (prev. 6)", delta_color="normal")
k4.metric("Historic Firsts", "2", "Back-to-back leadoff + 3-HR game", delta_color="off")

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📈  Historical Context", "🌎  Team Breakdown", "⚡  Key Moments"])


# ═══════════════════════════════════════════════════════════════════
# TAB 1 — Historical Context
# ═══════════════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns([3, 2], gap="large")

    with c1:
        st.markdown('<div class="section-label">Trend Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">HR per Game — Every WBC Edition</div>', unsafe_allow_html=True)

        colors = [ACCENT if "2026" in str(e) else ACCENT2 if e == "2009" else "#555555"
                  for e in hr_hist["edition"]]

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=hr_hist["edition"],
            y=hr_hist["hr_per_game"],
            marker_color=colors,
            marker_line_width=0,
            text=[f"{v:.2f}" for v in hr_hist["hr_per_game"]],
            textposition="outside",
            textfont=dict(family="DM Mono, monospace", size=11, color=TEXT_PRI),
        ))
        fig1.add_annotation(
            x="2026*", y=hr_hist[hr_hist["edition"] == "2026*"]["hr_per_game"].values[0] + 0.15,
            text="⚾ Record pace", showarrow=False,
            font=dict(family="DM Mono, monospace", size=10, color=ACCENT),
        )
        fig1.update_layout(
            plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
            font=dict(family="DM Mono, monospace", color=TEXT_SEC),
            xaxis=dict(showgrid=False, color=TEXT_SEC, tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor=GRID, color=TEXT_SEC,
                       title="HR per Game", zeroline=False),
            margin=dict(l=0, r=0, t=10, b=0),
            height=340,
            showlegend=False,
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.markdown('<div class="section-label">Record Tracker</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Multi-HR Games per Edition</div>', unsafe_allow_html=True)

        colors2 = [ACCENT if "2026" in str(e) else "#444444" for e in multi["edition"]]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=multi["edition"],
            y=multi["multi_hr_games"],
            marker_color=colors2,
            marker_line_width=0,
            text=multi["multi_hr_games"],
            textposition="outside",
            textfont=dict(family="DM Mono, monospace", size=12, color=TEXT_PRI),
        ))
        fig2.update_layout(
            plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
            font=dict(family="DM Mono, monospace", color=TEXT_SEC),
            xaxis=dict(showgrid=False, color=TEXT_SEC, tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor=GRID, color=TEXT_SEC,
                       title="Multi-HR Games", zeroline=False),
            margin=dict(l=0, r=0, t=10, b=0),
            height=340,
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Context callout
    st.markdown(f"""
    <div style="background:{CARD_BG};border:1px solid {BORDER};border-radius:12px;
                padding:1.2rem 1.6rem;margin-top:0.5rem">
      <span style="font-family:'DM Mono',monospace;font-size:0.65rem;
                   letter-spacing:0.15em;color:{ACCENT};text-transform:uppercase">
        Analyst Note
      </span>
      <p style="margin:0.4rem 0 0;font-size:0.88rem;color:{TEXT_SEC};line-height:1.6">
        The 2026 edition <em style="color:{TEXT_PRI}">appears to be on pace to set the all-time WBC record for home runs</em> 
        with 92 hit in pool play alone — surpassing the full-tournament record of 85 set in both 2009 and 2023. 
        This pattern <em>suggests</em> a structural shift worth exploring: tighter pitching limits, 
        roster construction optimized for short formats, and a possible ball composition change are all 
        candidate explanations. No single factor has been isolated yet.
      </p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# TAB 2 — Team Breakdown
# ═══════════════════════════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns([2, 3], gap="large")

    with c1:
        st.markdown('<div class="section-label">2026 Tournament</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">HR by Team</div>', unsafe_allow_html=True)

        adv_colors = {
            "Advanced":      ACCENT,
            "Quarterfinals": ACCENT2,
            "Eliminated":    "#444444",
        }
        team_hr_sorted = team_hr.sort_values("hr", ascending=True)
        bar_colors = [adv_colors[g] for g in team_hr_sorted["advancement_group"]]

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=team_hr_sorted["hr"],
            y=team_hr_sorted["team"],
            orientation="h",
            marker_color=bar_colors,
            marker_line_width=0,
            text=team_hr_sorted["hr"],
            textposition="outside",
            textfont=dict(family="DM Mono, monospace", size=10, color=TEXT_PRI),
        ))
        fig3.update_layout(
            plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
            font=dict(family="DM Mono, monospace", color=TEXT_SEC),
            xaxis=dict(showgrid=True, gridcolor=GRID, color=TEXT_SEC, zeroline=False),
            yaxis=dict(showgrid=False, color=TEXT_PRI, tickfont=dict(size=10)),
            margin=dict(l=0, r=30, t=10, b=0),
            height=620,
            showlegend=False,
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Legend
        for group, color in adv_colors.items():
            st.markdown(
                f'<span style="font-family:DM Mono,monospace;font-size:0.68rem;'
                f'color:{color}">■</span>'
                f'<span style="font-family:DM Mono,monospace;font-size:0.68rem;'
                f'color:{TEXT_SEC};margin-left:6px">{group}</span>&nbsp;&nbsp;&nbsp;',
                unsafe_allow_html=True,
            )

    with c2:
        st.markdown('<div class="section-label">Power vs Advancement</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">HR per Game by Team</div>', unsafe_allow_html=True)

        scatter_colors = [adv_colors[g] for g in team_hr["advancement_group"]]
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=team_hr["games_played"],
            y=team_hr["hr_per_game"],
            mode="markers+text",
            text=team_hr["team"],
            textposition="top center",
            textfont=dict(family="DM Mono, monospace", size=8, color=TEXT_SEC),
            marker=dict(
                size=team_hr["hr"].apply(lambda x: max(8, x * 2.5)),
                color=scatter_colors,
                line=dict(width=1, color=BG),
            ),
        ))
        fig4.update_layout(
            plot_bgcolor=CARD_BG, paper_bgcolor=CARD_BG,
            font=dict(family="DM Mono, monospace", color=TEXT_SEC),
            xaxis=dict(showgrid=True, gridcolor=GRID, color=TEXT_SEC,
                       title="Games Played", dtick=1),
            yaxis=dict(showgrid=True, gridcolor=GRID, color=TEXT_SEC,
                       title="HR per Game", zeroline=False),
            margin=dict(l=0, r=0, t=10, b=0),
            height=380,
            showlegend=False,
        )
        st.plotly_chart(fig4, use_container_width=True)

        # Insight callout
        st.markdown(f"""
        <div style="background:{CARD_BG};border:1px solid {BORDER};border-left:3px solid {ACCENT};
                    border-radius:10px;padding:1rem 1.2rem;margin-top:0.5rem">
          <span style="font-family:'DM Mono',monospace;font-size:0.65rem;
                       letter-spacing:0.12em;color:{ACCENT};text-transform:uppercase">
            Interesting Pattern
          </span>
          <p style="margin:0.4rem 0 0;font-size:0.85rem;color:{TEXT_SEC};line-height:1.6">
            All four semifinalists ranked in the top 5 for total HRs. The data <em style="color:{TEXT_PRI}">
            suggests a possible correlation</em> between power output and tournament advancement
            but with only 20 teams and 5 pool games each, the sample is too small to isolate HR 
            production as a causal factor.
          </p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# TAB 3 — Key Moments
# ═══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">Historic & Notable</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Standout Power Moments — 2026 WBC</div>', unsafe_allow_html=True)

    for _, row in moments.iterrows():
        historic_class = "moment-card historic" if row["historic"] else "moment-card"
        badge = '<span class="badge">WBC First</span>' if row["historic"] else ""
        st.markdown(f"""
        <div class="{historic_class}">
          <div class="moment-game">{row['game']}</div>
          <div class="moment-headline">{row['moment']}{badge}</div>
          <div class="moment-note">{row['players']} &nbsp;·&nbsp; {row['notes']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:{CARD_BG};border:1px solid {BORDER};border-radius:12px;
                padding:1.2rem 1.6rem">
      <span style="font-family:'DM Mono',monospace;font-size:0.65rem;
                   letter-spacing:0.15em;color:{ACCENT2};text-transform:uppercase">
        Limitations
      </span>
      <p style="margin:0.4rem 0 0;font-size:0.85rem;color:{TEXT_SEC};line-height:1.6">
        This analysis uses pool-play data only (32 games). No Statcast exit velocity or 
        launch angle data is available for WBC games, limiting deeper mechanical analysis. 
        Pitching inning caps, roster selection bias (power-heavy lineups), and possible 
        ball composition differences vs. regular MLB season are all uncontrolled variables.
      </p>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer-text">
  Dataset: Baseball Reference 2026 WBC (public) · MLB.com · Baseball America &nbsp;|&nbsp;
  Stack: Python · pandas · dbt · Streamlit · Railway &nbsp;|&nbsp;
  Built as a portfolio project · March 2026
</div>
""", unsafe_allow_html=True)
