FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

WORKDIR /app

COPY vendor/pat-rotator/pat_rotator.py /app/pat_rotator.py
COPY rotate_and_submit.py /app/rotate_and_submit.py
COPY run.py /app/run.py

RUN pip install --no-cache-dir requests

CMD ["python3", "/app/run.py"]
