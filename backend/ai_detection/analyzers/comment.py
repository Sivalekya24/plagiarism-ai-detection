import re


class CommentAnalyzer:

    @staticmethod
    def analyze(code: str):

        lines = code.splitlines()

        total_lines = len(lines)

        if total_lines == 0:

            return {

                "comment_lines": 0,

                "single_comments": 0,

                "block_comments": 0,

                "docstring_comments": 0,

                "comment_ratio": 0

            }

        single_comments = 0

        block_comments = 0

        docstring_comments = 0

        inside_block = False

        inside_docstring = False

        for line in lines:

            stripped = line.strip()

            # -----------------------------
            # Python Docstrings
            # -----------------------------

            if stripped.startswith('"""') or stripped.startswith("'''"):

                docstring_comments += 1

                if (

                    stripped.count('"""') == 1

                    or stripped.count("'''") == 1

                ):

                    inside_docstring = not inside_docstring

                continue

            if inside_docstring:

                docstring_comments += 1

                if (

                    stripped.endswith('"""')

                    or stripped.endswith("'''")

                ):

                    inside_docstring = False

                continue

            # -----------------------------
            # Block Comments
            # -----------------------------

            if stripped.startswith("/*"):

                block_comments += 1

                if "*/" not in stripped:

                    inside_block = True

                continue

            if inside_block:

                block_comments += 1

                if "*/" in stripped:

                    inside_block = False

                continue

            # -----------------------------
            # Single Line Comments
            # -----------------------------

            if (

                stripped.startswith("//")

                or stripped.startswith("#")

            ):

                single_comments += 1

        comment_lines = (

            single_comments

            + block_comments

            + docstring_comments

        )

        comment_ratio = (

            comment_lines / total_lines

            if total_lines

            else 0

        )

        return {

            "comment_lines": comment_lines,

            "single_comments": single_comments,

            "block_comments": block_comments,

            "docstring_comments": docstring_comments,

            "comment_ratio": round(

                comment_ratio,

                4

            )

        }