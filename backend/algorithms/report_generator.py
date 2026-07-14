class ReportGenerator:

    @staticmethod
    def generate(
        overall_similarity,
        algorithm_scores,
        matched_sentences
    ):

        if overall_similarity >= 80:
            risk = "High"

        elif overall_similarity >= 50:
            risk = "Medium"

        else:
            risk = "Low"

        confidence = round(

            (
                algorithm_scores["semantic"] +
                algorithm_scores["tfidf"] +
                algorithm_scores["winnowing"]

            ) / 3,

            2

        )

        return {

            "overall_similarity": overall_similarity,

            "risk_level": risk,

            "confidence": confidence,

            "algorithm_scores": algorithm_scores,

            "matched_sentences": matched_sentences

        }