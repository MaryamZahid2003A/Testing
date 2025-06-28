FROM python:3.12-slim

WORKDIR /app

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    php \
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

# Copy all files (including tests and web app)
COPY . .

# Add entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run your custom script
CMD ["./entrypoint.sh"]
