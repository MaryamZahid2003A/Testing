FROM php:8.2-apache

# Install mysqli extension
RUN docker-php-ext-install mysqli

# Copy app files to Apache server root
COPY ./app /var/www/html/

# Enable Apache mod_rewrite (optional but common)
RUN a2enmod rewrite