#!/usr/bin/env python3
"""
CLI script to sync player data from API-Football to local database.
"""

import sys
import os
import argparse

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.db.session import get_db
from app.services.player_sync_service import PlayerSyncService


def main():
    """Main function to sync player data."""
    parser = argparse.ArgumentParser(description="Sync player data from API-Football")
    parser.add_argument("--league", type=int, help="League ID to sync")
    parser.add_argument("--team", type=int, help="Team ID to sync")
    parser.add_argument("--season", type=int, help="Season year (defaults to environment setting)")
    parser.add_argument("--force", action="store_true", help="Force sync even if data exists")
    
    args = parser.parse_args()
    
    if not args.league and not args.team:
        print("❌ Error: Must specify either --league or --team")
        sys.exit(1)
    
    try:
        db = next(get_db())
        sync_service = PlayerSyncService()
        
        if args.league:
            print(f"🔄 Syncing players for league {args.league}, season {args.season or 'default'}")
            result = sync_service.sync_league_players(args.league, args.season, db)
        else:
            print(f"🔄 Syncing players for team {args.team}, season {args.season or 'default'}")
            result = sync_service.sync_team_players(args.team, args.season, None, db)
        
        if result["success"]:
            print("✅ Sync completed successfully!")
            print(f"📊 Results:")
            print(f"   Total players: {result['total_players']}")
            print(f"   New players: {result['new_players']}")
            print(f"   Updated players: {result['updated_players']}")
            print(f"   Errors: {result['errors']}")
        else:
            print(f"❌ Sync failed: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error during sync: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
