# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    wget \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Selenium to use Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test files
COPY . .

CMD ["python3", "-m", "unittest", "-v", "tests/test_taskmanager.py"]
