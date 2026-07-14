import io
import tokenize
from difflib import SequenceMatcher


class TokenSimilarity:

    @staticmethod
    def tokenize_code(code):

        tokens = []

        stream = io.StringIO(code)

        for token in tokenize.generate_tokens(stream.readline):

            if token.type in [

                tokenize.ENCODING,

                tokenize.NL,

                tokenize.NEWLINE,

                tokenize.INDENT,

                tokenize.DEDENT,

                tokenize.ENDMARKER

            ]:

                continue

            tokens.append(token.string)

        return tokens

    @staticmethod
    def calculate(code1, code2):

        tokens1 = TokenSimilarity.tokenize_code(code1)

        tokens2 = TokenSimilarity.tokenize_code(code2)

        similarity = SequenceMatcher(

            None,

            tokens1,

            tokens2

        ).ratio()

        return round(similarity * 100, 2)