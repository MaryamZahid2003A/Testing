# app/Dockerfile

FROM php:8.1-apache

# Enable required PHP extensions
RUN docker-php-ext-install mysqli

# Enable Apache rewrite
RUN a2enmod rewrite

# Copy app code to web root
COPY . /var/www/html/

# Set file ownership
RUN chown -R www-data:www-data /var/www/html
