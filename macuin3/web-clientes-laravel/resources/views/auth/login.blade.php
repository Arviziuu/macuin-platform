<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>MACUIN - Iniciar Sesión</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.css" rel="stylesheet">
<style>*{font-family:'Inter',sans-serif}body{background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 50%,#0f172a 100%);min-height:100vh;display:flex;align-items:center}
.login-card{max-width:440px;margin:auto;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.05)}
.login-card .card-body{padding:44px}
.logo-icon{width:64px;height:64px;background:linear-gradient(135deg,#60a5fa,#3b82f6);border-radius:16px;display:flex;align-items:center;justify-content:center;margin:0 auto 16px;font-size:1.8rem;color:#fff}
.form-control{border-radius:10px;padding:12px 16px;border:1.5px solid #e2e8f0}.form-control:focus{border-color:#3b82f6;box-shadow:0 0 0 4px rgba(59,130,246,.15)}
.btn-login{background:linear-gradient(135deg,#3b82f6,#2563eb);border:none;border-radius:10px;padding:12px;font-weight:600;font-size:1rem;transition:transform .2s}.btn-login:hover{transform:translateY(-1px)}</style>
</head><body><div class="container"><div class="card login-card"><div class="card-body">
<div class="logo-icon"><i class="bi bi-car-front-fill"></i></div>
<h4 class="text-center fw-bold mb-1">MACUIN</h4><p class="text-center text-muted mb-4">Portal de Clientes</p>
@if(session('error'))<div class="alert alert-danger py-2 small">{{ session('error') }}</div>@endif
<form method="POST" action="{{ route('login') }}">@csrf
<div class="mb-3"><label class="form-label small fw-500">Correo electrónico</label><input type="email" name="email" class="form-control" required autofocus placeholder="tu@empresa.com" value="{{ old('email') }}"></div>
<div class="mb-4"><label class="form-label small fw-500">Contraseña</label><input type="password" name="password" class="form-control" required placeholder="••••••••"></div>
<button type="submit" class="btn btn-login text-white w-100">Iniciar sesión</button></form>
<hr><p class="text-center mb-0 small">¿No tienes cuenta? <a href="{{ route('register') }}" class="fw-600" style="color:#3b82f6">Regístrate aquí</a></p>
</div></div></div></body></html>
