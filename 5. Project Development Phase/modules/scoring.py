def compute_final_score(semantic_score: float, filler_total: int, pause_ratio: float) -> dict:
    """
    Combines semantic understanding and fluency metrics into a final score.

    semantic_score: 0-1 (from Sentence-BERT)
    filler_total: count of filler words used
    pause_ratio: 0-1 (proportion of silence in speech)
    """
    # Fluency penalty: more fillers and higher pause ratio reduce fluency score
    filler_penalty = min(filler_total * 0.05, 0.3)  # cap penalty at 0.3
    pause_penalty = pause_ratio * 0.3               # pause ratio scaled

    fluency_score = max(1 - filler_penalty - pause_penalty, 0)

    # Weighted final score: 60% understanding, 40% fluency
    final_score = (0.6 * semantic_score) + (0.4 * fluency_score)

    if final_score >= 0.75:
        label = "Strong Performance"
    elif final_score >= 0.5:
        label = "Moderate Performance"
    else:
        label = "Needs Improvement"

    return {
        "semantic_score": round(semantic_score, 2),
        "fluency_score": round(fluency_score, 2),
        "final_score": round(final_score, 2),
        "label": label,
    }


# Quick manual test
if __name__ == "__main__":
    result = compute_final_score(semantic_score=0.76, filler_total=2, pause_ratio=0.23)
    print(result)