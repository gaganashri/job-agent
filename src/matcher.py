import faiss
import numpy as np
from src.embedder import get_embedding

class JobMatcher:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)
        self.job_ids = []

    def add_job(self, job_id, text):
        emb = get_embedding(text)
        if emb is not None:
            emb = np.array([emb]).astype("float32")
            self.index.add(emb)
            self.job_ids.append(job_id)

    def search(self, resume_text, top_k=3):
        query_emb = get_embedding(resume_text)
        if query_emb is None:
            return []
        query_emb = np.array([query_emb]).astype("float32")
        distances, indices = self.index.search(query_emb, top_k)
        return [(self.job_ids[i], distances[0][pos]) for pos, i in enumerate(indices[0])]
