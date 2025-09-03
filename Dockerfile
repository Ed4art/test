FROM python:3.12-slim
WORKDIR /app

# Чтоб логи сразу выводились и не забивался кеш pip
ENV PYTHONUNBUFFERED=1 PYTHONIOENCODING=utf-8 PIP_NO_CACHE_DIR=1

# Иногда нужны базовые инструменты сборки для зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Никаких портов — это long polling
CMD ["python", "bot.py"]
