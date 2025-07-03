from fastapi import FastAPI
from .models import Document, Patient
from .extractor import SimplePatientExtractor

app = FastAPI()
extractor = SimplePatientExtractor()

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the Patient Extractor API!"}


@app.post("/extract_patient", response_model=Patient)
def extract_patient_endpoint(doc: Document) -> Patient:
    """
    Takes a document in JSON format and returns the extracted patient name.
    """
    return extractor.extract(doc)
