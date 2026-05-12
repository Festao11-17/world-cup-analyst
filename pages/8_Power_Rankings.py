import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

FLAG_MAP = {
    "Brasile":"Girone_C/brasile","Francia":"Girone_I/francia","Argentina":"Girone_J/argentina",
    "Inghilterra":"Girone_L/inghilterra","Spagna":"Girone_H/spagna","Portogallo":"Girone_K/portogallo",
    "Germania":"Girone_E/germania","Olanda":"Girone_F/olanda","Belgio":"Girone_G/belgio",
    "Croazia":"Girone_L/croazia","Uruguay":"Girone_H/uruguay","Colombia":"Girone_K/colombia",
    "Marocco":"Girone_C/marocco","Senegal":"Girone_I/senegal","Giappone":"Girone_F/giappone",
    "Messico":"Girone_A/messico","USA":"Girone_D/stati_uniti","Australia":"Girone_D/australia",
    "Norvegia":"Girone_I/norvegia","Svizzera":"Girone_B/svizzera",
}
def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s.lower())}.png"

st.markdown("<h1>⚡ POWER RANKINGS</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#6b7a99;margin-bottom:24px'>Rating calcolato su attacco, centrocampo e difesa per ogni nazionale.</p>",
    unsafe_allow_html=True
)

df = pd.read_csv("data/team_stats.csv").sort_values("OverallRating", ascending=False).reset_index(drop=True)
df.index += 1

st.markdown("---")

# ── TOP 3 PODIO ───────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>🏆 Podio</span>", unsafe_allow_html=True)
medals = ["🥇","🥈","🥉"]
cols = st.columns(3)
for i, col in enumerate(cols):
    row = df.iloc[i]
    fp = flag_path(row["Squadra"])
    with col:
        if os.path.exists(fp):
            st.image(fp, width=80)
        st.markdown(
            f"<div class='wca-card' style='text-align:center'>"
            f"<div style='font-size:2rem'>{medals[i]}</div>"
            f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;letter-spacing:2px'>{row['Squadra']}</div>"
            f"<div style='font-size:2rem;color:#00d4ff;font-weight:700'>{row['OverallRating']}</div>"
            f"<div style='color:#6b7a99;font-size:11px;text-transform:uppercase;letter-spacing:1px'>Overall Rating</div>"
            f"<div class='wca-stat-row' style='justify-content:center;margin-top:10px'>"
            f"<div class='wca-stat'>⚔️ <span>{row['AttackRating']}</span></div>"
            f"<div class='wca-stat'>🔄 <span>{row['MidfieldRating']}</span></div>"
            f"<div class='wca-stat'>🛡️ <span>{row['DefenseRating']}</span></div>"
            f"</div></div>",
            unsafe_allow_html=True
        )

st.markdown("---")

# ── RANKING COMPLETO ──────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📋 Ranking Completo</span>", unsafe_allow_html=True)

for i, row in df.iterrows():
    fp = flag_path(row["Squadra"])
    medal = {1:"🥇",2:"🥈",3:"🥉"}.get(i, f"#{i}")

    col_flag, col_name, col_bars, col_overall = st.columns([1, 3, 6, 2])

    with col_flag:
        if os.path.exists(fp):
            st.image(fp, width=36)

    with col_name:
        st.markdown(
            f"<div style='padding-top:8px'>"
            f"<span style='color:#6b7a99;font-size:12px'>{medal}</span> "
            f"<span style='font-weight:700'>{row['Squadra']}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    with col_bars:
        for label, val, color in [
            ("⚔️ ATT", row["AttackRating"],   "#ff3b5c"),
            ("🔄 MID", row["MidfieldRating"], "#00d4ff"),
            ("🛡️ DEF", row["DefenseRating"],  "#00e5a0"),
        ]:
            pct = int((val - 50) / (95 - 50) * 100)
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:3px'>"
                f"<span style='font-size:11px;color:#6b7a99;width:52px'>{label}</span>"
                f"<div class='wca-bar-wrap' style='flex:1;margin:0'>"
                f"<div class='wca-bar' style='width:{pct}%;background:{color}'></div></div>"
                f"<span style='font-size:12px;color:#e8edf5;width:32px;text-align:right'>{val}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

    with col_overall:
        tier = "🟢" if row["OverallRating"] >= 80 else ("🟡" if row["OverallRating"] >= 68 else "🔴")
        st.markdown(
            f"<div style='text-align:center;padding-top:4px'>"
            f"<div style='font-size:1.6rem;font-weight:700;color:#00d4ff'>{row['OverallRating']}</div>"
            f"<div style='font-size:11px;color:#6b7a99'>{tier} Overall</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<hr style='border-color:#1f2d45;margin:6px 0'>", unsafe_allow_html=True)

st.markdown("---")

# ── BAR CHART COMPARATIVO ─────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📊 Confronto Visivo</span>", unsafe_allow_html=True)

rating_type = st.selectbox("Visualizza", ["OverallRating","AttackRating","MidfieldRating","DefenseRating"],
    format_func=lambda x: {"OverallRating":"Overall","AttackRating":"Attacco",
                            "MidfieldRating":"Centrocampo","DefenseRating":"Difesa"}[x])

df_plot = df.sort_values(rating_type, ascending=True)
colors  = ["#00d4ff" if v >= df[rating_type].quantile(0.75) else
           ("#f39c12" if v >= df[rating_type].median() else "#ff3b5c")
           for v in df_plot[rating_type]]

fig = go.Figure(go.Bar(
    x=df_plot[rating_type],
    y=df_plot["Squadra"],
    orientation='h',
    marker_color=colors,
    text=df_plot[rating_type],
    textposition="outside",
    textfont=dict(color="#e8edf5", size=12)
))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e8edf5"),
    xaxis=dict(gridcolor="#1f2d45", color="#6b7a99", range=[45, 100]),
    yaxis=dict(gridcolor="#1f2d45", color="#e8edf5"),
    height=560,
    margin=dict(t=20, b=20, l=10, r=60)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── RADAR MULTI-TEAM ──────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📈 Radar Comparativo</span>", unsafe_allow_html=True)
selected = st.multiselect("Seleziona squadre da confrontare", df["Squadra"].tolist(),
                          default=df["Squadra"].tolist()[:4])

if selected:
    stats = ["AttackRating","MidfieldRating","DefenseRating","OverallRating"]
    labels = ["Attacco","Centrocampo","Difesa","Overall"]
    colors_list = ["#00d4ff","#ff3b5c","#00e5a0","#f39c12","#a78bfa","#fb923c"]

    fig2 = go.Figure()
    for idx, team in enumerate(selected):
        row = df[df["Squadra"]==team].iloc[0]
        fig2.add_trace(go.Scatterpolar(
            r=[row[s] for s in stats],
            theta=labels,
            fill='toself',
            name=team,
            line=dict(color=colors_list[idx % len(colors_list)], width=2)
        ))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        polar=dict(bgcolor="rgba(26,32,53,0.6)",
                   radialaxis=dict(visible=True, range=[50,96], gridcolor="#1f2d45", color="#6b7a99"),
                   angularaxis=dict(gridcolor="#1f2d45", color="#6b7a99")),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8edf5")),
        height=460, showlegend=True
    )
    st.plotly_chart(fig2, use_container_width=True)