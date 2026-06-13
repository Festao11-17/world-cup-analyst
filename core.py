from __future__ import annotations

import random
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import quote

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

FLAG_MAP = {
    "Messico": "Girone_A/Messico",
    "Cechia": "Girone_A/Cechia",
    "Corea del Sud": "Girone_A/Corea_del_Sud",
    "Corea_del_Sud": "Girone_A/Corea_del_Sud",
    "Sudafrica": "Girone_A/Sudafrica",
    "Svizzera": "Girone_B/Svizzera",
    "Canada": "Girone_B/Canada",
    "Bosnia": "Girone_B/Bosnia_ed_Erzegovina",
    "Bosnia ed Erzegovina": "Girone_B/Bosnia_ed_Erzegovina",
    "Bosnia_ed_Erzegovina": "Girone_B/Bosnia_ed_Erzegovina",
    "Qatar": "Girone_B/Qatar",
    "Brasile": "Girone_C/Brasile",
    "Marocco": "Girone_C/Marocco",
    "Haiti": "Girone_C/Haiti",
    "Scozia": "Girone_C/Scozia",
    "Australia": "Girone_D/Australia",
    "Stati Uniti": "Girone_D/Stati_Uniti",
    "Stati_Uniti": "Girone_D/Stati_Uniti",
    "Paraguay": "Girone_D/Paraguay",
    "Turchia": "Girone_D/Turchia",
    "Germania": "Girone_E/Germania",
    "Ecuador": "Girone_E/Ecuador",
    "Costa d'Avorio": "Girone_E/Costa_d'Avorio",
    "Costa_d'Avorio": "Girone_E/Costa_d'Avorio",
    "Curacao": "Girone_E/Curacao",
    "Giappone": "Girone_F/Giappone",
    "Olanda": "Girone_F/Olanda",
    "Svezia": "Girone_F/Svezia",
    "Tunisia": "Girone_F/Tunisia",
    "Belgio": "Girone_G/Belgio",
    "Egitto": "Girone_G/Egitto",
    "Iran": "Girone_G/Iran",
    "Nuova Zelanda": "Girone_G/Nuova_Zelanda",
    "Nuova_Zelanda": "Girone_G/Nuova_Zelanda",
    "Spagna": "Girone_H/Spagna",
    "Uruguay": "Girone_H/Uruguay",
    "Arabia Saudita": "Girone_H/Arabia_Saudita",
    "Arabia_Saudita": "Girone_H/Arabia_Saudita",
    "Capo Verde": "Girone_H/Capo_Verde",
    "Capo_Verde": "Girone_H/Capo_Verde",
    "Francia": "Girone_I/Francia",
    "Senegal": "Girone_I/Senegal",
    "Norvegia": "Girone_I/Norvegia",
    "Iraq": "Girone_I/Iraq",
    "Argentina": "Girone_J/Argentina",
    "Algeria": "Girone_J/Algeria",
    "Austria": "Girone_J/Austria",
    "Giordania": "Girone_J/Giordania",
    "Portogallo": "Girone_K/Portogallo",
    "Colombia": "Girone_K/Colombia",
    "Rep. del Congo": "Girone_K/Repubblica_del_Congo",
    "Repubblica del Congo": "Girone_K/Repubblica_del_Congo",
    "Repubblica_del_Congo": "Girone_K/Repubblica_del_Congo",
    "Uzbekistan": "Girone_K/Uzbekistan",
    "Inghilterra": "Girone_L/Inghilterra",
    "Croazia": "Girone_L/Croazia",
    "Ghana": "Girone_L/Ghana",
    "Panama": "Girone_L/Panama",
}

GIRONI = {
    "A": ["Messico", "Cechia", "Corea del Sud", "Sudafrica"],
    "B": ["Svizzera", "Canada", "Bosnia", "Qatar"],
    "C": ["Brasile", "Marocco", "Haiti", "Scozia"],
    "D": ["Australia", "Stati Uniti", "Paraguay", "Turchia"],
    "E": ["Germania", "Ecuador", "Costa d'Avorio", "Curacao"],
    "F": ["Giappone", "Olanda", "Svezia", "Tunisia"],
    "G": ["Belgio", "Egitto", "Iran", "Nuova Zelanda"],
    "H": ["Spagna", "Uruguay", "Arabia Saudita", "Capo Verde"],
    "I": ["Francia", "Senegal", "Norvegia", "Iraq"],
    "J": ["Argentina", "Algeria", "Austria", "Giordania"],
    "K": ["Portogallo", "Colombia", "Rep. del Congo", "Uzbekistan"],
    "L": ["Inghilterra", "Croazia", "Ghana", "Panama"],
}

CSV_MAP = {
    "Cechia": "data/Girone_A/repubblica_ceca.csv",
    "Corea del Sud": "data/Girone_A/corea_del_sud.csv",
    "Messico": "data/Girone_A/messico.csv",
    "Sudafrica": "data/Girone_A/sud_africa.csv",
    "Bosnia": "data/Girone_B/bosnia.csv",
    "Canada": "data/Girone_B/canada.csv",
    "Qatar": "data/Girone_B/qatar.csv",
    "Svizzera": "data/Girone_B/svizzera.csv",
    "Brasile": "data/Girone_C/brasile.csv",
    "Haiti": "data/Girone_C/haiti.csv",
    "Marocco": "data/Girone_C/marocco.csv",
    "Scozia": "data/Girone_C/scozia.csv",
    "Australia": "data/Girone_D/australia.csv",
    "Paraguay": "data/Girone_D/paraguay.csv",
    "Stati Uniti": "data/Girone_D/usa.csv",
    "Turchia": "data/Girone_D/turchia.csv",
    "Costa d'Avorio": "data/Girone_E/costa_d'avorio.csv",
    "Curacao": "data/Girone_E/curacao.csv",
    "Ecuador": "data/Girone_E/ecuador.csv",
    "Germania": "data/Girone_E/germania.csv",
    "Giappone": "data/Girone_F/giappone.csv",
    "Olanda": "data/Girone_F/olanda.csv",
    "Svezia": "data/Girone_F/svezia.csv",
    "Tunisia": "data/Girone_F/tunisia.csv",
    "Belgio": "data/Girone_G/belgio.csv",
    "Egitto": "data/Girone_G/egitto.csv",
    "Iran": "data/Girone_G/iran.csv",
    "Nuova Zelanda": "data/Girone_G/nuova_zelanda.csv",
    "Arabia Saudita": "data/Girone_H/arabia_saudita.csv",
    "Capo Verde": "data/Girone_H/capo_verde.csv",
    "Spagna": "data/Girone_H/spagna.csv",
    "Uruguay": "data/Girone_H/uruguay.csv",
    "Francia": "data/Girone_I/francia.csv",
    "Iraq": "data/Girone_I/iraq.csv",
    "Norvegia": "data/Girone_I/norvegia.csv",
    "Senegal": "data/Girone_I/senegal.csv",
    "Algeria": "data/Girone_J/algeria.csv",
    "Argentina": "data/Girone_J/argentina.csv",
    "Austria": "data/Girone_J/austria.csv",
    "Giordania": "data/Girone_J/giordania.csv",
    "Colombia": "data/Girone_K/colombia.csv",
    "Portogallo": "data/Girone_K/portogallo.csv",
    "Rep. del Congo": "data/Girone_K/repubblica_del_congo.csv",
    "Uzbekistan": "data/Girone_K/uzbekistan.csv",
    "Croazia": "data/Girone_L/croazia.csv",
    "Ghana": "data/Girone_L/ghana.csv",
    "Inghilterra": "data/Girone_L/inghilterra.csv",
    "Panama": "data/Girone_L/panama.csv",
}

FIFA_RANKINGS = [
    {"Squadra": "Argentina", "RankingFIFA": 1, "Punti": 1874.3, "Girone": "J"},
    {"Squadra": "Francia", "RankingFIFA": 2, "Punti": 1851.4, "Girone": "I"},
    {"Squadra": "Spagna", "RankingFIFA": 3, "Punti": 1836.7, "Girone": "H"},
    {"Squadra": "Inghilterra", "RankingFIFA": 4, "Punti": 1806.9, "Girone": "L"},
    {"Squadra": "Brasile", "RankingFIFA": 5, "Punti": 1782.1, "Girone": "C"},
    {"Squadra": "Portogallo", "RankingFIFA": 6, "Punti": 1764.5, "Girone": "K"},
    {"Squadra": "Belgio", "RankingFIFA": 7, "Punti": 1742.8, "Girone": "G"},
    {"Squadra": "Olanda", "RankingFIFA": 8, "Punti": 1731.2, "Girone": "F"},
    {"Squadra": "Germania", "RankingFIFA": 9, "Punti": 1720.6, "Girone": "E"},
    {"Squadra": "Colombia", "RankingFIFA": 10, "Punti": 1698.4, "Girone": "K"},
    {"Squadra": "Croazia", "RankingFIFA": 11, "Punti": 1687.3, "Girone": "L"},
    {"Squadra": "Uruguay", "RankingFIFA": 12, "Punti": 1658.9, "Girone": "H"},
    {"Squadra": "Marocco", "RankingFIFA": 13, "Punti": 1641.5, "Girone": "C"},
    {"Squadra": "Svizzera", "RankingFIFA": 14, "Punti": 1630.8, "Girone": "B"},
    {"Squadra": "Messico", "RankingFIFA": 15, "Punti": 1618.2, "Girone": "A"},
    {"Squadra": "Stati Uniti", "RankingFIFA": 16, "Punti": 1605.7, "Girone": "D"},
    {"Squadra": "Giappone", "RankingFIFA": 17, "Punti": 1594.3, "Girone": "F"},
    {"Squadra": "Senegal", "RankingFIFA": 18, "Punti": 1581.6, "Girone": "I"},
    {"Squadra": "Austria", "RankingFIFA": 19, "Punti": 1568.4, "Girone": "J"},
    {"Squadra": "Norvegia", "RankingFIFA": 20, "Punti": 1554.7, "Girone": "I"},
    {"Squadra": "Turchia", "RankingFIFA": 21, "Punti": 1541.2, "Girone": "D"},
    {"Squadra": "Australia", "RankingFIFA": 22, "Punti": 1528.6, "Girone": "D"},
    {"Squadra": "Cechia", "RankingFIFA": 23, "Punti": 1514.9, "Girone": "A"},
    {"Squadra": "Ecuador", "RankingFIFA": 24, "Punti": 1501.3, "Girone": "E"},
    {"Squadra": "Algeria", "RankingFIFA": 25, "Punti": 1487.8, "Girone": "J"},
    {"Squadra": "Corea del Sud", "RankingFIFA": 26, "Punti": 1474.2, "Girone": "A"},
    {"Squadra": "Canada", "RankingFIFA": 27, "Punti": 1460.7, "Girone": "B"},
    {"Squadra": "Tunisia", "RankingFIFA": 28, "Punti": 1447.1, "Girone": "F"},
    {"Squadra": "Svezia", "RankingFIFA": 29, "Punti": 1433.5, "Girone": "F"},
    {"Squadra": "Ghana", "RankingFIFA": 30, "Punti": 1419.9, "Girone": "L"},
    {"Squadra": "Iran", "RankingFIFA": 31, "Punti": 1406.4, "Girone": "G"},
    {"Squadra": "Bosnia", "RankingFIFA": 32, "Punti": 1392.8, "Girone": "B"},
    {"Squadra": "Paraguay", "RankingFIFA": 33, "Punti": 1379.2, "Girone": "D"},
    {"Squadra": "Costa d'Avorio", "RankingFIFA": 34, "Punti": 1365.7, "Girone": "E"},
    {"Squadra": "Panama", "RankingFIFA": 35, "Punti": 1352.1, "Girone": "L"},
    {"Squadra": "Egitto", "RankingFIFA": 36, "Punti": 1338.5, "Girone": "G"},
    {"Squadra": "Scozia", "RankingFIFA": 37, "Punti": 1325.0, "Girone": "C"},
    {"Squadra": "Sudafrica", "RankingFIFA": 38, "Punti": 1311.4, "Girone": "A"},
    {"Squadra": "Arabia Saudita", "RankingFIFA": 39, "Punti": 1297.9, "Girone": "H"},
    {"Squadra": "Uzbekistan", "RankingFIFA": 40, "Punti": 1284.3, "Girone": "K"},
    {"Squadra": "Giordania", "RankingFIFA": 41, "Punti": 1270.8, "Girone": "J"},
    {"Squadra": "Iraq", "RankingFIFA": 42, "Punti": 1257.2, "Girone": "I"},
    {"Squadra": "Rep. del Congo", "RankingFIFA": 43, "Punti": 1243.7, "Girone": "K"},
    {"Squadra": "Nuova Zelanda", "RankingFIFA": 44, "Punti": 1230.1, "Girone": "G"},
    {"Squadra": "Qatar", "RankingFIFA": 45, "Punti": 1216.6, "Girone": "B"},
    {"Squadra": "Capo Verde", "RankingFIFA": 46, "Punti": 1203.0, "Girone": "H"},
    {"Squadra": "Curacao", "RankingFIFA": 47, "Punti": 1189.5, "Girone": "E"},
    {"Squadra": "Haiti", "RankingFIFA": 48, "Punti": 1175.9, "Girone": "C"},
]

ROLE_MAP = {
    "POR": "POR",
    "Portiere": "POR",
    "DIF": "DIF",
    "Difensore": "DIF",
    "CEN": "CEN",
    "Centrocampista": "CEN",
    "ALA": "ALA",
    "Ala": "ALA",
    "ATT": "ATT",
    "Attaccante": "ATT",
}

ROLE_LABELS = {
    "POR": "Portieri",
    "DIF": "Difensori",
    "CEN": "Centrocampisti",
    "ALA": "Ali",
    "ATT": "Attaccanti",
}

ROLE_ORDER = ["POR", "DIF", "CEN", "ALA", "ATT"]

ROLE_STATS = {
    "POR": ["Presenze", "Parate", "PassAccuracy", "DistanzaPercorsa"],
    "DIF": ["Presenze", "Gol", "Assist", "Tiri", "DuelliVinti", "DistanzaPercorsa", "PassAccuracy"],
    "CEN": ["Presenze", "Gol", "Assist", "xG", "Tiri", "KeyPasses", "DistanzaPercorsa", "PassAccuracy"],
    "ALA": ["Presenze", "Gol", "Assist", "xG", "Tiri", "Velocita", "Dribbling", "KeyPasses", "DistanzaPercorsa"],
    "ATT": ["Presenze", "Gol", "Assist", "xG", "Tiri", "Velocita", "DuelliVinti", "DistanzaPercorsa"],
}

STAT_META = {
    "Presenze": ("Presenze", ""),
    "Gol": ("Gol", ""),
    "Assist": ("Assist", ""),
    "xG": ("xG", ""),
    "Tiri": ("Tiri", ""),
    "Velocita": ("Velocita", " km/h"),
    "KeyPasses": ("Key passes", ""),
    "Dribbling": ("Dribbling", ""),
    "DuelliVinti": ("Duelli vinti", "%"),
    "DistanzaPercorsa": ("Distanza", " km"),
    "PassAccuracy": ("Pass accuracy", "%"),
    "Parate": ("Parate", ""),
}


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if hasattr(value, "item"):
        return value.item()
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, default)))


def flag_url(team: str) -> str | None:
    rel = FLAG_MAP.get(team, team)
    path = ASSETS_DIR / "flags" / f"{rel}.png"
    if not path.exists():
        return None
    return f"/assets/flags/{quote(rel, safe='/')}.png"


def team_group(team: str) -> str | None:
    for group, teams in GIRONI.items():
        if team in teams:
            return group
    return None


@lru_cache(maxsize=1)
def load_team_stats() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "team_stats.csv")


@lru_cache(maxsize=1)
def load_all_players() -> pd.DataFrame:
    frames = []
    for group_dir in sorted(DATA_DIR.glob("Girone_*")):
        if not group_dir.is_dir():
            continue
        for csv_path in sorted(group_dir.glob("*.csv")):
            try:
                frames.append(pd.read_csv(csv_path))
            except Exception:
                continue
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


@lru_cache(maxsize=None)
def load_players(team: str) -> pd.DataFrame:
    rel = CSV_MAP.get(team)
    if not rel:
        return pd.DataFrame()
    path = BASE_DIR / rel
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def team_record(team: str) -> dict[str, Any]:
    df = load_team_stats()
    row = df[df["Squadra"] == team]
    if row.empty:
        raise KeyError(f"Squadra non trovata: {team}")
    data = json_safe(row.iloc[0].to_dict())
    data["Girone"] = team_group(team)
    data["flag"] = flag_url(team)
    return data


def available_teams() -> list[dict[str, Any]]:
    teams = []
    for group, names in GIRONI.items():
        for name in names:
            item = team_record(name)
            item["Girone"] = group
            teams.append(item)
    return teams


def bootstrap_payload() -> dict[str, Any]:
    return {
        "groups": GIRONI,
        "teams": available_teams(),
        "home": home_payload(),
        "rankingGroups": ["Tutti"] + sorted(GIRONI.keys()),
    }


def player_summary(row: pd.Series) -> dict[str, Any]:
    team = str(row.get("Squadra", ""))
    return {
        "name": row.get("Giocatore", "N/D"),
        "team": team,
        "flag": flag_url(team),
        "goals": as_int(row.get("Gol")),
        "assists": as_int(row.get("Assist")),
        "xG": as_float(row.get("xG")),
    }


def home_payload() -> dict[str, Any]:
    df = load_team_stats()
    players = load_all_players()

    best_attack = df.loc[df["Gol"].idxmax()]
    best_xg = df.loc[df["xG"].idxmax()]
    best_possession = df.loc[df["Possesso"].idxmax()]

    top_stats = [
        {
            "label": "Miglior attacco",
            "value": best_attack["Squadra"],
            "detail": f"{best_attack['Gol']} gol/match",
            "flag": flag_url(best_attack["Squadra"]),
        },
        {
            "label": "Miglior xG",
            "value": best_xg["Squadra"],
            "detail": f"xG {best_xg['xG']}",
            "flag": flag_url(best_xg["Squadra"]),
        },
        {
            "label": "Miglior possesso",
            "value": best_possession["Squadra"],
            "detail": f"{best_possession['Possesso']}%",
            "flag": flag_url(best_possession["Squadra"]),
        },
    ]

    if not players.empty and "Gol" in players.columns:
        top_scorer = players.loc[players["Gol"].idxmax()]
        top_assist = players.loc[players["Assist"].idxmax()]
        top_stats.extend(
            [
                {
                    "label": "Capocannoniere",
                    "value": top_scorer["Giocatore"],
                    "detail": f"{as_int(top_scorer['Gol'])} gol · {top_scorer['Squadra']}",
                    "flag": flag_url(top_scorer["Squadra"]),
                },
                {
                    "label": "Top assistman",
                    "value": top_assist["Giocatore"],
                    "detail": f"{as_int(top_assist['Assist'])} assist · {top_assist['Squadra']}",
                    "flag": flag_url(top_assist["Squadra"]),
                },
            ]
        )

    sort_col = "OverallRating" if "OverallRating" in df.columns else "Gol"
    top_two = df.nlargest(2, sort_col)
    first = team_record(top_two.iloc[0]["Squadra"])
    second = team_record(top_two.iloc[1]["Squadra"])

    top_teams = []
    for index, row in df.sort_values("OverallRating", ascending=False).head(10).reset_index(drop=True).iterrows():
        top_teams.append(
            {
                "rank": index + 1,
                "team": row["Squadra"],
                "flag": flag_url(row["Squadra"]),
                "overall": row["OverallRating"],
                "attack": row["AttackRating"],
                "defense": row["DefenseRating"],
            }
        )

    top_scorers = []
    if not players.empty and "Gol" in players.columns:
        for index, row in players.sort_values("Gol", ascending=False).head(8).reset_index(drop=True).iterrows():
            summary = player_summary(row)
            summary["rank"] = index + 1
            top_scorers.append(summary)

    return json_safe(
        {
            "summary": {
                "teams": int(df["Squadra"].nunique()),
                "groups": len(GIRONI),
                "players": int(len(players)),
            },
            "topStats": top_stats,
            "featuredMatch": {
                "team1": first,
                "team2": second,
                "radar": radar_payload([first, second], ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]),
            },
            "leaderboards": {
                "teams": top_teams,
                "scorers": top_scorers,
            },
        }
    )


def radar_payload(teams: list[dict[str, Any]], stats: list[str]) -> dict[str, Any]:
    labels = {
        "Gol": "Gol",
        "xG": "xG",
        "Tiri": "Tiri",
        "Possesso": "Possesso",
        "PrecisionePassaggi": "Passaggi",
        "AttackRating": "Attacco",
        "MidfieldRating": "Centro",
        "DefenseRating": "Difesa",
        "OverallRating": "Overall",
    }
    return {
        "labels": [labels.get(stat, stat) for stat in stats],
        "series": [
            {
                "name": team["Squadra"],
                "values": [as_float(team.get(stat)) for stat in stats],
                "color": "#007f5f" if index == 0 else "#c43f4b",
            }
            for index, team in enumerate(teams)
        ],
    }


def comparison_payload(team1: str, team2: str) -> dict[str, Any]:
    if team1 == team2:
        raise ValueError("Seleziona due squadre diverse.")
    t1 = team_record(team1)
    t2 = team_record(team2)
    rows = []
    for label, key, suffix in [
        ("Gol/Match", "Gol", ""),
        ("xG", "xG", ""),
        ("Tiri", "Tiri", ""),
        ("Possesso", "Possesso", "%"),
        ("Precisione passaggi", "PrecisionePassaggi", "%"),
        ("Overall", "OverallRating", ""),
        ("Attacco", "AttackRating", ""),
        ("Centrocampo", "MidfieldRating", ""),
        ("Difesa", "DefenseRating", ""),
    ]:
        left = as_float(t1.get(key))
        right = as_float(t2.get(key))
        max_value = max(left, right, 0.01)
        rows.append(
            {
                "label": label,
                "key": key,
                "left": left,
                "right": right,
                "suffix": suffix,
                "leftWidth": round(left / max_value * 100, 1),
                "rightWidth": round(right / max_value * 100, 1),
                "leader": "left" if left >= right else "right",
            }
        )
    return json_safe(
        {
            "team1": t1,
            "team2": t2,
            "stats": rows,
            "radar": radar_payload([t1, t2], ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]),
            "rosters": {
                team1: roster_payload(team1),
                team2: roster_payload(team2),
            },
        }
    )


def normalize_role(role: Any) -> str:
    return ROLE_MAP.get(str(role), "ATT")


def player_stats(row: pd.Series, role: str) -> list[dict[str, Any]]:
    stats = []
    for key in ROLE_STATS.get(role, ROLE_STATS["ATT"]):
        if key not in row:
            continue
        value = row.get(key)
        if value is None:
            continue
        try:
            if pd.isna(value) or float(value) == 0:
                continue
        except (TypeError, ValueError):
            pass
        label, suffix = STAT_META.get(key, (key, ""))
        stats.append({"label": label, "value": json_safe(value), "suffix": suffix})
    return stats


def roster_payload(team: str) -> list[dict[str, Any]]:
    df = load_players(team)
    if df.empty:
        return []
    records: dict[str, list[dict[str, Any]]] = {role: [] for role in ROLE_ORDER}
    for _, row in df.iterrows():
        role = normalize_role(row.get("Ruolo"))
        records.setdefault(role, []).append(
            {
                "name": row.get("Giocatore", "N/D"),
                "age": json_safe(row.get("Età")),
                "role": role,
                "roleLabel": ROLE_LABELS.get(role, role),
                "stats": player_stats(row, role),
            }
        )
    return [
        {"role": role, "label": ROLE_LABELS[role], "players": records.get(role, [])}
        for role in ROLE_ORDER
        if records.get(role)
    ]


def prediction_payload(team1: str, team2: str) -> dict[str, Any]:
    if team1 == team2:
        raise ValueError("Seleziona due squadre diverse.")
    t1 = team_record(team1)
    t2 = team_record(team2)

    s1 = t1["OverallRating"] * 0.50 + t1["AttackRating"] * 0.25 + t1["MidfieldRating"] * 0.15 + t1["DefenseRating"] * 0.10
    s2 = t2["OverallRating"] * 0.50 + t2["AttackRating"] * 0.25 + t2["MidfieldRating"] * 0.15 + t2["DefenseRating"] * 0.10
    total = s1 + s2
    p1 = round((s1 / total) * 100, 1)
    p2 = round((s2 / total) * 100, 1)
    draw = round(max(0, 35 - abs(p1 - p2) * 0.8), 1)
    factor = (100 - draw) / 100
    p1_adj = round(p1 * factor, 1)
    p2_adj = round(p2 * factor, 1)
    xg1 = round(t1["xG"] * (t1["AttackRating"] / 75), 1)
    xg2 = round(t2["xG"] * (t2["AttackRating"] / 75), 1)
    goals1 = int(round(xg1 * 0.85))
    goals2 = int(round(xg2 * 0.85))

    departments = []
    for label, key in [
        ("Attacco", "AttackRating"),
        ("Centrocampo", "MidfieldRating"),
        ("Difesa", "DefenseRating"),
        ("Overall", "OverallRating"),
    ]:
        left = as_float(t1[key])
        right = as_float(t2[key])
        max_value = max(left, right, 0.01)
        departments.append(
            {
                "label": label,
                "left": left,
                "right": right,
                "leftWidth": round(left / max_value * 100, 1),
                "rightWidth": round(right / max_value * 100, 1),
                "leader": "left" if left >= right else "right",
            }
        )

    diff = abs(t1["OverallRating"] - t2["OverallRating"])
    fav, fav_p, underdog_p = (team1, p1_adj, p2_adj) if p1_adj > p2_adj else (team2, p2_adj, p1_adj)
    if diff >= 10:
        verdict = f"{fav} domina su carta con un gap di {diff:.1f} punti."
        verdict_type = "strong"
    elif diff >= 5:
        verdict = f"{fav} parte favorita ({fav_p}% vs {underdog_p}%), ma la partita resta aperta."
        verdict_type = "edge"
    else:
        verdict = f"Gap di soli {diff:.1f} punti. Partita da dettagli."
        verdict_type = "balanced"

    return json_safe(
        {
            "team1": t1,
            "team2": t2,
            "probability": {"team1": p1_adj, "draw": draw, "team2": p2_adj},
            "score": {"team1": goals1, "team2": goals2, "xg1": xg1, "xg2": xg2},
            "departments": departments,
            "radar": radar_payload([t1, t2], ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]),
            "insights": match_insights(team1, team2, t1, t2),
            "verdict": {"text": verdict, "type": verdict_type, "favorite": fav},
        }
    )


def match_insights(team1: str, team2: str, t1: dict[str, Any], t2: dict[str, Any]) -> list[dict[str, str]]:
    insights = []
    checks = [
        ("Attacco", "AttackRating", "ha un attacco nettamente superiore", "Attacchi molto equilibrati"),
        ("Centrocampo", "MidfieldRating", "domina il centrocampo", "Centrocampo equilibrato"),
        ("Difesa", "DefenseRating", "ha una difesa piu solida", "Difese simili"),
    ]
    for label, key, strong_text, balanced_text in checks:
        diff = t1[key] - t2[key]
        if diff >= 8:
            insights.append({"label": label, "tone": "home", "text": f"{team1} {strong_text} ({t1[key]} vs {t2[key]})."})
        elif diff <= -8:
            insights.append({"label": label, "tone": "away", "text": f"{team2} {strong_text} ({t2[key]} vs {t1[key]})."})
        else:
            insights.append({"label": label, "tone": "neutral", "text": f"{balanced_text} ({t1[key]} vs {t2[key]})."})

    xg_diff = t1["xG"] - t2["xG"]
    if xg_diff >= 0.3:
        insights.append({"label": "xG", "tone": "home", "text": f"{team1} crea occasioni di maggior qualita (xG {t1['xG']} vs {t2['xG']})."})
    elif xg_diff <= -0.3:
        insights.append({"label": "xG", "tone": "away", "text": f"{team2} crea occasioni di maggior qualita (xG {t2['xG']} vs {t1['xG']})."})
    else:
        insights.append({"label": "xG", "tone": "neutral", "text": "xG molto simile: partita che si decide nei dettagli."})

    poss_diff = t1["Possesso"] - t2["Possesso"]
    if poss_diff >= 5:
        insights.append({"label": "Possesso", "tone": "home", "text": f"{team1} controlla il pallone ({t1['Possesso']}% vs {t2['Possesso']}%)."})
    elif poss_diff <= -5:
        insights.append({"label": "Possesso", "tone": "away", "text": f"{team2} controlla il pallone ({t2['Possesso']}% vs {t1['Possesso']}%)."})

    overall_diff = abs(t1["OverallRating"] - t2["OverallRating"])
    if overall_diff < 3:
        insights.append({"label": "Gap", "tone": "neutral", "text": "Gap minimo: pronostico apertissimo."})
    elif overall_diff >= 12:
        stronger = team1 if t1["OverallRating"] > t2["OverallRating"] else team2
        tone = "home" if stronger == team1 else "away"
        insights.append({"label": "Gap", "tone": tone, "text": f"{stronger} e favorita su tutti i fronti."})
    return insights


def ratings_map() -> dict[str, dict[str, Any]]:
    return {row["Squadra"]: row.to_dict() for _, row in load_team_stats().iterrows()}


def get_score(ratings: dict[str, dict[str, Any]], team: str, column: str, default: float = 70.0) -> float:
    return as_float(ratings.get(team, {}).get(column), default)


def win_prob(ratings: dict[str, dict[str, Any]], team1: str, team2: str) -> tuple[float, float]:
    s1 = get_score(ratings, team1, "OverallRating") * 0.45 + get_score(ratings, team1, "AttackRating") * 0.30 + get_score(ratings, team1, "DefenseRating") * 0.25
    s2 = get_score(ratings, team2, "OverallRating") * 0.45 + get_score(ratings, team2, "AttackRating") * 0.30 + get_score(ratings, team2, "DefenseRating") * 0.25
    p1 = s1 / (s1 + s2)
    return round(p1 * 100, 1), round((1 - p1) * 100, 1)


def decide_winner(rng: random.Random, ratings: dict[str, dict[str, Any]], team1: str, team2: str) -> str:
    p1, _ = win_prob(ratings, team1, team2)
    result = p1 + rng.gauss(0, 8)
    return team1 if result > 50 else team2


def predict_score(rng: random.Random, ratings: dict[str, dict[str, Any]], team1: str, team2: str, winner: str | None, draw: bool = False) -> tuple[int, int]:
    g1 = int(round(max(0, get_score(ratings, team1, "xG", 1.0) * (get_score(ratings, team1, "AttackRating", 70) / 78) * rng.uniform(0.5, 1.3))))
    g2 = int(round(max(0, get_score(ratings, team2, "xG", 1.0) * (get_score(ratings, team2, "AttackRating", 70) / 78) * rng.uniform(0.5, 1.3))))
    if draw:
        equal = min(g1, g2)
        return equal, equal
    if winner == team1 and g1 <= g2:
        g1 = g2 + 1
    elif winner == team2 and g2 <= g1:
        g2 = g1 + 1
    return g1, g2


def simulate_match_ko(rng: random.Random, ratings: dict[str, dict[str, Any]], team1: str, team2: str) -> dict[str, Any]:
    p1, _ = win_prob(ratings, team1, team2)
    result = p1 + rng.gauss(0, 8)
    penalties = False
    if 47 < result < 53:
        winner = team1 if rng.random() > 0.5 else team2
        g1, g2 = predict_score(rng, ratings, team1, team2, winner=None, draw=True)
        penalties = True
    else:
        winner = team1 if result > 50 else team2
        g1, g2 = predict_score(rng, ratings, team1, team2, winner=winner, draw=False)
    return match_record(team1, team2, g1, g2, winner, penalties)


def match_record(team1: str, team2: str, goals1: int, goals2: int, winner: str | None, penalties: bool = False) -> dict[str, Any]:
    return {
        "team1": team1,
        "team2": team2,
        "goals1": goals1,
        "goals2": goals2,
        "winner": winner,
        "draw": goals1 == goals2 and not penalties,
        "penalties": penalties,
        "team1Flag": flag_url(team1),
        "team2Flag": flag_url(team2),
    }


def simulate_group(rng: random.Random, ratings: dict[str, dict[str, Any]], teams: list[str]) -> dict[str, Any]:
    pts = {team: 0 for team in teams}
    gf = {team: 0 for team in teams}
    ga = {team: 0 for team in teams}
    matches = []

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            team1, team2 = teams[i], teams[j]
            p1, p2 = win_prob(ratings, team1, team2)
            draw_chance = max(0, 0.28 - abs(p1 - p2) * 0.004)
            is_draw = rng.random() < draw_chance
            if is_draw:
                g1, g2 = predict_score(rng, ratings, team1, team2, winner=None, draw=True)
                pts[team1] += 1
                pts[team2] += 1
                winner = None
            else:
                winner = decide_winner(rng, ratings, team1, team2)
                g1, g2 = predict_score(rng, ratings, team1, team2, winner=winner, draw=False)
                pts[winner] += 3
            gf[team1] += g1
            ga[team1] += g2
            gf[team2] += g2
            ga[team2] += g1
            matches.append(match_record(team1, team2, g1, g2, winner))

    standing = sorted(teams, key=lambda team: (pts[team], gf[team] - ga[team], gf[team]), reverse=True)
    standing_records = []
    for index, team in enumerate(standing):
        diff = gf[team] - ga[team]
        standing_records.append(
            {
                "rank": index + 1,
                "team": team,
                "flag": flag_url(team),
                "points": pts[team],
                "goalsFor": gf[team],
                "goalsAgainst": ga[team],
                "goalDiff": diff,
                "qualified": index < 2,
            }
        )
    return {"standing": standing_records, "matches": matches, "raw": {"pts": pts, "gf": gf, "ga": ga}}


def monte_carlo_sim(ratings: dict[str, dict[str, Any]], count: int, base_seed: int) -> dict[str, float]:
    teams = [team for group_teams in GIRONI.values() for team in group_teams]
    wins = {team: 0 for team in teams}

    for index in range(count):
        rng = random.Random(base_seed + index * 31 + 7)
        qualified = []
        thirds = []
        for group_teams in GIRONI.values():
            group = simulate_group(rng, ratings, group_teams)
            standing = [row["team"] for row in group["standing"]]
            raw = group["raw"]
            qualified.extend(standing[:2])
            third = standing[2]
            thirds.append((third, raw["pts"][third], raw["gf"][third] - raw["ga"][third]))

        thirds = sorted(thirds, key=lambda row: (row[1], row[2]), reverse=True)[:8]
        qualified.extend([row[0] for row in thirds])
        rng.shuffle(qualified)
        qualified = qualified[:32]

        current = [(qualified[i], qualified[i + 1]) for i in range(0, len(qualified), 2)]
        while len(current) > 1:
            winners = [simulate_match_ko(rng, ratings, a, b)["winner"] for a, b in current]
            current = [(winners[i], winners[i + 1]) for i in range(0, len(winners), 2)]
        if current:
            champion = simulate_match_ko(rng, ratings, current[0][0], current[0][1])["winner"]
            wins[champion] += 1

    total = max(sum(wins.values()), 1)
    return {team: round(value / total * 100, 1) for team, value in wins.items() if value > 0}


def simulate_tournament(seed: int | None = None, monte_carlo_count: int = 500) -> dict[str, Any]:
    seed = int(seed if seed is not None else random.randint(1, 999_999))
    rng = random.Random(seed)
    ratings = ratings_map()
    qualified: list[str] = []
    thirds = []
    groups = []

    for group_name, teams in GIRONI.items():
        result = simulate_group(rng, ratings, teams)
        groups.append({"group": group_name, "teams": teams, "standing": result["standing"], "matches": result["matches"]})
        standing_names = [row["team"] for row in result["standing"]]
        raw = result["raw"]
        qualified.extend(standing_names[:2])
        third = standing_names[2]
        thirds.append((third, raw["pts"][third], raw["gf"][third] - raw["ga"][third]))

    third_sorted = sorted(thirds, key=lambda row: (row[1], row[2]), reverse=True)[:8]
    qualified.extend([row[0] for row in third_sorted])

    ko_rng = random.Random(seed + 1000)
    ko_rng.shuffle(qualified)
    qualified = qualified[:32]
    current_round = [(qualified[i], qualified[i + 1]) for i in range(0, len(qualified), 2)]
    round_names = ["Sedicesimi", "Ottavi", "Quarti", "Semifinali", "Finale"]
    rounds = []
    champion = None

    for round_name in round_names:
        if not current_round:
            break
        matches = []
        winners = []
        for team1, team2 in current_round:
            match = simulate_match_ko(ko_rng, ratings, team1, team2)
            matches.append(match)
            winners.append(match["winner"])
        rounds.append({"name": round_name, "matches": matches})
        if len(winners) == 1:
            champion = winners[0]
            break
        current_round = [(winners[i], winners[i + 1]) for i in range(0, len(winners), 2)]

    probabilities = monte_carlo_sim(ratings, monte_carlo_count, seed)
    probability_rows = [
        {"team": team, "probability": value, "flag": flag_url(team)}
        for team, value in sorted(probabilities.items(), key=lambda row: row[1], reverse=True)[:12]
    ]

    champion_stats = team_record(champion) if champion else None
    return json_safe(
        {
            "seed": seed,
            "groups": groups,
            "qualified": [{"team": team, "flag": flag_url(team)} for team in qualified],
            "rounds": rounds,
            "champion": champion_stats,
            "monteCarlo": probability_rows,
        }
    )


def fifa_rankings_payload(search: str = "", group: str = "Tutti", chart_group: str | None = None) -> dict[str, Any]:
    df_fifa = pd.DataFrame(FIFA_RANKINGS).sort_values("RankingFIFA").reset_index(drop=True)
    stats = load_team_stats()[["Squadra", "OverallRating", "AttackRating", "MidfieldRating", "DefenseRating"]]
    df = df_fifa.merge(stats, on="Squadra", how="left")
    filtered = df.copy()
    if search:
        filtered = filtered[filtered["Squadra"].str.lower().str.contains(search.lower())]
    if group and group != "Tutti":
        filtered = filtered[filtered["Girone"] == group]

    def enrich(row: pd.Series) -> dict[str, Any]:
        item = json_safe(row.to_dict())
        item["flag"] = flag_url(item["Squadra"])
        return item

    chart_group = chart_group or (group if group != "Tutti" else "A")
    if chart_group not in GIRONI:
        chart_group = "A"
    chart_df = df[df["Girone"] == chart_group].sort_values("Punti", ascending=True)

    return json_safe(
        {
            "items": [enrich(row) for _, row in filtered.iterrows()],
            "top3": [enrich(row) for _, row in df.head(3).iterrows()] if not search and group == "Tutti" else [],
            "chartGroup": chart_group,
            "chart": [enrich(row) for _, row in chart_df.iterrows()],
            "count": int(len(filtered)),
        }
    )
