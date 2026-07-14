class WeightedCodeSimilarity:

    @staticmethod
    def calculate(

        token,

        ast,

        winnowing

    ):

        weights = []

        scores = []

        if token > 0:

            weights.append(0.30)

            scores.append(token * 0.30)

        if ast > 0:

            weights.append(0.45)

            scores.append(ast * 0.45)

        if winnowing > 0:

            weights.append(0.25)

            scores.append(winnowing * 0.25)

        if not weights:

            return 0

        return round(

            sum(scores) / sum(weights),

            2

        )