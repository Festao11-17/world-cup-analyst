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

# Ranking FIFA reale — solo le 48 squadre qualificate, senza Italia
FIFA_RANKINGS = [
    {"Squadra":"Argentina",    "RankingFIFA":1,  "Punti":1874.3, "Girone":"J"},
    {"Squadra":"Francia",      "RankingFIFA":2,  "Punti":1851.4, "Girone":"I"},
    {"Squadra":"Spagna",       "RankingFIFA":3,  "Punti":1836.7, "Girone":"H"},
    {"Squadra":"Inghilterra",  "RankingFIFA":4,  "Punti":1806.9, "Girone":"L"},
    {"Squadra":"Brasile",      "RankingFIFA":5,  "Punti":1782.1, "Girone":"C"},
    {"Squadra":"Portogallo",   "RankingFIFA":6,  "Punti":1764.5, "Girone":"K"},
    {"Squadra":"Belgio",       "RankingFIFA":7,  "Punti":1742.8, "Girone":"G"},
    {"Squadra":"Olanda",       "RankingFIFA":8,  "Punti":1731.2, "Girone":"F"},
    {"Squadra":"Germania",     "RankingFIFA":9,  "Punti":1720.6, "Girone":"E"},
    {"Squadra":"Colombia",     "RankingFIFA":10, "Punti":1698.4, "Girone":"K"},
    {"Squadra":"Croazia",      "RankingFIFA":11, "Punti":1687.3, "Girone":"L"},
    {"Squadra":"Uruguay",      "RankingFIFA":12, "Punti":1658.9, "Girone":"H"},
    {"Squadra":"Marocco",      "RankingFIFA":13, "Punti":1641.5, "Girone":"C"},
    {"Squadra":"Svizzera",     "RankingFIFA":14, "Punti":1630.8, "Girone":"B"},
    {"Squadra":"Messico",      "RankingFIFA":15, "Punti":1618.2, "Girone":"A"},
    {"Squadra":"Stati Uniti",  "RankingFIFA":16, "Punti":1605.7, "Girone":"D"},
    {"Squadra":"Giappone",     "RankingFIFA":17, "Punti":1594.3, "Girone":"F"},
    {"Squadra":"Senegal",      "RankingFIFA":18, "Punti":1581.6, "Girone":"I"},
    {"Squadra":"Austria",      "RankingFIFA":19, "Punti":1568.4, "Girone":"J"},
    {"Squadra":"Norvegia",     "RankingFIFA":20, "Punti":1554.7, "Girone":"I"},
    {"Squadra":"Turchia",      "RankingFIFA":21, "Punti":1541.2, "Girone":"D"},
    {"Squadra":"Australia",    "RankingFIFA":22, "Punti":1528.6, "Girone":"D"},
    {"Squadra":"Cechia",       "RankingFIFA":23, "Punti":1514.9, "Girone":"A"},
    {"Squadra":"Ecuador",      "RankingFIFA":24, "Punti":1501.3, "Girone":"E"},
    {"Squadra":"Algeria",      "RankingFIFA":25, "Punti":1487.8, "Girone":"J"},
    {"Squadra":"Corea del Sud","RankingFIFA":26, "Punti":1474.2, "Girone":"A"},
    {"Squadra":"Canada",       "RankingFIFA":27, "Punti":1460.7, "Girone":"B"},
    {"Squadra":"Tunisia",      "RankingFIFA":28, "Punti":1447.1, "Girone":"F"},
    {"Squadra":"Svezia",       "RankingFIFA":29, "Punti":1433.5, "Girone":"F"},
    {"Squadra":"Ghana",        "RankingFIFA":30, "Punti":1419.9, "Girone":"L"},
    {"Squadra":"Iran",         "RankingFIFA":31, "Punti":1406.4, "Girone":"G"},
    {"Squadra":"Bosnia",       "RankingFIFA":32, "Punti":1392.8, "Girone":"B"},
    {"Squadra":"Paraguay",     "RankingFIFA":33, "Punti":1379.2, "Girone":"D"},
    {"Squadra":"Costa d'Avorio","RankingFIFA":34,"Punti":1365.7, "Girone":"E"},
    {"Squadra":"Panama",       "RankingFIFA":35, "Punti":1352.1, "Girone":"L"},
    {"Squadra":"Egitto",       "RankingFIFA":36, "Punti":1338.5, "Girone":"G"},
    {"Squadra":"Scozia",       "RankingFIFA":37, "Punti":1325.0, "Girone":"C"},
    {"Squadra":"Sudafrica",    "RankingFIFA":38, "Punti":1311.4, "Girone":"A"},
    {"Squadra":"Arabia Saudita","RankingFIFA":39,"Punti":1297.9, "Girone":"H"},
    {"Squadra":"Uzbekistan",   "RankingFIFA":40, "Punti":1284.3, "Girone":"K"},
    {"Squadra":"Giordania",    "RankingFIFA":41, "Punti":1270.8, "Girone":"J"},
    {"Squadra":"Iraq",         "RankingFIFA":42, "Punti":1257.2, "Girone":"I"},
    {"Squadra":"Rep. del Congo","RankingFIFA":43,"Punti":1243.7, "Girone":"K"},
    {"Squadra":"Nuova Zelanda","RankingFIFA":44, "Punti":1230.1, "Girone":"G"},
    {"Squadra":"Qatar",        "RankingFIFA":45, "Punti":1216.6, "Girone":"B"},
    {"Squadra":"Capo Verde",   "RankingFIFA":46, "Punti":1203.0, "Girone":"H"},
    {"Squadra":"Curacao",      "RankingFIFA":47, "Punti":1189.5, "Girone":"E"},
    {"Squadra":"Haiti",        "RankingFIFA":48, "Punti":1175.9, "Girone":"C"},
]

df_fifa = pd.DataFrame(FIFA_RANKINGS).sort_values("RankingFIFA").reset_index(drop=True)
df_stats = pd.read_csv("data/team_stats.csv")
df = df_fifa.merge(df_stats[["Squadra","OverallRating","AttackRating","MidfieldRating","DefenseRating"]], on="Squadra", how="left")

st.markdown("<h1>🌍 FIFA RANKINGS</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6b7a99;margin-bottom:8px'>Ranking FIFA ufficiale delle 48 nazionali qualificate al Mondiale 2026.</p>", unsafe_allow_html=True)

st.markdown("---")

# ── FILTRI ────────────────────────────────────────────────────────────────────
col_s, col_g = st.columns([3, 2])
with col_s:
    search = st.text_input("🔍 Cerca Nazionale", placeholder="Es. Brasile...")
with col_g:
    gironi = ["Tutti"] + sorted(df["Girone"].unique().tolist())
    sel_girone = st.selectbox("Filtra per Girone", gironi)

filtered = df.copy()
if search:
    filtered = filtered[filtered["Squadra"].str.lower().str.contains(search.lower())]
if sel_girone != "Tutti":
    filtered = filtered[filtered["Girone"] == sel_girone]

st.markdown(f"<span class='wca-section-label'>{len(filtered)} nazionali</span>", unsafe_allow_html=True)

# ── PODIO ─────────────────────────────────────────────────────────────────────
if sel_girone == "Tutti" and not search:
    st.markdown("<span class='wca-section-label'>🏆 Top 3 FIFA</span>", unsafe_allow_html=True)
    medals = ["🥇","🥈","🥉"]
    cols = st.columns(3)
    for i, col in enumerate(cols):
        row = df.iloc[i]
        fp = flag_path(row["Squadra"])
        with col:
            if os.path.exists(fp): st.image(fp, width=80)
            st.markdown(
                f"<div class='wca-card' style='text-align:center'>"
                f"<div style='font-size:2rem'>{medals[i]}</div>"
                f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;letter-spacing:2px'>{row['Squadra']}</div>"
                f"<div style='font-size:1.8rem;color:#00d4ff;font-weight:700'>#{int(row['RankingFIFA'])}</div>"
                f"<div style='color:#6b7a99;font-size:12px'>{row['Punti']} punti FIFA</div>"
                f"<div style='margin-top:8px'><span class='wca-badge'>Girone {row['Girone']}</span></div>"
                f"</div>", unsafe_allow_html=True
            )
    st.markdown("---")

# ── RANKING COMPLETO ──────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📋 Ranking Completo</span>", unsafe_allow_html=True)

for _, row in filtered.iterrows():
    fp = flag_path(row["Squadra"])
    rank = int(row["RankingFIFA"])
    medal = {1:"🥇",2:"🥈",3:"🥉"}.get(rank, f"#{rank}")
    tier = "🟢" if rank <= 10 else ("🟡" if rank <= 25 else "🔴")

    has_ratings = pd.notna(row.get("OverallRating"))

    col_flag, col_name, col_stats, col_rank = st.columns([1, 3, 5, 2])

    with col_flag:
        if os.path.exists(fp): st.image(fp, width=36)

    with col_name:
        st.markdown(
            f"<div style='padding-top:6px'>"
            f"<div style='font-weight:700;font-size:14px'>{row['Squadra']}</div>"
            f"<div style='color:#6b7a99;font-size:11px'>Girone {row['Girone']} · {row['Punti']} pt</div>"
            f"</div>", unsafe_allow_html=True
        )

    with col_stats:
        if has_ratings:
            for label, val, color in [
                ("⚔️", row["AttackRating"],   "#ff3b5c"),
                ("🔄", row["MidfieldRating"], "#00d4ff"),
                ("🛡️", row["DefenseRating"],  "#00e5a0"),
            ]:
                pct = int((float(val) - 50) / (95 - 50) * 100)
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:6px;margin-bottom:2px'>"
                    f"<span style='font-size:10px;width:16px'>{label}</span>"
                    f"<div style='flex:1;background:#1f2d45;border-radius:3px;height:6px'>"
                    f"<div style='width:{pct}%;background:{color};border-radius:3px;height:6px'></div></div>"
                    f"<span style='font-size:10px;color:#6b7a99;width:28px'>{val}</span>"
                    f"</div>", unsafe_allow_html=True
                )

    with col_rank:
        overall_str = f"{row['OverallRating']}" if has_ratings else "—"
        st.markdown(
            f"<div style='text-align:center;padding-top:4px'>"
            f"<div style='font-size:1.4rem;font-weight:700;color:#00d4ff'>{medal}</div>"
            f"<div style='font-size:11px;color:#6b7a99'>{tier} · {overall_str}</div>"
            f"</div>", unsafe_allow_html=True
        )

    st.markdown("<hr style='border-color:#1f2d45;margin:4px 0'>", unsafe_allow_html=True)

st.markdown("---")

# ── CHART PER GIRONE ──────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📊 Punti FIFA per Girone</span>", unsafe_allow_html=True)
girone_sel = st.selectbox("Girone", sorted(df["Girone"].unique().tolist()), key="chart_g")
df_g = df[df["Girone"] == girone_sel].sort_values("Punti", ascending=True)
colors = ["#00d4ff" if i == len(df_g)-1 else "#1f2d45" for i in range(len(df_g))]
fig = go.Figure(go.Bar(
    x=df_g["Punti"], y=df_g["Squadra"], orientation='h',
    marker_color=colors,
    text=[f"#{int(r)} · {p} pt" for r, p in zip(df_g["RankingFIFA"], df_g["Punti"])],
    textposition="outside", textfont=dict(color="#e8edf5", size=12)
))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e8edf5"),
    xaxis=dict(gridcolor="#1f2d45", color="#6b7a99"),
    yaxis=dict(gridcolor="#1f2d45", color="#e8edf5"),
    height=240, margin=dict(t=10, b=10, l=10, r=140), showlegend=False
)
st.plotly_chart(fig, use_container_width=True)