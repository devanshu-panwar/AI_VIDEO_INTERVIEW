import os
import re
import subprocess
import json
import ffmpeg
from google.cloud import speech
from google.api_core.exceptions import GoogleAPICallError, RetryError
import vertexai
from vertexai.preview.generative_models import GenerativeModel

# ==============================================================
# Initialize Gemini 2.0 Model
# ==============================================================
try:
    model = GenerativeModel("gemini-2.0-flash-001")
except Exception as e:
    print(f"⚠️ Warning: Gemini model initialization failed: {e}")
    model = None

# ==============================================================
# Helper: Determine form type from task_id
# ==============================================================
def determine_form_type(task_id: str) -> str:
    """
    Determines form type from the task_id.
    """
    if "technical_round" in task_id:
        return "technical"
    elif "hr_round" in task_id:
        return "hr"
    elif "cultural_fit" in task_id:
        return "cultural"
    else:
        return "unknown"

# ==============================================================
# Video Compression
# ==============================================================
def compress_video_wrapper(input_path, output_path, resolution="640x480", bitrate="500k"):
    try:
        width, height = resolution.split('x')
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vf", f"scale={width}:{height}",
            "-vcodec", "libx264",
            "-preset", "medium",
            "-b:v", bitrate,
            "-acodec", "aac",
            "-b:a", "64k",
            "-ac", "2",
            "-f", "mp4",
            "-movflags", "+faststart",
            output_path
        ]
        subprocess.run(command, check=True)
        print(f"✅ Video successfully compressed to: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error: {e}")
        raise

# ==============================================================
# Audio Extraction
# ==============================================================
def extract_audio_from_compressed_video(video_path, audio_path):
    """
    Extracts WAV audio from a given MP4/WebM video file using ffmpeg.
    """
    try:
        command = [
            "ffmpeg",
            "-i", video_path,
            "-ac", "1",
            "-ar", "16000",
            "-vn",
            "-f", "wav",
            "-acodec", "pcm_s16le",
            audio_path
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ Audio successfully extracted to: {audio_path}")
        return audio_path
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error while extracting audio: {e}")
        raise

# ==============================================================
# Google Cloud Speech-to-Text
# ==============================================================
def transcribe_with_vertex_ai(gcs_uri, language_code='en-IN'):
    """
    Transcribes audio using Google Cloud Speech-to-Text API.
    Auto-detects sample rate so we don't get empty results.
    """
    try:
        print(f"🔁 Sending to GCP STT: {gcs_uri}")
        client = speech.SpeechClient()

        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            language_code=language_code,
            enable_automatic_punctuation=True,
            model="default"
        )

        operation = client.long_running_recognize(config=config, audio=audio)
        print("⏳ Waiting for transcription to complete...")
        response = operation.result(timeout=600)
        print("✅ Transcription completed successfully.")

        if not response.results:
            print("⚠️ No transcription results returned.")
            return "No speech detected."

        transcript = []
        for result in response.results:
            if result.alternatives:
                transcript.append(result.alternatives[0].transcript)

        return "\n".join(transcript).strip()

    except (GoogleAPICallError, RetryError) as api_err:
        print("❌ Google API Error:", api_err)
        return f"[Error: {api_err}]"

    except Exception as e:
        print("❌ Unexpected error during transcription:", e)
        return f"[Transcription failed: {str(e)}]"

# ==============================================================
# Gemini Report Generators
# ==============================================================

def generate_hr_report_with_gemini(qa_pairs: list[dict]) -> str:
    """
    Generates a professional HR interview evaluation report using Gemini.
    """
    formatted_transcript = "\n\n".join(
        f"Q: {pair['question']}\nA: {pair['transcript']}" for pair in qa_pairs
    )

    prompt = f"""
You are an AI-powered HR assistant. Based on the structured interview transcript below,
generate a detailed and formal evaluation report.

Do not use asterisks (*). Use clean section headings.

Sections:
1. Candidate Introduction
2. Communication & Soft Skills
3. Behavioral Insights
4. Strengths & Positives
5. Areas of Concern or Improvement
6. Suggested Follow-up Questions
7. Final Recommendation

Transcript:
\"\"\"{formatted_transcript}\"\"\"
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.6,
            "top_p": 0.8,
            "top_k": 40
        }
    )

    return response.text.replace("*", "").strip()


def generate_technical_report_with_gemini(qa_pairs, model=model):
    """
    Generates a structured technical interview evaluation report.
    """
    formatted_qa = "\n\n".join([
        f"Q{i+1}: {pair['question']}\nExpected Answer: {pair['correct_answer']}\nCandidate Answer: {pair['transcript']}"
        for i, pair in enumerate(qa_pairs)
    ])

    prompt = f"""
You are an AI technical interview assistant. Below is the transcript of a technical interview.
For each question, the correct answer and the candidate’s response are provided.

Generate a structured report with sections:
1. Interview Summary
2. Strengths
3. Areas for Improvement
4. Communication & Confidence
5. Suggested Follow-up Questions
6. Final Assessment & Recommendation
7. Technical Score (out of 100)
8. Grammar & Fluency Score (out of 100)
9. Confidence Interval (High / Medium / Low)

Interview Data:
\"\"\"{formatted_qa}\"\"\"
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.5,
                "top_p": 0.85,
                "top_k": 40
            }
        )
        return response.text.replace("*", "").strip()
    except Exception as e:
        return f"[Error generating report: {e}]"


def generate_cultural_report_with_gemini(qa_pairs: list[dict]) -> dict:
    """
    Generates a professional Cultural Fit interview evaluation report using Gemini.
    """
    formatted_transcript = "\n\n".join(
        f"Q: {pair['question']}\nA: {pair['transcript']}" for pair in qa_pairs
    )

    prompt = f"""
You are an AI-powered cultural fit evaluation assistant.
Generate:
1. A detailed cultural fit evaluation report.
2. A JSON object with scores:
   - communication_score
   - teamwork_score
   - culture_alignment_score
   - final_recommendation

Do NOT use asterisks. Use clean section headings.

Transcript:
{formatted_transcript}
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.6,
                "top_p": 0.8,
                "top_k": 40
            }
        )
    except Exception as e:
        return {"report": "", "scores": {}, "error": f"Model generation failed: {e}"}

    cleaned_output = response.text.strip()
    json_match = re.search(r'\{.*?"communication_score".*?\}', cleaned_output, re.DOTALL)
    scores = {}
    report_text = cleaned_output
    error = None

    if json_match:
        json_text = json_match.group()
        try:
            scores = json.loads(json_text)
            report_text = cleaned_output.replace(json_text, "").replace("Report:", "").replace("JSON:", "").strip()
        except json.JSONDecodeError:
            error = "Failed to parse JSON from response."
    else:
        error = "Could not find a valid JSON section in the model output."

    return {"report": report_text, "scores": scores, "error": error}

# ==============================================================
# Report Section Parser
# ==============================================================
def parse_report_sections(text: str) -> dict:
    def extract(label_pattern: str) -> str:
        pattern = rf"{label_pattern}\s*\n(.*?)(?=\n\d+[\.\s]+|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def extract_list(label_pattern: str) -> list:
        return [q.strip() for q in extract(label_pattern).split("\n") if q.strip()]

    return {
        "introduction": extract(r"1[.\s]+Candidate Introduction"),
        "communication": extract(r"2[.\s]+Communication.*Soft Skills"),
        "behavioral_insights": extract(r"3[.\s]+Behavioral Insights"),
        "strengths": extract(r"4[.\s]+Strengths.*"),
        "concerns": extract(r"5[.\s]+Areas.*Improvement"),
        "follow_up_questions": extract_list(r"6[.\s]+Suggested Follow-up Questions"),
        "recommendation": extract(r"7[.\s]+Final Recommendation")
    }
