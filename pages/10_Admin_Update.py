"""
Pagina Admin — aggiorna i dati direttamente dall'app Streamlit.
Accessibile solo inserendo la password admin.
"""
import os
import subprocess
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

if st.button("🚀 Avvia Update", disabled=not api_key):
    with st.spinner("Aggiornamento in corso..."):
        cmd = ["python", "update_data.py", "--api-key", api_key, "--season", str(season)]
        if dry_run: cmd.append("--dry-run")
        if teams_only: cmd.append("--teams-only")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                st.success("✅ Update completato!")
                st.code(result.stdout, language="bash")
            else:
                st.error("❌ Errore durante l'update")
                st.code(result.stderr, language="bash")
        except subprocess.TimeoutExpired:
            st.error("❌ Timeout — l'update ha impiegato troppo tempo")
        except Exception as e:
            st.error(f"❌ Errore: {e}")

st.markdown("---")

# ── UPDATE MANUALE CSV ────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📁 Upload CSV Manuale</span>", unsafe_allow_html=True)

col_up1, col_up2 = st.columns(2)

with col_up1:
    st.markdown("**team_stats.csv**")
    uploaded_teams = st.file_uploader("Carica team_stats.csv", type="csv", key="teams")
    if uploaded_teams:
        df_new = pd.read_csv(uploaded_teams)
        required = ["Squadra","Gol","xG","Tiri","Possesso","PrecisionePassaggi"]
        if all(c in df_new.columns for c in required):
            st.dataframe(df_new.head(), use_container_width=True)
            if st.button("✅ Salva team_stats.csv"):
                # Ricalcola rating
                def norm(s):
                    mn,mx = s.min(),s.max()
                    return ((s-mn)/(mx-mn))*45+50 if mx!=mn else pd.Series([72.5]*len(s))
                df_new["AttackRating"]   = (norm(df_new["Gol"])*0.40+norm(df_new["xG"])*0.35+norm(df_new["Tiri"])*0.25).round(1)
                df_new["MidfieldRating"] = (norm(df_new["Possesso"])*0.50+norm(df_new["PrecisionePassaggi"])*0.50).round(1)
                df_new["DefenseRating"]  = (norm(df_new["Possesso"])*0.30+norm(df_new["PrecisionePassaggi"])*0.30+norm(df_new["Tiri"].max()+df_new["Tiri"].min()-df_new["Tiri"])*0.40).round(1)
                df_new["OverallRating"]  = (df_new["AttackRating"]*0.40+df_new["MidfieldRating"]*0.30+df_new["DefenseRating"]*0.30).round(1)
                df_new.to_csv("data/team_stats.csv", index=False)
                st.success("✅ Salvato e rating ricalcolati!")
        else:
            st.error(f"Colonne mancanti. Richieste: {required}")

with col_up2:
    st.markdown("**world_cup_players.csv**")
    uploaded_players = st.file_uploader("Carica world_cup_players.csv", type="csv", key="players")
    if uploaded_players:
        df_new_p = pd.read_csv(uploaded_players)
        required_p = ["Giocatore","Squadra","Ruolo","Età","Gol","Assist"]
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
            size  = round(os.path.getsize(fpath)/1024, 1)
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%d/%m/%Y %H:%M")
            st.markdown(
                f"<div class='wca-card' style='padding:8px 16px;margin-bottom:6px;display:flex;justify-content:space-between'>"
                f"<span>📄 {b}</span>"
                f"<span style='color:#6b7a99;font-size:12px'>{size} KB · {mtime}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Nessun backup trovato.")
else:
    st.info("Cartella data/raw/ non ancora creata.")