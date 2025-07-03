from fastapi import FastAPI
from .models import Document, Patient
from .extractor import SimplePatientExtractor

app = FastAPI()
extractor = SimplePatientExtractor()  # Tu instancies ta logique ici


@app.post("/extract_patient", response_model=Patient)
def extract_patient_endpoint(doc: Document) -> Patient:
    """
    Takes a document in JSON format and returns the extracted patient name.
    """
    return extractor.extract(doc)
