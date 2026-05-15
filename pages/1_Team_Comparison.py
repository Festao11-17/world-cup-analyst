import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

FLAG_MAP = {
    "Messico":"Girone_A/Messico","Cechia":"Girone_A/Cechia","Corea_del_Sud":"Girone_A/Corea_del_Sud","Sudafrica":"Girone_A/Sudafrica",
    "Svizzera":"Girone_B/Svizzera","Canada":"Girone_B/Canada","Bosnia_ed_Erzegovina":"Girone_B/Bosnia_ed_Erzegovina","Qatar":"Girone_B/Qatar",
    "Brasile":"Girone_C/Brasile","Marocco":"Girone_C/Marocco","Haiti":"Girone_C/Haiti","Scozia":"Girone_C/Scozia",
    "Australia":"Girone_D/Australia","Stati_Uniti":"Girone_D/Stati_Uniti","Paraguay":"Girone_D/Paraguay","Turchia":"Girone_D/Turchia",
    "Germania":"Girone_E/Germania","Ecuador":"Girone_E/Ecuador","Costa_d'Avorio":"Girone_E/Costa_d'Avorio","Curacao":"Girone_E/Curacao",
    "Giappone":"Girone_F/Giappone","Olanda":"Girone_F/Olanda","Svezia":"Girone_F/Svezia","Tunisia":"Girone_F/Tunisia",
    "Belgio":"Girone_G/Belgio","Egitto":"Girone_G/Egitto","Iran":"Girone_G/Iran","Nuova_Zelanda":"Girone_G/Nuova_Zelanda",
    "Spagna":"Girone_H/Spagna","Uruguay":"Girone_H/Uruguay","Arabia_Saudita":"Girone_H/Arabia_Saudita","Capo_Verde":"Girone_H/Capo_Verde",
    "Francia":"Girone_I/Francia","Senegal":"Girone_I/Senegal","Norvegia":"Girone_I/Norvegia","Iraq":"Girone_I/Iraq",
    "Argentina":"Girone_J/Argentina","Algeria":"Girone_J/Algeria","Austria":"Girone_J/Austria","Giordania":"Girone_J/Giordania",
    "Portogallo":"Girone_K/Portogallo","Colombia":"Girone_K/Colombia","Repubblica_del_Congo":"Girone_K/Repubblica_del_Congo","Uzbekistan":"Girone_K/Uzbekistan",
    "Inghilterra":"Girone_L/Inghilterra","Croazia":"Girone_L/Croazia","Ghana":"Girone_L/Ghana","Panama":"Girone_L/Panama",
}
def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"

st.markdown("<h1>📊 TEAM COMPARISON</h1>", unsafe_allow_html=True)

df = pd.read_csv("data/team_stats.csv")
teams = sorted(df["Squadra"].tolist())

# ── RICERCA ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    search1 = st.text_input("🔍 Cerca Squadra 1", placeholder="Es. Brasile...")
    filtered1 = [t for t in teams if search1.lower() in t.lower()] if search1 else teams
    team1 = st.selectbox("Squadra 1", filtered1, key="t1")

with col2:
    search2 = st.text_input("🔍 Cerca Squadra 2", placeholder="Es. Francia...")
    filtered2 = [t for t in teams if search2.lower() in t.lower()] if search2 else teams
    team2 = st.selectbox("Squadra 2", filtered2, key="t2")

if team1 == team2:
    st.warning("Seleziona due squadre diverse.")
    st.stop()

t1 = df[df["Squadra"] == team1].iloc[0]
t2 = df[df["Squadra"] == team2].iloc[0]

st.markdown("---")

# ── HEADER ───────────────────────────────────────────────────────────────────
col_l, col_c, col_r = st.columns([3, 1, 3])

with col_l:
    fp = flag_path(team1)
    if os.path.exists(fp): st.image(fp, width=70)
    st.markdown(f"### {team1}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Gol", t1["Gol"])
    c2.metric("xG", t1["xG"])
    c3.metric("Possesso", f"{t1['Possesso']}%")

with col_c:
    st.markdown(
        "<div style='text-align:center;padding-top:40px'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:#6b7a99;letter-spacing:3px'>VS</div>"
        "</div>", unsafe_allow_html=True
    )

with col_r:
    fp2 = flag_path(team2)
    if os.path.exists(fp2): st.image(fp2, width=70)
    st.markdown(f"### {team2}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Gol", t2["Gol"])
    c2.metric("xG", t2["xG"])
    c3.metric("Possesso", f"{t2['Possesso']}%")

st.markdown("---")

# ── STATS GRID ───────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📊 Statistiche a Confronto</span>", unsafe_allow_html=True)

for label, k1, k2, suffix in [
    ("⚽ Gol/Match",       t1["Gol"],               t2["Gol"],               ""),
    ("📐 xG",              t1["xG"],                t2["xG"],                ""),
    ("🎯 Tiri",            t1["Tiri"],              t2["Tiri"],              ""),
    ("🔵 Possesso",        t1["Possesso"],          t2["Possesso"],          "%"),
    ("✅ Prec. Passaggi",  t1["PrecisionePassaggi"],t2["PrecisionePassaggi"],"%"),
    ("⭐ Overall Rating",  t1["OverallRating"],     t2["OverallRating"],     ""),
    ("⚔️ Attack Rating",   t1["AttackRating"],      t2["AttackRating"],      ""),
    ("🛡️ Defense Rating",  t1["DefenseRating"],     t2["DefenseRating"],     ""),
]:
    max_v = max(float(k1), float(k2), 0.01)
    w1 = int(float(k1) / max_v * 100)
    w2 = int(float(k2) / max_v * 100)
    c1_col = "#00d4ff" if float(k1) >= float(k2) else "#6b7a99"
    c2_col = "#ff3b5c" if float(k2) > float(k1) else "#6b7a99"
    st.markdown(
        f"<div style='margin-bottom:12px'>"
        f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
        f"<span style='font-weight:700;color:{c1_col}'>{k1}{suffix}</span>"
        f"<span style='font-size:12px;color:#6b7a99'>{label}</span>"
        f"<span style='font-weight:700;color:{c2_col}'>{k2}{suffix}</span>"
        f"</div>"
        f"<div style='display:flex;gap:4px'>"
        f"<div style='flex:1;background:#1f2d45;border-radius:4px;height:8px;display:flex;justify-content:flex-end'>"
        f"<div style='width:{w1}%;background:#00d4ff;border-radius:4px;height:8px'></div></div>"
        f"<div style='flex:1;background:#1f2d45;border-radius:4px;height:8px'>"
        f"<div style='width:{w2}%;background:#ff3b5c;border-radius:4px;height:8px'></div></div>"
        f"</div></div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ── RADAR ────────────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📈 Radar</span>", unsafe_allow_html=True)

stats = ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]
fig = go.Figure()
for team, data, color in [(team1, t1, "#00d4ff"), (team2, t2, "#ff3b5c")]:
    fig.add_trace(go.Scatterpolar(
        r=[data[s] for s in stats], theta=stats,
        fill='toself', name=team, line=dict(color=color, width=2)
    ))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    polar=dict(bgcolor="rgba(26,32,53,0.6)",
               radialaxis=dict(visible=True, gridcolor="#1f2d45", color="#6b7a99"),
               angularaxis=dict(gridcolor="#1f2d45", color="#6b7a99")),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8edf5")),
    height=420, showlegend=True
)
st.plotly_chart(fig, use_container_width=True)