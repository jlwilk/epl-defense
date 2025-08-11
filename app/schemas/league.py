from __future__ import annotations

from pydantic import BaseModel


class LeagueOut(BaseModel):
    id: int
    name: str
    type: str | None = None
    country: str | None = None

    model_config = {"from_attributes": True}


