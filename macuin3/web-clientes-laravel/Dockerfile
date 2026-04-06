FROM php:8.3-cli

RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip git curl libzip-dev libpq-dev \
    && docker-php-ext-install zip pdo pdo_pgsql \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www

# Create required directories FIRST
RUN mkdir -p bootstrap/cache \
    storage/framework/sessions \
    storage/framework/views \
    storage/framework/cache \
    storage/logs \
    && chmod -R 777 bootstrap/cache storage

COPY composer.json .
RUN composer install --no-interaction --no-scripts 2>/dev/null || true

COPY . .

# Ensure permissions after copy
RUN chmod -R 777 bootstrap/cache storage \
    && composer install --no-interaction --optimize-autoloader \
    && cp -n .env.example .env 2>/dev/null || true \
    && php artisan key:generate --force 2>/dev/null || true \
    && php artisan config:clear 2>/dev/null || true

EXPOSE 8080

CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8080"]
