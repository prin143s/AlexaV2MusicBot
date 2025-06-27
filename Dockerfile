
FROM python:3.10-slim

# Environment variables to disable cache
ENV PIP_NO_CACHE_DIR=yes
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Start the bot
CMD ["python3", "main.py"]
