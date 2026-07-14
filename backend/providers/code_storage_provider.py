import os
import shutil


class CodeStorageProvider:

    REPOSITORY_FOLDER = "code_repository"

    def __init__(self):

        os.makedirs(self.REPOSITORY_FOLDER, exist_ok=True)

    def save(self, uploaded_file):

        filename = os.path.basename(uploaded_file)

        destination = os.path.join(

            self.REPOSITORY_FOLDER,

            filename

        )

        shutil.copy2(

            uploaded_file,

            destination

        )

        return destination

    def list_documents(self):

        return os.listdir(

            self.REPOSITORY_FOLDER

        )

    def delete(self, filename):

        path = os.path.join(

            self.REPOSITORY_FOLDER,

            filename

        )

        if os.path.exists(path):

            os.remove(path)

            return True

        return False   