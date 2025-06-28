FROM python:3.12-slim

WORKDIR /app

# Install Chrome, PHP and dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    apache2 \
    php \
    libapache2-mod-php \
    wget \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Enable PHP site
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf \
    && a2enmod rewrite

# Set environment variables for Selenium to use Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files (PHP app and tests)
COPY . .

# Add entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Start Apache and then run tests
CMD ["./entrypoint.sh"]
