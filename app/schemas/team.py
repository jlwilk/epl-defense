from __future__ import annotations

from pydantic import BaseModel


class TeamOut(BaseModel):
    id: int
    name: str
    code: str | None = None
    country: str | None = None

    model_config = {"from_attributes": True}


