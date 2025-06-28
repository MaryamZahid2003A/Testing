FROM python:3.12-slim

WORKDIR /app

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

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 80

CMD ["./entrypoint.sh"]
