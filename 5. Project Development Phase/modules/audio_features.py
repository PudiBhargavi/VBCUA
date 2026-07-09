import librosa
import numpy as np
import re

FILLER_WORDS = ["um", "uh", "like", "you know", "actually", "basically", "so"]


def count_filler_words(transcript: str) -> dict:
    """
    Counts filler word occurrences in a transcript.
    """
    transcript_lower = transcript.lower()
    counts = {}
    total = 0
    for filler in FILLER_WORDS:
        # word-boundary match so "so" doesn't match inside other words
        count = len(re.findall(rf"\b{re.escape(filler)}\b", transcript_lower))
        if count > 0:
            counts[filler] = count
        total += count
    return {"counts": counts, "total": total}


def analyze_audio(audio_path: str) -> dict:
    """
    Extracts pause ratio and RMS energy from an audio file.
    """
    y, sr = librosa.load(audio_path, sr=16000)

    # Total duration
    duration = librosa.get_duration(y=y, sr=sr)

    # Detect non-silent intervals
    intervals = librosa.effects.split(y, top_db=30)
    voiced_duration = sum((end - start) for start, end in intervals) / sr
    pause_duration = duration - voiced_duration
    pause_ratio = pause_duration / duration if duration > 0 else 0

    # RMS energy (average loudness/clarity proxy)
    rms = librosa.feature.rms(y=y)[0]
    avg_rms = float(np.mean(rms))

    return {
        "duration_sec": round(duration, 2),
        "pause_ratio": round(pause_ratio, 2),
        "avg_rms_energy": round(avg_rms, 4),
    }


# Quick manual test
if __name__ == "__main__":
    transcript = "Machine learning is a branch of artificial intelligence, um, that enables computers to, like, learn from data."

    filler_result = count_filler_words(transcript)
    audio_result = analyze_audio("sample_audio/test.m4a")

    print("Filler Word Analysis:", filler_result)
    print("Audio Feature Analysis:", audio_result)