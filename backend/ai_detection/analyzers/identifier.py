import re


class IdentifierAnalyzer:

    IDENTIFIER_PATTERN = r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"

    KEYWORDS = {

        # Control Flow
        "if", "else", "elif", "switch", "case",
        "for", "while", "do", "break", "continue",
        "return", "goto", "yield",

        # Exception Handling
        "try", "catch", "finally", "throw", "throws",

        # OOP
        "class", "struct", "interface", "enum",
        "extends", "implements", "this", "super",
        "new",

        # Access Modifiers
        "public", "private", "protected",
        "internal", "static", "final",
        "abstract", "virtual", "override",
        "sealed", "const", "readonly",

        # Data Types
        "void", "int", "long", "short", "float",
        "double", "char", "bool", "boolean",
        "byte", "string", "String", "decimal",
        "object", "dynamic", "auto",

        # Python
        "def", "lambda", "async", "await",
        "None", "True", "False", "pass",
        "global", "nonlocal", "del",
        "with", "as", "is", "in",

        # JavaScript
        "function", "var", "let", "const",
        "undefined", "null",

        # Go
        "func", "defer", "go", "select",
        "chan", "map", "range",

        # PHP
        "echo", "namespace", "trait",

        # Imports
        "import", "from", "using",
        "include", "require", "package",

        # Misc
        "sizeof", "typeof", "instanceof",

    }

    @staticmethod
    def analyze(code: str):

        identifiers = re.findall(

            IdentifierAnalyzer.IDENTIFIER_PATTERN,

            code

        )

        identifiers = [

            identifier

            for identifier in identifiers

            if identifier not in IdentifierAnalyzer.KEYWORDS

        ]

        total_identifiers = len(identifiers)

        if total_identifiers == 0:

            return {

                "identifier_count": 0,

                "unique_identifier_count": 0,

                "identifier_diversity": 0,

                "average_identifier_length": 0,

                "camel_case_count": 0,

                "snake_case_count": 0,

                "uppercase_identifier_count": 0,

                "single_character_identifier_count": 0

            }

        unique_identifiers = len(set(identifiers))

        identifier_diversity = (

            unique_identifiers /

            total_identifiers

        )

        average_identifier_length = (

            sum(

                len(identifier)

                for identifier in identifiers

            )

            /

            total_identifiers

        )

        camel_case_count = sum(

            1

            for identifier in identifiers

            if re.match(

                r"^[a-z]+(?:[A-Z][a-zA-Z0-9]*)+$",

                identifier

            )

        )

        snake_case_count = sum(

            1

            for identifier in identifiers

            if re.match(

                r"^[a-z]+(?:_[a-z0-9]+)+$",

                identifier

            )

        )

        uppercase_identifier_count = sum(

            1

            for identifier in identifiers

            if identifier.isupper()

        )

        single_character_identifier_count = sum(

            1

            for identifier in identifiers

            if len(identifier) == 1

        )

        return {

            "identifier_count": total_identifiers,

            "unique_identifier_count": unique_identifiers,

            "identifier_diversity": round(

                identifier_diversity,

                4

            ),

            "average_identifier_length": round(

                average_identifier_length,

                2

            ),

            "camel_case_count": camel_case_count,

            "snake_case_count": snake_case_count,

            "uppercase_identifier_count": uppercase_identifier_count,

            "single_character_identifier_count": single_character_identifier_count

        }