FROM php:8.2-apache

RUN docker-php-ext-install mysqli

COPY wait-for-db.sh /wait-for-db.sh
COPY ./app /var/www/html/

RUN chmod +x /wait-for-db.sh && a2enmod rewrite

CMD ["/wait-for-db.sh"]
