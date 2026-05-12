import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="World Cup Analyst",
    page_icon="assets/logo.png",
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Mapping squadra → file bandiera
FLAG_MAP = {
    "Brasile":      "Girone_C/brasile",
    "Francia":      "Girone_I/francia",
    "Argentina":    "Girone_J/argentina",
    "Inghilterra":  "Girone_L/inghilterra",
    "Spagna":       "Girone_H/spagna",
    "Portogallo":   "Girone_K/portogallo",
    "Germania":     "Girone_E/germania",
    "Olanda":       "Girone_F/olanda",
    "Belgio":       "Girone_G/belgio",
    "Croazia":      "Girone_L/croazia",
    "Uruguay":      "Girone_H/uruguay",
    "Colombia":     "Girone_K/colombia",
    "Marocco":      "Girone_C/marocco",
    "Senegal":      "Girone_I/senegal",
    "Giappone":     "Girone_F/giappone",
    "Messico":      "Girone_A/messico",
    "USA":          "Girone_D/stati_uniti",
    "Australia":    "Girone_D/australia",
    "Norvegia":     "Girone_I/norvegia",
    "Svizzera":     "Girone_B/svizzera",
}

def flag_path(squadra):
    return f"assets/flags/{FLAG_MAP.get(squadra, squadra.lower())}.png"

def flag_img(squadra, width=32):
    p = flag_path(squadra)
    if os.path.exists(p):
        return st.image(p, width=width)

# ── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=100)
    st.markdown("### WORLD CUP\nANALYST")
    st.markdown("---")
    st.markdown(
        "<span class='wca-badge'>FIFA WORLD CUP 2026</span>",
        unsafe_allow_html=True
    )

# ── DATI ────────────────────────────────────────────────────────────────────
df_teams   = pd.read_csv("data/team_stats.csv")
df_players = pd.read_csv("data/world_cup_players.csv")

# ── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 40px 0 20px;">
  <div style="color:#6b7a99;font-size:11px;letter-spacing:3px;text-transform:uppercase;font-weight:600;margin-bottom:8px;">
    FIFA WORLD CUP 2026 · ANALYTICS PLATFORM
  </div>
  <h1 style="font-size:4rem;margin:0;line-height:1">WORLD CUP<br>ANALYST</h1>
  <p style="color:#6b7a99;margin-top:12px;font-size:15px;max-width:500px">
    Statistiche avanzate, radar, profili e previsioni per tutte le 20 nazionali del Mondiale 2026.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── TOP STATS ───────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📊 Top Stats</span>", unsafe_allow_html=True)

best_attack  = df_teams.loc[df_teams["Gol"].idxmax()]
best_xg      = df_teams.loc[df_teams["xG"].idxmax()]
best_poss    = df_teams.loc[df_teams["Possesso"].idxmax()]
top_scorer   = df_players.loc[df_players["Gol"].idxmax()]
top_assist   = df_players.loc[df_players["Assist"].idxmax()]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("⚽ Miglior Attacco",  best_attack["Squadra"],  f"{best_attack['Gol']} gol/match")
c2.metric("📐 Miglior xG",       best_xg["Squadra"],      f"xG {best_xg['xG']}")
c3.metric("🔵 Miglior Possesso", best_poss["Squadra"],    f"{best_poss['Possesso']}%")
c4.metric("🥇 Capocannoniere",   top_scorer["Giocatore"], f"{int(top_scorer['Gol'])} gol")
c5.metric("🎯 Top Assistman",    top_assist["Giocatore"], f"{int(top_assist['Assist'])} assist")

st.markdown("---")

# ── FEATURED MATCH ──────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>🔥 Featured Match</span>", unsafe_allow_html=True)

top2 = df_teams.nlargest(2, "Gol")
t1, t2 = top2.iloc[0], top2.iloc[1]

stats = ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]

col_l, col_c, col_r = st.columns([3, 1, 3])

with col_l:
    fp = flag_path(t1["Squadra"])
    if os.path.exists(fp):
        st.image(fp, width=56)
    st.markdown(f"### {t1['Squadra']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Gol", t1["Gol"])
    c2.metric("xG", t1["xG"])
    c3.metric("Poss.", f"{t1['Possesso']}%")

with col_c:
    st.markdown(
        "<div style='text-align:center;padding-top:40px'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:#6b7a99;letter-spacing:3px'>VS</div>"
        "<div style='width:1px;height:60px;background:#1f2d45;margin:8px auto'></div>"
        "</div>",
        unsafe_allow_html=True
    )

with col_r:
    fp2 = flag_path(t2["Squadra"])
    if os.path.exists(fp2):
        st.image(fp2, width=56)
    st.markdown(f"### {t2['Squadra']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Gol", t2["Gol"])
    c2.metric("xG", t2["xG"])
    c3.metric("Poss.", f"{t2['Possesso']}%")

# Radar premium
fig = go.Figure()
for team, color in [(t1, "#00d4ff"), (t2, "#ff3b5c")]:
    fig.add_trace(go.Scatterpolar(
        r=[team[s] for s in stats], theta=stats,
        fill='toself', name=team["Squadra"],
        line=dict(color=color, width=2),
        fillcolor=color.replace("ff", "22") if "#" in color else color,
        opacity=0.85
    ))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    polar=dict(
        bgcolor="rgba(26,32,53,0.6)",
        radialaxis=dict(visible=True, gridcolor="#1f2d45", color="#6b7a99", linecolor="#1f2d45"),
        angularaxis=dict(gridcolor="#1f2d45", color="#6b7a99", linecolor="#1f2d45")
    ),
    showlegend=True,
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8edf5")),
    height=380, margin=dict(t=30, b=30)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── LEADERBOARD ─────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>🏆 Leaderboard</span>", unsafe_allow_html=True)

col_lb, col_pl = st.columns(2)

with col_lb:
    st.markdown("#### Ranking Nazionali")
    df_ranked = df_teams.sort_values("Gol", ascending=False).reset_index(drop=True)
    medals = {0:"🥇", 1:"🥈", 2:"🥉"}

    for i, row in df_ranked.iterrows():
        medal = medals.get(i, f"{i+1}.")
        fp = flag_path(row["Squadra"])
        c1, c2 = st.columns([1, 6])
        with c1:
            if os.path.exists(fp):
                st.image(fp, width=28)
            else:
                st.write(medal)
        with c2:
            st.markdown(
                f"<div class='wca-card' style='padding:10px 16px;margin-bottom:6px'>"
                f"<b>{medal} {row['Squadra']}</b>"
                f"<div class='wca-stat-row'>"
                f"<div class='wca-stat'>⚽ <span>{row['Gol']}</span></div>"
                f"<div class='wca-stat'>xG <span>{row['xG']}</span></div>"
                f"<div class='wca-stat'>🔵 <span>{row['Possesso']}%</span></div>"
                f"</div></div>",
                unsafe_allow_html=True
            )

with col_pl:
    st.markdown("#### Top Marcatori")
    top5 = df_players.sort_values("Gol", ascending=False).head(8).reset_index(drop=True)
    for i, row in top5.iterrows():
        medal = medals.get(i, f"{i+1}.")
        fp = flag_path(row["Squadra"])
        c1, c2 = st.columns([1, 6])
        with c1:
            if os.path.exists(fp):
                st.image(fp, width=28)
        with c2:
            st.markdown(
                f"<div class='wca-card' style='padding:10px 16px;margin-bottom:6px'>"
                f"<b>{medal} {row['Giocatore']}</b> "
                f"<span style='color:#6b7a99;font-size:12px'>{row['Squadra']}</span>"
                f"<div class='wca-stat-row'>"
                f"<div class='wca-stat'>⚽ <span>{int(row['Gol'])}</span></div>"
                f"<div class='wca-stat'>🎯 <span>{int(row['Assist'])}</span></div>"
                f"<div class='wca-stat'>xG <span>{row['xG']}</span></div>"
                f"</div></div>",
                unsafe_allow_html=True
            )

st.markdown("---")

# ── NAV CARDS ───────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📂 Sezioni</span>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
sections = [
    ("🌍", "Nazionali", "Filtra e cerca giocatori per squadra"),
    ("🏳️", "Team Profile", "Scheda completa di ogni nazionale"),
    ("🌟", "Player Profile", "Profilo dettagliato giocatore"),
    ("📊", "Team Comparison", "Confronto radar tra nazionali"),
    ("👤", "Player Comparison", "Confronto statistiche giocatori"),
]
for col, (icon, title, desc) in zip([c1,c2,c3,c4,c5], sections):
    with col:
        st.markdown(
            f"<div class='wca-card' style='text-align:center;padding:20px 12px'>"
            f"<div style='font-size:2rem'>{icon}</div>"
            f"<div style='font-weight:700;margin:8px 0 4px'>{title}</div>"
            f"<div style='color:#6b7a99;font-size:12px'>{desc}</div>"
            f"</div>",
            unsafe_allow_html=True
        )