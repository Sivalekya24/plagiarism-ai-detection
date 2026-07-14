from providers.repository_provider import RepositoryProvider
from providers.report_provider import ReportProvider
from providers.storage_provider import StorageProvider

from engines.document_engine import DocumentEngine


class RepositoryEngine:

    def __init__(self):

        self.repository = RepositoryProvider()

        self.document_engine = DocumentEngine()

        self.storage = StorageProvider()

    def compare_against_repository(self, uploaded_file_path):

        uploaded_text = self.repository.extract(
            uploaded_file_path
        )

        repository_documents = self.repository.get_all_documents()

        if len(repository_documents) == 0:

            self.storage.save_document(
                uploaded_file_path
            )

            return {

                "repository_size": 0,

                "highest_similarity": 0,

                "matched_document": None,

                "risk_level": "None",

                "matches": [],

                "message": "Repository was empty. Document stored successfully."

            }

        comparison_results = []

        for document in repository_documents:

            repository_text = self.repository.extract(
                document["path"]
            )

            report = self.document_engine.compare(

                uploaded_text,

                repository_text

            )

            comparison_results.append({

                "document_name": document["name"],

                "similarity": report["overall_similarity"],

                "report": report

            })

        top_matches = ReportProvider.top_matches(

            comparison_results,

            limit=5

        )

        summary = ReportProvider.summary(

            top_matches

        )

        self.storage.save_document(
            uploaded_file_path
        )

        return {

            "repository_size": len(repository_documents),

            "highest_similarity": summary["highest_similarity"],

            "matched_document": summary["matched_document"],

            "risk_level": summary["risk_level"],

            "matches": top_matches,

            "message": "Comparison completed successfully."

        }