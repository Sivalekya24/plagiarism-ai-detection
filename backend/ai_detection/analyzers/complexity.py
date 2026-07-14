import re


class ComplexityAnalyzer:

    LOOP_PATTERN = r"\b(for|while|do|foreach)\b"

    BRANCH_PATTERN = r"\b(if|else|elif|switch|case|catch)\b"

    LOGICAL_PATTERN = r"&&|\|\|| and | or "

    FUNCTION_PATTERN = (
        r"\b(def|function|func|void|int|float|double|char|bool|"
        r"public|private|protected|static)\b"
    )

    @staticmethod
    def analyze(code: str):

        loop_count = len(

            re.findall(

                ComplexityAnalyzer.LOOP_PATTERN,

                code

            )

        )

        branch_count = len(

            re.findall(

                ComplexityAnalyzer.BRANCH_PATTERN,

                code

            )

        )

        logical_count = len(

            re.findall(

                ComplexityAnalyzer.LOGICAL_PATTERN,

                code

            )

        )

        function_count = len(

            re.findall(

                ComplexityAnalyzer.FUNCTION_PATTERN,

                code

            )

        )

        # -------------------------
        # Maximum Nesting Depth
        # -------------------------

        current_depth = 0

        max_depth = 0

        for character in code:

            if character == "{":

                current_depth += 1

                max_depth = max(

                    max_depth,

                    current_depth

                )

            elif character == "}":

                current_depth = max(

                    0,

                    current_depth - 1

                )

        # -------------------------
        # Approximate Cyclomatic Complexity
        # -------------------------

        cyclomatic_complexity = (

            1

            + loop_count

            + branch_count

            + logical_count

        )

        return {

            "loop_count": loop_count,

            "branch_count": branch_count,

            "logical_operator_count": logical_count,

            "function_count": function_count,

            "max_nesting_depth": max_depth,

            "cyclomatic_complexity": cyclomatic_complexity

        }