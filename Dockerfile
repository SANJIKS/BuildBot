FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
COPY main.py /app/main.py

WORKDIR /app

CMD ["python", "main.py"]
