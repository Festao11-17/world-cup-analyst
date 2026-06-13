# World Cup Analyst

Dashboard web per analisi, confronto squadre, predizioni match, simulazione torneo e ranking FIFA del Mondiale 2026.

## Avvio locale

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Apri `http://127.0.0.1:8000`.

## Deploy online

L'app e pronta per piattaforme Python ASGI come Render, Railway, Fly.io o Heroku-compatible.

Start command:

```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

Nel repository sono presenti:

- `Procfile` per piattaforme Heroku-compatible.
- `render.yaml` per deploy Render Blueprint.
- `requirements.txt` senza Streamlit.
