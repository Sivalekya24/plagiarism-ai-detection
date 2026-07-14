import math
import re
from collections import Counter


class EntropyAnalyzer:

    @staticmethod
    def analyze(code: str):

        if not code:

            return {

                "character_entropy": 0,

                "token_entropy": 0

            }

        # -------------------------
        # Character Entropy
        # -------------------------

        characters = Counter(code)

        total_characters = len(code)

        character_entropy = 0

        for count in characters.values():

            probability = count / total_characters

            character_entropy -= (

                probability *

                math.log2(probability)

            )

        # -------------------------
        # Token Entropy
        # -------------------------

        tokens = re.findall(

            r"[A-Za-z_][A-Za-z0-9_]*",

            code

        )

        if len(tokens) == 0:

            token_entropy = 0

        else:

            token_counter = Counter(tokens)

            token_entropy = 0

            total_tokens = len(tokens)

            for count in token_counter.values():

                probability = count / total_tokens

                token_entropy -= (

                    probability *

                    math.log2(probability)

                )

        return {

            "character_entropy": round(

                character_entropy,

                4

            ),

            "token_entropy": round(

                token_entropy,

                4

            )

        }