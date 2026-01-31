# 🇰🇷→🇯🇵 Shorts Translator

한국 유튜브 숏츠를 일본어 더빙 버전으로 자동 변환하는 웹 서비스입니다.

![Demo](https://img.shields.io/badge/Status-Ready-brightgreen)

## ✨ 기능

- 🎬 유튜브 숏츠 자동 다운로드
- 🎤 한국어 음성 인식 (Whisper AI)
- 🔄 한국어 → 일본어 자동 번역
- 🗣️ 자연스러운 일본어 더빙 (ElevenLabs)
- 🎥 영상 + 새 오디오 합성

---

## 🚀 Railway 배포 가이드 (5분 완료!)

### Step 1: GitHub에 코드 업로드

1. [GitHub](https://github.com) 로그인
2. 우측 상단 `+` → `New repository` 클릭
3. Repository name: `shorts-translator`
4. `Create repository` 클릭
5. 터미널에서 아래 명령어 실행:

```bash
cd shorts-translator
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shorts-translator.git
git push -u origin main
```

### Step 2: Railway 계정 생성 & 연결

1. [Railway](https://railway.app) 접속
2. `Start a New Project` 클릭
3. `Deploy from GitHub repo` 선택
4. GitHub 계정 연결 (처음이면)
5. `shorts-translator` 레포지토리 선택

### Step 3: 환경변수 설정 ⚠️ 중요!

1. Railway 대시보드에서 프로젝트 클릭
2. `Variables` 탭 클릭
3. `+ New Variable` 클릭
4. 아래 내용 추가:

| Variable | Value |
|----------|-------|
| `ELEVENLABS_API_KEY` | `sk_c76e9e19c597a207dc7e734c5f4fe42ca26800752d48db46` |

5. `Add` 클릭

### Step 4: 도메인 생성

1. `Settings` 탭 클릭
2. `Networking` 섹션에서 `Generate Domain` 클릭
3. 생성된 URL (예: `https://shorts-translator-xxxx.up.railway.app`)

### Step 5: 완료! 🎉

생성된 URL을 팀원들에게 공유하세요!

---

## 🖥️ 로컬 실행 (테스트용)

```bash
# 1. 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. FFmpeg 설치
# Mac: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: https://ffmpeg.org/download.html

# 4. 환경변수 설정
export ELEVENLABS_API_KEY=sk_c76e9e19c597a207dc7e734c5f4fe42ca26800752d48db46

# 5. 서버 실행
python app.py

# 6. 브라우저에서 접속
# http://localhost:5000
```

---

## 📁 프로젝트 구조

```
shorts-translator/
├── app.py              # Flask 백엔드 서버
├── templates/
│   └── index.html      # 웹 UI
├── requirements.txt    # Python 의존성
├── nixpacks.toml       # Railway 배포 설정
├── .env.example        # 환경변수 예시
└── README.md           # 이 파일
```

---

## ⚙️ 기술 스택

| 기술 | 용도 |
|------|------|
| Flask | 웹 서버 |
| yt-dlp | 유튜브 다운로드 |
| Whisper | 음성 인식 |
| deep-translator | 번역 |
| ElevenLabs | 일본어 TTS |
| FFmpeg | 영상 처리 |

---

## 🔧 트러블슈팅

### "영상 다운로드 실패" 오류
- 유튜브 URL이 올바른지 확인
- Shorts URL 형식: `https://youtube.com/shorts/VIDEO_ID`

### "TTS 생성 실패" 오류
- ElevenLabs API 키가 올바른지 확인
- ElevenLabs 무료 크레딧 잔액 확인

### 배포 후 작동 안 함
- Railway Variables에 API 키가 제대로 설정되었는지 확인
- Railway Logs에서 오류 메시지 확인

---

## 💰 비용

- **Railway**: 무료 티어 (월 $5 크레딧)
- **ElevenLabs**: 무료 티어 (월 10,000자)

일반적인 사용량으로는 **무료**로 사용 가능합니다!

---

## 📞 문의

문제가 있으면 GitHub Issues에 등록해주세요.

---

Made with ❤️ for Korean → Japanese content creators
