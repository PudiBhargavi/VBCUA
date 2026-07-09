import json
from modules.transcription import transcribe_audio
from modules.semantic_analysis import compute_similarity, get_understanding_label
from modules.audio_features import count_filler_words, analyze_audio
from modules.scoring import compute_final_score

with open("data/reference_concepts.json", "r") as f:
    REFERENCE_CONCEPTS = json.load(f)


def evaluate_explanation(audio_path: str, concept_name: str) -> dict:
    """
    Full pipeline: audio in -> complete evaluation out.
    concept_name must match a key in reference_concepts.json
    """
    reference_text = REFERENCE_CONCEPTS.get(concept_name)
    if reference_text is None:
        raise ValueError(f"Unknown concept: {concept_name}")

    transcript = transcribe_audio(audio_path)
    semantic_score = compute_similarity(transcript, reference_text)
    understanding_label = get_understanding_label(semantic_score)

    filler_result = count_filler_words(transcript)
    audio_result = analyze_audio(audio_path)

    final_result = compute_final_score(
        semantic_score=semantic_score,
        filler_total=filler_result["total"],
        pause_ratio=audio_result["pause_ratio"],
    )

    return {
        "concept": concept_name,
        "transcript": transcript,
        "semantic_score": semantic_score,
        "understanding_label": understanding_label,
        "filler_words": filler_result,
        "audio_features": audio_result,
        "final_result": final_result,
    }


if __name__ == "__main__":
    result = evaluate_explanation("sample_audio/test.m4a", "Machine Learning")
    import json as j
    print(j.dumps(result, indent=2))