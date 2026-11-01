from __future__ import annotations

import re
from pydantic import BaseModel, Field, field_validator


class Palette(BaseModel):
    id: str | None = None
    name: str | None = None
    body: str
    corner: str
    ink: str
    accent: str
    scene: str | None
    blush: str
    fluid: str
    panel: str

    @field_validator('body', 'corner', 'ink', 'accent', 'scene', 'blush', 'fluid', 'panel')
    @classmethod
    def color(cls, value):
        if value is not None and not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
            raise ValueError('Color must be six-digit hex')
        return value.upper() if value else value


class State(BaseModel):
    expression: str
    decorations: list[str] = Field(default_factory=list, max_length=11)
    palette: Palette
