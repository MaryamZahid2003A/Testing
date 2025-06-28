FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 chromium chromium-driver

# Install Python packages
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project
COPY . /app

# Default command (can be overridden by Jenkins)
CMD ["pytest", "tests/"]
