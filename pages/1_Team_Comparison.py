import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

FLAG_MAP = {
    "Messico":"Girone_A/Messico","Cechia":"Girone_A/Cechia","Corea del Sud":"Girone_A/Corea_del_Sud","Sudafrica":"Girone_A/Sudafrica",
    "Svizzera":"Girone_B/Svizzera","Canada":"Girone_B/Canada","Bosnia":"Girone_B/Bosnia_ed_Erzegovina","Qatar":"Girone_B/Qatar",
    "Brasile":"Girone_C/Brasile","Marocco":"Girone_C/Marocco","Haiti":"Girone_C/Haiti","Scozia":"Girone_C/Scozia",
    "Australia":"Girone_D/Australia","Stati Uniti":"Girone_D/Stati_Uniti","Paraguay":"Girone_D/Paraguay","Turchia":"Girone_D/Turchia",
    "Germania":"Girone_E/Germania","Ecuador":"Girone_E/Ecuador","Costa d'Avorio":"Girone_E/Costa_d'Avorio","Curacao":"Girone_E/Curacao",
    "Giappone":"Girone_F/Giappone","Olanda":"Girone_F/Olanda","Svezia":"Girone_F/Svezia","Tunisia":"Girone_F/Tunisia",
    "Belgio":"Girone_G/Belgio","Egitto":"Girone_G/Egitto","Iran":"Girone_G/Iran","Nuova Zelanda":"Girone_G/Nuova_Zelanda",
    "Spagna":"Girone_H/Spagna","Uruguay":"Girone_H/Uruguay","Arabia Saudita":"Girone_H/Arabia_Saudita","Capo Verde":"Girone_H/Capo_Verde",
    "Francia":"Girone_I/Francia","Senegal":"Girone_I/Senegal","Norvegia":"Girone_I/Norvegia","Iraq":"Girone_I/Iraq",
    "Argentina":"Girone_J/Argentina","Algeria":"Girone_J/Algeria","Austria":"Girone_J/Austria","Giordania":"Girone_J/Giordania",
    "Portogallo":"Girone_K/Portogallo","Colombia":"Girone_K/Colombia","Rep. del Congo":"Girone_K/Repubblica_del_Congo","Uzbekistan":"Girone_K/Uzbekistan",
    "Inghilterra":"Girone_L/Inghilterra","Croazia":"Girone_L/Croazia","Ghana":"Girone_L/Ghana","Panama":"Girone_L/Panama",
}

GIRONI = {
    "A": ["Messico",     "Cechia",       "Corea del Sud",  "Sudafrica"],
    "B": ["Svizzera",    "Canada",       "Bosnia",         "Qatar"],
    "C": ["Brasile",     "Marocco",      "Haiti",          "Scozia"],
    "D": ["Australia",   "Stati Uniti",  "Paraguay",       "Turchia"],
    "E": ["Germania",    "Ecuador",      "Costa d'Avorio", "Curacao"],
    "F": ["Giappone",    "Olanda",       "Svezia",         "Tunisia"],
    "G": ["Belgio",      "Egitto",       "Iran",           "Nuova Zelanda"],
    "H": ["Spagna",      "Uruguay",      "Arabia Saudita", "Capo Verde"],
    "I": ["Francia",     "Senegal",      "Norvegia",       "Iraq"],
    "J": ["Argentina",   "Algeria",      "Austria",        "Giordania"],
    "K": ["Portogallo",  "Colombia",     "Rep. del Congo", "Uzbekistan"],
    "L": ["Inghilterra", "Croazia",      "Ghana",          "Panama"],
}

CSV_MAP = {
    "Cechia":           "data/Girone_A/repubblica_ceca.csv",
    "Corea del Sud":    "data/Girone_A/corea_del_sud.csv",
    "Sudafrica":        "data/Girone_A/sud_africa.csv",
    "Bosnia":           "data/Girone_B/bosnia.csv",
    "Canada":           "data/Girone_B/canada.csv",
    "Svizzera":         "data/Girone_B/svizzera.csv",
    "Brasile":          "data/Girone_C/brasile.csv",
    "Haiti":            "data/Girone_C/haiti.csv",
    "Marocco":          "data/Girone_C/marocco.csv",
    "Scozia":           "data/Girone_C/scozia.csv",
    "Turchia":          "data/Girone_D/turchia.csv",
    "Stati Uniti":      "data/Girone_D/usa.csv",
    "Costa d'Avorio":   "data/Girone_E/costa_d'avorio.csv",
    "Curacao":          "data/Girone_E/curacao.csv",
    "Germania":         "data/Girone_E/germania.csv",
    "Giappone":         "data/Girone_F/giappone.csv",
    "Olanda":           "data/Girone_F/olanda.csv",
    "Svezia":           "data/Girone_F/svezia.csv",
    "Tunisia":          "data/Girone_F/tunisia.csv",
    "Belgio":           "data/Girone_G/belgio.csv",
    "Egitto":           "data/Girone_G/egitto.csv",
    "Nuova Zelanda":    "data/Girone_G/nuova_zelanda.csv",
    "Capo Verde":       "data/Girone_H/capo_verde.csv",
    "Spagna":           "data/Girone_H/spagna.csv",
    "Francia":          "data/Girone_I/francia.csv",
    "Norvegia":         "data/Girone_I/norvegia.csv",
    "Senegal":          "data/Girone_I/senegal.csv",
    "Argentina":        "data/Girone_J/argentina.csv",
    "Austria":          "data/Girone_J/austria.csv",
    "Colombia":         "data/Girone_K/colombia.csv",
    "Portogallo":       "data/Girone_K/portogallo.csv",
    "Rep. del Congo":   "data/Girone_K/repubblica_del_congo.csv",
    "Croazia":          "data/Girone_L/croazia.csv",
    "Inghilterra":      "data/Girone_L/inghilterra.csv",
    "Panama":           "data/Girone_L/panama.csv",
}

def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"

def load_players(team):
    path = CSV_MAP.get(team)
    if path and os.path.exists(path):
        return pd.read_csv(path)
    return None

def render_player_stats(row):
    """Genera le statistiche HTML in base al ruolo del giocatore."""
    ruolo = row.get("Ruolo", "")

    if ruolo == "POR":
        parate = int(row["Parate"]) if "Parate" in row and pd.notna(row.get("Parate")) else 0
        stats_html = (
            f"<div class='wca-stat'>🧤 Parate <span>{parate}</span></div>"
            f"<div class='wca-stat'>📋 Presenze <span>{int(row.get('Presenze', 0))}</span></div>"
            f"<div class='wca-stat'>📐 Pass% <span>{row.get('PassAccuracy', 0)}%</span></div>"
        )
    elif ruolo == "DIF":
        stats_html = (
            f"<div class='wca-stat'>📋 Presenze <span>{int(row.get('Presenze', 0))}</span></div>"
            f"<div class='wca-stat'>⚽ Gol <span>{int(row.get('Gol', 0))}</span></div>"
            f"<div class='wca-stat'>🎯 Assist <span>{int(row.get('Assist', 0))}</span></div>"
            f"<div class='wca-stat'>🤼 Duelli <span>{int(row.get('DuelliVinti', 0))}</span></div>"
        )
    elif ruolo == "CEN":
        stats_html = (
            f"<div class='wca-stat'>📋 Presenze <span>{int(row.get('Presenze', 0))}</span></div>"
            f"<div class='wca-stat'>⚽ Gol <span>{int(row.get('Gol', 0))}</span></div>"
            f"<div class='wca-stat'>🎯 Assist <span>{int(row.get('Assist', 0))}</span></div>"
            f"<div class='wca-stat'>🔑 KeyPass <span>{int(row.get('KeyPasses', 0))}</span></div>"
        )
    elif ruolo == "ALA":
        stats_html = (
            f"<div class='wca-stat'>📋 Presenze <span>{int(row.get('Presenze', 0))}</span></div>"
            f"<div class='wca-stat'>⚽ Gol <span>{int(row.get('Gol', 0))}</span></div>"
            f"<div class='wca-stat'>🎯 Assist <span>{int(row.get('Assist', 0))}</span></div>"
            f"<div class='wca-stat'>🌀 Dribbling <span>{int(row.get('Dribbling', 0))}</span></div>"
        )
    else:  # ATT
        stats_html = (
            f"<div class='wca-stat'>📋 Presenze <span>{int(row.get('Presenze', 0))}</span></div>"
            f"<div class='wca-stat'>⚽ Gol <span>{int(row.get('Gol', 0))}</span></div>"
            f"<div class='wca-stat'>🎯 Assist <span>{int(row.get('Assist', 0))}</span></div>"
            f"<div class='wca-stat'>📐 xG <span>{row.get('xG', 0)}</span></div>"
        )
    return stats_html

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>📊 TEAM COMPARISON</h1>", unsafe_allow_html=True)

df = pd.read_csv("data/team_stats.csv")
gironi_list = [f"Girone {k}" for k in GIRONI.keys()]

col1, col2 = st.columns(2)
with col1:
    girone1 = st.selectbox("Girone Squadra 1", gironi_list, key="g1")
    squadre1 = GIRONI[girone1.replace("Girone ", "")]
    team1 = st.selectbox("Squadra 1", squadre1, key="t1")
with col2:
    girone2 = st.selectbox("Girone Squadra 2", gironi_list, key="g2")
    squadre2 = GIRONI[girone2.replace("Girone ", "")]
    team2 = st.selectbox("Squadra 2", squadre2, key="t2")

if team1 == team2:
    st.warning("Seleziona due squadre diverse.")
    st.stop()

t1_row = df[df["Squadra"] == team1]
t2_row = df[df["Squadra"] == team2]

if t1_row.empty or t2_row.empty:
    st.error("Dati non trovati per una delle squadre selezionate.")
    st.stop()

t1 = t1_row.iloc[0]
t2 = t2_row.iloc[0]

st.markdown("---")

# ── HEADER ────────────────────────────────────────────────────────────────────
col_l, col_c, col_r = st.columns([3, 1, 3])
with col_l:
    fp = flag_path(team1)
    if os.path.exists(fp): st.image(fp, width=70)
    st.markdown(f"### {team1}")
    st.markdown(f"<span class='wca-badge'>Girone {girone1.replace('Girone ', '')}</span>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Gol", t1["Gol"])
    c2.metric("xG", t1["xG"])
    c3.metric("Possesso", f"{t1['Possesso']}%")

with col_c:
    st.markdown(
        "<div style='text-align:center;padding-top:40px'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:#6b7a99;letter-spacing:3px'>VS</div>"
        "</div>",
        unsafe_allow_html=True
    )

with col_r:
    fp2 = flag_path(team2)
    if os.path.exists(fp2): st.image(fp2, width=70)
    st.markdown(f"### {team2}")
    st.markdown(f"<span class='wca-badge'>Girone {girone2.replace('Girone ', '')}</span>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Gol", t2["Gol"])
    c2.metric("xG", t2["xG"])
    c3.metric("Possesso", f"{t2['Possesso']}%")

st.markdown("---")

# ── STATS A CONFRONTO ─────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📊 Statistiche a Confronto</span>", unsafe_allow_html=True)

stats_confronto = [
    ("⚽ Gol/Match",       "Gol",                ""),
    ("📐 xG",              "xG",                 ""),
    ("🎯 Tiri",            "Tiri",               ""),
    ("🔵 Possesso",        "Possesso",           "%"),
    ("✅ Prec. Passaggi",  "PrecisionePassaggi", "%"),
    ("⭐ Overall",         "OverallRating",      ""),
    ("⚔️ Attacco",         "AttackRating",       ""),
    ("🎯 Centrocampo",     "MidfieldRating",     ""),
    ("🛡️ Difesa",          "DefenseRating",      ""),
]

for label, col, suffix in stats_confronto:
    v1 = float(t1[col])
    v2 = float(t2[col])
    max_v = max(v1, v2, 0.01)
    w1 = int(v1 / max_v * 100)
    w2 = int(v2 / max_v * 100)
    c1c = "#00d4ff" if v1 >= v2 else "#6b7a99"
    c2c = "#ff3b5c" if v2 > v1 else "#6b7a99"
    st.markdown(
        f"<div style='margin-bottom:12px'>"
        f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
        f"<span style='font-weight:700;color:{c1c}'>{v1}{suffix}</span>"
        f"<span style='font-size:12px;color:#6b7a99'>{label}</span>"
        f"<span style='font-weight:700;color:{c2c}'>{v2}{suffix}</span>"
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

# ── RADAR ─────────────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📈 Radar</span>", unsafe_allow_html=True)

radar_stats = ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]
fig = go.Figure()
for team, data, color in [(team1, t1, "#00d4ff"), (team2, t2, "#ff3b5c")]:
    fig.add_trace(go.Scatterpolar(
        r=[data[s] for s in radar_stats],
        theta=radar_stats,
        fill='toself',
        name=team,
        line=dict(color=color, width=2)
    ))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    polar=dict(
        bgcolor="rgba(26,32,53,0.6)",
        radialaxis=dict(visible=True, gridcolor="#1f2d45", color="#6b7a99"),
        angularaxis=dict(gridcolor="#1f2d45", color="#6b7a99")
    ),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8edf5")),
    height=420,
    showlegend=True
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── ROSA SQUADRE ──────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>👥 Rosa delle Squadre</span>", unsafe_allow_html=True)

# Legenda ruoli
st.markdown(
    "<div style='display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px'>"
    "<span class='wca-badge'>🧤 POR — Portiere: Parate · Presenze · Pass%</span>"
    "<span class='wca-badge'>🛡️ DIF — Difensore: Presenze · Gol · Assist · Duelli</span>"
    "<span class='wca-badge'>🔄 CEN — Centrocampista: Presenze · Gol · Assist · KeyPass</span>"
    "<span class='wca-badge wca-badge-red'>🌀 ALA — Ala: Presenze · Gol · Assist · Dribbling</span>"
    "<span class='wca-badge wca-badge-red'>⚽ ATT — Attaccante: Presenze · Gol · Assist · xG</span>"
    "</div>",
    unsafe_allow_html=True
)

role_colors = {
    "ATT": "wca-badge-red", "ALA": "wca-badge-red",
    "CEN": "wca-badge",     "DIF": "wca-badge",
    "POR": "wca-badge"
}

col_p1, col_p2 = st.columns(2)
for col, team in [(col_p1, team1), (col_p2, team2)]:
    with col:
        fp_flag = flag_path(team)
        if os.path.exists(fp_flag):
            st.image(fp_flag, width=36)
        st.markdown(f"**{team}**")
        df_players = load_players(team)
        if df_players is None:
            st.info("Rosa non ancora disponibile.")
        else:
            # Raggruppa per ruolo: POR → DIF → CEN → ALA → ATT
            role_order = ["POR", "DIF", "CEN", "ALA", "ATT"]
            for ruolo in role_order:
                gruppo = df_players[df_players["Ruolo"] == ruolo]
                if gruppo.empty:
                    continue
                ruolo_label = {
                    "POR": "🧤 Portieri",
                    "DIF": "🛡️ Difensori",
                    "CEN": "🔄 Centrocampisti",
                    "ALA": "🌀 Ali",
                    "ATT": "⚽ Attaccanti"
                }[ruolo]
                st.markdown(
                    f"<div style='color:#6b7a99;font-size:11px;text-transform:uppercase;"
                    f"letter-spacing:1px;font-weight:600;margin:10px 0 6px'>{ruolo_label}</div>",
                    unsafe_allow_html=True
                )
                for _, row in gruppo.iterrows():
                    rc = role_colors.get(ruolo, "wca-badge")
                    stats_html = render_player_stats(row)
                    st.markdown(
                        f"<div class='wca-card' style='padding:10px 14px;margin-bottom:6px'>"
                        f"<div style='display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px'>"
                        f"<span style='font-weight:700;font-size:14px'>{row['Giocatore']}</span>"
                        f"<span class='{rc}'>{ruolo}</span>"
                        f"<span style='color:#6b7a99;font-size:11px'>{row.get('Età','')} anni</span>"
                        f"</div>"
                        f"<div class='wca-stat-row'>{stats_html}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )