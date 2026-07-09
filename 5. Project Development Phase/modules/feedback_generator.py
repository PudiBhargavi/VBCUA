import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

_api_key = os.getenv("GEMINI_API_KEY")
if not _api_key:
    raise ValueError("GEMINI_API_KEY not found. Make sure it's set in your .env file.")

genai.configure(api_key=_api_key)
_model = genai.GenerativeModel("gemini-2.5-flash")


def generate_feedback(result: dict) -> str:
    """
    Uses Gemini to turn raw evaluation scores into a natural-language
    feedback paragraph for the user.

    Args:
        result: the dict returned by evaluate_explanation()

    Returns:
        A short feedback paragraph as a string.
    """
    fr = result["final_result"]

    prompt = f"""
You are an educational assessment assistant. A student gave a spoken explanation
of the concept "{result['concept']}". Here is their transcript and evaluation data:

Transcript: "{result['transcript']}"

Semantic understanding score (0-1): {fr['semantic_score']}
Understanding level: {result['understanding_label']}
Fluency score (0-1): {fr['fluency_score']}
Filler words used: {result['filler_words']['total']}
Pause ratio: {result['audio_features']['pause_ratio']}
Overall performance: {fr['label']} ({fr['final_score']})

Write a short, encouraging, specific feedback paragraph (3-4 sentences) for the
student. Mention what they explained well, anything they may have missed or
gotten slightly wrong about the concept, and one concrete tip to improve their
fluency or clarity next time. Keep the tone supportive, not harsh. Do not repeat
the raw numbers back verbatim; speak naturally like a mentor would.
"""

    response = _model.generate_content(prompt)
    return response.text.strip()


# Quick manual test
if __name__ == "__main__":
    from modules.pipeline import evaluate_explanation

    result = evaluate_explanation("sample_audio/test.m4a", "Machine Learning")
    feedback = generate_feedback(result)
    print("AI Feedback:\n", feedback)