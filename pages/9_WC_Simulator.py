import os, random
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

FLAG_MAP = {
    "Brasile":      "Girone_C/Brasile",
    "Francia":      "Girone_I/Francia",
    "Argentina":    "Girone_J/Argentina",
    "Inghilterra":  "Girone_L/Inghilterra",
    "Spagna":       "Girone_H/Spagna",
    "Portogallo":   "Girone_K/Portogallo",
    "Germania":     "Girone_E/Germania",
    "Olanda":       "Girone_F/Olanda",
    "Belgio":       "Girone_G/Belgio",
    "Croazia":      "Girone_L/Croazia",
    "Uruguay":      "Girone_H/Uruguay",
    "Colombia":     "Girone_K/Colombia",
    "Marocco":      "Girone_C/Marocco",
    "Senegal":      "Girone_I/Senegal",
    "Giappone":     "Girone_F/Giappone",
    "Messico":      "Girone_A/Messico",
    "USA":          "Girone_D/Stati_Uniti",
    "Australia":    "Girone_D/Australia",
    "Norvegia":     "Girone_I/Norvegia",
    "Svizzera":     "Girone_B/Svizzera",
}
def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"
def flag_img(s, w=28):
    p = flag_path(s)
    return p if os.path.exists(p) else None

# ── DATI ────────────────────────────────────────────────────────────────────
df = pd.read_csv("data/team_stats.csv")
ratings = {r["Squadra"]: r for _, r in df.iterrows()}

# ── FUNZIONI SIMULAZIONE ────────────────────────────────────────────────────
def win_prob(t1, t2):
    """Probabilità vittoria t1 vs t2 basata su rating."""
    r1 = ratings[t1]
    r2 = ratings[t2]
    s1 = r1["OverallRating"]*0.45 + r1["AttackRating"]*0.30 + r1["DefenseRating"]*0.25
    s2 = r2["OverallRating"]*0.45 + r2["AttackRating"]*0.30 + r2["DefenseRating"]*0.25
    p1 = s1 / (s1 + s2)
    return round(p1 * 100, 1), round((1-p1) * 100, 1)

def simulate_match(t1, t2):
    """Simula partita con rating + randomness moderata."""
    p1, p2 = win_prob(t1, t2)
    roll = random.random() * 100
    # Randomness: ±15% per sorprese
    noise = random.gauss(0, 8)
    return t1 if (p1 + noise) > 50 else t2

def predict_score(t1, t2):
    r1, r2 = ratings[t1], ratings[t2]
    g1 = round(max(0, r1["xG"] * (r1["AttackRating"]/78) * random.uniform(0.6, 1.3)), 1)
    g2 = round(max(0, r2["xG"] * (r2["AttackRating"]/78) * random.uniform(0.6, 1.3)), 1)
    return int(round(g1)), int(round(g2))

# ── UI ───────────────────────────────────────────────────────────────────────
st.markdown("<h1>🌍 WORLD CUP SIMULATOR</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#6b7a99;margin-bottom:8px'>Simula l'intero torneo basandoti sui Power Rating. "
    "Ogni run è diversa grazie alla randomness.</p>",
    unsafe_allow_html=True
)

teams_all = df["Squadra"].tolist()

# SEED per riproducibilità opzionale
col_btn, col_seed = st.columns([2, 3])
with col_btn:
    run_sim = st.button("▶️ Simula Mondiale", use_container_width=True)
with col_seed:
    use_seed = st.checkbox("Usa seed fisso (risultati riproducibili)")
    if use_seed:
        seed_val = st.number_input("Seed", value=42, step=1)

if run_sim:
    if use_seed:
        random.seed(int(seed_val))

    # ── KNOCKOUT DA 16 ───────────────────────────────────────────────────────
    # Prendi le 16 migliori squadre per OverallRating come "qualificate"
    top16 = df.sort_values("OverallRating", ascending=False)["Squadra"].tolist()[:16]

    # Bracket: seed 1 vs 16, 2 vs 15 ecc.
    bracket = [(top16[i], top16[15-i]) for i in range(8)]

    rounds = {
        "Ottavi di Finale": bracket,
    }

    results_by_round = {}
    current_round = bracket

    round_names = ["Ottavi di Finale", "Quarti di Finale", "Semifinale", "Finale"]

    all_round_results = []

    for round_name in round_names:
        st.markdown("---")
        st.markdown(f"<span class='wca-section-label'>{round_name}</span>", unsafe_allow_html=True)

        winners = []
        round_data = []

        for t1, t2 in current_round:
            p1, p2 = win_prob(t1, t2)
            winner = simulate_match(t1, t2)
            g1, g2 = predict_score(t1, t2)
            if winner == t2:
                g1, g2 = g2, g1  # assicura coerenza score
            winners.append(winner)
            round_data.append({"t1": t1, "t2": t2, "winner": winner, "g1": g1, "g2": g2, "p1": p1, "p2": p2})

        all_round_results.append((round_name, round_data))

        # Mostra match cards
        cols_per_row = min(len(round_data), 4)
        for row_start in range(0, len(round_data), cols_per_row):
            row_matches = round_data[row_start:row_start+cols_per_row]
            cols = st.columns(len(row_matches))
            for col, m in zip(cols, row_matches):
                with col:
                    w_color_1 = "#00d4ff" if m["winner"] == m["t1"] else "#6b7a99"
                    w_color_2 = "#ff3b5c" if m["winner"] == m["t2"] else "#6b7a99"
                    fp1 = flag_img(m["t1"])
                    fp2 = flag_img(m["t2"])

                    # Flag row
                    fc1, fc2, fc3 = st.columns([2,1,2])
                    with fc1:
                        if fp1: st.image(fp1, width=32)
                    with fc2:
                        st.markdown("<div style='text-align:center;padding-top:4px;color:#6b7a99;font-size:11px'>VS</div>", unsafe_allow_html=True)
                    with fc3:
                        if fp2: st.image(fp2, width=32)

                    st.markdown(
                        f"<div class='wca-card' style='padding:12px;text-align:center;margin-top:4px'>"
                        f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                        f"<span style='font-weight:700;font-size:13px;color:{w_color_1}'>{m['t1']}</span>"
                        f"<span style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;letter-spacing:3px'>{m['g1']}-{m['g2']}</span>"
                        f"<span style='font-weight:700;font-size:13px;color:{w_color_2}'>{m['t2']}</span>"
                        f"</div>"
                        f"<div style='font-size:11px;color:#6b7a99;margin-top:6px'>"
                        f"{m['p1']}% — {m['p2']}%</div>"
                        f"<div style='margin-top:8px'>"
                        f"<span class='wca-badge' style='font-size:10px'>🏆 {m['winner']}</span>"
                        f"</div></div>",
                        unsafe_allow_html=True
                    )

        # Prepara prossimo round (accoppia winners in ordine)
        next_round = []
        for i in range(0, len(winners), 2):
            if i+1 < len(winners):
                next_round.append((winners[i], winners[i+1]))
        current_round = next_round

        if round_name == "Finale":
            champion = winners[0]
            break

    # ── CAMPIONE ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("<span class='wca-section-label'>🏆 Campione del Mondo</span>", unsafe_allow_html=True)

    fp_champ = flag_img(champion)
    col_c, col_info = st.columns([1, 3])
    with col_c:
        if fp_champ: st.image(fp_champ, width=120)
    with col_info:
        champ_r = ratings[champion]
        st.markdown(
            f"<div style='padding:8px 0'>"
            f"<div style='color:#6b7a99;font-size:11px;letter-spacing:3px;text-transform:uppercase'>FIFA WORLD CUP 2026</div>"
            f"<h1 style='color:#00d4ff;font-size:3.5rem;margin:4px 0'>{champion}</h1>"
            f"<span class='wca-badge'>⭐ {champ_r['OverallRating']} Overall</span>"
            f"<span class='wca-badge' style='margin-left:8px'>⚔️ {champ_r['AttackRating']} ATT</span>"
            f"<span class='wca-badge' style='margin-left:8px'>🛡️ {champ_r['DefenseRating']} DEF</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    # ── WIN PROBABILITY TORNEO ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("<span class='wca-section-label'>📊 Win Probability — Torneo</span>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7a99;font-size:13px'>Probabilità teorica di vincere il torneo basata sul rating (500 simulazioni Monte Carlo).</p>", unsafe_allow_html=True)

    @st.cache_data
    def monte_carlo(teams, n=500):
        wins = {t: 0 for t in teams}
        for _ in range(n):
            bracket_mc = [(teams[i], teams[15-i]) for i in range(8)]
            current = bracket_mc
            for _ in range(4):
                next_r = []
                w_list = []
                for a, b in current:
                    w_list.append(simulate_match(a, b))
                for i in range(0, len(w_list), 2):
                    if i+1 < len(w_list):
                        next_r.append((w_list[i], w_list[i+1]))
                    else:
                        next_r.append((w_list[i], w_list[i]))
                current = next_r
            if current:
                winner_mc = simulate_match(current[0][0], current[0][1])
                wins[winner_mc] += 1
        return {t: round(v/n*100, 1) for t, v in wins.items()}

    probs = monte_carlo(top16)
    prob_df = pd.DataFrame(list(probs.items()), columns=["Squadra","Probabilità"]).sort_values("Probabilità", ascending=False).head(10)

    # Bar chart win probability
    colors_prob = ["#00d4ff" if i==0 else ("#f39c12" if i<3 else "#1f2d45") for i in range(len(prob_df))]
    fig = go.Figure(go.Bar(
        x=prob_df["Squadra"], y=prob_df["Probabilità"],
        marker_color=colors_prob,
        text=[f"{v}%" for v in prob_df["Probabilità"]],
        textposition="outside", textfont=dict(color="#e8edf5")
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8edf5"),
        xaxis=dict(gridcolor="#1f2d45", color="#6b7a99"),
        yaxis=dict(gridcolor="#1f2d45", color="#6b7a99", title="% vittoria torneo"),
        height=360, margin=dict(t=30, b=10), showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # Top 5 cards
    st.markdown("<span class='wca-section-label'>🎯 Top 5 Favoriti</span>", unsafe_allow_html=True)
    cols5 = st.columns(5)
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
    for i, (col, (_, row)) in enumerate(zip(cols5, prob_df.head(5).iterrows())):
        with col:
            fp = flag_img(row["Squadra"])
            if fp: st.image(fp, width=52)
            st.markdown(
                f"<div class='wca-card' style='text-align:center;padding:12px'>"
                f"<div style='font-size:1.4rem'>{medals[i]}</div>"
                f"<div style='font-weight:700;font-size:14px'>{row['Squadra']}</div>"
                f"<div style='font-size:1.8rem;color:#00d4ff;font-weight:700'>{row['Probabilità']}%</div>"
                f"</div>",
                unsafe_allow_html=True
            )

else:
    # Stato iniziale — mostra preview squadre qualificate
    st.markdown("---")
    st.markdown("<span class='wca-section-label'>🎯 16 Squadre Qualificate (per Rating)</span>", unsafe_allow_html=True)

    top16_preview = df.sort_values("OverallRating", ascending=False).head(16).reset_index(drop=True)
    top16_preview.index += 1

    cols = st.columns(4)
    for i, (_, row) in enumerate(top16_preview.iterrows()):
        with cols[i % 4]:
            fp = flag_img(row["Squadra"])
            medal = {1:"🥇",2:"🥈",3:"🥉"}.get(i+1, f"#{i+1}")
            tier = "🟢" if row["OverallRating"] >= 80 else ("🟡" if row["OverallRating"] >= 68 else "🔴")
            c_flag, c_info = st.columns([1,3])
            with c_flag:
                if fp: st.image(fp, width=32)
            with c_info:
                st.markdown(
                    f"<div class='wca-card' style='padding:8px 12px;margin-bottom:6px'>"
                    f"<span style='font-size:11px;color:#6b7a99'>{medal}</span> "
                    f"<b style='font-size:13px'>{row['Squadra']}</b><br>"
                    f"<span style='color:#00d4ff;font-size:12px'>{row['OverallRating']} {tier}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

    st.markdown(
        "<div style='text-align:center;padding:32px;color:#6b7a99'>"
        "<div style='font-size:3rem'>▶️</div>"
        "<div style='font-size:16px;margin-top:8px'>Premi il bottone per simulare il torneo</div>"
        "</div>",
        unsafe_allow_html=True
    )