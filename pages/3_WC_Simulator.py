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

# ── DATI ─────────────────────────────────────────────────────────────────────
df = pd.read_csv("data/team_stats.csv")
ratings = {r["Squadra"]: r for _, r in df.iterrows()}

# ── FUNZIONI ─────────────────────────────────────────────────────────────────
def get_score(t, col, default=70):
    r = ratings.get(t, {})
    try: return float(r[col])
    except: return default

def win_prob(t1, t2):
    s1 = get_score(t1,"OverallRating")*0.45 + get_score(t1,"AttackRating")*0.30 + get_score(t1,"DefenseRating")*0.25
    s2 = get_score(t2,"OverallRating")*0.45 + get_score(t2,"AttackRating")*0.30 + get_score(t2,"DefenseRating")*0.25
    p1 = s1 / (s1 + s2)
    return round(p1*100, 1), round((1-p1)*100, 1)

def decide_winner(t1, t2):
    p1, _ = win_prob(t1, t2)
    result = p1 + random.gauss(0, 8)
    return t1 if result > 50 else t2

def predict_score(t1, t2, winner, draw=False):
    g1 = int(round(max(0, get_score(t1,"xG",1.0) * (get_score(t1,"AttackRating",70)/78) * random.uniform(0.5, 1.3))))
    g2 = int(round(max(0, get_score(t2,"xG",1.0) * (get_score(t2,"AttackRating",70)/78) * random.uniform(0.5, 1.3))))
    if draw:
        eq = min(g1, g2)
        return eq, eq
    # Forza coerenza: il vincitore deve avere più gol
    if winner == t1 and g1 <= g2:
        g1 = g2 + 1
    elif winner == t2 and g2 <= g1:
        g2 = g1 + 1
    return g1, g2

def simulate_match_ko(t1, t2):
    p1, _ = win_prob(t1, t2)
    result = p1 + random.gauss(0, 8)
    if 47 < result < 53:
        winner = t1 if random.random() > 0.5 else t2
        g1, g2 = predict_score(t1, t2, winner=None, draw=True)
        return winner, g1, g2, True
    winner = t1 if result > 50 else t2
    g1, g2 = predict_score(t1, t2, winner=winner, draw=False)
    return winner, g1, g2, False

def simulate_group(teams):
    pts = {t: 0 for t in teams}
    gf  = {t: 0 for t in teams}
    ga  = {t: 0 for t in teams}
    matches = []
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):
            t1, t2 = teams[i], teams[j]
            p1, p2 = win_prob(t1, t2)
            draw_chance = max(0, 0.28 - abs(p1 - p2) * 0.004)
            is_draw = random.random() < draw_chance
            if is_draw:
                g1, g2 = predict_score(t1, t2, winner=None, draw=True)
                pts[t1] += 1
                pts[t2] += 1
            else:
                winner = decide_winner(t1, t2)
                g1, g2 = predict_score(t1, t2, winner=winner, draw=False)
                if winner == t1: pts[t1] += 3
                else:            pts[t2] += 3
            gf[t1]+=g1; ga[t1]+=g2; gf[t2]+=g2; ga[t2]+=g1
            matches.append((t1, t2, g1, g2))
    standing = sorted(teams, key=lambda t: (pts[t], gf[t]-ga[t], gf[t]), reverse=True)
    return standing, pts, gf, ga, matches

def monte_carlo_sim(n, base_seed):
    """Simulazione Monte Carlo completamente autonoma, nessuna dipendenza esterna."""
    wins = {t: 0 for t in sum(GIRONI.values(), [])}
    rat = {r["Squadra"]: r for _, r in pd.read_csv("data/team_stats.csv").iterrows()}

    def gs(t, col, d=70):
        try: return float(rat.get(t,{}).get(col, d))
        except: return d

    def wp(t1, t2):
        s1 = gs(t1,"OverallRating")*0.45+gs(t1,"AttackRating")*0.30+gs(t1,"DefenseRating")*0.25
        s2 = gs(t2,"OverallRating")*0.45+gs(t2,"AttackRating")*0.30+gs(t2,"DefenseRating")*0.25
        return s1/(s1+s2)

    def sm(t1, t2):
        p = wp(t1, t2)*100 + random.gauss(0, 8)
        if 47 < p < 53: return t1 if random.random()>0.5 else t2
        return t1 if p > 50 else t2

    def ps(t1, t2):
        g1 = int(round(max(0, gs(t1,"xG",1.0)*(gs(t1,"AttackRating")/78)*random.uniform(0.5,1.3))))
        g2 = int(round(max(0, gs(t2,"xG",1.0)*(gs(t2,"AttackRating")/78)*random.uniform(0.5,1.3))))
        return g1, g2

    def sg(teams):
        pts={t:0 for t in teams}; gf={t:0 for t in teams}; ga={t:0 for t in teams}
        for i in range(len(teams)):
            for j in range(i+1,len(teams)):
                t1,t2=teams[i],teams[j]; g1,g2=ps(t1,t2)
                if g1>g2: pts[t1]+=3
                elif g2>g1: pts[t2]+=3
                else: pts[t1]+=1;pts[t2]+=1
                gf[t1]+=g1;ga[t1]+=g2;gf[t2]+=g2;ga[t2]+=g1
        return sorted(teams,key=lambda t:(pts[t],gf[t]-ga[t],gf[t]),reverse=True)

    for i in range(n):
        random.seed(base_seed + i * 31 + 7)
        q = []
        terze_mc = []
        for g_teams in GIRONI.values():
            s = sg(g_teams)
            q.append(s[0]); q.append(s[1])
            # Raccogli terze con punti simulati (stima semplice)
            terze_mc.append(s[2])
        # Aggiungi 8 terze casuali per arrivare a 32
        random.shuffle(terze_mc)
        q += terze_mc[:8]
        random.shuffle(q)
        # Assicura 32 squadre (potatura o padding)
        q = q[:32]
        curr = [(q[k], q[k+1]) for k in range(0, len(q), 2)]
        for _ in range(4):
            w = [sm(a,b) for a,b in curr]
            curr = [(w[k],w[k+1]) for k in range(0,len(w)-1,2)]
        if curr:
            wins[sm(curr[0][0],curr[0][1])] += 1

    total = max(sum(wins.values()), 1)
    return {t: round(v/total*100,1) for t,v in wins.items() if v>0}

def show_match_card(col, t1, t2, g1, g2, winner, penalties=False, draw=False):
    with col:
        fp1, fp2 = flag_img(t1), flag_img(t2)
        c1,c2,c3 = st.columns([2,1,2])
        with c1:
            if fp1: st.image(fp1, width=30)
        with c2:
            st.markdown("<div style='text-align:center;color:#6b7a99;font-size:10px;padding-top:6px'>VS</div>", unsafe_allow_html=True)
        with c3:
            if fp2: st.image(fp2, width=30)
        # Colori: grigio per entrambi se pareggio
        wc1 = "#6b7a99" if draw else ("#00d4ff" if winner==t1 else "#6b7a99")
        wc2 = "#6b7a99" if draw else ("#ff3b5c" if winner==t2 else "#6b7a99")
        pen = "<div style='font-size:10px;color:#f39c12;margin-top:2px'>🟡 Rigori</div>" if penalties else ""
        # Footer: pareggio o vincitore
        if draw:
            footer = "<div style='margin-top:6px;font-size:10px;color:#6b7a99'>🤝 Pareggio</div>"
        else:
            footer = f"<div style='margin-top:6px'><span class='wca-badge' style='font-size:10px'>🏆 {winner}</span></div>"
        st.markdown(
            f"<div class='wca-card' style='padding:10px;text-align:center;margin-top:4px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center'>"
            f"<span style='font-weight:700;font-size:12px;color:{wc1}'>{t1}</span>"
            f"<span style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;letter-spacing:2px'>{g1}-{g2}</span>"
            f"<span style='font-weight:700;font-size:12px;color:{wc2}'>{t2}</span>"
            f"</div>{pen}{footer}"
            f"</div>", unsafe_allow_html=True
        )

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>🌍 WORLD CUP SIMULATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6b7a99'>Simula il Mondiale 2026 completo: fase a gironi → ottavi → quarti → semifinali → finale.</p>", unsafe_allow_html=True)

if "sim_count" not in st.session_state:
    st.session_state.sim_count = 0

run_sim = st.button("▶️ Simula Mondiale 2026", use_container_width=True)

if run_sim:
    st.session_state.sim_count += 1
    # Seed diverso ad ogni click
    sim_seed = st.session_state.sim_count * 17 + 2026

    random.seed(sim_seed)

    # ── FASE A GIRONI ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("<h2>📋 FASE A GIRONI</h2>", unsafe_allow_html=True)

    qualificate = []
    terze = []
    all_results = {}

    for gname, teams in GIRONI.items():
        standing, pts, gf, ga, matches = simulate_group(teams)
        all_results[gname] = (standing, pts, gf, ga, matches)
        qualificate.append(standing[0])
        qualificate.append(standing[1])
        terze.append((standing[2], pts[standing[2]], gf[standing[2]]-ga[standing[2]]))

    terze_sorted = sorted(terze, key=lambda x:(x[1],x[2]), reverse=True)[:8]
    qualificate += [t[0] for t in terze_sorted]

    sel_g = st.selectbox("📂 Seleziona Girone per i risultati", [f"Girone {k}" for k in GIRONI.keys()])
    gkey = sel_g.replace("Girone ","")
    standing, pts, gf, ga, matches = all_results[gkey]

    col_class, col_matches = st.columns([2,3])
    with col_class:
        st.markdown(f"<span class='wca-section-label'>Classifica {sel_g}</span>", unsafe_allow_html=True)
        for rank, t in enumerate(standing):
            fp = flag_img(t)
            diff = gf[t]-ga[t]
            diff_str = f"+{diff}" if diff>0 else str(diff)
            bg = "#1a2035" if rank<2 else "#111827"
            border = "#00d4ff" if rank==0 else ("#00e5a0" if rank==1 else "#1f2d45")
            passed = "✅" if rank<2 else ""
            cf, ci = st.columns([1,5])
            with cf:
                if fp: st.image(fp, width=28)
            with ci:
                st.markdown(
                    f"<div style='background:{bg};border-left:3px solid {border};padding:6px 12px;border-radius:6px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center'>"
                    f"<span style='font-weight:700;font-size:13px'>{rank+1}. {t} {passed}</span>"
                    f"<span style='color:#6b7a99;font-size:11px'><b style='color:#00d4ff'>{pts[t]}pt</b> &nbsp;{gf[t]}:{ga[t]} &nbsp;{diff_str}</span>"
                    f"</div>", unsafe_allow_html=True
                )

    with col_matches:
        st.markdown(f"<span class='wca-section-label'>Risultati {sel_g}</span>", unsafe_allow_html=True)
        mc = st.columns(3)
        for idx,(t1,t2,g1,g2) in enumerate(matches):
            is_draw = (g1 == g2)
            winner = t1 if g1>g2 else (t2 if g2>g1 else t1)
            show_match_card(mc[idx%3], t1, t2, g1, g2, winner, draw=is_draw)

    st.markdown("---")
    st.markdown(f"<span class='wca-section-label'>✅ {len(qualificate)} squadre qualificate agli ottavi</span>", unsafe_allow_html=True)
    qc = st.columns(8)
    for i,t in enumerate(qualificate):
        with qc[i%8]:
            fp = flag_img(t)
            if fp: st.image(fp, width=36)
            st.markdown(f"<div style='font-size:10px;text-align:center;color:#e8edf5'>{t}</div>", unsafe_allow_html=True)

    # ── KNOCKOUT ──────────────────────────────────────────────────────────────
    random.seed(sim_seed + 1000)
    random.shuffle(qualificate)
    current_round = [(qualificate[i], qualificate[i+1]) for i in range(0, len(qualificate), 2)]
    round_names = ["Ottavi di Finale","Quarti di Finale","Semifinale","Finale"]
    champion = None

    for rname in round_names:
        if not current_round: break
        st.markdown("---")
        st.markdown(f"<h2>{rname.upper()}</h2>", unsafe_allow_html=True)
        winners=[]; round_data=[]
        for t1,t2 in current_round:
            winner, penalties = simulate_match(t1, t2, knockout=True)
            g1,g2 = predict_score(t1,t2)
            if penalties: g1=g2=min(g1,g2,1)
            elif winner==t2: g1,g2=g2,g1
            winners.append(winner)
            round_data.append({"t1":t1,"t2":t2,"winner":winner,"g1":g1,"g2":g2,"pen":penalties})

        cols_n = min(len(round_data),4)
        for rs in range(0,len(round_data),cols_n):
            rm = round_data[rs:rs+cols_n]
            cols = st.columns(len(rm))
            for col,m in zip(cols,rm):
                show_match_card(col,m["t1"],m["t2"],m["g1"],m["g2"],m["winner"],m["pen"])

        current_round=[(winners[i],winners[i+1]) for i in range(0,len(winners)-1,2)]
        if rname=="Finale": champion=winners[0]

    # ── CAMPIONE ──────────────────────────────────────────────────────────────
    if champion:
        st.markdown("---")
        st.markdown("<span class='wca-section-label'>🏆 Campione del Mondo</span>", unsafe_allow_html=True)
        fpc = flag_img(champion)
        cc, ci = st.columns([1,3])
        with cc:
            if fpc: st.image(fpc, width=130)
        with ci:
            cr = ratings.get(champion,{})
            st.markdown(
                f"<div style='padding:8px 0'>"
                f"<div style='color:#6b7a99;font-size:11px;letter-spacing:3px;text-transform:uppercase'>FIFA WORLD CUP 2026 · CAMPIONE</div>"
                f"<h1 style='color:#00d4ff;font-size:3.5rem;margin:4px 0'>{champion}</h1>"
                f"<span class='wca-badge'>⭐ {cr.get('OverallRating','—')} Overall</span>"
                f"<span class='wca-badge' style='margin-left:8px'>⚔️ {cr.get('AttackRating','—')} ATT</span>"
                f"<span class='wca-badge' style='margin-left:8px'>🛡️ {cr.get('DefenseRating','—')} DEF</span>"
                f"</div>", unsafe_allow_html=True
            )

        # ── MONTE CARLO ───────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("<span class='wca-section-label'>📊 Win Probability — Monte Carlo</span>", unsafe_allow_html=True)
        st.markdown("<p style='color:#6b7a99;font-size:13px'>500 simulazioni indipendenti del torneo.</p>", unsafe_allow_html=True)

        with st.spinner("Calcolo probabilità..."):
            probs = monte_carlo_sim(500, base_seed=sim_seed)

        prob_df = (pd.DataFrame(list(probs.items()), columns=["Squadra","Probabilità"])
                   .sort_values("Probabilità", ascending=False).head(12).reset_index(drop=True))

        if prob_df.empty:
            st.warning("Nessun dato disponibile per il grafico.")
        else:
            bar_colors = ["#00d4ff" if i==0 else ("#f39c12" if i<3 else ("#00e5a0" if i<6 else "#1f2d45")) for i in range(len(prob_df))]
            fig = go.Figure(go.Bar(
                x=prob_df["Squadra"], y=prob_df["Probabilità"],
                marker_color=bar_colors,
                text=[f"{v}%" for v in prob_df["Probabilità"]],
                textposition="outside", textfont=dict(color="#e8edf5", size=13),
                marker_line_width=0,
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e8edf5"),
                xaxis=dict(gridcolor="#1f2d45", color="#6b7a99", tickfont=dict(size=11)),
                yaxis=dict(gridcolor="#1f2d45", color="#6b7a99", title="% vittoria torneo",
                           ticksuffix="%", range=[0, prob_df["Probabilità"].max()*1.3]),
                height=400, margin=dict(t=20,b=20,l=10,r=10), showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<span class='wca-section-label'>🎯 Top 5 Favoriti</span>", unsafe_allow_html=True)
            cols5 = st.columns(5)
            medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
            for i,(col,(_,row)) in enumerate(zip(cols5, prob_df.head(5).iterrows())):
                with col:
                    fp = flag_img(row["Squadra"])
                    if fp: st.image(fp, width=60)
                    st.markdown(
                        f"<div class='wca-card' style='text-align:center;padding:14px 10px'>"
                        f"<div style='font-size:1.6rem'>{medals[i]}</div>"
                        f"<div style='font-weight:700;font-size:14px;margin:6px 0'>{row['Squadra']}</div>"
                        f"<div style='font-size:2rem;color:#00d4ff;font-weight:700;font-family:Bebas Neue,sans-serif'>{row['Probabilità']}%</div>"
                        f"<div style='font-size:10px;color:#6b7a99;text-transform:uppercase;letter-spacing:1px'>vittoria torneo</div>"
                        f"</div>", unsafe_allow_html=True
                    )

else:
    st.markdown("---")
    st.markdown("<span class='wca-section-label'>📋 Gironi Ufficiali — FIFA World Cup 2026</span>", unsafe_allow_html=True)
    gcols = st.columns(4)
    for idx,(name,teams) in enumerate(GIRONI.items()):
        with gcols[idx%4]:
            st.markdown(f"<div class='wca-card' style='padding:14px;margin-bottom:12px'><div style='font-family:Bebas Neue,sans-serif;font-size:1.3rem;letter-spacing:2px;margin-bottom:10px;color:#00d4ff'>GIRONE {name}</div>", unsafe_allow_html=True)
            for t in teams:
                fp=flag_img(t); rating=ratings.get(t,{}).get("OverallRating","—")
                c1,c2=st.columns([1,4])
                with c1:
                    if fp: st.image(fp, width=24)
                with c2:
                    st.markdown(f"<div style='font-size:12px;padding:2px 0'>{t} <span style='color:#6b7a99;font-size:11px'>· {rating}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;padding:32px;color:#6b7a99'><div style='font-size:3rem'>▶️</div><div style='font-size:16px;margin-top:8px'>Premi il bottone per simulare il Mondiale 2026</div></div>", unsafe_allow_html=True)