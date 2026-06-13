from __future__ import annotations

from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from core import (
    BASE_DIR,
    bootstrap_payload,
    comparison_payload,
    fifa_rankings_payload,
    json_safe,
    prediction_payload,
    simulate_tournament,
)


STATIC_DIR = BASE_DIR / "static"
ASSETS_DIR = BASE_DIR / "assets"


def api_response(data, status_code: int = 200) -> JSONResponse:
    return JSONResponse(json_safe(data), status_code=status_code)


def api_error(message: str, status_code: int = 400) -> JSONResponse:
    return api_response({"error": message}, status_code=status_code)


async def index(_request):
    return FileResponse(STATIC_DIR / "index.html")


async def api_bootstrap(_request):
    return api_response(bootstrap_payload())


async def api_compare(request):
    team1 = request.query_params.get("team1", "Spagna")
    team2 = request.query_params.get("team2", "Francia")
    try:
        return api_response(comparison_payload(team1, team2))
    except (KeyError, ValueError) as exc:
        return api_error(str(exc))


async def api_predict(request):
    team1 = request.query_params.get("team1", "Spagna")
    team2 = request.query_params.get("team2", "Francia")
    try:
        return api_response(prediction_payload(team1, team2))
    except (KeyError, ValueError) as exc:
        return api_error(str(exc))


async def api_simulate(request):
    raw_seed = request.query_params.get("seed")
    try:
        seed = int(raw_seed) if raw_seed else None
    except ValueError:
        return api_error("Seed non valido.")
    return api_response(simulate_tournament(seed=seed))


async def api_rankings(request):
    search = request.query_params.get("search", "")
    group = request.query_params.get("group", "Tutti")
    chart_group = request.query_params.get("chart_group")
    return api_response(fifa_rankings_payload(search=search, group=group, chart_group=chart_group))


routes = [
    Route("/", index),
    Route("/api/bootstrap", api_bootstrap),
    Route("/api/compare", api_compare),
    Route("/api/predict", api_predict),
    Route("/api/simulate", api_simulate),
    Route("/api/rankings", api_rankings),
    Mount("/static", StaticFiles(directory=STATIC_DIR), name="static"),
    Mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets"),
    Route("/{path:path}", index),
]

app = Starlette(debug=False, routes=routes)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
