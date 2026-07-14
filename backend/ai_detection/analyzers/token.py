import re


class TokenAnalyzer:

    OPERATORS = {

        "+", "-", "*", "/", "%",

        "=", "==", "!=", "<", ">", "<=", ">=",

        "&&", "||", "!", "&", "|", "^", "~",

        "<<", ">>",

        "+=", "-=", "*=", "/=", "%=",

        "++", "--",

        "->", "::", ".", ",", ";", ":"

    }

    KEYWORDS = {

        "if", "else", "for", "while", "switch", "case",

        "return", "break", "continue",

        "try", "catch", "finally",

        "class", "struct", "interface",

        "public", "private", "protected",

        "static", "void",

        "def", "function", "func",

        "import", "include", "using",

        "package", "namespace",

        "new", "this", "super",

        "true", "false", "null"

    }

    @staticmethod
    def analyze(code: str):

        words = re.findall(

            r"[A-Za-z_][A-Za-z0-9_]*",

            code

        )

        total_tokens = len(words)

        unique_tokens = len(set(words))

        keyword_count = sum(

            1

            for token in words

            if token in TokenAnalyzer.KEYWORDS

        )

        operator_count = 0

        for operator in TokenAnalyzer.OPERATORS:

            operator_count += code.count(operator)

        number_literals = len(

            re.findall(

                r"\b\d+(\.\d+)?\b",

                code

            )

        )

        string_literals = len(

            re.findall(

                r'".*?"|\'.*?\'',

                code,

                re.DOTALL

            )

        )

        import_count = len(

            re.findall(

                r"\b(import|include|using|require|package)\b",

                code

            )

        )

        loop_count = len(

            re.findall(

                r"\b(for|while|do)\b",

                code

            )

        )

        branch_count = len(

            re.findall(

                r"\b(if|else|switch|case)\b",

                code

            )

        )

        function_keywords = len(

            re.findall(

                r"\b(def|function|func|void)\b",

                code

            )

        )

        token_diversity = (

            unique_tokens / total_tokens

            if total_tokens

            else 0

        )

        return {

            "total_tokens": total_tokens,

            "unique_tokens": unique_tokens,

            "token_diversity": round(

                token_diversity,

                4

            ),

            "keyword_count": keyword_count,

            "operator_count": operator_count,

            "number_literals": number_literals,

            "string_literals": string_literals,

            "import_count": import_count,

            "loop_count": loop_count,

            "branch_count": branch_count,

            "function_keyword_count": function_keywords

        }