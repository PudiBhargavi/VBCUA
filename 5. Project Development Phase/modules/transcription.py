import whisper

# Load model once (base model balances speed and accuracy)
_model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes spoken audio into text using Whisper.

    Args:
        audio_path: path to an audio file (.wav, .mp3, etc.)

    Returns:
        The transcribed text as a string.
    """
    result = _model.transcribe(audio_path)
    return result["text"].strip()


# Quick manual test
if __name__ == "__main__":
    test_file = "sample_audio/test.m4a"  # update with a real file
    text = transcribe_audio(test_file)
    print("Transcript:", text)