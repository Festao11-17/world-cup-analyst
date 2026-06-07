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
    # Girone A
    "Cechia":           "data/Girone_A/repubblica_ceca.csv",
    "Corea del Sud":    "data/Girone_A/corea_del_sud.csv",
    "Messico":          "data/Girone_A/messico.csv",
    "Sudafrica":        "data/Girone_A/sud_africa.csv",
    # Girone B
    "Bosnia":           "data/Girone_B/bosnia.csv",
    "Canada":           "data/Girone_B/canada.csv",
    "Qatar":            "data/Girone_B/qatar.csv",
    "Svizzera":         "data/Girone_B/svizzera.csv",
    # Girone C
    "Brasile":          "data/Girone_C/brasile.csv",
    "Haiti":            "data/Girone_C/haiti.csv",
    "Marocco":          "data/Girone_C/marocco.csv",
    "Scozia":           "data/Girone_C/scozia.csv",
    # Girone D
    "Australia":        "data/Girone_D/australia.csv",
    "Paraguay":         "data/Girone_D/paraguay.csv",
    "Stati Uniti":      "data/Girone_D/usa.csv",
    "Turchia":          "data/Girone_D/turchia.csv",
    # Girone E
    "Costa d'Avorio":   "data/Girone_E/costa_d'avorio.csv",
    "Curacao":          "data/Girone_E/curacao.csv",
    "Ecuador":          "data/Girone_E/ecuador.csv",
    "Germania":         "data/Girone_E/germania.csv",
    # Girone F
    "Giappone":         "data/Girone_F/giappone.csv",
    "Olanda":           "data/Girone_F/olanda.csv",
    "Svezia":           "data/Girone_F/svezia.csv",
    "Tunisia":          "data/Girone_F/tunisia.csv",
    # Girone G
    "Belgio":           "data/Girone_G/belgio.csv",
    "Egitto":           "data/Girone_G/egitto.csv",
    "Iran":             "data/Girone_G/iran.csv",
    "Nuova Zelanda":    "data/Girone_G/nuova_zelanda.csv",
    # Girone H
    "Arabia Saudita":   "data/Girone_H/arabia_saudita.csv",
    "Capo Verde":       "data/Girone_H/capo_verde.csv",
    "Spagna":           "data/Girone_H/spagna.csv",
    "Uruguay":          "data/Girone_H/uruguay.csv",
    # Girone I
    "Francia":          "data/Girone_I/francia.csv",
    "Iraq":             "data/Girone_I/iraq.csv",
    "Norvegia":         "data/Girone_I/norvegia.csv",
    "Senegal":          "data/Girone_I/senegal.csv",
    # Girone J
    "Algeria":          "data/Girone_J/algeria.csv",
    "Argentina":        "data/Girone_J/argentina.csv",
    "Austria":          "data/Girone_J/austria.csv",
    "Giordania":        "data/Girone_J/giordania.csv",
    # Girone K
    "Colombia":         "data/Girone_K/colombia.csv",
    "Portogallo":       "data/Girone_K/portogallo.csv",
    "Rep. del Congo":   "data/Girone_K/repubblica_del_congo.csv",
    "Uzbekistan":       "data/Girone_K/uzbekistan.csv",
    # Girone L
    "Croazia":          "data/Girone_L/croazia.csv",
    "Ghana":            "data/Girone_L/ghana.csv",
    "Inghilterra":      "data/Girone_L/inghilterra.csv",
    "Panama":           "data/Girone_L/panama.csv",
}

# Colonne da escludere dalla visualizzazione (già mostrate nell'intestazione)
SKIP_COLS = {"Squadra", "Ruolo", "Età", "Giocatore"}

# Etichette, emoji e unità per ogni colonna
COL_META = {
    "Presenze":          ("📋", "Presenze",        ""),
    "Gol":               ("⚽", "Gol",             ""),
    "Assist":            ("🎯", "Assist",           ""),
    "xG":                ("📐", "xG",              ""),
    "Tiri":              ("🔫", "Tiri",            ""),
    "Velocita":          ("⚡", "Velocità",         " km/h"),
    "KeyPasses":         ("🔑", "KeyPasses",       " p/p"),
    "Dribbling":         ("🌀", "Dribbling",        " p/p"),
    "DuelliVinti":       ("🤼", "Duelli Vinti",     "%"),
    "DistanzaPercorsa":  ("🏃", "Dist.",            " km"),
    "PassAccuracy":      ("✅", "Pass%",            "%"),
    "Parate":            ("🧤", "Parate",           ""),
}

def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"

def load_players(team):
    path = CSV_MAP.get(team)
    if path and os.path.exists(path):
        return pd.read_csv(path)
    return None

def render_player_card(row):
    """Genera la card HTML del giocatore con statistiche appropriate per ruolo."""
    ruolo = row.get("Ruolo", "")

    # Colonne da mostrare in base al ruolo
    if ruolo == "POR":
        # Portieri: mostra tutte le stat > 0 (escluse quelle di movimento offensivo)
        cols_show = ["Presenze", "Parate", "PassAccuracy", "DistanzaPercorsa"]
    elif ruolo == "DIF":
        cols_show = ["Presenze", "Gol", "Assist", "Tiri", "DuelliVinti",
                     "DistanzaPercorsa", "PassAccuracy"]
    elif ruolo == "CEN":
        cols_show = ["Presenze", "Gol", "Assist", "xG", "Tiri", "KeyPasses",
                     "DistanzaPercorsa", "PassAccuracy"]
    elif ruolo == "ALA":
        cols_show = ["Presenze", "Gol", "Assist", "xG", "Tiri", "Velocita",
                     "Dribbling", "KeyPasses", "DistanzaPercorsa"]
    else:  # ATT
        cols_show = ["Presenze", "Gol", "Assist", "xG", "Tiri", "Velocita",
                     "DuelliVinti", "DistanzaPercorsa"]

    stats_html = ""
    for col in cols_show:
        if col not in row or pd.isna(row[col]):
            continue
        val = row[col]
        # Salta tutti i valori a 0 — nessuna statistica inutile
        try:
            if float(val) == 0:
                continue
        except (ValueError, TypeError):
            pass
        emoji, label, unit = COL_META.get(col, ("", col, ""))
        # Formattazione valore
        if isinstance(val, float) and val == int(val):
            val_str = str(int(val))
        else:
            val_str = str(val)
        stats_html += (
            f"<div class='wca-stat'>{emoji} {label} "
            f"<span>{val_str}{unit}</span></div>"
        )

    role_colors = {
        "ATT": "wca-badge-red", "ALA": "wca-badge-red",
        "CEN": "wca-badge",     "DIF": "wca-badge",
        "POR": "wca-badge"
    }
    rc = role_colors.get(ruolo, "wca-badge")

    return (
        f"<div class='wca-card' style='padding:10px 14px;margin-bottom:6px'>"
        f"<div style='display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px'>"
        f"<span style='font-weight:700;font-size:14px'>{row['Giocatore']}</span>"
        f"<span class='{rc}'>{ruolo}</span>"
        f"<span style='color:#6b7a99;font-size:11px'>{row.get('Età','')} anni</span>"
        f"</div>"
        f"<div class='wca-stat-row'>{stats_html}</div>"
        f"</div>"
    )

def render_rosa(team):
    """Mostra la rosa di una squadra divisa per ruolo."""
    fp_flag = flag_path(team)
    if os.path.exists(fp_flag):
        st.image(fp_flag, width=36)
    st.markdown(f"**{team}**")

    df_players = load_players(team)
    if df_players is None:
        st.info("Rosa non ancora disponibile.")
        return

    role_order = {
        "POR": "🧤 Portieri",
        "DIF": "🛡️ Difensori",
        "CEN": "🔄 Centrocampisti",
        "ALA": "🌀 Ali",
        "ATT": "⚽ Attaccanti"
    }
    for ruolo, label in role_order.items():
        gruppo = df_players[df_players["Ruolo"] == ruolo]
        if gruppo.empty:
            continue
        st.markdown(
            f"<div style='color:#6b7a99;font-size:11px;text-transform:uppercase;"
            f"letter-spacing:1px;font-weight:600;margin:10px 0 4px'>{label}</div>",
            unsafe_allow_html=True
        )
        for _, row in gruppo.iterrows():
            st.markdown(render_player_card(row), unsafe_allow_html=True)

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>📊 TEAM COMPARISON</h1>", unsafe_allow_html=True)

df = pd.read_csv("data/team_stats.csv")
gironi_list = [f"Girone {k}" for k in GIRONI.keys()]

col1, col2 = st.columns(2)
with col1:
    girone1 = st.selectbox("Girone Squadra 1", gironi_list, key="g1")
    team1   = st.selectbox("Squadra 1", GIRONI[girone1.replace("Girone ", "")], key="t1")
with col2:
    girone2 = st.selectbox("Girone Squadra 2", gironi_list, key="g2")
    team2   = st.selectbox("Squadra 2", GIRONI[girone2.replace("Girone ", "")], key="t2")

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
    c1.metric("Gol", t1["Gol"]); c2.metric("xG", t1["xG"]); c3.metric("Possesso", f"{t1['Possesso']}%")
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
    st.markdown(f"<span class='wca-badge'>Girone {girone2.replace('Girone ', '')}</span>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Gol", t2["Gol"]); c2.metric("xG", t2["xG"]); c3.metric("Possesso", f"{t2['Possesso']}%")

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
    v1 = float(t1[col]); v2 = float(t2[col])
    max_v = max(v1, v2, 0.01)
    w1 = int(v1/max_v*100); w2 = int(v2/max_v*100)
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
radar_stats = ["Gol","xG","Tiri","Possesso","PrecisionePassaggi"]
fig = go.Figure()
for team, data, color in [(team1, t1, "#00d4ff"), (team2, t2, "#ff3b5c")]:
    fig.add_trace(go.Scatterpolar(
        r=[data[s] for s in radar_stats], theta=radar_stats,
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

st.markdown("---")

# ── ROSA SQUADRE ──────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>👥 Rosa delle Squadre</span>", unsafe_allow_html=True)

# Legenda unità di misura
st.markdown(
    "<div style='color:#6b7a99;font-size:11px;margin-bottom:12px'>"
    "📐 xG = gol attesi &nbsp;·&nbsp; ✅ Pass Accuracy = % &nbsp;·&nbsp; "
    "🏃 Dist. Percorsa = km/partita &nbsp;·&nbsp; ⚡ Velocità = km/h max"
    "</div>",
    unsafe_allow_html=True
)

col_p1, col_p2 = st.columns(2)
with col_p1:
    render_rosa(team1)
with col_p2:
    render_rosa(team2)