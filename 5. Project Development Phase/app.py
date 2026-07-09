import streamlit as st
import tempfile
import matplotlib.pyplot as plt
import librosa
import librosa.display

from modules.pipeline import evaluate_explanation, REFERENCE_CONCEPTS

st.set_page_config(page_title="VBCUA", page_icon="🎙️", layout="centered")

# ---------------------------------------------------------------------------
# Theme: dark "recording studio" palette + custom typography
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

:root {
    --bg: #14171C;
    --surface: #1E2229;
    --surface-2: #262B33;
    --amber: #E8A33D;
    --teal: #4FD1C5;
    --text: #F2F1ED;
    --muted: #8B92A0;
}

.stApp {
    background-color: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

/* Hide default streamlit chrome that fights the theme */
header[data-testid="stHeader"] { background: transparent; }

/* Hero */
.vbcua-hero {
    padding: 2.2rem 1.8rem 1.8rem 1.8rem;
    border-radius: 14px;
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-2) 100%);
    border: 1px solid #2E3440;
    margin-bottom: 1.6rem;
}
.vbcua-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    color: var(--teal);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.vbcua-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2rem;
    margin: 0;
    color: var(--text);
}
.vbcua-subtitle {
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.5rem;
    max-width: 38rem;
    line-height: 1.5;
}

/* Section labels */
.vbcua-section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--text);
    margin: 1.6rem 0 0.7rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Score cards */
.vbcua-card-row { display: flex; gap: 0.8rem; margin-bottom: 0.8rem; }
.vbcua-card {
    flex: 1;
    background: var(--surface);
    border: 1px solid #2E3440;
    border-radius: 12px;
    padding: 1rem 1.1rem;
}
.vbcua-card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.35rem;
}
.vbcua-card-value {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 1.7rem;
    color: var(--amber);
}
.vbcua-card-value.teal { color: var(--teal); }

.vbcua-verdict {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    padding: 0.9rem 1.1rem;
    border-radius: 10px;
    background: var(--surface-2);
    border-left: 3px solid var(--amber);
    margin-bottom: 0.4rem;
}

/* Transcript box */
.vbcua-transcript {
    background: var(--surface);
    border: 1px solid #2E3440;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    color: var(--text);
    line-height: 1.6;
    font-size: 0.93rem;
}

/* Streamlit widget overrides */
div[data-baseweb="select"] > div, .stFileUploader {
    background-color: var(--surface) !important;
    border-color: #2E3440 !important;
    color: var(--text) !important;
}
.stButton button, .stDownloadButton button {
    background-color: var(--amber) !important;
    color: #14171C !important;
    font-weight: 600 !important;
    border: none !important;
}
.stButton button:hover, .stDownloadButton button:hover { opacity: 0.9; }

/* File uploader drop zone */
section[data-testid="stFileUploaderDropzone"] {
    background-color: var(--surface) !important;
    border: 1px dashed #2E3440 !important;
}
section[data-testid="stFileUploaderDropzone"] button {
    background-color: var(--surface-2) !important;
    color: var(--text) !important;
    border: 1px solid #2E3440 !important;
}
section[data-testid="stFileUploaderDropzone"] span,
section[data-testid="stFileUploaderDropzone"] small,
section[data-testid="stFileUploaderDropzone"] div {
    color: var(--muted) !important;
}
label, .stMarkdown, p { color: var(--text) !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    """
<div class="vbcua-hero">
    <div class="vbcua-eyebrow">SPEECH &amp; CONCEPT EVALUATION</div>
    <div class="vbcua-title">🎙️ Voice-Based Concept Understanding Analyser</div>
    <div class="vbcua-subtitle">
        Upload a spoken explanation of a concept. The system transcribes your speech,
        measures how closely it matches the core idea, and scores your delivery —
        fluency, pauses, and clarity — in one evaluation.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
concept = st.selectbox("Concept you're explaining", list(REFERENCE_CONCEPTS.keys()))
audio_file = st.file_uploader(
    "Upload your spoken explanation", type=["wav", "mp3", "m4a"]
)

if audio_file is not None:
    with tempfile.NamedTemporaryFile(
        delete=False, suffix="." + audio_file.name.split(".")[-1]
    ) as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    st.audio(audio_file)

    if st.button("Analyze recording"):
        with st.spinner("Transcribing and scoring your explanation..."):
            result = evaluate_explanation(tmp_path, concept)

        fr = result["final_result"]

        # Verdict
        st.markdown(
            f'<div class="vbcua-verdict">{fr["label"]} — {fr["final_score"]:.2f} / 1.00</div>',
            unsafe_allow_html=True,
        )

        # Score cards
        st.markdown('<div class="vbcua-card-row">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="vbcua-card">
                <div class="vbcua-card-label">Semantic Score</div>
                <div class="vbcua-card-value">{fr['semantic_score']:.2f}</div>
            </div>
            <div class="vbcua-card">
                <div class="vbcua-card-label">Understanding</div>
                <div class="vbcua-card-value teal" style="font-size:1.1rem;">{result['understanding_label']}</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="vbcua-card-row">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="vbcua-card">
                <div class="vbcua-card-label">Fluency Score</div>
                <div class="vbcua-card-value">{fr['fluency_score']:.2f}</div>
            </div>
            <div class="vbcua-card">
                <div class="vbcua-card-label">Filler Words Used</div>
                <div class="vbcua-card-value teal">{result['filler_words']['total']}</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # AI-generated feedback
        from modules.feedback_generator import generate_feedback
        st.markdown('<div class="vbcua-section-label">🤖 AI Feedback</div>', unsafe_allow_html=True)
        with st.spinner("Generating personalized feedback..."):
            feedback_text = generate_feedback(result)
        st.markdown(f'<div class="vbcua-transcript">{feedback_text}</div>', unsafe_allow_html=True)

        # Transcript
        st.markdown(
            '<div class="vbcua-section-label">📝 Transcript</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="vbcua-transcript">{result["transcript"]}</div>',
            unsafe_allow_html=True,
        )

        # Waveform — restyled to match dark theme
        st.markdown(
            '<div class="vbcua-section-label">🔊 Waveform</div>', unsafe_allow_html=True
        )
        y, sr = librosa.load(tmp_path, sr=16000)

        plt.rcParams["font.family"] = "sans-serif"
        fig, ax = plt.subplots(figsize=(10, 2.6))
        fig.patch.set_facecolor("#1E2229")
        ax.set_facecolor("#1E2229")
        librosa.display.waveshow(y, sr=sr, ax=ax, color="#4FD1C5")
        ax.set_xlabel("Time (s)", color="#8B92A0")
        ax.tick_params(colors="#8B92A0")
        for spine in ax.spines.values():
            spine.set_color("#2E3440")
        st.pyplot(fig)

        # PDF report download
        from modules.report_generator import generate_pdf_report

        pdf_path = generate_pdf_report(result, tmp_path)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name=f"VBCUA_Report_{concept.replace(' ', '_')}.pdf",
                mime="application/pdf",
            )
