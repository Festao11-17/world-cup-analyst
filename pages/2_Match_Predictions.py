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
def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"

st.markdown("<h1>🔮 MATCH PREDICTION</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6b7a99;margin-bottom:24px'>Predizioni basate su Power Rating, xG e statistiche avanzate.</p>", unsafe_allow_html=True)

df = pd.read_csv("data/team_stats.csv")
teams = sorted(df["Squadra"].tolist())

# ── SOLO RICERCA ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    search1 = st.text_input("🔍 Squadra Casa", placeholder="Scrivi per cercare... es. Brasile")
    results1 = [t for t in teams if search1.lower() in t.lower()] if search1 else []
    if not search1:
        st.caption("Inizia a scrivere per cercare una squadra")
        st.stop()
    if not results1:
        st.warning("Nessuna squadra trovata.")
        st.stop()
    team1 = results1[0] if len(results1) == 1 else st.selectbox("Seleziona", results1, key="s1")

with col2:
    search2 = st.text_input("🔍 Squadra Ospite", placeholder="Scrivi per cercare... es. Francia")
    results2 = [t for t in teams if search2.lower() in t.lower()] if search2 else []
    if not search2:
        st.caption("Inizia a scrivere per cercare una squadra")
        st.stop()
    if not results2:
        st.warning("Nessuna squadra trovata.")
        st.stop()
    team2 = results2[0] if len(results2) == 1 else st.selectbox("Seleziona", results2, key="s2")

if team1 == team2:
    st.warning("Seleziona due squadre diverse.")
    st.stop()

t1 = df[df["Squadra"] == team1].iloc[0]
t2 = df[df["Squadra"] == team2].iloc[0]

st.markdown("---")

# ── HEADER ────────────────────────────────────────────────────────────────────
col_l, col_c, col_r = st.columns([3, 1, 3])
with col_l:
    fp = flag_path(team1)
    if os.path.exists(fp): st.image(fp, width=70)
    st.markdown(f"### {team1}")
    st.markdown(f"<span class='wca-badge'>⭐ {t1['OverallRating']} Overall</span>", unsafe_allow_html=True)
with col_c:
    st.markdown("<div style='text-align:center;padding-top:36px'><div style='font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:#6b7a99;letter-spacing:3px'>VS</div></div>", unsafe_allow_html=True)
with col_r:
    fp2 = flag_path(team2)
    if os.path.exists(fp2): st.image(fp2, width=70)
    st.markdown(f"### {team2}")
    st.markdown(f"<span class='wca-badge'>⭐ {t2['OverallRating']} Overall</span>", unsafe_allow_html=True)

st.markdown("---")

# ── CALCOLO ───────────────────────────────────────────────────────────────────
s1 = t1["OverallRating"]*0.50 + t1["AttackRating"]*0.25 + t1["MidfieldRating"]*0.15 + t1["DefenseRating"]*0.10
s2 = t2["OverallRating"]*0.50 + t2["AttackRating"]*0.25 + t2["MidfieldRating"]*0.15 + t2["DefenseRating"]*0.10
total = s1 + s2
p1 = round((s1/total)*100, 1)
p2 = round((s2/total)*100, 1)
draw = round(max(0, 35 - abs(p1-p2)*0.8), 1)
factor = (100-draw)/100
p1_adj = round(p1*factor, 1)
p2_adj = round(p2*factor, 1)
xg1 = round(t1["xG"]*(t1["AttackRating"]/75), 1)
xg2 = round(t2["xG"]*(t2["AttackRating"]/75), 1)
goals1 = int(round(xg1*0.85))
goals2 = int(round(xg2*0.85))

# ── WIN PROBABILITY ───────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📊 Win Probability</span>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric(f"🏆 {team1}", f"{p1_adj}%")
c2.metric("🤝 Pareggio", f"{draw}%")
c3.metric(f"🏆 {team2}", f"{p2_adj}%")
st.markdown(
    f"<div style='margin:16px 0 8px;display:flex;border-radius:8px;overflow:hidden;height:28px'>"
    f"<div style='width:{p1_adj}%;background:#00d4ff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700'>{p1_adj}%</div>"
    f"<div style='width:{draw}%;background:#1f2d45;display:flex;align-items:center;justify-content:center;font-size:12px;color:#6b7a99'>{draw}%</div>"
    f"<div style='width:{p2_adj}%;background:#ff3b5c;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700'>{p2_adj}%</div>"
    f"</div><div style='display:flex;justify-content:space-between;font-size:11px;color:#6b7a99'>"
    f"<span>{team1}</span><span>Pareggio</span><span>{team2}</span></div>",
    unsafe_allow_html=True
)

st.markdown("---")

# ── SCORE ─────────────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>⚽ Risultato Previsto</span>", unsafe_allow_html=True)
cs1, cscore, cs2 = st.columns([2, 1, 2])
with cs1:
    st.markdown(f"<div class='wca-card' style='text-align:center'><div style='font-size:11px;color:#6b7a99;text-transform:uppercase;letter-spacing:1px'>xG Previsto</div><div style='font-size:3rem;font-family:Bebas Neue,sans-serif;color:#00d4ff'>{xg1}</div><div style='font-size:12px;color:#6b7a99'>{team1}</div></div>", unsafe_allow_html=True)
with cscore:
    st.markdown(f"<div style='text-align:center;padding-top:20px'><div style='font-family:Bebas Neue,sans-serif;font-size:3.5rem;letter-spacing:4px'>{goals1} - {goals2}</div><div style='color:#6b7a99;font-size:11px;text-transform:uppercase;letter-spacing:2px'>Pronostico</div></div>", unsafe_allow_html=True)
with cs2:
    st.markdown(f"<div class='wca-card' style='text-align:center'><div style='font-size:11px;color:#6b7a99;text-transform:uppercase;letter-spacing:1px'>xG Previsto</div><div style='font-size:3rem;font-family:Bebas Neue,sans-serif;color:#ff3b5c'>{xg2}</div><div style='font-size:12px;color:#6b7a99'>{team2}</div></div>", unsafe_allow_html=True)

st.markdown("---")

# ── ANALISI REPARTO ───────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📈 Analisi per Reparto</span>", unsafe_allow_html=True)
for label, r1, r2 in [
    ("⚔️ Attacco",     t1["AttackRating"],   t2["AttackRating"]),
    ("🔄 Centrocampo", t1["MidfieldRating"],  t2["MidfieldRating"]),
    ("🛡️ Difesa",      t1["DefenseRating"],   t2["DefenseRating"]),
    ("⭐ Overall",     t1["OverallRating"],   t2["OverallRating"]),
]:
    max_r = max(float(r1), float(r2), 0.01)
    c1c = "#00d4ff" if float(r1) >= float(r2) else "#6b7a99"
    c2c = "#ff3b5c" if float(r2) > float(r1) else "#6b7a99"
    st.markdown(
        f"<div style='margin-bottom:14px'>"
        f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
        f"<span style='font-weight:700;color:{c1c}'>{r1}</span>"
        f"<span style='font-size:12px;color:#6b7a99'>{label}</span>"
        f"<span style='font-weight:700;color:{c2c}'>{r2}</span>"
        f"</div>"
        f"<div style='display:flex;gap:4px'>"
        f"<div style='flex:1;background:#1f2d45;border-radius:4px;height:8px;display:flex;justify-content:flex-end'>"
        f"<div style='width:{int(float(r1)/max_r*100)}%;background:#00d4ff;border-radius:4px;height:8px'></div></div>"
        f"<div style='flex:1;background:#1f2d45;border-radius:4px;height:8px'>"
        f"<div style='width:{int(float(r2)/max_r*100)}%;background:#ff3b5c;border-radius:4px;height:8px'></div></div>"
        f"</div></div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ── RADAR ─────────────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📡 Radar Confronto</span>", unsafe_allow_html=True)
stats = ["Gol","xG","Tiri","Possesso","PrecisionePassaggi"]
fig = go.Figure()
for team, data, color in [(team1, t1, "#00d4ff"), (team2, t2, "#ff3b5c")]:
    fig.add_trace(go.Scatterpolar(r=[data[s] for s in stats], theta=stats, fill='toself', name=team, line=dict(color=color, width=2)))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    polar=dict(bgcolor="rgba(26,32,53,0.6)", radialaxis=dict(visible=True, gridcolor="#1f2d45", color="#6b7a99"), angularaxis=dict(gridcolor="#1f2d45", color="#6b7a99")),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8edf5")), height=400, showlegend=True
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── INSIGHTS ──────────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>💡 Match Insights</span>", unsafe_allow_html=True)
insights = []
att_diff = t1["AttackRating"] - t2["AttackRating"]
if att_diff >= 8:    insights.append(("⚔️", f"{team1} ha un attacco nettamente superiore ({t1['AttackRating']} vs {t2['AttackRating']}).", "cyan"))
elif att_diff <= -8: insights.append(("⚔️", f"{team2} ha un attacco nettamente superiore ({t2['AttackRating']} vs {t1['AttackRating']}).", "red"))
else:                insights.append(("⚔️", f"Attacchi molto equilibrati ({t1['AttackRating']} vs {t2['AttackRating']}).", "muted"))
mid_diff = t1["MidfieldRating"] - t2["MidfieldRating"]
if mid_diff >= 8:    insights.append(("🔄", f"{team1} domina il centrocampo ({t1['MidfieldRating']} vs {t2['MidfieldRating']}).", "cyan"))
elif mid_diff <= -8: insights.append(("🔄", f"{team2} domina il centrocampo ({t2['MidfieldRating']} vs {t1['MidfieldRating']}).", "red"))
else:                insights.append(("🔄", f"Centrocampo equilibrato ({t1['MidfieldRating']} vs {t2['MidfieldRating']}).", "muted"))
def_diff = t1["DefenseRating"] - t2["DefenseRating"]
if def_diff >= 8:    insights.append(("🛡️", f"{team1} ha una difesa più solida ({t1['DefenseRating']} vs {t2['DefenseRating']}).", "cyan"))
elif def_diff <= -8: insights.append(("🛡️", f"{team2} ha una difesa più solida ({t2['DefenseRating']} vs {t1['DefenseRating']}).", "red"))
else:                insights.append(("🛡️", f"Difese simili ({t1['DefenseRating']} vs {t2['DefenseRating']}).", "muted"))
xg_diff = t1["xG"] - t2["xG"]
if xg_diff >= 0.3:    insights.append(("📐", f"{team1} crea occasioni di maggior qualità (xG {t1['xG']} vs {t2['xG']}).", "cyan"))
elif xg_diff <= -0.3: insights.append(("📐", f"{team2} crea occasioni di maggior qualità (xG {t2['xG']} vs {t1['xG']}).", "red"))
else:                 insights.append(("📐", "xG molto simile — partita che si decide nei dettagli.", "muted"))
pos_diff = t1["Possesso"] - t2["Possesso"]
if pos_diff >= 5:    insights.append(("🔵", f"{team1} controlla il pallone ({t1['Possesso']}% vs {t2['Possesso']}%).", "cyan"))
elif pos_diff <= -5: insights.append(("🔵", f"{team2} controlla il pallone ({t2['Possesso']}% vs {t1['Possesso']}%).", "red"))
overall_diff = abs(t1["OverallRating"] - t2["OverallRating"])
if overall_diff < 3:
    insights.append(("⚡", "Gap minimo — pronostico apertissimo.", "muted"))
elif overall_diff >= 12:
    stronger = team1 if t1["OverallRating"] > t2["OverallRating"] else team2
    insights.append(("⚡", f"{stronger} è favorita su tutti i fronti.", "cyan" if stronger == team1 else "red"))
color_map = {"cyan":"#00d4ff","red":"#ff3b5c","muted":"#6b7a99"}
for emoji, text, ck in insights:
    c = color_map[ck]
    st.markdown(f"<div class='wca-card' style='padding:12px 18px;margin-bottom:8px;border-left:3px solid {c}'><span style='margin-right:10px'>{emoji}</span><span style='color:{c};font-size:14px'>{text}</span></div>", unsafe_allow_html=True)

st.markdown("---")

# ── VERDETTO ──────────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>🏆 Verdetto</span>", unsafe_allow_html=True)
diff = abs(t1["OverallRating"] - t2["OverallRating"])
fav, fav_p, und_p = (team1, p1_adj, p2_adj) if p1_adj > p2_adj else (team2, p2_adj, p1_adj)
if diff >= 10:   verdict = f"<span class='wca-badge'>🟢 FAVORITA NETTA</span> &nbsp; <b>{fav}</b> domina su carta con un gap di <b>{diff:.1f} punti</b>."
elif diff >= 5:  verdict = f"<span class='wca-badge'>🟡 LEGGERO VANTAGGIO</span> &nbsp; <b>{fav}</b> parte favorita ({fav_p}% vs {und_p}%), ma la partita è aperta."
else:            verdict = f"<span class='wca-badge wca-badge-red'>🔴 EQUILIBRIO TOTALE</span> &nbsp; Gap di soli <b>{diff:.1f} punti</b>. Ogni dettaglio conta."
st.markdown(f"<div class='wca-card'>{verdict}</div>", unsafe_allow_html=True)