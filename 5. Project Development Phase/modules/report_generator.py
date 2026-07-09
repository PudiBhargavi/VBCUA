import os
import tempfile
import matplotlib.pyplot as plt
import librosa
import librosa.display
from fpdf import FPDF


def _generate_waveform_image(audio_path: str) -> str:
    """
    Renders a waveform plot to a temporary PNG file and returns its path.
    """
    y, sr = librosa.load(audio_path, sr=16000)

    fig, ax = plt.subplots(figsize=(7, 2.2))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    librosa.display.waveshow(y, sr=sr, ax=ax, color='#2563EB')
    ax.set_xlabel("Time (s)")
    ax.set_title("Audio Waveform")

    img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    fig.savefig(img_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return img_path


def generate_pdf_report(result: dict, audio_path: str, output_path: str = None) -> str:
    """
    Generates a structured PDF report from a pipeline result dict.

    Args:
        result: the dict returned by evaluate_explanation()
        audio_path: path to the original audio file (used to render the waveform)
        output_path: where to save the PDF. If None, a temp file is created.

    Returns:
        Path to the generated PDF file.
    """
    if output_path is None:
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name

    fr = result["final_result"]
    waveform_img = _generate_waveform_image(audio_path)

    pdf = FPDF()
    pdf.add_page()

    # --- Header ---
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Voice-Based Concept Understanding Analyser", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Evaluation Report", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # --- Concept + Verdict ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Concept: {result['concept']}", ln=True)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(180, 95, 20)
    pdf.cell(0, 9, f"Overall: {fr['label']}  ({fr['final_score']:.2f} / 1.00)", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # --- Score table ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Evaluation Metrics", ln=True)
    pdf.set_font("Helvetica", "", 11)

    rows = [
        ("Semantic Score", f"{fr['semantic_score']:.2f}"),
        ("Understanding Level", result["understanding_label"]),
        ("Fluency Score", f"{fr['fluency_score']:.2f}"),
        ("Filler Words Used", str(result["filler_words"]["total"])),
        ("Pause Ratio", f"{result['audio_features']['pause_ratio']:.2f}"),
        ("Audio Duration (s)", f"{result['audio_features']['duration_sec']:.2f}"),
    ]
    for label, value in rows:
        pdf.cell(60, 8, label, border=0)
        pdf.cell(0, 8, value, ln=True)
    pdf.ln(2)

    # --- Filler word breakdown ---
    counts = result["filler_words"]["counts"]
    if counts:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, "Filler Word Breakdown:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for word, count in counts.items():
            pdf.cell(0, 6, f"  - \"{word}\": {count} time(s)", ln=True)
        pdf.ln(2)
    
    # --- AI Feedback ---
    from modules.feedback_generator import generate_feedback
    feedback_text = generate_feedback(result)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "AI-Generated Feedback", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, feedback_text)
    pdf.ln(2)

    # --- Transcript ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Transcript", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, result["transcript"])
    pdf.ln(2)

    # --- Waveform image ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Waveform", ln=True)
    pdf.image(waveform_img, w=170)

    pdf.output(output_path)

    # Clean up temp waveform image
    try:
        os.remove(waveform_img)
    except OSError:
        pass

    return output_path


# Quick manual test
if __name__ == "__main__":
    from modules.pipeline import evaluate_explanation

    result = evaluate_explanation("sample_audio/test.m4a", "Machine Learning")
    path = generate_pdf_report(result, "sample_audio/test.m4a", "reports/test_report.pdf")
    print(f"Report saved to: {path}")