from providers.repository_provider import RepositoryProvider
from providers.report_provider import ReportProvider

from engines.document_engine import DocumentEngine


class PasteEngine:

    def __init__(self):

        self.repository = RepositoryProvider()

        self.document_engine = DocumentEngine()

    def check_plagiarism(self, pasted_text):

        repository_documents = self.repository.get_all_documents()

        comparison_results = []

        for document in repository_documents:

            repository_text = self.repository.extract(
                document["path"]
            )

            result = self.document_engine.compare(
                pasted_text,
                repository_text
            )

            comparison_results.append({

                "document_name": document["name"],

                "similarity": result["overall_similarity"],

                "report": result

            })

        top_matches = ReportProvider.top_matches(
            comparison_results,
            limit=5
        )

        summary = ReportProvider.summary(
            top_matches
        )

        return {

            "repository_size": len(repository_documents),

            "highest_similarity": summary["highest_similarity"],

            "matched_document": summary["matched_document"],

            "risk_level": summary["risk_level"],

            "matches": top_matches

        }