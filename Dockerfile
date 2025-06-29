# Use a lightweight Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install required system packages including Apache, PHP, and Chromium
RUN apt-get update && apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php \
    php-mysqli \
    chromium \
    chromium-driver \
    curl \
    unzip \
    wget \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Selenium to locate Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Copy Python dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . .

# Make sure PHP files (like signup.php) are copied to Apache's web root
RUN mkdir -p /var/www/html && \
    cp -r app/* /var/www/html/ && \
    chown -R www-data:www-data /var/www/html

# Enable Apache modules and set server name
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf && \
    a2enmod rewrite

# Fix PHP error reporting (optional, version-agnostic way)
RUN echo "display_errors=On\nerror_reporting=E_ALL" >> $(php --ini | grep "Loaded Configuration" | awk '{print $4}')

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose Apache port
EXPOSE 80

# Run Apache and Selenium tests
CMD ["./entrypoint.sh"]
