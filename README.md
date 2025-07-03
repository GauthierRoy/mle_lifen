# Lifen Machine Learning Engineer Challenge - Patient Name Extraction

This repository contains a solution for Part A.1 of the Lifen ML Engineer challenge. It implements a simple, rule-based heuristic to extract a patient's name from a medical document and serves it via a minimal FastAPI web service.

## Setup

This project uses Poetry for dependency management.

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```

## Usage

### Running the Web Server

To start the FastAPI server, run the following command from the project's root directory:

```bash
poetry run uvicorn src.lifen_challenge.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

You can access the interactive API documentation at `http://127.0.0.1:8000/docs` to test the endpoint.

### Running Tests

The project includes both unit and integration tests. To run the full test suite:

```bash
poetry run python -m pytest tests
```

## Future Improvements

This baseline solution is intentionally simple. Several improvements could be made to handle more complex documents and increase accuracy.

### 1. Heuristic & Logic Improvements

The core extraction logic can be enhanced by combining multiple rules:

*   **Exclusion Logic:** Create a list of "negative keywords" (e.g., `Dr`, `Docteur`, `Gynécologue`, `Chirurgienne`). If a potential name is preceded by one of these words, it should be disqualified as a patient. This would correctly handle cases where doctor names are present.

*   **Positional Logic:** Use the bbox coordinates to infer the role of a name based on its location. A common pattern is for the patient's name to be in the top-left or top-center of the document (the recipient block of a letter)

*   **Heuristic Scoring System:** Move from a single-pass system to a scoring model. Different rules would contribute points to potential candidates:
    *   Name follows `Patient:` keyword: +10 points
    *   Name found in top-left quadrant of the page: +5 points
    *   Name is not preceded by a medical title: +2 points
    The system would then select the candidate with the highest score, making the logic more robust to varied document layouts.

*   **Configuration Management:** Instead of hard-coding keywords (`patient`, `nom`, etc.) in the source code, move them to a configuration file (e.g., `config.yaml`). This makes it easier to update the logic without changing the code.

### 2. Operational & Production Improvements

*   **Containerization:** Package the application using **Docker**. This ensures a consistent and reproducible environment for deployment, simplifying the setup process and eliminating "it works on my machine" issues.

*   **Logging and Monitoring:** Implement structured logging. For each request, log the input document's identifier and the extracted name. By logging cases where the heuristic fails (returns an empty name), we can collect a dataset of difficult examples to guide future heuristic improvements.
