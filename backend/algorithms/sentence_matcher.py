from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SentenceMatcher:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def match(self, sentences1, sentences2, threshold=80):

        if not sentences1 or not sentences2:
            return []

        embeddings1 = self.model.encode(
            sentences1,
            convert_to_numpy=True
        )

        embeddings2 = self.model.encode(
            sentences2,
            convert_to_numpy=True
        )

        matches = []

        for i, emb1 in enumerate(embeddings1):

            similarities = cosine_similarity(
                [emb1],
                embeddings2
            )[0]

            best_index = similarities.argmax()

            best_score = similarities[best_index] * 100

            if best_score >= threshold:

                matches.append({

                    "document1_sentence": sentences1[i],

                    "document2_sentence": sentences2[best_index],

                    "similarity": round(float(best_score), 2)

                })

        return matches