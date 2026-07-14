import pandas as pd


FEATURE_COLUMNS = [

    # Structure
    "total_lines",
    "blank_lines",
    "blank_line_ratio",
    "average_line_length",
    "max_line_length",
    "min_line_length",
    "line_length_variance",
    "empty_line_groups",

    # Comments
    "comment_lines",
    "single_comments",
    "block_comments",
    "docstring_comments",
    "comment_ratio",

    # Identifiers
    "identifier_count",
    "unique_identifier_count",
    "identifier_diversity",
    "average_identifier_length",
    "camel_case_count",
    "snake_case_count",
    "uppercase_identifier_count",
    "single_character_identifier_count",

    # Tokens
    "total_tokens",
    "unique_tokens",
    "token_diversity",
    "keyword_count",
    "operator_count",
    "number_literals",
    "string_literals",
    "import_count",

    # Complexity
    "loop_count",
    "branch_count",
    "function_keyword_count",
    "logical_operator_count",
    "function_count",
    "max_nesting_depth",
    "cyclomatic_complexity",

     "language",
     
    # Entropy
    "character_entropy",
    "token_entropy"

]


class CodeFeatureVector:

    @staticmethod
    def split(df):

        X = df[FEATURE_COLUMNS]

        y = df["Label"]

        return X, y