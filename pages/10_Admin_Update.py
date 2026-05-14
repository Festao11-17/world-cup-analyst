import os
import streamlit as st
import pandas as pd
from datetime import datetime

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1>⚙️ ADMIN — DATA UPDATE</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6b7a99'>Aggiorna il database direttamente dall'app.</p>", unsafe_allow_html=True)

# ── AUTH ─────────────────────────────────────────────────────────────────────
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "wca2026")

with st.expander("🔐 Login Admin", expanded=True):
    pwd = st.text_input("Password", type="password")
    if pwd != ADMIN_PASSWORD:
        st.warning("Inserisci la password admin per continuare.")
        st.stop()
    st.success("✅ Accesso consentito")

st.markdown("---")

# ── STATO DATABASE ────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📊 Stato Database Attuale</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if os.path.exists("data/team_stats.csv"):
        df_t = pd.read_csv("data/team_stats.csv")
        mod_time = datetime.fromtimestamp(os.path.getmtime("data/team_stats.csv"))
        st.metric("Squadre nel database", len(df_t))
        st.caption(f"Ultimo aggiornamento: {mod_time.strftime('%d/%m/%Y %H:%M')}")
    else:
        st.error("team_stats.csv non trovato")

with col2:
    if os.path.exists("data/world_cup_players.csv"):
        df_p = pd.read_csv("data/world_cup_players.csv")
        mod_time2 = datetime.fromtimestamp(os.path.getmtime("data/world_cup_players.csv"))
        st.metric("Giocatori nel database", len(df_p))
        st.caption(f"Ultimo aggiornamento: {mod_time2.strftime('%d/%m/%Y %H:%M')}")
    else:
        st.error("world_cup_players.csv non trovato")

st.markdown("---")

# ── UPDATE VIA API ────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>🔄 Aggiorna via API-Football</span>", unsafe_allow_html=True)

api_key = st.text_input(
    "API Key (api-football.com)",
    value=os.environ.get("FOOTBALL_API_KEY", ""),
    type="password",
    help="Ottieni la key gratuita su api-football.com (100 chiamate/giorno)"
)

col_opt1, col_opt2, col_opt3 = st.columns(3)
with col_opt1:
    season = st.number_input("Stagione", value=2026, step=1)
with col_opt2:
    dry_run = st.checkbox("Dry Run (non sovrascrive)", value=True)
with col_opt3:
    teams_only = st.checkbox("Solo team stats")

def calc_ratings(df):
    def norm(s, a=50, b=95):
        mn, mx = s.min(), s.max()
        if mx == mn:
            return pd.Series([72.5] * len(s), index=s.index)
        return ((s - mn) / (mx - mn)) * (b - a) + a
    df["AttackRating"]   = (norm(df["Gol"])*0.40 + norm(df["xG"])*0.35 + norm(df["Tiri"])*0.25).round(1)
    df["MidfieldRating"] = (norm(df["Possesso"])*0.50 + norm(df["PrecisionePassaggi"])*0.50).round(1)
    df["DefenseRating"]  = (norm(df["Possesso"])*0.30 + norm(df["PrecisionePassaggi"])*0.30 +
                            norm(df["Tiri"].max() + df["Tiri"].min() - df["Tiri"])*0.40).round(1)
    df["OverallRating"]  = (df["AttackRating"]*0.40 + df["MidfieldRating"]*0.30 + df["DefenseRating"]*0.30).round(1)
    return df

if st.button("🚀 Avvia Update", disabled=not api_key):
    with st.spinner("Aggiornamento in corso..."):
        try:
            import requests as req

            HEADERS = {
                "x-apisports-key": api_key,
                "x-rapidapi-host": "v3.football.api-sports.io"
            }
            BASE = "https://v3.football.api-sports.io"
            calls = [0]

            def api_get(endpoint, params=None):
                r = req.get(f"{BASE}/{endpoint}", headers=HEADERS, params=params)
                calls[0] += 1
                return r.json().get("response", [])

            # 1. Trova league ID
            st.write("🔍 Cerco Mondiale 2026...")
            leagues = api_get("leagues", {"name": "FIFA World Cup", "season": int(season)})
            if not leagues:
                st.error("❌ Mondiale 2026 non trovato nell'API.")
                st.info("💡 Usa l'upload manuale CSV qui sotto.")
                st.stop()

            league_id = leagues[0]["league"]["id"]
            st.write(f"✅ League ID: {league_id}")

            # 2. Fetch squadre
            st.write("📋 Fetch squadre...")
            teams_resp = api_get("teams", {"league": league_id, "season": int(season)})
            st.write(f"✅ {len(teams_resp)} squadre trovate")

            TEAM_MAP = {
                "Brazil": "Brasile", "France": "Francia", "Argentina": "Argentina",
                "England": "Inghilterra", "Spain": "Spagna", "Portugal": "Portogallo",
                "Germany": "Germania", "Netherlands": "Olanda", "Belgium": "Belgio",
                "Croatia": "Croazia", "Uruguay": "Uruguay", "Colombia": "Colombia",
                "Morocco": "Marocco", "Senegal": "Senegal", "Japan": "Giappone",
                "Mexico": "Messico", "USA": "USA", "Australia": "Australia",
                "Norway": "Norvegia", "Switzerland": "Svizzera",
            }
            teams_resp = [t for t in teams_resp if t["team"]["name"] in TEAM_MAP]

            # 3. Team stats
            rows = []
            prog = st.progress(0)
            for i, t in enumerate(teams_resp):
                name_it = TEAM_MAP[t["team"]["name"]]
                stats = api_get("teams/statistics", {
                    "team": t["team"]["id"],
                    "league": league_id,
                    "season": int(season)
                })
                if stats:
                    s = stats[0]
                    gol = float(s["goals"]["for"]["average"]["total"] or 0)
                    shots_total = s.get("shots", {}).get("total", {}).get("total", 10) or 10
                    played = s["fixtures"]["played"]["total"] or 1
                    pass_acc = s.get("passes", {}).get("accuracy", {}).get("total", 80) or 80
                    rows.append({
                        "Squadra": name_it,
                        "Gol": round(gol, 1),
                        "xG": round(gol * 0.9, 1),
                        "Tiri": round(shots_total / played, 1),
                        "Possesso": 50,
                        "PrecisionePassaggi": int(pass_acc),
                    })
                prog.progress((i + 1) / max(len(teams_resp), 1))

            if rows:
                df_new = calc_ratings(pd.DataFrame(rows))
                if not dry_run:
                    df_new.to_csv("data/team_stats.csv", index=False)
                    st.success(f"✅ team_stats.csv aggiornato! ({len(df_new)} squadre)")
                else:
                    st.success(f"✅ Dry run OK — {len(df_new)} squadre processate (non salvato)")
                    st.dataframe(df_new, use_container_width=True)

            st.info(f"📡 Chiamate API usate: {calls[0]}")

        except Exception as e:
            st.error(f"❌ Errore: {e}")
            import traceback
            st.code(traceback.format_exc())

st.markdown("---")

# ── UPLOAD MANUALE CSV ────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📁 Upload CSV Manuale</span>", unsafe_allow_html=True)

col_up1, col_up2 = st.columns(2)

with col_up1:
    st.markdown("**team_stats.csv**")
    uploaded_teams = st.file_uploader("Carica team_stats.csv", type="csv", key="teams")
    if uploaded_teams:
        df_new = pd.read_csv(uploaded_teams)
        required = ["Squadra", "Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]
        if all(c in df_new.columns for c in required):
            st.dataframe(df_new.head(), use_container_width=True)
            if st.button("✅ Salva team_stats.csv"):
                df_new = calc_ratings(df_new)
                df_new.to_csv("data/team_stats.csv", index=False)
                st.success("✅ Salvato e rating ricalcolati!")
        else:
            st.error(f"Colonne mancanti. Richieste: {required}")

with col_up2:
    st.markdown("**world_cup_players.csv**")
    uploaded_players = st.file_uploader("Carica world_cup_players.csv", type="csv", key="players")
    if uploaded_players:
        df_new_p = pd.read_csv(uploaded_players)
        required_p = ["Giocatore", "Squadra", "Ruolo", "Età", "Gol", "Assist"]
        if all(c in df_new_p.columns for c in required_p):
            st.dataframe(df_new_p.head(), use_container_width=True)
            if st.button("✅ Salva world_cup_players.csv"):
                df_new_p.to_csv("data/world_cup_players.csv", index=False)
                st.success(f"✅ Salvato! {len(df_new_p)} giocatori.")
        else:
            st.error(f"Colonne mancanti. Richieste: {required_p}")

st.markdown("---")

# ── STORICO BACKUP ────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>🗂️ Storico Backup</span>", unsafe_allow_html=True)

raw_dir = "data/raw"
if os.path.exists(raw_dir):
    backups = sorted(os.listdir(raw_dir), reverse=True)
    if backups:
        for b in backups[:8]:
            fpath = os.path.join(raw_dir, b)
            size  = round(os.path.getsize(fpath) / 1024, 1)
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%d/%m/%Y %H:%M")
            st.markdown(
                f"<div class='wca-card' style='padding:8px 16px;margin-bottom:6px;"
                f"display:flex;justify-content:space-between'>"
                f"<span>📄 {b}</span>"
                f"<span style='color:#6b7a99;font-size:12px'>{size} KB · {mtime}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Nessun backup trovato.")
else:
    st.info("Cartella data/raw/ non ancora creata.")