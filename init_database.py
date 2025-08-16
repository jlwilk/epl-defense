#!/usr/bin/env python3
"""
Database initialization script for EPL Defense API.
Run this script to create all database tables.
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.db.init_db import init_db, drop_db

def main():
    """Main function to initialize the database."""
    print("🏗️  Initializing EPL Defense Database...")
    
    try:
        # Initialize database
        init_db()
        print("✅ Database initialized successfully!")
        print("📊 Tables created:")
        print("   - League")
        print("   - Team")
        print("   - Venue") 
        print("   - Player")
        print("   - Fixture")
        print("   - FixtureEvent")
        print("   - FixtureLineup")
        print("   - FixtureLineupPlayer")
        print("   - FixtureStatistics")
        
        print("\n🚀 Ready to ingest data!")
        print("   Use: POST /ingestion/epl/2025")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
