# tests/test_main.py

from fastapi.testclient import TestClient
from src.lifen_challenge.main import app

client = TestClient(app)


def test_extract_patient_endpoint_success():
    """
    This tests the full flow from HTTP request to HTTP response.
    """
    test_document_json = {
        "pages": [
            {
                "words": [
                    {
                        "text": "Patient:",
                        "bbox": {
                            "x_min": 0.1,
                            "x_max": 0.2,
                            "y_min": 0.1,
                            "y_max": 0.2,
                        },
                    },
                    {
                        "text": "Hugo",
                        "bbox": {
                            "x_min": 0.2,
                            "x_max": 0.3,
                            "y_min": 0.1,
                            "y_max": 0.2,
                        },
                    },
                    {
                        "text": "Victor",
                        "bbox": {
                            "x_min": 0.3,
                            "x_max": 0.4,
                            "y_min": 0.1,
                            "y_max": 0.2,
                        },
                    },
                ]
            }
        ]
    }

    # The expected JSON response from the server
    expected_response_json = {"first_name": "Hugo", "last_name": "Victor"}

    response = client.post("/extract_patient", json=test_document_json)

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_response_json


def test_extract_patient_endpoint_no_keyword():
    """
    Integration test for a case where no patient should be found.
    """
    test_document_json = {
        "pages": [
            {
                "words": [
                    {
                        "text": "Some",
                        "bbox": {
                            "x_min": 0.1,
                            "x_max": 0.2,
                            "y_min": 0.1,
                            "y_max": 0.2,
                        },
                    },
                    {
                        "text": "random",
                        "bbox": {
                            "x_min": 0.2,
                            "x_max": 0.3,
                            "y_min": 0.1,
                            "y_max": 0.2,
                        },
                    },
                    {
                        "text": "text",
                        "bbox": {
                            "x_min": 0.3,
                            "x_max": 0.4,
                            "y_min": 0.1,
                            "y_max": 0.2,
                        },
                    },
                ]
            }
        ]
    }

    expected_response_json = {"first_name": None, "last_name": None}

    response = client.post("/extract_patient", json=test_document_json)

    assert response.status_code == 200
    assert response.json() == expected_response_json
