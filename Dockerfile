FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install Apache, PHP, Chrome, and dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    apache2 \
    php \
    libapache2-mod-php \
    php-mysqli \
    wget \
    unzip \
    curl \
    nano \
    && rm -rf /var/lib/apt/lists/*

# PHP errors shown in browser (optional)
RUN echo "display_errors=On\nerror_reporting=E_ALL" >> /etc/php/7.4/apache2/php.ini || true

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything into container
COPY . .

# Copy PHP files to Apache root
RUN cp -r app/* /var/www/html/

# Permissions
RUN chown -R www-data:www-data /var/www/html

# Enable mod_rewrite and ServerName
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf && \
    a2enmod rewrite

# Set executable entrypoint
RUN chmod +x entrypoint.sh

EXPOSE 80

# Start Apache and run Selenium tests
CMD ["./entrypoint.sh"]
