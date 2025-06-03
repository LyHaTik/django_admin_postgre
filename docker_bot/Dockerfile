FROM python:3.10.5-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY ./bot /bot/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat

CMD ["python", "main.py"]
