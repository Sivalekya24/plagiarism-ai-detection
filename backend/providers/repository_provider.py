import os
from datetime import datetime

from services.extraction_service import TextExtractor


class RepositoryProvider:

    def __init__(self):

        self.repository_path = "database/documents"

        os.makedirs(self.repository_path, exist_ok=True)

    def get_all_documents(self):

        documents = []

        for file in os.listdir(self.repository_path):

            path = os.path.join(self.repository_path, file)

            if os.path.isfile(path):

                documents.append({

                    "filename": file,

                    "path": path,

                    "uploadedAt": datetime.fromtimestamp(
                        os.path.getmtime(path)
                    ).strftime("%Y-%m-%d %H:%M"),

                    "sizeKb": round(
                        os.path.getsize(path) / 1024,
                        2
                    )

                })

        return documents

    def extract(self, path):

        return TextExtractor.extract_text(path)