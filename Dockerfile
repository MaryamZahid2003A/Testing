# ✅ Use lightweight Python base image
FROM python:3.12-slim

# ✅ Set working directory inside container
WORKDIR /app

# ✅ Install system packages: Apache, PHP, Selenium dependencies
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

# ✅ Set environment variables for Selenium to locate Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# ✅ Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Clean Apache default HTML folder & copy your PHP app
RUN rm -rf /var/www/html/*
COPY app/ /var/www/html/
RUN chown -R www-data:www-data /var/www/html

# ✅ Copy test files and startup script
COPY tests/ /app/tests/
COPY entrypoint.sh .

# ✅ Enable Apache modules & set basic config
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf && \
    a2enmod rewrite

# ✅ Show PHP errors (optional for dev/debug)
RUN echo "display_errors=On\nerror_reporting=E_ALL" >> $(php --ini | grep "Loaded Configuration" | awk '{print $4}')

# ✅ Ensure entrypoint is executable
RUN chmod +x entrypoint.sh

# ✅ Expose Apache web port
EXPOSE 80

# ✅ Default command
CMD ["./entrypoint.sh"]
