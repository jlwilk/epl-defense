from __future__ import annotations

import json
from typing import Optional

import typer
from rich import print
from rich.table import Table

from .api_client import ApiClient, EPL_LEAGUE_ID

app = typer.Typer(add_completion=False, help="EPL stats CLI with caching")


def main() -> None:
    app()


@app.command()
def health() -> None:
    client = ApiClient.from_env()
    data = client.health()
    print({"remaining": client.budget.remaining(), "status": data.get("response")})


@app.command()
def leagues() -> None:
    client = ApiClient.from_env()
    data = client.leagues()
    print({"count": data.get("results"), "sample": data.get("response", [])[:3]})


@app.command()
def standings(season: int = typer.Option(..., help="Season year, e.g. 2024"),
              league: int = typer.Option(EPL_LEAGUE_ID, help="League id, EPL=39")) -> None:
    client = ApiClient.from_env()
    data = client.standings(league=league, season=season)
    # Pretty print keys we care about
    resp = data.get("response", [])
    print(json.dumps(resp[:1], indent=2))


@app.command()
def warmup(season: int = typer.Option(2024, help="Season for EPL"),
           league: int = typer.Option(EPL_LEAGUE_ID, help="League id, EPL=39"),
           limit: int = typer.Option(50, help="Max requests to spend now")) -> None:
    """Prefetch common endpoints to populate cache while respecting budget."""
    client = ApiClient.from_env()
    remaining = client.budget.remaining()
    to_use = min(limit, remaining)
    if to_use <= 0:
        print("No remaining budget to warmup cache")
        raise typer.Exit(code=0)

    # Strategy: spend up to 'to_use' sequential GETs; requests served from cache won't count
    calls = 0
    def safe_call(fn):
        nonlocal calls
        try:
            fn()
            calls += 1
        except Exception as e:
            print(f"skip: {e}")

    # 1. Standings
    safe_call(lambda: client.standings(league=league, season=season))

    # 2. Teams in league-season
    safe_call(lambda: client.teams(league=league, season=season))

    # 3. Recent fixtures in season for EPL
    safe_call(lambda: client.fixtures(league=league, season=season, last=50))

    print({"spent": calls, "remaining": client.budget.remaining()})


@app.command()
def defense_table(season: int = typer.Option(..., help="Season year, e.g. 2024"),
                  league: int = typer.Option(EPL_LEAGUE_ID, help="League id, EPL=39")) -> None:
    """Show goals conceded totals per team using teams/statistics, cached."""
    client = ApiClient.from_env()
    teams_resp = client.teams(league=league, season=season)
    teams = teams_resp.get("response", [])
    table = Table(title=f"EPL {season} Defense (Goals Conceded)")
    table.add_column("Team")
    table.add_column("Conceded")
    for t in teams:
        team_id = t.get("team", {}).get("id")
        name = t.get("team", {}).get("name") or str(team_id)
        if not team_id:
            continue
        stats = client.team_statistics(league=league, season=season, team=team_id)
        # Path per docs: response.goals.against.total.total (all matches)
        conceded = None
        try:
            conceded = (
                stats.get("response", {})
                .get("goals", {})
                .get("against", {})
                .get("total", {})
                .get("total")
            )
        except Exception:
            conceded = None
        table.add_row(name, str(conceded) if conceded is not None else "-")
    print(table)




