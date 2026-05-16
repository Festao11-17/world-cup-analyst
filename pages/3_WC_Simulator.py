import os, random
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

def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"
def flag_img(s):
    p = flag_path(s)
    return p if os.path.exists(p) else None

df = pd.read_csv("data/team_stats.csv")
ratings = {r["Squadra"]: r for _, r in df.iterrows()}

def win_prob(t1, t2):
    r1, r2 = ratings.get(t1, {}), ratings.get(t2, {})
    s1 = float(r1.get("OverallRating",70))*0.45 + float(r1.get("AttackRating",70))*0.30 + float(r1.get("DefenseRating",70))*0.25
    s2 = float(r2.get("OverallRating",70))*0.45 + float(r2.get("AttackRating",70))*0.30 + float(r2.get("DefenseRating",70))*0.25
    p1 = s1 / (s1 + s2)
    return round(p1*100, 1), round((1-p1)*100, 1)

def simulate_match(t1, t2):
    p1, _ = win_prob(t1, t2)
    return t1 if (p1 + random.gauss(0, 8)) > 50 else t2

def predict_score(t1, t2):
    r1, r2 = ratings.get(t1, {}), ratings.get(t2, {})
    g1 = int(round(max(0, float(r1.get("xG",1.0)) * (float(r1.get("AttackRating",70))/78) * random.uniform(0.5, 1.3))))
    g2 = int(round(max(0, float(r2.get("xG",1.0)) * (float(r2.get("AttackRating",70))/78) * random.uniform(0.5, 1.3))))
    return g1, g2

def simulate_group(teams):
    pts = {t: 0 for t in teams}
    gf  = {t: 0 for t in teams}
    ga  = {t: 0 for t in teams}
    matches = []
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):
            t1, t2 = teams[i], teams[j]
            g1, g2 = predict_score(t1, t2)
            if g1 > g2:   pts[t1] += 3
            elif g2 > g1: pts[t2] += 3
            else:         pts[t1] += 1; pts[t2] += 1
            gf[t1] += g1; ga[t1] += g2
            gf[t2] += g2; ga[t2] += g1
            matches.append((t1, t2, g1, g2))
    standing = sorted(teams, key=lambda t: (pts[t], gf[t]-ga[t], gf[t]), reverse=True)
    return standing, pts, gf, ga, matches

def show_match_card(col, t1, t2, g1, g2, p1, p2, winner):
    with col:
        fp1, fp2 = flag_img(t1), flag_img(t2)
        c1, c2, c3 = st.columns([2,1,2])
        with c1:
            if fp1: st.image(fp1, width=30)
        with c2:
            st.markdown("<div style='text-align:center;color:#6b7a99;font-size:10px;padding-top:6px'>VS</div>", unsafe_allow_html=True)
        with c3:
            if fp2: st.image(fp2, width=30)
        wc1 = "#00d4ff" if winner == t1 else "#6b7a99"
        wc2 = "#ff3b5c" if winner == t2 else "#6b7a99"
        st.markdown(
            f"<div class='wca-card' style='padding:10px;text-align:center;margin-top:4px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center'>"
            f"<span style='font-weight:700;font-size:12px;color:{wc1}'>{t1}</span>"
            f"<span style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;letter-spacing:2px'>{g1}-{g2}</span>"
            f"<span style='font-weight:700;font-size:12px;color:{wc2}'>{t2}</span>"
            f"</div>"
            f"<div style='font-size:10px;color:#6b7a99;margin-top:4px'>{p1}% — {p2}%</div>"
            f"</div>",
            unsafe_allow_html=True
        )

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>🌍 WORLD CUP SIMULATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6b7a99'>Simula il Mondiale 2026 completo: fase a gironi → ottavi → quarti → semifinali → finale.</p>", unsafe_allow_html=True)

run_sim = st.button("▶️ Simula Mondiale 2026", use_container_width=True)

if run_sim:
    random.seed(2026)

    # ── FASE A GIRONI ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("<h2>📋 FASE A GIRONI</h2>", unsafe_allow_html=True)

    qualificate = []
    terze = []

    for girone_name, teams in GIRONI.items():
        st.markdown(f"<span class='wca-section-label'>Girone {girone_name}</span>", unsafe_allow_html=True)
        standing, pts, gf, ga, matches = simulate_group(teams)

        col_class, col_matches = st.columns([2, 3])

        with col_class:
            for rank, t in enumerate(standing):
                fp = flag_img(t)
                diff = gf[t] - ga[t]
                diff_str = f"+{diff}" if diff > 0 else str(diff)
                bg = "#1a2035" if rank < 2 else "#111827"
                border = "#00d4ff" if rank == 0 else ("#00e5a0" if rank == 1 else "#1f2d45")
                c_f, c_info = st.columns([1, 5])
                with c_f:
                    if fp: st.image(fp, width=28)
                with c_info:
                    st.markdown(
                        f"<div style='background:{bg};border-left:3px solid {border};"
                        f"padding:6px 12px;border-radius:6px;margin-bottom:4px;"
                        f"display:flex;justify-content:space-between;align-items:center'>"
                        f"<span style='font-weight:700;font-size:13px'>{rank+1}. {t}</span>"
                        f"<span style='color:#6b7a99;font-size:11px'>"
                        f"<b style='color:#00d4ff'>{pts[t]}pt</b> &nbsp;"
                        f"{gf[t]}:{ga[t]} &nbsp;{diff_str}"
                        f"</span></div>",
                        unsafe_allow_html=True
                    )

        with col_matches:
            match_cols = st.columns(3)
            for idx, (t1, t2, g1, g2) in enumerate(matches):
                p1, p2 = win_prob(t1, t2)
                winner = t1 if g1 > g2 else (t2 if g2 > g1 else t1)
                show_match_card(match_cols[idx % 3], t1, t2, g1, g2, p1, p2, winner)

        qualificate.append(standing[0])
        qualificate.append(standing[1])
        terze.append((standing[2], pts[standing[2]], gf[standing[2]] - ga[standing[2]]))

    terze_sorted = sorted(terze, key=lambda x: (x[1], x[2]), reverse=True)[:8]
    qualificate += [t[0] for t in terze_sorted]

    st.markdown("---")
    st.markdown(f"<span class='wca-section-label'>✅ {len(qualificate)} squadre qualificate agli ottavi</span>", unsafe_allow_html=True)
    q_cols = st.columns(8)
    for i, t in enumerate(qualificate):
        with q_cols[i % 8]:
            fp = flag_img(t)
            if fp: st.image(fp, width=36)
            st.markdown(f"<div style='font-size:10px;text-align:center;color:#e8edf5'>{t}</div>", unsafe_allow_html=True)

    # ── FASE KNOCKOUT ─────────────────────────────────────────────────────────
    random.shuffle(qualificate)
    current_round = [(qualificate[i], qualificate[i+1]) for i in range(0, len(qualificate), 2)]
    round_names = ["Ottavi di Finale", "Quarti di Finale", "Semifinale", "Finale"]
    champion = None

    for round_name in round_names:
        if not current_round: break
        st.markdown("---")
        st.markdown(f"<h2>{round_name.upper()}</h2>", unsafe_allow_html=True)

        winners = []
        round_data = []
        for t1, t2 in current_round:
            p1, p2 = win_prob(t1, t2)
            winner = simulate_match(t1, t2)
            g1, g2 = predict_score(t1, t2)
            if winner == t2: g1, g2 = g2, g1
            winners.append(winner)
            round_data.append({"t1":t1,"t2":t2,"winner":winner,"g1":g1,"g2":g2,"p1":p1,"p2":p2})

        cols_n = min(len(round_data), 4)
        for row_start in range(0, len(round_data), cols_n):
            row_m = round_data[row_start:row_start+cols_n]
            cols  = st.columns(len(row_m))
            for col, m in zip(cols, row_m):
                show_match_card(col, m["t1"], m["t2"], m["g1"], m["g2"], m["p1"], m["p2"], m["winner"])

        current_round = [(winners[i], winners[i+1]) for i in range(0, len(winners)-1, 2)]
        if round_name == "Finale":
            champion = winners[0]

    # ── CAMPIONE ──────────────────────────────────────────────────────────────
    if champion:
        st.markdown("---")
        st.markdown("<span class='wca-section-label'>🏆 Campione del Mondo</span>", unsafe_allow_html=True)
        fp_champ = flag_img(champion)
        col_c, col_info = st.columns([1, 3])
        with col_c:
            if fp_champ: st.image(fp_champ, width=130)
        with col_info:
            champ_r = ratings.get(champion, {})
            st.markdown(
                f"<div style='padding:8px 0'>"
                f"<div style='color:#6b7a99;font-size:11px;letter-spacing:3px;text-transform:uppercase'>FIFA WORLD CUP 2026</div>"
                f"<h1 style='color:#00d4ff;font-size:3.5rem;margin:4px 0'>{champion}</h1>"
                f"<span class='wca-badge'>⭐ {champ_r.get('OverallRating','—')} Overall</span>"
                f"<span class='wca-badge' style='margin-left:8px'>⚔️ {champ_r.get('AttackRating','—')} ATT</span>"
                f"<span class='wca-badge' style='margin-left:8px'>🛡️ {champ_r.get('DefenseRating','—')} DEF</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        # ── MONTE CARLO ───────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("<span class='wca-section-label'>📊 Win Probability Torneo — Monte Carlo</span>", unsafe_allow_html=True)
        st.markdown("<p style='color:#6b7a99;font-size:13px'>300 simulazioni complete del torneo.</p>", unsafe_allow_html=True)

        @st.cache_data
        def monte_carlo(n=300):
            wins = {t: 0 for t in FLAG_MAP.keys()}
            for seed_i in range(n):
                random.seed(seed_i)
                q = []
                for g_teams in GIRONI.values():
                    s, *_ = simulate_group(g_teams)
                    q.append(s[0]); q.append(s[1])
                random.shuffle(q)
                curr = [(q[i], q[i+1]) for i in range(0, len(q), 2)]
                for _ in range(4):
                    w = [simulate_match(a, b) for a, b in curr]
                    curr = [(w[i], w[i+1]) for i in range(0, len(w)-1, 2)]
                if curr:
                    wins[simulate_match(curr[0][0], curr[0][1])] += 1
            return {t: round(v/n*100, 1) for t, v in wins.items() if v > 0}

        probs = monte_carlo()
        prob_df = (pd.DataFrame(list(probs.items()), columns=["Squadra","Probabilità"])
                   .sort_values("Probabilità", ascending=False).head(12))

        colors_p = ["#00d4ff" if i==0 else ("#f39c12" if i<3 else "#1f2d45") for i in range(len(prob_df))]
        fig = go.Figure(go.Bar(
            x=prob_df["Squadra"], y=prob_df["Probabilità"],
            marker_color=colors_p,
            text=[f"{v}%" for v in prob_df["Probabilità"]],
            textposition="outside", textfont=dict(color="#e8edf5")
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e8edf5"),
            xaxis=dict(gridcolor="#1f2d45", color="#6b7a99"),
            yaxis=dict(gridcolor="#1f2d45", color="#6b7a99"),
            height=360, margin=dict(t=30, b=10), showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<span class='wca-section-label'>🎯 Top 5 Favoriti</span>", unsafe_allow_html=True)
        cols5 = st.columns(5)
        medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
        for i, (col, (_, row)) in enumerate(zip(cols5, prob_df.head(5).iterrows())):
            with col:
                fp = flag_img(row["Squadra"])
                if fp: st.image(fp, width=52)
                st.markdown(
                    f"<div class='wca-card' style='text-align:center;padding:12px'>"
                    f"<div>{medals[i]}</div>"
                    f"<div style='font-weight:700;font-size:13px'>{row['Squadra']}</div>"
                    f"<div style='font-size:1.6rem;color:#00d4ff;font-weight:700'>{row['Probabilità']}%</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

else:
    st.markdown("---")
    st.markdown("<span class='wca-section-label'>📋 Gironi Ufficiali — FIFA World Cup 2026</span>", unsafe_allow_html=True)
    girone_cols = st.columns(4)
    for idx, (name, teams) in enumerate(GIRONI.items()):
        with girone_cols[idx % 4]:
            st.markdown(
                f"<div class='wca-card' style='padding:14px;margin-bottom:12px'>"
                f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.3rem;letter-spacing:2px;margin-bottom:10px;color:#00d4ff'>GIRONE {name}</div>",
                unsafe_allow_html=True
            )
            for t in teams:
                fp = flag_img(t)
                rating = ratings.get(t, {}).get("OverallRating", "—")
                cc1, cc2 = st.columns([1, 4])
                with cc1:
                    if fp: st.image(fp, width=24)
                with cc2:
                    st.markdown(f"<div style='font-size:12px;padding:2px 0'>{t} <span style='color:#6b7a99;font-size:11px'>· {rating}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align:center;padding:32px;color:#6b7a99'>"
        "<div style='font-size:3rem'>▶️</div>"
        "<div style='font-size:16px;margin-top:8px'>Premi il bottone per simulare il Mondiale 2026</div>"
        "</div>",
        unsafe_allow_html=True
    )