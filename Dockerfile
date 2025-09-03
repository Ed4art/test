FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1 PYTHONIOENCODING=utf-8

# Бот запускается как фон-процесс (long polling), веб-порт не нужен
CMD ["python", "bot.py"]
