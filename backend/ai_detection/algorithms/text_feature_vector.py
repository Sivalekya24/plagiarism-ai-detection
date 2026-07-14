import pandas as pd


FEATURE_COLUMNS = [

    "total_words",

    "unique_words",

    "lexical_diversity",

    "average_sentence_length",

    "sentence_variance",

    "repetition_score",

    "punctuation_ratio",

    "average_word_length",

    "burstiness",

    "stopword_ratio",

    "readability_score",

    "repeated_phrase_ratio",


]


class TextFeatureVector:

    @staticmethod
    def build(features):

        return pd.DataFrame(

            [[

                features[column]

                for column in FEATURE_COLUMNS

            ]],

            columns=FEATURE_COLUMNS

        )