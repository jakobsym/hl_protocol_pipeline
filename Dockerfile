FROM python:3.9-slim

# force output to stdout/stderr
# prevent .pyc files from being created
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy rest of code
COPY . .

RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "src/main.py"]