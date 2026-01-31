import os
import uuid
import tempfile
import subprocess
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
import requests

app = Flask(__name__)
CORS(app)

# ElevenLabs API 설정
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY', '')

# 일본어 음성 ID (ElevenLabs - Yuki)
JAPANESE_VOICE_ID = "yoZ06aMxZJJ28mfd3POQ"

# 임시 파일 저장 경로
TEMP_DIR = tempfile.gettempdir()
OUTPUT_DIR = os.path.join(TEMP_DIR, 'shorts_output')
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/translate', methods=['POST'])
def translate_video():
    try:
        data = request.json
        youtube_url = data.get('url')
        
        if not youtube_url:
            return jsonify({'error': 'YouTube URL이 필요합니다'}), 400
        
        job_id = str(uuid.uuid4())[:8]
        
        # 1. 유튜브 영상 다운로드
        video_path = download_youtube(youtube_url, job_id)
        if not video_path:
            return jsonify({'error': '영상 다운로드 실패'}), 500
        
        # 2. 오디오 추출
        audio_path = extract_audio(video_path, job_id)
        if not audio_path:
            return jsonify({'error': '오디오 추출 실패'}), 500
        
        # 3. 음성 인식 (한국어)
        korean_text = transcribe_audio(audio_path)
        if not korean_text:
            return jsonify({'error': '음성 인식 실패'}), 500
        
        # 4. 번역 (한국어 → 일본어)
        japanese_text = translate_text(korean_text)
        if not japanese_text:
            return jsonify({'error': '번역 실패'}), 500
        
        # 5. 일본어 TTS 생성
        japanese_audio_path = generate_japanese_tts(japanese_text, job_id)
        if not japanese_audio_path:
            return jsonify({'error': 'TTS 생성 실패'}), 500
        
        # 6. 영상 + 새 오디오 합성
        output_path = merge_video_audio(video_path, japanese_audio_path, job_id)
        if not output_path:
            return jsonify({'error': '영상 합성 실패'}), 500
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'korean_text': korean_text,
            'japanese_text': japanese_text,
            'download_url': f'/api/download/{job_id}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<job_id>')
def download_video(job_id):
    output_path = os.path.join(OUTPUT_DIR, f'{job_id}_final.mp4')
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True, download_name=f'japanese_shorts_{job_id}.mp4')
    return jsonify({'error': '파일을 찾을 수 없습니다'}), 404


def download_youtube(url, job_id):
    try:
        output_path = os.path.join(OUTPUT_DIR, f'{job_id}_original.mp4')
        
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return output_path
    except Exception as e:
        print(f"다운로드 오류: {e}")
        return None


def extract_audio(video_path, job_id):
    try:
        audio_path = os.path.join(OUTPUT_DIR, f'{job_id}_audio.wav')
        
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn', '-acodec', 'pcm_s16le',
            '-ar', '16000', '-ac', '1',
            '-y', audio_path
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        return audio_path
    except Exception as e:
        print(f"오디오 추출 오류: {e}")
        return None


def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="ko")
        return result['text']
    except Exception as e:
        print(f"음성 인식 오류: {e}")
        return None


def translate_text(korean_text):
    try:
        translator = GoogleTranslator(source='ko', target='ja')
        japanese_text = translator.translate(korean_text)
        return japanese_text
    except Exception as e:
        print(f"번역 오류: {e}")
        return None


def generate_japanese_tts(text, job_id):
    try:
        audio_path = os.path.join(OUTPUT_DIR, f'{job_id}_japanese.mp3')
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{JAPANESE_VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open(audio_path, 'wb') as f:
                f.write(response.content)
            return audio_path
        else:
            print(f"TTS 오류: {response.text}")
            return None
            
    except Exception as e:
        print(f"TTS 생성 오류: {e}")
        return None


def merge_video_audio(video_path, audio_path, job_id):
    try:
        output_path = os.path.join(OUTPUT_DIR, f'{job_id}_final.mp4')
        
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-shortest',
            '-y', output_path
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        return output_path
    except Exception as e:
        print(f"영상 합성 오류: {e}")
        return None


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
