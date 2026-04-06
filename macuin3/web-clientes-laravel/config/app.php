<?php
return [
    'name' => env('APP_NAME', 'MACUIN-Clientes'), 'env' => env('APP_ENV', 'local'),
    'debug' => (bool) env('APP_DEBUG', true), 'url' => env('APP_URL', 'http://localhost:8080'),
    'timezone' => 'America/Mexico_City', 'locale' => 'es', 'fallback_locale' => 'en',
    'faker_locale' => 'es_MX', 'cipher' => 'AES-256-CBC', 'key' => env('APP_KEY'),
    'maintenance' => ['driver' => 'file'],
];
