import google.generativeai as genai
import json
import typing_extensions as typing
import time
import os

# Define the output structure
class CallAnalysis(typing.TypedDict):
    pass_fail: str
    sentiment: str
    top_concerns: list[str]
    evidence: list[str]

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            time.sleep(2)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")

def analyze_call(transcript: str | None, api_key: str, audio_path: str | None = None) -> CallAnalysis:
    """
    Analyzes a call transcript or audio using Google Gemini API.
    """
    if not api_key:
        raise ValueError("API Key is required.")
    
    if not transcript and not audio_path:
         raise ValueError("Either transcript or audio file must be provided.")

    genai.configure(api_key=api_key)
    
    # 1. Prepare Content Parts
    content_parts = []
    
    base_prompt = """
    You are an expert Call Quality Auditor. Your job is to analyze the following call and evaluate it based on specific criteria.

    **Analyze this call and tell me if it is a bad call or high-concern call.**
    
    **Look for:**
    - Rude or unprofessional agent behavior
    - Customer frustration
    - Escalation triggers
    - Policy/compliance violations
    - Misinformation
    - Safety or legal risks
    - Repeated unresolved issues
    """
    content_parts.append(base_prompt)

    if audio_path:
        # Upload processing
        print(f"Uploading audio file: {audio_path}")
        audio_file = upload_to_gemini(audio_path, mime_type="audio/mp3") # Generic fallback
        wait_for_files_active([audio_file])
        content_parts.append("Here is the audio recording of the call:")
        content_parts.append(audio_file)
    
    if transcript:
        content_parts.append("**Transcript:**")
        content_parts.append(transcript)

    content_parts.append("""
    **Output Requirements:**
    Return a JSON object with the following structure:
    {
        "pass_fail": "Pass" or "Fail",
        "sentiment": "Positive", "Neutral", or "Negative",
        "top_concerns": ["List", "of", "top", "concerns"],
        "evidence": ["List", "of", "specific", "evidence", "quotes", "from", "the", "call"]
    }
    
    If the call is a "Fail" or "High Concern", ensure you clearly list the reasons in "top_concerns" and provide quotes in "evidence".
    """)
    
    # 2. Model Fallback Logic
    # We try specific versions available to the user first
    model_names_to_try = [
        'gemini-2.5-flash',
        'gemini-2.0-flash',
        'gemini-2.0-flash-001',
        'gemini-1.5-flash' # Fallback
    ]
    
    response_text = None
    last_error = None

    for model_name in model_names_to_try:
        try:
            print(f"Trying model: {model_name}")
            model = genai.GenerativeModel(model_name, generation_config={"response_mime_type": "application/json"})
            response = model.generate_content(content_parts)
            response_text = response.text
            print(f"Success with model: {model_name}")
            break
        except Exception as e:
            print(f"Failed with model {model_name}: {e}")
            last_error = e
            continue

    if not response_text:
         # Try to list available models to help debugging
         available_models = []
         try:
             for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
         except:
             available_models = ["Could not list models"]

         return {
            "pass_fail": "Error",
            "sentiment": "Error",
            "top_concerns": [
                f"All specific models failed. Last error: {str(last_error)}", 
                f"Available Models for your Key: {', '.join(available_models)}"
            ],
            "evidence": []
        }

    # 3. Parse Result
    try:
        result = json.loads(response_text)
        return result
    except Exception as e:
        # If we failed to parse, or if we fell through all models (response_text is None check handled above)
        # But wait, if response_text IS None, we returned earlier.
        # So this catch is for JSON parsing.
        
        # Let's add a robust check: IF valid response but JSON fail, return error.
        return {
            "pass_fail": "Error",
            "sentiment": "Error",
            "top_concerns": [f"JSON Parsing failed: {str(e)}", f"Raw output: {response_text[:100]}..."],
            "evidence": []
        }

    # Note: The 'Everything failed' return is above at line 110.
    # We need to enhance THAT one.
