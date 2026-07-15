import os
from datetime import datetime


class StatisticsProvider:

    def __init__(self):

        self.repository = "database/documents"

        os.makedirs(self.repository, exist_ok=True)

    def get_statistics(self):

        files = []

        total_size = 0

        latest_modified = None

        for file in os.listdir(self.repository):

            path = os.path.join(self.repository, file)

            if os.path.isfile(path):

                size = os.path.getsize(path)

                total_size += size

                files.append(file)

                modified_time = os.path.getmtime(path)

                if latest_modified is None or modified_time > latest_modified:

                    latest_modified = modified_time

        return {

            "totalDocuments": len(files),

            "totalSizeKb": round(total_size / 1024, 2),

            "lastUpdated": (

                datetime.fromtimestamp(latest_modified).strftime(
                    "%Y-%m-%d %H:%M"
                )

                if latest_modified

                else "-"

            )

        }