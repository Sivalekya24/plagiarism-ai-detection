from algorithms.winnowing import Winnowing
from algorithms.code_preprocessor import CodePreprocessor


class CodeWinnowing:

    @staticmethod
    def calculate(code1, code2):

        code1 = CodePreprocessor.preprocess(code1)

        code2 = CodePreprocessor.preprocess(code2)

        return Winnowing.similarity(

            code1,

            code2

        )