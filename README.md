# 🎧 AI Call Quality Auditor

This application acts as an automated Quality Assurance (QA) specialist for customer service calls. It uses Google's advanced **Gemini 2.5 AI** models to analyze conversation dynamics, detect compliance issues, and evaluate agent performance.

## 🚀 How It Works

### 1. **Input Processing**
You can provide data in two ways:
*   **Text Transcript**: Paste a raw transcript of the conversation (Agent vs. Customer).
*   **Audio File**: Upload an audio recording (`.mp3`, `.wav`, etc.). The app sends the audio file directly to Gemini's multimodal API, which "listens" to the call without needing a separate transcription step.

### 2. **AI Analysis**
Once you click **Analyze Call**, the app sends the data to the **Google Gemini API** with a strictly engineered prompt. The AI is instructed to look for:
*   ❌ Rude or unprofessional behavior
*   😤 Customer frustration markers
*   ⚠️ Escalation triggers (requests for a manager, threats to cancel)
*   📜 Policy & compliance violations
*   🤥 Misinformation
*   ⚖️ Legal risks

### 3. **Smart Fallback System**
The app is built for reliability. It automatically tries the best available model for your API key, cycling through:
1.  `gemini-2.5-flash` (Fastest & Newest)
2.  `gemini-2.0-flash`
3.  `gemini-1.5-flash`

### 4. **Structured Output**
The AI returns a structured JSON response containing:
*   **Pass/Fail Status**: An overall verdict on the call quality.
*   **Sentiment**: The prevailing mood (Positive, Neutral, Negative).
*   **Top Concerns**: A bulleted list of any critical issues found.
*   **Evidence**: Direct quotes or timestamps from the call to support its findings.

## 🛠️ Tech Stack
*   **Frontend**: [Streamlit](https://streamlit.io/) (Python-based web UI)
*   **Backend Intelligence**: [Google Gemini API](https://ai.google.dev/)
*   **Dependency Management**: `uv` (Fast Python package installer)

## 🔑 Setup
1.  Get an API Key from [Google AI Studio](https://aistudio.google.com/).
2.  Add it to a `.env` file (`API_KEY=your_key`) or enter it in the sidebar.
3.  Run with `uv run streamlit run app.py`.
