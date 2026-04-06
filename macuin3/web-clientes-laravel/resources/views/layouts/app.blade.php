<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>@yield('title', 'MACUIN Autopartes')</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        *{font-family:'Inter',sans-serif}
        body{background:#f8fafc}
        .navbar-macuin{background:linear-gradient(135deg,#0f172a,#1e3a5f);box-shadow:0 2px 12px rgba(0,0,0,.15);padding:12px 0}
        .navbar-macuin .navbar-brand{font-weight:700;font-size:1.3rem;color:#fff!important;display:flex;align-items:center;gap:8px}
        .navbar-macuin .navbar-brand i{color:#60a5fa;font-size:1.5rem}
        .navbar-macuin .nav-link{color:rgba(255,255,255,.75)!important;font-weight:500;font-size:.9rem;padding:8px 16px!important;border-radius:8px;transition:all .2s}
        .navbar-macuin .nav-link:hover,.navbar-macuin .nav-link.active{color:#fff!important;background:rgba(96,165,250,.15)}
        .navbar-macuin .user-info{color:rgba(255,255,255,.6);font-size:.85rem}
        .product-card{border:none;border-radius:16px;box-shadow:0 1px 4px rgba(0,0,0,.06);transition:all .25s;overflow:hidden}
        .product-card:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,0,0,.1)}
        .product-card .card-body{padding:20px}
        .product-card .price{color:#0f172a;font-size:1.3rem;font-weight:700}
        .product-card .category-badge{background:#eff6ff;color:#2563eb;font-size:.75rem;font-weight:600;border-radius:6px;padding:4px 10px}
        .badge-recibido{background:#dbeafe;color:#1d4ed8} .badge-en_proceso{background:#fef3c7;color:#b45309}
        .badge-enviado{background:#d1fae5;color:#047857} .badge-entregado{background:#ccfbf1;color:#0f766e}
        .badge-cancelado{background:#fee2e2;color:#b91c1c}
        .btn-macuin{background:linear-gradient(135deg,#3b82f6,#2563eb);border:none;color:#fff;border-radius:10px;font-weight:600;padding:10px 24px}
        .btn-macuin:hover{background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;transform:translateY(-1px)}
        .card{border:none;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
        .form-control,.form-select{border-radius:10px;border:1.5px solid #e2e8f0;padding:10px 14px}
        .form-control:focus,.form-select:focus{border-color:#3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,.12)}
        .stock-available{color:#059669;font-weight:600;font-size:.85rem}
        .stock-unavailable{color:#dc2626;font-weight:600;font-size:.85rem}
        footer{background:#f1f5f9;border-top:1px solid #e2e8f0}
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-macuin">
    <div class="container">
        <a class="navbar-brand" href="{{ route('catalogo') }}"><i class="bi bi-car-front-fill"></i> MACUIN</a>
        @if(session('api_token'))
        <div class="d-flex align-items-center gap-2 flex-wrap">
            <a href="{{ route('catalogo') }}" class="nav-link {{ request()->routeIs('catalogo*') ? 'active' : '' }}"><i class="bi bi-grid-3x3-gap"></i> Catálogo</a>
            <a href="{{ route('pedidos.index') }}" class="nav-link {{ request()->routeIs('pedidos*') ? 'active' : '' }}"><i class="bi bi-bag"></i> Mis Pedidos</a>
            <a href="{{ route('pedidos.create') }}" class="nav-link"><i class="bi bi-cart-plus-fill"></i> Nuevo Pedido</a>
            <span class="user-info ms-2">{{ session('user.nombre') ?? '' }}</span>
            <a href="{{ route('logout') }}" class="btn btn-outline-light btn-sm ms-1" style="border-radius:8px">Salir</a>
        </div>
        @endif
    </div>
</nav>
<div class="container py-4">
    @if(session('success'))<div class="alert alert-success alert-dismissible fade show">{{ session('success') }}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>@endif
    @if(session('error'))<div class="alert alert-danger alert-dismissible fade show">{{ session('error') }}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>@endif
    @yield('content')
</div>
<footer class="text-center text-muted py-3 mt-5"><small>&copy; {{ date('Y') }} MACUIN Autopartes Automotrices</small></footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
@yield('scripts')
</body>
</html>
