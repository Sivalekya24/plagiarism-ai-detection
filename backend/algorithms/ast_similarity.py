import ast
from difflib import SequenceMatcher

from algorithms.code_preprocessor import CodePreprocessor


class ASTSimilarity:

    @staticmethod
    def calculate(code1, code2):

        try:

            code1 = CodePreprocessor.preprocess(code1)

            code2 = CodePreprocessor.preprocess(code2)

            tree1 = ast.dump(
                ast.parse(code1),
                annotate_fields=False,
                include_attributes=False
            )

            tree2 = ast.dump(
                ast.parse(code2),
                annotate_fields=False,
                include_attributes=False
            )

            similarity = SequenceMatcher(
                None,
                tree1,
                tree2
            ).ratio()

            return round(similarity * 100, 2)

        except Exception as e:
            print("AST ERROR:", e)
        return 0