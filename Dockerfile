# ✅ Base image
FROM python:3.12-slim

# ✅ Set working directory
WORKDIR /app

# ✅ Install system dependencies
RUN apt-get update && apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php \
    php-mysqli \
    curl \
    wget \
    unzip \
    nano \
    gnupg \
    ca-certificates \
    fonts-liberation \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ✅ Install Chromium browser & driver from official source
RUN apt-get update && \
    apt-get install -y chromium chromium-driver --no-install-recommends || echo "Chromium not available on slim base" && \
    rm -rf /var/lib/apt/lists/*

# ✅ Set Chromium path for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# ✅ Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy app and tests
COPY app/ /var/www/html/
COPY tests/ /app/tests/
COPY entrypoint.sh .

# ✅ Set permissions
RUN chown -R www-data:www-data /var/www/html

# ✅ Enable Apache modules
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf && \
    a2enmod rewrite

# ✅ Enable PHP error display for debugging
RUN echo "display_errors=On\nerror_reporting=E_ALL" >> $(php --ini | grep "Loaded Configuration" | awk '{print $4}')

# ✅ Make entrypoint executable
RUN chmod +x entrypoint.sh

EXPOSE 80

# ✅ Default command
CMD ["./entrypoint.sh"]
