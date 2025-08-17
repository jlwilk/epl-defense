from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query

from app.config import get_settings
from app.services.api_client import ApiClientV3

router = APIRouter(prefix="/fixtures", tags=["fixtures"])


@router.get("/")
def list_fixtures(
    season: int = Query(None, description="Season year (defaults to 2025)"),
    league: int | None = Query(None, description="League id; defaults to settings.LEAGUE_ID"),
    team: int | None = Query(None, description="Team ID to filter fixtures"),
    last: int | None = Query(None, description="Return last N fixtures"),
    next: int | None = Query(None, description="Return next N fixtures"),
    from_date: str | None = Query(None, description="From date (YYYY-MM-DD)"),
    to_date: str | None = Query(None, description="To date (YYYY-MM-DD)"),
    round: str | None = Query(None, description="Round of the season"),
    status: str | None = Query(None, description="Fixture status (TBD, NS, 1H, HT, 2H, FT, AET, PEN, BT, SUSP, INT, PST, CANC, ABD, AWD, WO)"),
) -> Dict[str, Any]:
    """Get fixtures with comprehensive filtering options."""
    settings = get_settings()
    league_id = league or settings.league_id_default
    season_id = season or settings.season_default
    
    # API requires at least one parameter, so we'll always include season and league
    params: Dict[str, Any] = {
        "season": season_id,
        "league": league_id
    }
    
    if team:
        params["team"] = team
    if last:
        params["last"] = last
    if next:
        params["next"] = next
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if round:
        params["round"] = round
    if status:
        params["status"] = status
        
    try:
        client = ApiClientV3()
        data = client.get("/fixtures", params=params)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{fixture_id}/players")
def get_fixture_player_stats(fixture_id: int) -> Dict[str, Any]:
    """Get player statistics for a specific fixture.
    
    This endpoint provides detailed statistics for each player in a fixture,
    including goals, assists, cards, shots, passes, tackles, and other performance metrics.
    """
    try:
        client = ApiClientV3()
        data = client.get_fixture_players(fixture_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{fixture_id}/players/stored")
def get_stored_fixture_player_stats(fixture_id: int) -> Dict[str, Any]:
    """Get stored fixture player statistics from the local database.
    
    This endpoint returns player statistics that have been ingested and stored locally,
    providing faster access to historical data without hitting the external API.
    """
    try:
        from app.db.session import SessionLocal
        from app.models import FixturePlayerStats
        from sqlalchemy.orm import Session
        
        db: Session = SessionLocal()
        
        # Get all player stats for this fixture
        player_stats = db.query(FixturePlayerStats).filter(
            FixturePlayerStats.fixture_id == fixture_id
        ).all()
        
        if not player_stats:
            return {
                "fixture_id": fixture_id,
                "message": "No player statistics found for this fixture",
                "player_stats": []
            }
        
        # Group by team
        team_stats = {}
        for stat in player_stats:
            team_id = stat.team_id
            if team_id not in team_stats:
                team_stats[team_id] = []
            
            team_stats[team_id].append({
                "player_id": stat.player_id,
                "position": stat.position,
                "number": stat.number,
                "is_starter": stat.is_starter,
                "minutes": stat.minutes,
                "rating": stat.rating,
                "goals": stat.goals,
                "assists": stat.assists,
                "penalty_goals": stat.penalty_goals,
                "penalty_missed": stat.penalty_missed,
                "yellow_cards": stat.yellow_cards,
                "red_cards": stat.red_cards,
                "shots_total": stat.shots_total,
                "shots_on_target": stat.shots_on_target,
                "passes_total": stat.passes_total,
                "passes_accuracy": stat.passes_accuracy,
                "key_passes": stat.key_passes,
                "tackles_total": stat.tackles_total,
                "blocks_total": stat.blocks_total,
                "interceptions_total": stat.interceptions_total,
                "duels_total": stat.duels_total,
                "duels_won": stat.duels_won,
                "dribbles_attempts": stat.dribbles_attempts,
                "dribbles_success": stat.dribbles_success,
                "fouls_drawn": stat.fouls_drawn,
                "fouls_committed": stat.fouls_committed,
                "saves": stat.saves,
                "goals_conceded": stat.goals_conceded,
                "clean_sheets": stat.clean_sheets
            })
        
        return {
            "fixture_id": fixture_id,
            "total_players": len(player_stats),
            "teams": team_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if 'db' in locals():
            db.close()


@router.get("/live")
def get_live_fixtures(
    league: int | None = Query(None, description="League ID to filter live fixtures"),
) -> Dict[str, Any]:
    """Get all currently live fixtures."""
    try:
        client = ApiClientV3()
        settings = get_settings()
        
        # API requires BOTH season AND league parameters together
        params: Dict[str, Any] = {
            "season": settings.season_default,
            "league": league or settings.league_id_default
        }
            
        data = client.get("/fixtures", params=params)
        
        # Filter to only live fixtures from the response
        if data.get("response"):
            live_fixtures = [
                fixture for fixture in data["response"] 
                if fixture.get("fixture", {}).get("status", {}).get("short") in ["1H", "HT", "2H", "ET", "P", "BT"]
            ]
            data["response"] = live_fixtures
            data["results"] = len(live_fixtures)
        
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/head-to-head")
def get_head_to_head(
    h2h: str = Query(..., description="Two team IDs separated by '-' (e.g., '42-50')"),
    season: int = Query(None, description="Season year (defaults to 2025)"),
    last: int | None = Query(None, description="Return last N fixtures"),
) -> Dict[str, Any]:
    """Get head-to-head fixtures between two teams."""
    settings = get_settings()
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        params: Dict[str, Any] = {"h2h": h2h}
        if season_id:
            params["season"] = season_id
        if last:
            params["last"] = last
            
        data = client.get("/fixtures/headtohead", params=params)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/rounds")
def get_fixture_rounds(
    league: int = Query(..., description="League ID"),
    season: int = Query(None, description="Season year (defaults to 2025)"),
    current: bool | None = Query(None, description="Get current round only"),
) -> Dict[str, Any]:
    """Get all rounds for a league/season."""
    settings = get_settings()
    season_id = season or settings.season_default
    try:
        client = ApiClientV3()
        params: Dict[str, Any] = {"league": league}
        if season_id:
            params["season"] = season_id
        if current is not None:
            params["current"] = current
            
        data = client.get("/fixtures/rounds", params=params)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/date/{date}")
def get_fixtures_by_date(
    date: str,
    league: int | None = Query(None, description="League ID to filter"),
    season: int | None = Query(None, description="Season year"),
) -> Dict[str, Any]:
    """Get all fixtures for a specific date."""
    try:
        client = ApiClientV3()
        params: Dict[str, Any] = {"date": date}
        if league:
            params["league"] = league
        if season:
            params["season"] = season
            
        data = client.get("/fixtures", params=params)
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/league/{league_id}/season/{season_id}/round/{round}")
def get_round_fixtures(
    league_id: int,
    season_id: int,
    round: str,
) -> Dict[str, Any]:
    """Get all fixtures for a specific round in a league/season."""
    try:
        client = ApiClientV3()
        data = client.get("/fixtures", params={
            "league": league_id,
            "season": season_id,
            "round": round
        })
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/team/{team_id}/form")
def get_team_form(
    team_id: int,
    season: int = Query(None, description="Season year (defaults to 2025)"),
    league: int | None = Query(None, description="League ID"),
    last: int = Query(5, description="Number of recent fixtures to analyze"),
) -> Dict[str, Any]:
    """Get team form based on recent fixtures."""
    settings = get_settings()
    season_id = season or settings.season_default
    league_id = league or settings.league_id_default
    try:
        client = ApiClientV3()
        data = client.get("/fixtures", params={
            "team": team_id,
            "season": season_id,
            "league": league_id,
            "last": last
        })
        
        # Analyze form from recent fixtures
        fixtures = data.get("response", [])
        form_analysis = {
            "team_id": team_id,
            "season": season_id,
            "league": league_id,
            "last_n_fixtures": last,
            "fixtures": fixtures,
            "form_summary": {
                "total": len(fixtures),
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0
            }
        }
        
        # Calculate form statistics
        for fixture in fixtures:
            if fixture.get("goals") and fixture.get("goals").get("home") and fixture.get("goals").get("away"):
                home_goals = fixture["goals"]["home"]
                away_goals = fixture["goals"]["away"]
                
                if fixture["teams"]["home"]["id"] == team_id:
                    # Team is home
                    form_analysis["form_summary"]["goals_for"] += home_goals
                    form_analysis["form_summary"]["goals_against"] += away_goals
                    if home_goals > away_goals:
                        form_analysis["form_summary"]["wins"] += 1
                    elif home_goals == away_goals:
                        form_analysis["form_summary"]["draws"] += 1
                    else:
                        form_analysis["form_summary"]["losses"] += 1
                else:
                    # Team is away
                    form_analysis["form_summary"]["goals_for"] += away_goals
                    form_analysis["form_summary"]["goals_against"] += home_goals
                    if away_goals > home_goals:
                        form_analysis["form_summary"]["wins"] += 1
                    elif away_goals == home_goals:
                        form_analysis["form_summary"]["draws"] += 1
                    else:
                        form_analysis["form_summary"]["losses"] += 1
        
        return form_analysis
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


# Dynamic routes must come after specific paths
@router.get("/{fixture_id}")
def get_fixture(fixture_id: int) -> Dict[str, Any]:
    """Get detailed information about a specific fixture."""
    try:
        client = ApiClientV3()
        data = client.get("/fixtures", params={"id": fixture_id})
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{fixture_id}/events")
def get_fixture_events(fixture_id: int) -> Dict[str, Any]:
    """Get all events for a specific fixture (goals, cards, substitutions, etc.)."""
    try:
        client = ApiClientV3()
        data = client.get("/fixtures/events", params={"fixture": fixture_id})
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{fixture_id}/lineups")
def get_fixture_lineups(fixture_id: int) -> Dict[str, Any]:
    """Get lineups for both teams in a specific fixture."""
    try:
        client = ApiClientV3()
        data = client.get("/fixtures/lineups", params={"fixture": fixture_id})
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{fixture_id}/players")
def get_fixture_players(fixture_id: int) -> Dict[str, Any]:
    """Get player statistics for a specific fixture."""
    try:
        client = ApiClientV3()
        data = client.get("/fixtures/players", params={"fixture": fixture_id})
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{fixture_id}/statistics")
def get_fixture_statistics(fixture_id: int) -> Dict[str, Any]:
    """Get team statistics for a specific fixture."""
    try:
        client = ApiClientV3()
        data = client.get("/fixtures/statistics", params={"fixture": fixture_id})
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


