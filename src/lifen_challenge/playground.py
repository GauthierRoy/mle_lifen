from .models import Document, Patient
from .extractor import SimplePatientExtractor
import json

json_docs_example_with_keyword = """
{"pages":[{"words":[{"text":"Patient:","bbox":{"x_min":0.2,"x_max":0.25,"y_min":0.09,"y_max":0.1}},{"text":"Jean","bbox":{"x_min":0.44,"x_max":0.48,"y_min":0.09,"y_max":0.1}},{"text":"DUPONT","bbox":{"x_min":0.49,"x_max":0.57,"y_min":0.09,"y_max":0.1}},{"text":"Docteur","bbox":{"x_min":0.6,"x_max":0.67,"y_min":0.16,"y_max":0.17}},{"text":"Nicolas","bbox":{"x_min":0.67,"x_max":0.73,"y_min":0.16,"y_max":0.17}}]}],"original_page_count":1,"needs_ocr_case":"no_ocr"}
"""
document_object = Document.model_validate_json(json_docs_example_with_keyword)
print(document_object)
extractor = SimplePatientExtractor()

# Example usage of the extractor
patient = extractor.extract(document_object)
# steps
lines = extractor._reconstruct_lines(document_object)
print(lines)
