"""
update_data.py — World Cup Analyst
Aggiorna automaticamente team_stats.csv e world_cup_players.csv
usando API-Football (api-football.com).

USO:
    python update_data.py --api-key TUA_API_KEY
    python update_data.py --api-key TUA_API_KEY --season 2026

PIANO FREE: 100 chiamate/giorno — sufficiente per update completo.
"""

import argparse
import requests
import pandas as pd
import json
import os
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────
API_BASE = "https://v3.football.api-sports.io"
WC_2026_ID = 1  # Sostituisci con l'ID reale del torneo Mondiale 2026
              # Trovi l'ID con: GET /leagues?name=FIFA+World+Cup&season=2026

TEAM_NAME_MAP = {
    # API name → nome nel tuo dataset
    "Brazil": "Brasile",
    "France": "Francia",
    "Argentina": "Argentina",
    "England": "Inghilterra",
    "Spain": "Spagna",
    "Portugal": "Portogallo",
    "Germany": "Germania",
    "Netherlands": "Olanda",
    "Belgium": "Belgio",
    "Croatia": "Croazia",
    "Uruguay": "Uruguay",
    "Colombia": "Colombia",
    "Morocco": "Marocco",
    "Senegal": "Senegal",
    "Japan": "Giappone",
    "Mexico": "Messico",
    "USA": "USA",
    "Australia": "Australia",
    "Norway": "Norvegia",
    "Switzerland": "Svizzera",
}

POSITION_MAP = {
    "Attacker": "ATT",
    "Midfielder": "CEN",
    "Defender": "DIF",
    "Goalkeeper": "POR",
    "Forward": "ATT",
    "Winger": "ALA",
}

# ── API CLIENT ───────────────────────────────────────────────────────────────
class FootballAPI:
    def __init__(self, api_key):
        self.headers = {
            "x-apisports-key": api_key,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
        self.calls_made = 0

    def get(self, endpoint, params=None):
        url = f"{API_BASE}/{endpoint}"
        resp = requests.get(url, headers=self.headers, params=params)
        self.calls_made += 1
        resp.raise_for_status()
        data = resp.json()
        remaining = resp.headers.get("x-ratelimit-requests-remaining", "?")
        print(f"  [{self.calls_made}] GET /{endpoint} → {len(data.get('response', []))} risultati | Chiamate rimanenti: {remaining}")
        return data.get("response", [])

    def get_league_id(self, season=2026):
        """Trova l'ID del Mondiale 2026."""
        results = self.get("leagues", {"name": "FIFA World Cup", "season": season})
        for r in results:
            print(f"  League trovata: {r['league']['name']} — ID: {r['league']['id']} — Season: {r['seasons']}")
        return results[0]["league"]["id"] if results else None

    def get_teams(self, league_id, season=2026):
        return self.get("teams", {"league": league_id, "season": season})

    def get_team_stats(self, team_id, league_id, season=2026):
        results = self.get("teams/statistics", {
            "team": team_id, "league": league_id, "season": season
        })
        return results[0] if results else None

    def get_players(self, team_id, league_id, season=2026, page=1):
        return self.get("players", {
            "team": team_id, "league": league_id,
            "season": season, "page": page
        })

    def get_top_scorers(self, league_id, season=2026):
        return self.get("players/topscorers", {
            "league": league_id, "season": season
        })

    def get_top_assists(self, league_id, season=2026):
        return self.get("players/topassists", {
            "league": league_id, "season": season
        })


# ── PROCESSING ───────────────────────────────────────────────────────────────
def process_team_stats(api, teams_data, league_id, season):
    """Costruisce team_stats.csv dai dati API."""
    rows = []
    for t in teams_data:
        team_name_api = t["team"]["name"]
        team_name_it  = TEAM_NAME_MAP.get(team_name_api, team_name_api)
        team_id       = t["team"]["id"]

        print(f"\n  Fetching stats: {team_name_it}...")
        stats = api.get_team_stats(team_id, league_id, season)
        if not stats:
            print(f"  ⚠️  Nessuna stat per {team_name_it}")
            continue

        goals_for  = stats["goals"]["for"]["average"]["total"] or 0
        goals_ag   = stats["goals"]["against"]["average"]["total"] or 0
        possession = stats.get("fixtures", {}).get("played", {}).get("total", 0)

        # Alcuni campi potrebbero non esserci — usa fallback
        passes     = stats.get("passes", {})
        pass_acc   = passes.get("accuracy", {}).get("total", 80) or 80
        shots      = stats.get("shots", {}).get("total", {}).get("total", 10) or 10
        shots_pg   = round(shots / max(stats["fixtures"]["played"]["total"], 1), 1)

        rows.append({
            "Squadra":             team_name_it,
            "Gol":                 float(goals_for),
            "xG":                  round(float(goals_for) * 0.9, 1),  # stima se xG non disponibile
            "Tiri":                shots_pg,
            "Possesso":            50,  # API-Football basic non ha possesso per tornei, stima
            "PrecisionePassaggi":  int(pass_acc),
        })

    return pd.DataFrame(rows)


def process_players(api, teams_data, league_id, season):
    """Costruisce world_cup_players.csv dai dati API."""
    all_players = []

    for t in teams_data:
        team_name_api = t["team"]["name"]
        team_name_it  = TEAM_NAME_MAP.get(team_name_api, team_name_api)
        team_id       = t["team"]["id"]

        print(f"\n  Fetching players: {team_name_it}...")
        players_data = api.get_players(team_id, league_id, season)

        for p in players_data:
            player   = p.get("player", {})
            stats_list = p.get("statistics", [{}])
            s        = stats_list[0] if stats_list else {}

            pos_raw  = player.get("position", "Midfielder")
            position = POSITION_MAP.get(pos_raw, "CEN")

            goals    = s.get("goals", {}).get("total", 0) or 0
            assists  = s.get("goals", {}).get("assists", 0) or 0
            shots    = s.get("shots", {}).get("total", 0) or 0
            passes   = s.get("passes", {})
            key_pass = passes.get("key", 0) or 0
            pass_acc = passes.get("accuracy", 80) or 80
            dribbles = s.get("dribbles", {}).get("success", 0) or 0
            duels_w  = s.get("duels", {}).get("won", 0) or 0
            games    = s.get("games", {})
            apps     = games.get("appearences", 0) or 0
            speed    = 75  # non disponibile via API standard

            all_players.append({
                "Giocatore":          player.get("name", "Unknown"),
                "Squadra":            team_name_it,
                "Ruolo":              position,
                "Età":                player.get("age", 25),
                "Presenze":           apps,
                "Gol":                goals,
                "Assist":             assists,
                "xG":                 round(goals * 0.85, 1),
                "Tiri":               shots,
                "Velocita":           speed,
                "KeyPasses":          key_pass,
                "Dribbling":          dribbles,
                "DuelliVinti":        duels_w,
                "ProgressiveCarries": round(dribbles * 0.6, 1),
                "PassAccuracy":       int(pass_acc),
            })

    return pd.DataFrame(all_players)


def add_power_ratings(df_teams):
    """Ricalcola Power Ratings dopo l'update."""
    def norm(series, new_min=50, new_max=95):
        mn, mx = series.min(), series.max()
        if mx == mn: return pd.Series([72.5]*len(series), index=series.index)
        return ((series - mn) / (mx - mn)) * (new_max - new_min) + new_min

    df_teams["AttackRating"]   = (norm(df_teams["Gol"])*0.40 + norm(df_teams["xG"])*0.35 + norm(df_teams["Tiri"])*0.25).round(1)
    df_teams["MidfieldRating"] = (norm(df_teams["Possesso"])*0.50 + norm(df_teams["PrecisionePassaggi"])*0.50).round(1)
    df_teams["DefenseRating"]  = (norm(df_teams["Possesso"])*0.30 + norm(df_teams["PrecisionePassaggi"])*0.30 + norm(df_teams["Tiri"].max()+df_teams["Tiri"].min()-df_teams["Tiri"])*0.40).round(1)
    df_teams["OverallRating"]  = (df_teams["AttackRating"]*0.40 + df_teams["MidfieldRating"]*0.30 + df_teams["DefenseRating"]*0.30).round(1)
    return df_teams


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Update World Cup Analyst data")
    parser.add_argument("--api-key",  required=True, help="API-Football API key")
    parser.add_argument("--season",   type=int, default=2026, help="Stagione (default: 2026)")
    parser.add_argument("--dry-run",  action="store_true", help="Non sovrascrive i CSV, salva in raw/")
    parser.add_argument("--teams-only", action="store_true", help="Aggiorna solo team_stats.csv")
    args = parser.parse_args()

    print("\n" + "="*60)
    print("  WORLD CUP ANALYST — DATA UPDATE")
    print(f"  Season: {args.season}")
    print(f"  Dry run: {args.dry_run}")
    print("="*60)

    api = FootballAPI(args.api_key)

    # 1. Trova league ID
    print("\n[1/4] Cerco ID Mondiale 2026...")
    league_id = api.get_league_id(args.season)
    if not league_id:
        print("❌ Mondiale 2026 non trovato. Verifica la stagione o l'API key.")
        return
    print(f"  ✅ League ID: {league_id}")

    # 2. Fetch squadre
    print("\n[2/4] Fetch squadre...")
    teams_data = api.get_teams(league_id, args.season)
    # Filtra solo squadre nel nostro dataset
    teams_data = [t for t in teams_data if t["team"]["name"] in TEAM_NAME_MAP]
    print(f"  ✅ {len(teams_data)} squadre trovate")

    # 3. Team stats
    print("\n[3/4] Fetch team stats...")
    df_teams = process_team_stats(api, teams_data, league_id, args.season)
    df_teams = add_power_ratings(df_teams)
    print(f"  ✅ {len(df_teams)} squadre processate")

    # 4. Players
    if not args.teams_only:
        print("\n[4/4] Fetch giocatori...")
        df_players = process_players(api, teams_data, league_id, args.season)
        print(f"  ✅ {len(df_players)} giocatori processati")
    else:
        print("\n[4/4] Skippato (--teams-only)")
        df_players = None

    # 5. Salva
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    if args.dry_run:
        # Salva in raw/ senza sovrascrivere
        df_teams.to_csv(f"data/raw/team_stats_{timestamp}.csv", index=False)
        if df_players is not None:
            df_players.to_csv(f"data/raw/players_{timestamp}.csv", index=False)
        print(f"\n  ✅ Salvato in data/raw/ (dry run)")
    else:
        # Backup dei vecchi file
        for f in ["data/team_stats.csv", "data/world_cup_players.csv"]:
            if os.path.exists(f):
                backup = f.replace("data/", f"data/raw/backup_{timestamp}_")
                os.rename(f, backup)
                print(f"  Backup: {backup}")

        df_teams.to_csv("data/team_stats.csv", index=False)
        df_teams.to_csv(f"data/processed/team_stats_{timestamp}.csv", index=False)
        if df_players is not None:
            df_players.to_csv("data/world_cup_players.csv", index=False)
            df_players.to_csv(f"data/processed/players_{timestamp}.csv", index=False)

        print(f"\n  ✅ CSV aggiornati con successo!")
        print(f"  📊 {len(df_teams)} squadre | {len(df_players) if df_players is not None else 0} giocatori")

    print(f"\n  📡 Chiamate API usate: {api.calls_made}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()