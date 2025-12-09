import streamlit as st
from analyzer import analyze_call
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Call Quality Auditor",
    page_icon="🎧",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .pass-tag {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    .fail-tag {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    .status-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-header">🎧 AI Call Quality Auditor</div>', unsafe_allow_html=True)

    # --- Sidebar / Configuration ---
    with st.sidebar:
        st.header("Configuration")
        
        # 1. API Key Handling
        env_api_key = os.getenv("API_KEY")
        if env_api_key:
            st.success("✅ API Key loaded from environment")
            api_key = env_api_key
        else:
            api_key = st.text_input("Enter Gemini API Key", type="password")
            st.info("Tip: Create a `.env` file with `API_KEY=your_key` to skip this.")
            st.markdown("[Get API Key](https://aistudio.google.com/)")

        st.markdown("---")
        with st.expander("Troubleshoot"):
            st.write("If analysis fails, check your API key permissions.")
            if st.button("Clear Cache / Restart"):
                st.rerun()

    # --- Main Content ---
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("1. Input Data")
        
        tab_text, tab_audio = st.tabs(["📝 Text Transcript", "🎤 Audio File"])
        
        transcript_input = None
        audio_file_path = None
        
        with tab_text:
            transcript_input = st.text_area("Paste call transcript:", height=400, placeholder="Agent: Hello...\nCustomer: ...")
            
        with tab_audio:
            uploaded_file = st.file_uploader("Upload Audio (MP3, WAV)", type=['mp3', 'wav', 'm4a', 'ogg'])
            if uploaded_file:
                # Save temp file
                audio_file_path = f"temp_{uploaded_file.name}"
                with open(audio_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.audio(uploaded_file)
                st.success(f"Uploaded: {uploaded_file.name}")

        analyze_btn = st.button("🚀 Analyze Call", type="primary", use_container_width=True)

    with col2:
        st.subheader("2. Analysis Results")
        
        if analyze_btn:
            # Input Validation
            if not api_key:
                st.error("❌ Missing API Key. Please configure it in the sidebar.")
                st.stop()
            
            if not transcript_input and not audio_file_path:
                st.warning("⚠️ Please provide a transcript or upload an audio file.")
                st.stop()

            # Process
            with st.spinner("🤖 AI is analyzing the call..."):
                try:
                    result = analyze_call(
                        transcript=transcript_input,
                        api_key=api_key,
                        audio_path=audio_file_path
                    )
                    
                    # Cleanup
                    if audio_file_path and os.path.exists(audio_file_path):
                        os.remove(audio_file_path)

                    # --- Display Results ---
                    
                    # Pass/Fail Banner
                    status = result.get("pass_fail", "Unknown").upper()
                    if "PASS" in status:
                        st.markdown(f'<div class="status-container"><div class="pass-tag">✅ {status}</div></div>', unsafe_allow_html=True)
                    elif "FAIL" in status or "HIGH" in status:
                        st.markdown(f'<div class="status-container"><div class="fail-tag">❌ {status}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="status-container"><b>Status: {status}</b></div>', unsafe_allow_html=True)

                    st.markdown("### Summary")
                    st.write(f"**Sentiment:** {result.get('sentiment', 'N/A')}")
                    
                    st.markdown("### ⚠️ Top Concerns")
                    concerns = result.get("top_concerns", [])
                    if concerns:
                        for c in concerns:
                            st.write(f"- {c}")
                    else:
                        st.write("No major concerns.")
                        
                    st.markdown("### 🔍 Evidence")
                    evidence = result.get("evidence", [])
                    if evidence:
                        for e in evidence:
                            st.info(f'"{e}"')
                    else:
                        st.write("No specific evidence cited.")

                except Exception as e:
                    st.error(f"Analysis Error: {str(e)}")
                    if audio_file_path and os.path.exists(audio_file_path):
                        os.remove(audio_file_path)

if __name__ == "__main__":
    main()
