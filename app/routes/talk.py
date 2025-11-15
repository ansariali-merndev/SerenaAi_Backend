from flask import Blueprint, request, jsonify
from app.utils.response import error_response
from openai import OpenAI
from app.utils.token_decorator import token_required
from app.env import GROQ_API_KEY
from app.models.analysis import Analysis
from app.utils.constant import SYSTEM_PROMPT
from app.extensions import db
import os
import json
import base64
from gtts import gTTS
import io

talk_bp = Blueprint("talk", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def text_to_speech_gtts(text, language='en'):
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        
        audio_base64 = base64.b64encode(audio_io.read()).decode('utf-8')
        return audio_base64
        
    except Exception as e:
        return None

@talk_bp.route("/talk", methods=["POST"])
@token_required
def talk(user_id):
    try:
        if 'audio' not in request.files:
            return jsonify({
                "success": False,
                "message": "No audio file recieved"
            }), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({
                "success": False,
                "message": "No audio file selected"
            }), 400
        
        audio_path = os.path.join(UPLOAD_FOLDER, "temp_recording.webm")
        audio_file.save(audio_path)
        
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        
        with open(audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=file,
                response_format="text"
            )
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        user_text = transcription.strip()
        
        if not user_text:
            return jsonify({
                "success": False,
                "error": "Could not transcribe audio. Please try again.",
                "suggestion": "Speak clearly and ensure your microphone is working."
            }), 200
        
        chat_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        response_text = chat_response.choices[0].message.content.strip()
        
        try:
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            analysis_result = json.loads(response_text)
            
            is_err_resp = analysis_result.get("error")
            
            audio_data = {}
            if not is_err_resp:
                summary_text = analysis_result.get("summary", "")
                if summary_text:
                    summary_audio = text_to_speech_gtts(summary_text)
                    if summary_audio:
                        audio_data["summary_audio"] = summary_audio
                
                suggestion_text = analysis_result.get("suggestion", "")
                if suggestion_text:
                    suggestion_audio = text_to_speech_gtts(suggestion_text)
                    if suggestion_audio:
                        audio_data["suggestion_audio"] = suggestion_audio
                
                audio_data["mime_type"] = "audio/mpeg"
                
                new_analysis = Analysis(
                    anger=analysis_result.get("anger", 0),
                    anxiety=analysis_result.get("anxiety", 0),
                    calmness=analysis_result.get("calmness", 0),
                    happiness=analysis_result.get("happiness", 0),
                    sadness=analysis_result.get("sadness", 0),
                    stress=analysis_result.get("stress", 0),
                    user_id=user_id
                )
            
                db.session.add(new_analysis)
                db.session.commit()
            else:
                summary_text = analysis_result.get("error", "")
                if summary_text:
                    summary_audio = text_to_speech_gtts(summary_text)
                    if summary_audio:
                        audio_data["summary_audio"] = summary_audio
                
                suggestion_text = analysis_result.get("suggestion", "")
                if suggestion_text:
                    suggestion_audio = text_to_speech_gtts(suggestion_text)
                    if suggestion_audio:
                        audio_data["suggestion_audio"] = suggestion_audio
                
                audio_data["mime_type"] = "audio/mpeg"
            
            response_data = {
                "success": not is_err_resp,
                "result": analysis_result,
                "audio": audio_data if audio_data else ""
            }
            
            return jsonify(response_data), 200
            
        except json.JSONDecodeError:
            return jsonify({
                "success": False,
                "error": "Failed to analyze emotions properly.",
                "suggestion": "Please try again with clear audio."
            }), 200
        
    except Exception as e:
        return error_response(e)