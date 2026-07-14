from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TFIDFSimilarity:

    @staticmethod
    def calculate(text1: str, text2: str):

        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform([text1, text2])

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        return round(similarity * 100, 2)