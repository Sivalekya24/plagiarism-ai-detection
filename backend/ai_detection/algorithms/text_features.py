import re
from collections import Counter

import textstat
from nltk.corpus import stopwords


class TextFeatures:

    STOPWORDS = set(stopwords.words("english"))

    @staticmethod
    def burstiness(sentence_lengths):

        if len(sentence_lengths) < 2:
            return 0

        mean = sum(sentence_lengths) / len(sentence_lengths)

        variance = sum(
            (x - mean) ** 2
            for x in sentence_lengths
        ) / len(sentence_lengths)

        std = variance ** 0.5

        if mean == 0:
            return 0

        return round(std / mean, 4)

    @staticmethod
    def stopword_ratio(words):

        if not words:
            return 0

        count = sum(
            1
            for word in words
            if word in TextFeatures.STOPWORDS
        )

        return round(count / len(words), 4)

    @staticmethod
    def readability(text):

        try:
            return round(
                textstat.flesch_reading_ease(text),
                2
            )
        except Exception:
            return 0

    @staticmethod
    def repeated_phrase_ratio(words):

        if len(words) < 3:
            return 0

        phrases = [

            " ".join(words[i:i + 3])

            for i in range(len(words) - 2)

        ]

        counter = Counter(phrases)

        repeated = sum(

            value

            for value in counter.values()

            if value > 1

        )

        return round(

            repeated / len(phrases),

            4

        )

    @staticmethod
    def extract(text: str):

        words = re.findall(

            r"\b\w+\b",

            text.lower()

        )

        sentences = re.split(

            r"[.!?]+",

            text

        )

        sentences = [

            s.strip()

            for s in sentences

            if s.strip()

        ]

        total_words = len(words)

        unique_words = len(set(words))

        sentence_lengths = [

            len(s.split())

            for s in sentences

        ]

        average_sentence_length = (

            sum(sentence_lengths)

            / len(sentence_lengths)

            if sentence_lengths

            else 0

        )

        sentence_variance = (

            sum(

                (x - average_sentence_length) ** 2

                for x in sentence_lengths

            )

            / len(sentence_lengths)

            if sentence_lengths

            else 0

        )

        lexical_diversity = (

            unique_words / total_words

            if total_words

            else 0

        )

        counter = Counter(words)

        repeated_words = sum(

            count - 1

            for count in counter.values()

            if count > 1

        )

        repetition_score = (

            repeated_words / total_words

            if total_words

            else 0

        )

        punctuation = len(

            re.findall(

                r"[.,!?;:]",

                text

            )

        )

        punctuation_ratio = (

            punctuation / total_words

            if total_words

            else 0

        )

        average_word_length = (

            sum(

                len(word)

                for word in words

            )

            / total_words

            if total_words

            else 0

        )

        return {

            "total_words": total_words,

            "unique_words": unique_words,

            "lexical_diversity": round(
                lexical_diversity,
                4
            ),

            "average_sentence_length": round(
                average_sentence_length,
                2
            ),

            "sentence_variance": round(
                sentence_variance,
                2
            ),

            "repetition_score": round(
                repetition_score,
                4
            ),

            "punctuation_ratio": round(
                punctuation_ratio,
                4
            ),

            "average_word_length": round(
                average_word_length,
                2
            ),

            "burstiness": TextFeatures.burstiness(
                sentence_lengths
            ),

            "stopword_ratio": TextFeatures.stopword_ratio(
                words
            ),

            "readability_score": TextFeatures.readability(
                text
            ),

            "repeated_phrase_ratio": TextFeatures.repeated_phrase_ratio(
                words
            )

            
        }