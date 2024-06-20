FROM python:3.9-slim-bullseye

WORKDIR /app

COPY main.py requirements.txt ./

RUN apt update && apt install -y build-essential && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]