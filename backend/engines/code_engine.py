from algorithms.code_preprocessor import CodePreprocessor

from algorithms.token_similarity import TokenSimilarity

from algorithms.ast_similarity import ASTSimilarity

from algorithms.code_winnowing import CodeWinnowing

from algorithms.weighted_code_similarity import WeightedCodeSimilarity


class CodeEngine:

    def compare(self, code1, code2):

        code1 = CodePreprocessor.preprocess(code1)

        code2 = CodePreprocessor.preprocess(code2)

        token = 0
        ast_score = 0
        winnowing = 0

        try:

            token = TokenSimilarity.calculate(
                code1,
                code2
            )

        except Exception:
            pass

        try:

            ast_score = ASTSimilarity.calculate(
                code1,
                code2
            )

        except Exception:
            pass

        try:

            winnowing = CodeWinnowing.calculate(
                code1,
                code2
            )

        except Exception:
            pass

        final = WeightedCodeSimilarity.calculate(
            token,
            ast_score,
            winnowing
        )

        return {

            "overall_similarity": final,

            "algorithm_scores": {

                "token": token,

                "ast": ast_score,

                "winnowing": winnowing

            }

        }