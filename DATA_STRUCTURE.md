# World Cup Analyst — Struttura Progetto

## Struttura Cartelle

```
world-cup-analyst/
├── app.py
├── update_data.py
├── requirements.txt
├── README.md
├── DATA_STRUCTURE.md
│
├── pages/
│   ├── 1_Team_Comparison.py
│   ├── 2_Player_Comparison.py
│   ├── 3_Match_Predictions.py
│   ├── 4_Nazionali.py
│   ├── 5_Player_Scouting.py
│   ├── 6_Player_Profile.py
│   ├── 7_Team_Profile.py
│   ├── 8_Power_Rankings.py
│   ├── 9_WC_Simulator.py
│   └── 10_Admin_Update.py
│
├── data/
│   ├── team_stats.csv
│   ├── world_cup_players.csv
│   ├── raw/                   ← creata automaticamente da update_data.py
│   └── processed/             ← creata automaticamente da update_data.py
│
└── assets/
    ├── logo.png
    ├── style.css
    └── flags/
        ├── Girone_A/  → Cechia, Corea_del_Sud, Messico, Sudafrica
        ├── Girone_B/  → Bosnia_ed_Erzegovina, Canada, Qatar, Svizzera
        ├── Girone_C/  → Brasile, Haiti, Marocco, Scozia
        ├── Girone_D/  → Australia, Paraguay, Stati_Uniti, Turchia
        ├── Girone_E/  → Costa_d'Avorio, Curacao, Ecuador, Germania
        ├── Girone_F/  → Giappone, Olanda, Svezia, Tunisia
        ├── Girone_G/  → Belgio, Egitto, Iran, Nuova_Zelanda
        ├── Girone_H/  → Arabia_Saudita, Capo_Verde, Spagna, Uruguay
        ├── Girone_I/  → Francia, Iraq, Norvegia, Senegal
        ├── Girone_J/  → Algeria, Argentina, Austria, Giordania
        ├── Girone_K/  → Colombia, Portogallo, Repubblica_del_Congo, Uzbekistan
        └── Girone_L/  → Croazia, Ghana, Inghilterra, Panama
```

## Aggiornamento Dati

### Via script (terminale)
```bash
# Update completo
python update_data.py --api-key TUA_KEY

# Solo team stats
python update_data.py --api-key TUA_KEY --teams-only

# Dry run — testa senza sovrascrivere
python update_data.py --api-key TUA_KEY --dry-run
```

### Via pagina Admin nell'app
1. Vai su `⚙️ Admin — Update Data`
2. Inserisci la password admin
3. Inserisci la API key
4. Clicca **Avvia Update**

### Upload manuale CSV
Nella pagina Admin puoi caricare CSV aggiornati manualmente.
I Power Rating vengono ricalcolati automaticamente al salvataggio.

## Secrets (Streamlit Cloud)

Vai su **Manage app → Settings → Secrets** e aggiungi:

```toml
FOOTBALL_API_KEY = "la_tua_api_key"
ADMIN_PASSWORD   = "scegli_password_sicura"
```

## Note Importanti

- I file PNG delle bandiere hanno la **prima lettera maiuscola** (es. `Brasile.png`)
- Il FLAG_MAP nei file Python usa lo stesso formato esatto