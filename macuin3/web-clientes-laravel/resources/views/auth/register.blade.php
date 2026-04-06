<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>MACUIN - Registro</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>*{font-family:'Inter',sans-serif}body{background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 50%,#0f172a 100%);min-height:100vh;display:flex;align-items:center}
.register-card{max-width:560px;margin:auto;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.4)}
.register-card .card-body{padding:36px}
.form-control,.form-select{border-radius:10px;padding:10px 14px;border:1.5px solid #e2e8f0}.form-control:focus{border-color:#3b82f6;box-shadow:0 0 0 4px rgba(59,130,246,.15)}
.btn-register{background:linear-gradient(135deg,#3b82f6,#2563eb);border:none;border-radius:10px;padding:12px;font-weight:600}</style>
</head><body><div class="container"><div class="card register-card"><div class="card-body">
<h4 class="text-center fw-bold mb-1" style="color:#0f172a">MACUIN</h4><p class="text-center text-muted mb-3">Registro de Cliente</p>
@if(session('error'))<div class="alert alert-danger py-2 small">{{ session('error') }}</div>@endif
<form method="POST" action="{{ route('register') }}">@csrf
<div class="row mb-3"><div class="col-md-6"><label class="form-label small fw-500">Nombre *</label><input type="text" name="nombre" class="form-control" required value="{{ old('nombre') }}"></div>
<div class="col-md-6"><label class="form-label small fw-500">Apellido *</label><input type="text" name="apellido" class="form-control" required value="{{ old('apellido') }}"></div></div>
<div class="row mb-3"><div class="col-md-6"><label class="form-label small fw-500">Email *</label><input type="email" name="email" class="form-control" required value="{{ old('email') }}"></div>
<div class="col-md-6"><label class="form-label small fw-500">Contraseña *</label><input type="password" name="password" class="form-control" required minlength="6"></div></div>
<div class="mb-3"><label class="form-label small fw-500">Teléfono</label><input type="text" name="telefono" class="form-control" value="{{ old('telefono') }}"></div>
<div class="row mb-3"><div class="col-md-6"><label class="form-label small fw-500">Razón Social</label><input type="text" name="razon_social" class="form-control" value="{{ old('razon_social') }}"></div>
<div class="col-md-6"><label class="form-label small fw-500">RFC</label><input type="text" name="rfc" class="form-control" value="{{ old('rfc') }}"></div></div>
<div class="mb-3"><label class="form-label small fw-500">Dirección</label><input type="text" name="direccion" class="form-control" value="{{ old('direccion') }}"></div>
<div class="row mb-3"><div class="col-md-4"><label class="form-label small fw-500">Ciudad</label><input type="text" name="ciudad" class="form-control" value="{{ old('ciudad') }}"></div>
<div class="col-md-4"><label class="form-label small fw-500">Estado</label><input type="text" name="estado" class="form-control" value="{{ old('estado') }}"></div>
<div class="col-md-4"><label class="form-label small fw-500">C.P.</label><input type="text" name="codigo_postal" class="form-control" value="{{ old('codigo_postal') }}"></div></div>
<button type="submit" class="btn btn-register text-white w-100">Registrarme</button></form>
<hr><p class="text-center mb-0 small">¿Ya tienes cuenta? <a href="{{ route('login') }}" style="color:#3b82f6;font-weight:600">Inicia sesión</a></p>
</div></div></div></body></html>
