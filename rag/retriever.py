from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class BrandRAG:
    def __init__(self):
        self.docs = []

    def add_text(self, text):
        for part in [p.strip() for p in text.split("\n") if p.strip()]:
            self.docs.append(part)

    def retrieve(self, query, top_k=5):
        if not self.docs:
            return "(No saved brand knowledge yet.)"
        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform(self.docs + [query])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
        ranked = scores.argsort()[::-1][:top_k]
        return "\n".join(f"- {self.docs[i]}" for i in ranked)
