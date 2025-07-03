# src/lifen_challenge/models.py

from pydantic import BaseModel
from typing import List


class BBox(BaseModel):
    x_min: float
    x_max: float
    y_min: float
    y_max: float


class Word(BaseModel):
    text: str
    bbox: BBox


class Page(BaseModel):
    words: List[Word]


class Document(BaseModel):
    pages: List[Page]


class Patient(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
