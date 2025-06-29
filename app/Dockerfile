# Use lightweight Python base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install Apache, PHP, and Chromium for Selenium
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

# Set env vars for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy only PHP app files to Apache's web root
RUN rm -rf /var/www/html/*   # Remove all existing files
COPY app/ /var/www/html/     
RUN chown -R www-data:www-data /var/www/html

# ✅ Copy test and support scripts to container
COPY tests/ /app/tests/
COPY entrypoint.sh .

# Enable Apache rewrite and set server name
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf && a2enmod rewrite

# Optional: show PHP errors
RUN echo "display_errors=On\nerror_reporting=E_ALL" >> $(php --ini | grep "Loaded Configuration" | awk '{print $4}')

# Ensure entrypoint is executable
RUN chmod +x entrypoint.sh

# Expose Apache HTTP port
EXPOSE 80

# Run Apache and Selenium test runner
CMD ["./entrypoint.sh"]
