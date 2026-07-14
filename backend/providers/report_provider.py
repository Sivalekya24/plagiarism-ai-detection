class ReportProvider:

    @staticmethod
    def top_matches(results, limit=5):

        if not results:
            return []

        results = sorted(

            results,

            key=lambda item: item["similarity"],

            reverse=True

        )

        return results[:limit]

    @staticmethod
    def summary(matches):

        if not matches:

            return {

                "highest_similarity": 0,

                "matched_document": None,

                "risk_level": "None"

            }

        best = matches[0]

        similarity = round(

            best["similarity"],

            2

        )

        if similarity >= 80:

            risk = "High"

        elif similarity >= 50:

            risk = "Medium"

        else:

            risk = "Low"

        return {

            "highest_similarity": similarity,

            "matched_document": best["document_name"],

            "risk_level": risk

        }