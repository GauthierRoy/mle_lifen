# src/lifen_challenge/models.py

from pydantic import BaseModel, ConfigDict
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

DOCUMENT_EXAMPLE = {
    "pages": [
        {
            "words": [
                {
                    "text": "Patient:",
                    "bbox": {"x_min": 0.1, "x_max": 0.2, "y_min": 0.1, "y_max": 0.2},
                },
                {
                    "text": "Hugo",
                    "bbox": {"x_min": 0.2, "x_max": 0.3, "y_min": 0.1, "y_max": 0.2},
                },
                {
                    "text": "Victor",
                    "bbox": {"x_min": 0.3, "x_max": 0.4, "y_min": 0.1, "y_max": 0.2},
                },
            ]
        }
    ]
}

class Document(BaseModel):
    pages: List[Page]
    model_config = ConfigDict(json_schema_extra={"example": DOCUMENT_EXAMPLE})# type: ignore


class Patient(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
