# tests/test_extractor.py

import pytest
from src.lifen_challenge.models import Document, Patient, Word, BBox, Page
from src.lifen_challenge.extractor import SimplePatientExtractor


# A pytest fixture makes it easy to reuse the extractor instance
@pytest.fixture
def extractor():
    return SimplePatientExtractor()


def test_extract_patient_with_keyword(extractor):
    """
    Tests the happy path: a patient name is found next to a keyword.
    """
    # Create a mock document object that simulates the "Hugo Victor" case
    doc = Document(
        pages=[
            Page(
                words=[
                    Word(
                        text="Patient:",
                        bbox=BBox(x_min=0.1, x_max=0.2, y_min=0.1, y_max=0.2),
                    ),
                    Word(
                        text="Hugo",
                        bbox=BBox(x_min=0.2, x_max=0.3, y_min=0.1, y_max=0.2),
                    ),
                    Word(
                        text="Victor",
                        bbox=BBox(x_min=0.3, x_max=0.4, y_min=0.1, y_max=0.2),
                    ),
                ]
            )
        ]
    )

    expected_patient = Patient(first_name="Hugo", last_name="Victor")
    result = extractor.extract(doc)

    assert result == expected_patient


def test_no_patient_found_without_keyword(extractor):
    """
    Tests the graceful failure path: no keyword is present.
    """
    # Create a mock document object that simulates the "Juliette Martin" case
    doc = Document(
        pages=[
            Page(
                words=[
                    Word(
                        text="JULIETTE",
                        bbox=BBox(x_min=0.1, x_max=0.2, y_min=0.1, y_max=0.2),
                    ),
                    Word(
                        text="MARTIN",
                        bbox=BBox(x_min=0.2, x_max=0.3, y_min=0.1, y_max=0.2),
                    ),
                    Word(
                        text="Docteur",
                        bbox=BBox(x_min=0.1, x_max=0.2, y_min=0.2, y_max=0.3),
                    ),
                    Word(
                        text="Nicolas",
                        bbox=BBox(x_min=0.2, x_max=0.3, y_min=0.2, y_max=0.3),
                    ),
                ]
            )
        ]
    )

    # The heuristic should fail and return an empty Patient object
    expected_patient = Patient()
    result = extractor.extract(doc)

    assert result == expected_patient


def test_extract_with_empty_document(extractor):
    """
    Tests the edge case of an empty document.
    """
    doc = Document(pages=[])

    expected_patient = Patient()
    result = extractor.extract(doc)

    assert result == expected_patient
