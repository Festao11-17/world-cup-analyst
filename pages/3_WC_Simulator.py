import os, random
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="WC Simulator · World Cup Analyst",
    page_icon="assets/logo.png",
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  FLAG_MAP COMPLETO — 48 SQUADRE FIFA WORLD CUP 2026
# ══════════════════════════════════════════════════════════════════
FLAG_MAP = {
    "Cechia":           "Girone_A/Cechia",
    "Corea del Sud":    "Girone_A/Corea_del_Sud",
    "Messico":          "Girone_A/Messico",
    "Sudafrica":        "Girone_A/Sudafrica",
    "Bosnia":           "Girone_B/Bosnia_ed_Erzegovina",
    "Canada":           "Girone_B/Canada",
    "Qatar":            "Girone_B/Qatar",
    "Svizzera":         "Girone_B/Svizzera",
    "Brasile":          "Girone_C/Brasile",
    "Haiti":            "Girone_C/Haiti",
    "Marocco":          "Girone_C/Marocco",
    "Scozia":           "Girone_C/Scozia",
    "Australia":        "Girone_D/Australia",
    "Paraguay":         "Girone_D/Paraguay",
    "USA":              "Girone_D/Stati_Uniti",
    "Turchia":          "Girone_D/Turchia",
    "Costa d'Avorio":   "Girone_E/Costa_d'Avorio",
    "Curacao":          "Girone_E/Curacao",
    "Ecuador":          "Girone_E/Ecuador",
    "Germania":         "Girone_E/Germania",
    "Giappone":         "Girone_F/Giappone",
    "Olanda":           "Girone_F/Olanda",
    "Svezia":           "Girone_F/Svezia",
    "Tunisia":          "Girone_F/Tunisia",
    "Belgio":           "Girone_G/Belgio",
    "Egitto":           "Girone_G/Egitto",
    "Iran":             "Girone_G/Iran",
    "Nuova Zelanda":    "Girone_G/Nuova_Zelanda",
    "Arabia Saudita":   "Girone_H/Arabia_Saudita",
    "Capo Verde":       "Girone_H/Capo_Verde",
    "Spagna":           "Girone_H/Spagna",
    "Uruguay":          "Girone_H/Uruguay",
    "Francia":          "Girone_I/Francia",
    "Iraq":             "Girone_I/Iraq",
    "Norvegia":         "Girone_I/Norvegia",
    "Senegal":          "Girone_I/Senegal",
    "Algeria":          "Girone_J/Algeria",
    "Argentina":        "Girone_J/Argentina",
    "Austria":          "Girone_J/Austria",
    "Giordania":        "Girone_J/Giordania",
    "Colombia":         "Girone_K/Colombia",
    "Portogallo":       "Girone_K/Portogallo",
    "Rep. del Congo":   "Girone_K/Repubblica_del_Congo",
    "Uzbekistan":       "Girone_K/Uzbekistan",
    "Croazia":          "Girone_L/Croazia",
    "Ghana":            "Girone_L/Ghana",
    "Inghilterra":      "Girone_L/Inghilterra",
    "Panama":           "Girone_L/Panama",
}

GIRONI = {
    "A": ["Cechia",         "Corea del Sud",  "Messico",         "Sudafrica"],
    "B": ["Bosnia",         "Canada",         "Qatar",           "Svizzera"],
    "C": ["Brasile",        "Haiti",          "Marocco",         "Scozia"],
    "D": ["Australia",      "Paraguay",       "USA",             "Turchia"],
    "E": ["Costa d'Avorio", "Curacao",        "Ecuador",         "Germania"],
    "F": ["Giappone",       "Olanda",         "Svezia",          "Tunisia"],
    "G": ["Belgio",         "Egitto",         "Iran",            "Nuova Zelanda"],
    "H": ["Arabia Saudita", "Capo Verde",     "Spagna",          "Uruguay"],
    "I": ["Francia",        "Iraq",           "Norvegia",        "Senegal"],
    "J": ["Algeria",        "Argentina",      "Austria",         "Giordania"],
    "K": ["Colombia",       "Portogallo",     "Rep. del Congo",  "Uzbekistan"],
    "L": ["Croazia",        "Ghana",          "Inghilterra",     "Panama"],
}

# Rating fallback per squadre non nel CSV
FALLBACK_RATING = {
    "Cechia": 68, "Corea del Sud": 65, "Sudafrica": 58,
    "Bosnia": 62, "Canada": 63, "Qatar": 52, "Haiti": 45,
    "Scozia": 62, "Paraguay": 60, "Turchia": 67,
    "Costa d'Avorio": 64, "Curacao": 48, "Ecuador": 63,
    "Svezia": 67, "Tunisia": 60, "Egitto": 62, "Iran": 60,
    "Nuova Zelanda": 50, "Arabia Saudita": 58, "Capo Verde": 54,
    "Iraq": 50, "Algeria": 63, "Austria": 65, "Giordania": 52,
    "Rep. del Congo": 55, "Uzbekistan": 55, "Ghana": 60,
    "Panama": 55, "Norvegia": 70,
}

def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"
def flag_img(s):
    p = flag_path(s)
    return p if os.path.exists(p) else None

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=110)
    st.markdown("### WORLD CUP\nANALYST")
    st.markdown("---")
    st.markdown("<span class='wca-badge'>FIFA WORLD CUP 2026</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("Simulazione completa:\n\n**12 gironi** → fase a gironi\n\n**32 squadre** agli ottavi\n\n**Fino alla Finale** 🏆")

# ── CARICA DATI CSV ───────────────────────────────────────────────────────────
df_csv = pd.read_csv("data/team_stats.csv")

all_ratings = {}
for _, row in df_csv.iterrows():
    all_ratings[row["Squadra"]] = {
        "OverallRating":  float(row.get("OverallRating",  70)),
        "AttackRating":   float(row.get("AttackRating",   65)),
        "DefenseRating":  float(row.get("DefenseRating",  65)),
        "xG":             float(row.get("xG",             1.2)),
    }

for team, rating in FALLBACK_RATING.items():
    if team not in all_ratings:
        all_ratings[team] = {
            "OverallRating":  float(rating),
            "AttackRating":   float(int(rating * 0.95)),
            "DefenseRating":  float(int(rating * 0.95)),
            "xG":             round(rating / 70 * 1.2, 2),
        }

for teams_list in GIRONI.values():
    for team in teams_list:
        if team not in all_ratings:
            all_ratings[team] = {"OverallRating": 55.0, "AttackRating": 52.0, "DefenseRating": 52.0, "xG": 1.0}

# ── FUNZIONI SIMULAZIONE ──────────────────────────────────────────────────────
def get_score(team):
    r = all_ratings[team]
    return r["OverallRating"]*0.45 + r["AttackRating"]*0.30 + r["DefenseRating"]*0.25

def win_prob(t1, t2):
    s1, s2 = get_score(t1), get_score(t2)
    p1 = round(s1 / (s1 + s2) * 100, 1)
    return p1, round(100 - p1, 1)

def simulate_match(t1, t2):
    p1, _ = win_prob(t1, t2)
    return t1 if (p1 + random.gauss(0, 8)) > 50 else t2

def predict_score(t1, t2):
    r1, r2 = all_ratings[t1], all_ratings[t2]
    g1 = int(round(max(0, r1["xG"] * (r1["AttackRating"]/78) * random.uniform(0.5, 1.4))))
    g2 = int(round(max(0, r2["xG"] * (r2["AttackRating"]/78) * random.uniform(0.5, 1.4))))
    return g1, g2

def simulate_match_ko(t1, t2):
    winner = simulate_match(t1, t2)
    g1, g2 = predict_score(t1, t2)
    if winner == t1 and g1 <= g2:   g1 = g2 + 1
    elif winner == t2 and g2 <= g1: g2 = g1 + 1
    pen = False
    if g1 == g2:
        s1, s2 = get_score(t1), get_score(t2)
        winner = t1 if random.random() < s1/(s1+s2) else t2
        pen = True
    return winner, g1, g2, pen

def simulate_group(teams):
    pts = {t: 0 for t in teams}
    gf  = {t: 0 for t in teams}
    ga  = {t: 0 for t in teams}
    results = []
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):
            t1, t2 = teams[i], teams[j]
            winner = simulate_match(t1, t2)
            s1, s2 = predict_score(t1, t2)
            if winner == t1 and s1 <= s2: s1 = s2 + 1
            elif winner == t2 and s2 <= s1: s2 = s1 + 1
            p1, p2 = win_prob(t1, t2)
            if abs(p1-p2) < 12 and random.random() < 0.28:
                eq = min(s1, s2); s1 = s2 = eq
                pts[t1] += 1; pts[t2] += 1
            elif winner == t1: pts[t1] += 3
            else:              pts[t2] += 3
            gf[t1] += s1; ga[t1] += s2
            gf[t2] += s2; ga[t2] += s1
            results.append((t1, t2, s1, s2))
    ranking = sorted(teams, key=lambda t: (pts[t], gf[t]-ga[t], gf[t]), reverse=True)
    return ranking, pts, gf, ga, results

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:30px 0 10px">
  <div style="color:#6b7a99;font-size:11px;letter-spacing:3px;text-transform:uppercase;font-weight:600;margin-bottom:6px">
    FIFA WORLD CUP 2026 · SIMULATORE
  </div>
  <h1 style="font-size:3.5rem;margin:0;line-height:1">WC SIMULATOR</h1>
  <p style="color:#6b7a99;margin-top:10px;font-size:14px">
    48 squadre · 12 gironi · Fase a eliminazione diretta · Basato sui Power Rating reali
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col_btn, col_seed = st.columns([2, 3])
with col_btn:
    run_sim = st.button("▶️ Simula Mondiale", use_container_width=True, type="primary")
with col_seed:
    use_seed = st.checkbox("Usa seed fisso (risultati riproducibili)")
    seed_val = None
    if use_seed:
        seed_val = st.number_input("Seed", value=42, step=1, label_visibility="collapsed")

# ════════════════════════════════════════════════════════════════════════════
if run_sim:
    if seed_val is not None:
        random.seed(int(seed_val))

    # ── FASE A GIRONI ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<h2 style='font-family:Bebas Neue,sans-serif;font-size:2rem;letter-spacing:3px'>⚽ FASE A GIRONI</h2>",
        unsafe_allow_html=True
    )

    qualificate_1a = []
    qualificate_2a = []
    all_terze      = []

    girone_cols = st.columns(3)
    medals_g    = ["🥇","🥈","🥉","❌"]
    badge_styles = [
        "background:rgba(0,212,255,0.1);color:#00d4ff;border-color:#00d4ff",
        "background:rgba(0,212,255,0.06);color:#6b9eff;border-color:#6b9eff",
        "background:rgba(255,200,0,0.08);color:#ffc800;border-color:#ffc800",
        "background:rgba(255,59,92,0.08);color:#ff3b5c;border-color:#ff3b5c",
    ]
    qual_labels = ["✓ 1ª","✓ 2ª","3ª","OUT"]

    for idx, (gid, teams) in enumerate(GIRONI.items()):
        ranking, pts, gf, ga, results = simulate_group(teams)
        qualificate_1a.append(ranking[0])
        qualificate_2a.append(ranking[1])
        all_terze.append({
            "team": ranking[2],
            "pts":  pts[ranking[2]],
            "diff": gf[ranking[2]] - ga[ranking[2]],
            "gf":   gf[ranking[2]],
        })

        with girone_cols[idx % 3]:
            st.markdown(
                f"<div class='wca-card' style='padding:16px 18px;margin-bottom:16px'>"
                f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;"
                f"letter-spacing:2px;color:#00d4ff;margin-bottom:12px'>GIRONE {gid}</div>",
                unsafe_allow_html=True
            )
            for rank_i, team in enumerate(ranking):
                diff = gf[team] - ga[team]
                opacity = "opacity:0.38;" if rank_i == 3 else ""
                badge = (
                    f"<span class='wca-badge' style='{badge_styles[rank_i]};"
                    f"font-size:9px;padding:1px 5px;margin-left:5px'>{qual_labels[rank_i]}</span>"
                )
                fp = flag_path(team)
                c_flag, c_data = st.columns([1, 5])
                with c_flag:
                    if os.path.exists(fp): st.image(fp, width=24)
                with c_data:
                    st.markdown(
                        f"<div style='display:flex;align-items:center;gap:6px;"
                        f"padding:4px 0;border-bottom:1px solid #1f2d45;{opacity}'>"
                        f"<span style='font-size:11px'>{medals_g[rank_i]}</span>"
                        f"<span style='font-weight:600;font-size:12px;flex:1'>{team}</span>"
                        f"<span style='color:#00d4ff;font-weight:700;font-size:12px;"
                        f"min-width:18px;text-align:center'>{pts[team]}</span>"
                        f"<span style='color:#6b7a99;font-size:10px;min-width:36px;"
                        f"text-align:right'>{gf[team]}:{ga[team]}</span>"
                        f"{badge}</div>",
                        unsafe_allow_html=True
                    )
            st.markdown("</div>", unsafe_allow_html=True)

    # Migliori 8 terze
    terze_sorted = sorted(all_terze, key=lambda x: (x["pts"],x["diff"],x["gf"]), reverse=True)
    best8 = [t["team"] for t in terze_sorted[:8]]

    st.markdown(
        f"<div class='wca-card' style='padding:16px 20px;margin-bottom:8px'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.1rem;letter-spacing:2px;"
        f"color:#ffc800;margin-bottom:10px'>🥉 MIGLIORI 8 TERZE — passano agli Ottavi</div>"
        f"<div style='display:flex;flex-wrap:wrap;gap:8px'>",
        unsafe_allow_html=True
    )
    for t in best8:
        st.markdown(
            f"<span class='wca-badge' style='background:rgba(255,200,0,0.08);"
            f"color:#ffc800;border-color:#ffc800'>{t}</span>",
            unsafe_allow_html=True
        )
    st.markdown("</div></div>", unsafe_allow_html=True)

    bracket_32 = qualificate_1a + qualificate_2a + best8
    random.shuffle(bracket_32)

    # ── FUNZIONE RENDER TURNO KO ─────────────────────────────────────────────
    def render_ko_round(round_name, matches_list, cols_n=4):
        st.markdown("---")
        st.markdown(
            f"<h2 style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;"
            f"letter-spacing:3px'>{round_name}</h2>",
            unsafe_allow_html=True
        )
        winners, losers = [], []
        cols_n = min(cols_n, len(matches_list))
        for row_start in range(0, len(matches_list), cols_n):
            row_m = matches_list[row_start:row_start+cols_n]
            cols  = st.columns(len(row_m))
            for col, (t1, t2) in zip(cols, row_m):
                winner, g1, g2, pen = simulate_match_ko(t1, t2)
                loser = t2 if winner == t1 else t1
                winners.append(winner); losers.append(loser)
                pen_str = " r." if pen else ""
                p1, p2  = win_prob(t1, t2)
                c1 = "#00d4ff" if winner == t1 else "#6b7a99"
                c2 = "#00d4ff" if winner == t2 else "#6b7a99"
                w1 = "700" if winner == t1 else "400"
                w2 = "700" if winner == t2 else "400"
                with col:
                    fp1 = flag_img(t1); fp2 = flag_img(t2)
                    fc1, fvs, fc2 = st.columns([2,1,2])
                    with fc1:
                        if fp1: st.image(fp1, width=30)
                    with fvs:
                        st.markdown("<div style='text-align:center;padding-top:6px;color:#6b7a99;font-size:10px'>VS</div>", unsafe_allow_html=True)
                    with fc2:
                        if fp2: st.image(fp2, width=30)
                    st.markdown(
                        f"<div class='wca-card' style='padding:12px;text-align:center;margin-top:4px'>"
                        f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                        f"<span style='font-weight:{w1};font-size:12px;color:{c1}'>{t1}</span>"
                        f"<span style='font-family:Bebas Neue,sans-serif;font-size:1.4rem;"
                        f"letter-spacing:2px'>{g1}–{g2}{pen_str}</span>"
                        f"<span style='font-weight:{w2};font-size:12px;color:{c2}'>{t2}</span>"
                        f"</div>"
                        f"<div style='font-size:10px;color:#6b7a99;margin-top:4px'>{p1}% — {p2}%</div>"
                        f"<div style='margin-top:6px'>"
                        f"<span class='wca-badge' style='font-size:10px'>🏆 {winner}</span>"
                        f"</div></div>",
                        unsafe_allow_html=True
                    )
        return winners, losers

    # Ottavi (16 partite)
    m_ottavi = [(bracket_32[i*2], bracket_32[i*2+1]) for i in range(16)]
    ottavi_w, _ = render_ko_round("⚔️ OTTAVI DI FINALE", m_ottavi, 4)

    # Quarti (8 partite)
    m_qf = [(ottavi_w[i*2], ottavi_w[i*2+1]) for i in range(8)]
    qf_w, _ = render_ko_round("⚡ QUARTI DI FINALE", m_qf, 4)

    # Semifinali (4 partite)
    m_sf = [(qf_w[i*2], qf_w[i*2+1]) for i in range(4)]
    sf_w, sf_l = render_ko_round("🔥 SEMIFINALI", m_sf, 2)

    # 3° posto
    st.markdown("---")
    st.markdown(
        "<h2 style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;"
        "letter-spacing:3px'>🥉 FINALE 3° POSTO</h2>",
        unsafe_allow_html=True
    )
    b1, b2 = sf_l[0], sf_l[1]
    bw, bg1, bg2, bpen = simulate_match_ko(b1, b2)
    bl = b2 if bw == b1 else b1
    bpen_str = " r." if bpen else ""
    bc = st.columns(3)
    with bc[0]:
        fp = flag_img(b1)
        if fp: st.image(fp, width=40)
        st.markdown(f"<span style='color:{'#00d4ff' if bw==b1 else '#6b7a99'};font-weight:700'>{b1}</span>", unsafe_allow_html=True)
    with bc[1]:
        st.markdown(
            f"<div style='text-align:center;padding-top:8px;font-family:Bebas Neue,sans-serif;"
            f"font-size:2rem;letter-spacing:3px'>{bg1}–{bg2}{bpen_str}</div>",
            unsafe_allow_html=True
        )
    with bc[2]:
        fp2 = flag_img(b2)
        if fp2: st.image(fp2, width=40)
        st.markdown(f"<span style='color:{'#00d4ff' if bw==b2 else '#6b7a99'};font-weight:700'>{b2}</span>", unsafe_allow_html=True)

    # ── FINALE ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<h2 style='font-family:Bebas Neue,sans-serif;font-size:2.5rem;"
        "letter-spacing:4px;text-align:center'>🏆 FINALE</h2>",
        unsafe_allow_html=True
    )
    f1, f2 = sf_w[0], sf_w[1]
    champion, fg1, fg2, fpen = simulate_match_ko(f1, f2)
    runner_up = f2 if champion == f1 else f1
    fpen_str = " rig." if fpen else ""

    col_f1, col_vs, col_f2 = st.columns([3, 1, 3])
    with col_f1:
        fp1 = flag_img(f1)
        if fp1: st.image(fp1, width=72)
        gc = "#ffd700" if champion == f1 else "#6b7a99"
        st.markdown(f"<h3 style='color:{gc}'>{f1}</h3>", unsafe_allow_html=True)
        if champion == f1:
            st.markdown("<span class='wca-badge' style='background:rgba(255,215,0,0.12);color:#ffd700;border-color:#ffd700'>🏆 CAMPIONE DEL MONDO</span>", unsafe_allow_html=True)
    with col_vs:
        st.markdown(
            f"<div style='text-align:center;padding-top:28px'>"
            f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.5rem;"
            f"color:#e8edf5;letter-spacing:4px'>{fg1}–{fg2}</div>"
            f"<div style='color:#6b7a99;font-size:11px;margin-top:4px'>FINALE{fpen_str}</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_f2:
        fp2 = flag_img(f2)
        if fp2: st.image(fp2, width=72)
        gc2 = "#ffd700" if champion == f2 else "#6b7a99"
        st.markdown(f"<h3 style='color:{gc2}'>{f2}</h3>", unsafe_allow_html=True)
        if champion == f2:
            st.markdown("<span class='wca-badge' style='background:rgba(255,215,0,0.12);color:#ffd700;border-color:#ffd700'>🏆 CAMPIONE DEL MONDO</span>", unsafe_allow_html=True)

    # ── PODIO ─────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<h2 style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;"
        "letter-spacing:3px;text-align:center'>PODIO FINALE</h2>",
        unsafe_allow_html=True
    )
    podio = [
        ("🥇 CAMPIONE",  champion,  "#ffd700"),
        ("🥈 FINALISTA", runner_up, "#c0c0c0"),
        ("🥉 3° POSTO",  bw,        "#cd7f32"),
        ("4° POSTO",     bl,        "#6b7a99"),
    ]
    for col, (label, team, color) in zip(st.columns(4), podio):
        with col:
            fp = flag_img(team)
            if fp: st.image(fp, width=52)
            r = all_ratings.get(team, {})
            st.markdown(
                f"<div class='wca-card' style='text-align:center;padding:16px;border-color:{color}'>"
                f"<div style='color:{color};font-size:11px;font-weight:700;"
                f"text-transform:uppercase;letter-spacing:1px;margin-bottom:8px'>{label}</div>"
                f"<div style='font-weight:700;font-size:15px;margin-bottom:8px'>{team}</div>"
                f"<span class='wca-badge' style='border-color:{color};color:{color};"
                f"background:transparent'>⭐ {int(r.get('OverallRating',0))}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

    # ── MONTE CARLO ───────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<span class='wca-section-label'>📊 Win Probability — Monte Carlo (500 simulazioni)</span>",
        unsafe_allow_html=True
    )

    all_48_teams = [t for g in GIRONI.values() for t in g]

    @st.cache_data
    def monte_carlo_48(teams_tuple, n=500):
        wins = {t: 0 for t in teams_tuple}
        for _ in range(n):
            q1_mc, q2_mc, t3_mc = [], [], []
            for gid, gteams in GIRONI.items():
                rk, pts_mc, gf_mc, ga_mc, _ = simulate_group(gteams)
                q1_mc.append(rk[0]); q2_mc.append(rk[1])
                t3_mc.append({"team": rk[2], "pts": pts_mc[rk[2]],
                               "diff": gf_mc[rk[2]]-ga_mc[rk[2]], "gf": gf_mc[rk[2]]})
            b8_mc = [x["team"] for x in sorted(t3_mc, key=lambda x:(x["pts"],x["diff"],x["gf"]), reverse=True)[:8]]
            b32_mc = q1_mc + q2_mc + b8_mc
            random.shuffle(b32_mc)
            current = [(b32_mc[i*2], b32_mc[i*2+1]) for i in range(16)]
            for _ in range(4):
                nxt = [simulate_match(a, b) for a, b in current]
                current = [(nxt[i*2], nxt[i*2+1]) for i in range(len(nxt)//2)]
            if current:
                ch = simulate_match(current[0][0], current[0][1])
                if ch in wins: wins[ch] += 1
        return {t: round(v/n*100, 1) for t, v in wins.items()}

    probs   = monte_carlo_48(tuple(all_48_teams))
    prob_df = (pd.DataFrame(list(probs.items()), columns=["Squadra","Prob"])
               .sort_values("Prob", ascending=False).head(12))

    bar_colors = ["#ffd700" if i==0 else ("#c0c0c0" if i==1 else ("#cd7f32" if i==2 else "#1f2d45"))
                  for i in range(len(prob_df))]
    fig = go.Figure(go.Bar(
        x=prob_df["Squadra"], y=prob_df["Prob"],
        marker_color=bar_colors,
        text=[f"{v}%" for v in prob_df["Prob"]],
        textposition="outside", textfont=dict(color="#e8edf5", size=11)
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8edf5"),
        xaxis=dict(gridcolor="#1f2d45", color="#6b7a99", tickfont=dict(size=11)),
        yaxis=dict(gridcolor="#1f2d45", color="#6b7a99", title="% vittoria torneo"),
        height=380, margin=dict(t=40, b=20), showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<span class='wca-section-label'>🎯 Top 5 Favoriti al Titolo</span>", unsafe_allow_html=True)
    gold_c = ["#ffd700","#c0c0c0","#cd7f32","#6b7a99","#6b7a99"]
    medal5 = ["🥇","🥈","🥉","4️⃣","5️⃣"]
    for col, (medal, (_, row), color) in zip(st.columns(5), zip(medal5, prob_df.head(5).iterrows(), gold_c)):
        with col:
            fp = flag_img(row["Squadra"])
            if fp: st.image(fp, width=52)
            r = all_ratings.get(row["Squadra"], {})
            st.markdown(
                f"<div class='wca-card' style='text-align:center;padding:14px;border-color:{color}'>"
                f"<div style='font-size:1.5rem'>{medal}</div>"
                f"<div style='font-weight:700;font-size:14px;margin:6px 0'>{row['Squadra']}</div>"
                f"<div style='font-size:1.8rem;color:{color};font-weight:700'>{row['Prob']}%</div>"
                f"<div style='color:#6b7a99;font-size:11px;margin-top:4px'>"
                f"Rating {int(r.get('OverallRating',0))}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;color:#6b7a99;font-size:12px;padding-bottom:20px'>"
        "🔄 Premi di nuovo <b>▶️ Simula Mondiale</b> per una simulazione diversa.</div>",
        unsafe_allow_html=True
    )

# ════════════════════════════════════════════════════════════════════════════
else:
    # Stato iniziale — mostra i 12 gironi con barre di forza
    st.markdown(
        "<span class='wca-section-label'>🌍 I 12 Gironi — FIFA World Cup 2026</span>",
        unsafe_allow_html=True
    )
    g_cols = st.columns(3)
    for idx, (gid, teams) in enumerate(GIRONI.items()):
        with g_cols[idx % 3]:
            st.markdown(
                f"<div class='wca-card' style='padding:16px 18px;margin-bottom:16px'>"
                f"<div style='font-family:Bebas Neue,sans-serif;font-size:1.3rem;"
                f"letter-spacing:2px;color:#00d4ff;margin-bottom:12px'>GIRONE {gid}</div>",
                unsafe_allow_html=True
            )
            teams_sorted = sorted(teams, key=lambda t: all_ratings.get(t, {}).get("OverallRating", 50), reverse=True)
            for team in teams_sorted:
                fp = flag_path(team)
                ov = int(all_ratings.get(team, {}).get("OverallRating", 50))
                bar_w = int(ov * 0.78)
                c_flag, c_info = st.columns([1, 5])
                with c_flag:
                    if os.path.exists(fp): st.image(fp, width=24)
                with c_info:
                    st.markdown(
                        f"<div style='padding:3px 0'>"
                        f"<div style='display:flex;justify-content:space-between'>"
                        f"<span style='font-size:12px;font-weight:500'>{team}</span>"
                        f"<span style='color:#00d4ff;font-size:11px;font-weight:700'>{ov}</span>"
                        f"</div>"
                        f"<div class='wca-bar-wrap' style='margin:3px 0 5px'>"
                        f"<div class='wca-bar' style='width:{bar_w}%;"
                        f"background:linear-gradient(90deg,#00d4ff,#0055aa)'></div>"
                        f"</div></div>",
                        unsafe_allow_html=True
                    )
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;padding:24px;color:#6b7a99'>"
        "<div style='font-size:2.5rem'>▶️</div>"
        "<div style='font-size:15px;margin-top:8px'>Premi il bottone per simulare il Mondiale completo</div>"
        "<div style='font-size:12px;margin-top:4px'>48 squadre · fase a gironi · ottavi · quarti · semifinali · finale</div>"
        "</div>",
        unsafe_allow_html=True
    )