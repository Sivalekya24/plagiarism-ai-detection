import os
import shutil


class StorageProvider:

    def __init__(self):

        self.repository = "database/documents"

        os.makedirs(self.repository, exist_ok=True)

    def save_document(self, uploaded_file_path):

        destination = os.path.join(

            self.repository,

            os.path.basename(uploaded_file_path)

        )

        if os.path.abspath(uploaded_file_path) != os.path.abspath(destination):

            shutil.copy2(

                uploaded_file_path,

                destination

            )

        return destination