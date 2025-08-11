EPL Defense
===========

English Premier League stats app using API-Football v3 with aggressive caching to stay within 100 requests/day.

Docs: [API-Football v3](https://www.api-football.com/documentation-v3)

Quick start
-----------

1. Create a virtual environment and install:

```
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

2. Create `.env`:

```
APIFOOTBALL_API_KEY=your_key_here
APIFOOTBALL_BASE_URL=https://v3.football.api-sports.io
CACHE_NAME=.cache/epl_cache
CACHE_EXPIRE=86400
```

3. Try the CLI:

```
epl health
epl leagues
epl standings --season 2024 --league 39
```

Caching
-------

- Transparent HTTP caching via `requests-cache` with per-endpoint TTLs
- Daily budget guard (100 requests/day) with timestamps and burst safety
- Warmup script to prefetch common EPL endpoints




