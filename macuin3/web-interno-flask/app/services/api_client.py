import requests, os
API_BASE = os.getenv("FLASK_API_BASE_URL", "http://api-fastapi:8000")

def api_url(path): return f"{API_BASE}/api/v1{path}"

def api_get(path, token=None, params=None):
    h = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.get(api_url(path), headers=h, params=params, timeout=10)

def api_post(path, token=None, json=None):
    h = {"Content-Type": "application/json"}
    if token: h["Authorization"] = f"Bearer {token}"
    return requests.post(api_url(path), headers=h, json=json, timeout=10)

def api_put(path, token=None, json=None):
    h = {"Content-Type": "application/json"}
    if token: h["Authorization"] = f"Bearer {token}"
    return requests.put(api_url(path), headers=h, json=json, timeout=10)

def api_delete(path, token=None):
    h = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.delete(api_url(path), headers=h, timeout=10)
