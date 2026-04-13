FROM python:3.11-slim

ENV TZ=Asia/Seoul \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 시스템 의존성 (pdfplumber 등 최소)
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 파일
COPY . .

# SQLite 데이터 디렉토리 (Railway Volume 마운트 타깃)
RUN mkdir -p /app/data

# Railway PORT 동적 주입
EXPOSE 8080

# 시작 시: V29 PT 데이터 생성 후 gunicorn 실행
# --workers 1 (SQLite 동시 쓰기 제약), --timeout 120
CMD sh -c "python scripts/create_v29.py && gunicorn 'app:create_app()' --bind 0.0.0.0:${PORT:-8080} --workers 1 --timeout 120 --keep-alive 5 --access-logfile -"
