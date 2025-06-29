FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install required system packages
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

# Configure PHP error display (optional but useful)
RUN echo "display_errors=On\nerror_reporting=E_ALL" >> /etc/php/7.4/apache2/php.ini || true

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into /app
COPY . /app

# Copy PHP files to Apache root
RUN cp -r /app/app/* /var/www/html/

# Give proper permissions
RUN chown -R www-data:www-data /var/www/html

# Enable Apache rewrite module and set ServerName
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf && \
    a2enmod rewrite

# Copy and make entrypoint executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port 80 for web
EXPOSE 80

# Start Apache and run tests
CMD ["/app/entrypoint.sh"]
