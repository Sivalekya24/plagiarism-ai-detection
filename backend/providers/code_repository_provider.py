import os

from services.extraction_service import TextExtractor


class CodeRepositoryProvider:

    REPOSITORY_FOLDER = "code_repository"

    def __init__(self):

        os.makedirs(self.REPOSITORY_FOLDER, exist_ok=True)

    def extract(self, path):

        return TextExtractor.extract_text(path)

    def get_all_documents(self):

        documents = []

        for file in os.listdir(self.REPOSITORY_FOLDER):

            path = os.path.join(self.REPOSITORY_FOLDER, file)

            if os.path.isfile(path):

                documents.append({

                    "name": file,

                    "path": path

                })

        return documents