FROM python:3.10-slim


# System dependencies
RUN apt update && apt install -y ffmpeg libopus-dev libwebp-dev git

# Create working directory
WORKDIR /app

# Copy files
COPY . /app

# Install Python deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Start bot
CMD ["python", "main.py"]
