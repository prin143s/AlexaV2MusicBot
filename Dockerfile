FROM python:3.10-slim

ENV PIP_NO_CACHE_DIR=yes
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .

# Install git + pip upgrade tools
RUN apt-get update && apt-get install -y git
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
