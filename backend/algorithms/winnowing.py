import hashlib


class Winnowing:

    @staticmethod
    def preprocess(text):

        text = text.lower()

        text = "".join(
            ch for ch in text
            if ch.isalnum() or ch.isspace()
        )

        text = " ".join(text.split())

        return text

    @staticmethod
    def generate_kgrams(text, k=5):

        return [

            text[i:i+k]

            for i in range(len(text)-k+1)

        ]

    @staticmethod
    def hash_kgrams(kgrams):

        hashes = []

        for gram in kgrams:

            h = hashlib.md5(
                gram.encode()
            ).hexdigest()

            hashes.append(
                int(h, 16)
            )

        return hashes

    @staticmethod
    def fingerprints(hashes, window_size=4):

        fingerprints = []

        if len(hashes) < window_size:

            return hashes

        for i in range(

            len(hashes)-window_size+1

        ):

            window = hashes[i:i+window_size]

            fingerprints.append(
                min(window)
            )

        return list(set(fingerprints))

    @staticmethod
    def similarity(text1, text2):

        text1 = Winnowing.preprocess(text1)

        text2 = Winnowing.preprocess(text2)

        grams1 = Winnowing.generate_kgrams(text1)

        grams2 = Winnowing.generate_kgrams(text2)

        hashes1 = Winnowing.hash_kgrams(grams1)

        hashes2 = Winnowing.hash_kgrams(grams2)

        fp1 = set(
            Winnowing.fingerprints(hashes1)
        )

        fp2 = set(
            Winnowing.fingerprints(hashes2)
        )

        if len(fp1) == 0 or len(fp2) == 0:

            return 0

        intersection = len(
            fp1.intersection(fp2)
        )

        union = len(
            fp1.union(fp2)
        )

        return round(
            (intersection / union) * 100,
            2
        )