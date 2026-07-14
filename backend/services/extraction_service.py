import os
import pdfplumber
from docx import Document


class TextExtractor:

    @staticmethod
    def extract_text(file_path: str) -> str:

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return TextExtractor.extract_pdf(file_path)

        elif extension == ".docx":
            return TextExtractor.extract_docx(file_path)

        elif extension == ".txt":
            return TextExtractor.extract_txt(file_path)

        elif extension in [".py", ".java", ".js", ".c", ".cpp"]:
            return TextExtractor.extract_code(file_path)

        else:
            raise ValueError(f"Unsupported file format: {extension}")


    @staticmethod
    def extract_pdf(file_path):

        text = ""

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text


    @staticmethod
    def extract_docx(file_path):

        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )


    @staticmethod
    def extract_txt(file_path):

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

            return file.read()


    @staticmethod
    def extract_code(file_path):

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

            return file.read()