FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir requests typer

ENTRYPOINT ["python", "app/cli/main.py"]