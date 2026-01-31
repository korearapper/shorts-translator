FROM python:3.11-slim

# ffmpeg 설치 (수정됨)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 의존성 먼저 설치 (캐싱 활용)
COPY shorts-translator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY shorts-translator/ .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--timeout", "300", "--workers", "2"]
