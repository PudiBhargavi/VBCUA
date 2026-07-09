# VBCUA — Voice-Based Concept Understanding Analyser

An AI-powered web application that evaluates how effectively a user understands
and explains a concept through spoken communication. VBCUA combines speech-to-text
transcription (OpenAI Whisper), semantic similarity analysis (Sentence-BERT), audio
fluency analysis (Librosa), and AI-generated feedback (Google Gemini) into a single
evaluation pipeline, with a Streamlit dashboard and downloadable PDF reports.

🔗 **Live Demo:** https://malfoydraco-vbcua.hf.space

Built as part of the SmartBridge Virtual Internship Program (Google Cloud / GenAI track).

## Repository Structure

This repository follows the project's 8-phase documentation structure:

1. **Brainstorming & Ideation** — Problem statement, brainstorming, empathy map
2. **Requirement Analysis** — Technology stack, solution requirements, data flow diagram, customer journey map
3. **Project Design Phase** — Problem-solution fit, proposed solution, solution architecture
4. **Project Planning Phase** — Milestones, task allocation, sprint planning
5. **Project Development Phase** — Source code and development documentation
6. **Project Testing** — Functional and performance testing results
7. **Project Documentation** — Final report, executable files guide
8. **Project Demonstration** — Demo planning, feature demonstration, team involvement

## Tech Stack

- **Frontend:** Streamlit
- **Speech-to-Text:** OpenAI Whisper
- **Semantic Analysis:** Sentence-BERT (sentence-transformers)
- **Audio Processing:** Librosa
- **AI Feedback:** Google Gemini API
- **PDF Reports:** fpdf2
- **Deployment:** Docker + Hugging Face Spaces

## How to Run Locally

1. Clone the repository:
    ```bash
    git clone https://github.com/PudiBhargavi/VBCUA.git
    cd "VBCUA/5. Project Development Phase"
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate   # Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Install ffmpeg and ensure it's added to your system PATH (required by Whisper)

5. Create a `.env` file in the same folder with your Gemini API key:
    ```text
    GEMINI_API_KEY=your_key_here
    ```

6. Run the application:
    ```bash
    streamlit run app.py
    ```

7. Open your browser at `http://localhost:8501`

## Team

- **Team Lead:** Pudi Bhargavi — Core AI pipeline, backend, UI, deployment
- **Team Member:** Kanderi Bhavana — Project documentation

## License

This project was developed as part of an academic virtual internship program.

## Acknowledgements

Developed as part of the SmartBridge Virtual Internship Program in collaboration with Google Cloud (Generative AI Track).

## 🎥 Project Demo

▶ **Watch the Demo on YouTube:**  
https://youtu.be/_ArJnygVXp0

📁 **Google Drive Backup**
https://drive.google.com/file/d/15D7ALl3BlUrjWlFotnxEsmq6dvD_WU2L/view?usp=sharing
