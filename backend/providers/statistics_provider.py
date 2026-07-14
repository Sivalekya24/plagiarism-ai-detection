import os


class StatisticsProvider:

    def __init__(self):

        self.repository = "database/documents"

        os.makedirs(self.repository, exist_ok=True)

    def get_statistics(self):

        files = []

        total_size = 0

        extensions = {}

        for file in os.listdir(self.repository):

            path = os.path.join(self.repository, file)

            if os.path.isfile(path):

                size = os.path.getsize(path)

                total_size += size

                ext = os.path.splitext(file)[1].lower()

                extensions[ext] = extensions.get(ext, 0) + 1

                files.append(file)

        return {

            "total_documents": len(files),

            "repository_size_mb": round(total_size / (1024 * 1024), 2),

            "file_types": extensions,

            "documents": files

        }