class WeightedSimilarity:

    @staticmethod
    def calculate(

        tfidf_score,

        semantic_score,

        winnowing_score

    ):

        # Production weights

        weights = {

            "semantic": 0.45,

            "winnowing": 0.35,

            "tfidf": 0.20

        }

        score = (

            semantic_score * weights["semantic"]

            +

            winnowing_score * weights["winnowing"]

            +

            tfidf_score * weights["tfidf"]

        )

        return round(score, 2)