from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSimilarity:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def calculate(self, text1: str, text2: str):

        embeddings = self.model.encode(
            [text1, text2],
            convert_to_numpy=True
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        return round(float(similarity) * 100, 2)