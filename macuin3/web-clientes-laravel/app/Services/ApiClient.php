<?php
namespace App\Services;
use Illuminate\Support\Facades\Http;

class ApiClient {
    protected string $baseUrl;
    public function __construct() { $this->baseUrl = env('API_BASE_URL', 'http://api-fastapi:8000/api/v1'); }
    public function get(string $path, ?string $token = null, array $params = []) {
        $r = Http::timeout(10); if ($token) $r = $r->withToken($token);
        return $r->get($this->baseUrl . $path, $params);
    }
    public function post(string $path, array $data = [], ?string $token = null) {
        $r = Http::timeout(10); if ($token) $r = $r->withToken($token);
        return $r->post($this->baseUrl . $path, $data);
    }
    public function getRaw(string $path, ?string $token = null) {
        $r = Http::timeout(10); if ($token) $r = $r->withToken($token);
        return $r->get($this->baseUrl . $path);
    }
}
