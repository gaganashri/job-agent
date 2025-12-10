from sentence_transformers import SentenceTransformer

# Lightweight, fast, accurate embedding model
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def get_embedding(text: str):
    """
    Returns a 384-dimensional embedding for the given text.
    """
    try:
        return model.encode([text])[0]
    except Exception as e:
        print("Embedding error:", e)
        return None

# Test
if __name__ == "__main__":
    sample = "Artificial Intelligence Engineer with Python and ML experience."
    emb = get_embedding(sample)
    print("Embedding length:", len(emb))
    print(emb[:10])
