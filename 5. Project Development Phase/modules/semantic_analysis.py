from sentence_transformers import SentenceTransformer, util

# Load model once
_model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(transcript: str, reference_text: str) -> float:
    """
    Computes semantic similarity between the user's transcript
    and a reference concept explanation.

    Returns a similarity score between 0 and 1.
    """
    embeddings = _model.encode([transcript, reference_text], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return float(similarity[0][0])


def get_understanding_label(score: float) -> str:
    """
    Converts a similarity score into a qualitative label.
    """
    if score >= 0.75:
        return "Strong Understanding"
    elif score >= 0.5:
        return "Moderate Understanding"
    else:
        return "Poor Understanding"


# Quick manual test
if __name__ == "__main__":
    transcript = "Machine learning is a branch of artificial intelligence that enables computers to learn from data without being explicitly programmed for every task. Insteadof following fixed tools, machine learning algorithms identify patterns, make predictions, and improve their performance as they process more data. It is widely used in applications such as recommendation systems, spamming, meditation, and speech recognition for data exchange and healthcare. There are three main types of machine learning, supervised learning and supervised learning and reinforcement learning. As technology continues to evolve, machine learning is being a vital role in automating tasks and helping organizations make smarter data-driven decisions."
    reference = "Machine learning is a subset of AI where systems learn patterns from data to make predictions without explicit programming."

    score = compute_similarity(transcript, reference)
    label = get_understanding_label(score)

    print(f"Similarity Score: {score:.2f}")
    print(f"Understanding Level: {label}")