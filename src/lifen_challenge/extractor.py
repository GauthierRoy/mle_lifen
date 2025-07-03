# src/lifen_challenge/extractor.py

from typing import List
from .models import Document, Patient, Word


class SimplePatientExtractor:
    """
    Extracts a patient's name using the simplest possible heuristic.
    """

    PATIENT_KEYWORDS = ["patient", "nom", "prénom"]

    def extract(self, doc: Document) -> Patient:
        """
        Main extraction method. It reconstructs lines and applies the keyword-based
        heuristic to return the first patient's name found.

        Args:
            doc: A Document object containing words and their coordinates.

        Returns:
            A Patient object, which will be empty if no name is found.
        """
        lines_of_words = self._reconstruct_lines(doc)

        for line in lines_of_words:
            # check if any keyword is in the line
            for i, word in enumerate(line):
                if word.text.lower().strip(":") in self.PATIENT_KEYWORDS:
                    # keyword found, extract the name after this index
                    patient = self._extract_name_after_index(line, i)
                    if patient.first_name or patient.last_name:
                        return patient  # return the first name found in the document

        return Patient()  # empty Patient object if no name is found

    def _reconstruct_lines(
        self, doc: Document, y_tolerance: float = 0.01
    ) -> List[List[Word]]:
        """
        Reconstructs lines of words from the document by grouping words that are vertically aligned within a tolerance.

        Args:
            doc: The document to process.
            y_tolerance: The vertical tolerance for words on the same line.

        Returns:
            A list of lines, where each line is a list of Word objects.
        """
        all_words = [word for page in doc.pages for word in page.words]
        if not all_words:
            return []

        # sort top-to-bottom, then left-to-right
        all_words.sort(key=lambda w: (w.bbox.y_min, w.bbox.x_min))

        lines = []
        current_line = [all_words[0]]
        for word in all_words[1:]:
            # group words if their vertical positions are similar to first word y
            if abs(word.bbox.y_min - current_line[0].bbox.y_min) < y_tolerance:
                current_line.append(word)
            else:
                lines.append(current_line)
                current_line = [word]
        lines.append(current_line)  # add last line

        return lines

    def _extract_name_after_index(
        self, line_words: List[Word], keyword_index: int
    ) -> Patient:
        """
        Given a line and the index of a keyword, extracts the subsequent
        capitalized words as the patient's name.

        Args:
            line_words: A list of Word objects for a single line.
            keyword_index: The index of the keyword within the line.

        Returns:
            A Patient object with the extracted names.
        """
        potential_name_parts = []
        # look at words after the keyword
        for word in line_words[keyword_index + 1 :]:
            # A "name part" is capitalized and contains letters.
            if word.text.istitle() or word.text.isupper():
                potential_name_parts.append(word.text.strip(".,;:"))

        if not potential_name_parts:
            return Patient()
        if len(potential_name_parts) == 1:
            return Patient(last_name=potential_name_parts[0])
        else:
            # Assume first part is first name, second is last name.
            return Patient(
                first_name=potential_name_parts[0],
                last_name=potential_name_parts[1],
            )
