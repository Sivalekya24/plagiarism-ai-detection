import re


class FingerprintSimilarity:

    @staticmethod
    def _normalize(text: str):

        text = text.lower()

        text = re.sub(r"[^\w\s]", "", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text

    @staticmethod
    def _generate_shingles(text: str, k: int = 3):

        words = text.split()

        if len(words) < k:
            return set()

        shingles = set()

        for i in range(len(words) - k + 1):
            shingle = " ".join(words[i:i + k])
            shingles.add(shingle)

        return shingles

    @classmethod
    def calculate(cls, text1: str, text2: str):

        text1 = cls._normalize(text1)
        text2 = cls._normalize(text2)

        shingles1 = cls._generate_shingles(text1)
        shingles2 = cls._generate_shingles(text2)

        if not shingles1 and not shingles2:
            return 100.0

        if not shingles1 or not shingles2:
            return 0.0

        intersection = len(shingles1.intersection(shingles2))
        union = len(shingles1.union(shingles2))

        similarity = (intersection / union) * 100

        return round(similarity, 2)