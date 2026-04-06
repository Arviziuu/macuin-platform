@extends('layouts.app')@section('title',$autoparte['nombre'].' - MACUIN')
@section('content')
<a href="{{ route('catalogo') }}" class="btn btn-outline-secondary btn-sm mb-3" style="border-radius:8px"><i class="bi bi-arrow-left"></i> Volver</a>
<div class="row g-4"><div class="col-md-8"><div class="card p-4">
<span class="category-badge mb-2" style="width:fit-content;background:#eff6ff;color:#2563eb;font-size:.8rem;font-weight:600;border-radius:6px;padding:5px 12px">{{ $autoparte['categoria_nombre'] ?? 'General' }}</span>
<h3 class="fw-bold mt-2">{{ $autoparte['nombre'] }}</h3>
<p class="text-muted">SKU: <code>{{ $autoparte['sku'] }}</code> · Marca: <strong>{{ $autoparte['marca'] ?? 'N/A' }}</strong></p>
@if($autoparte['descripcion'])<h6 class="mt-4 fw-600">Descripción</h6><p>{{ $autoparte['descripcion'] }}</p>@endif
@if($autoparte['compatibilidad_vehicular'])<h6 class="mt-3 fw-600">Compatibilidad</h6><p><i class="bi bi-car-front text-primary"></i> {{ $autoparte['compatibilidad_vehicular'] }}</p>@endif
</div></div>
<div class="col-md-4"><div class="card p-4">
<div class="price mb-2" style="font-size:2rem;font-weight:700;color:#0f172a">${{ number_format($autoparte['precio'],2) }} <small class="text-muted" style="font-size:.9rem">MXN</small></div>
@if(($autoparte['stock_actual']??0)>0)
<div class="p-3 rounded-3 mb-3" style="background:#f0fdf4"><i class="bi bi-check-circle-fill text-success"></i> <strong class="text-success">Disponible</strong> — {{ $autoparte['stock_actual'] }} unidades</div>
<a href="{{ route('pedidos.create') }}" class="btn btn-macuin w-100"><i class="bi bi-cart-plus-fill"></i> Agregar a Pedido</a>
@else<div class="p-3 rounded-3" style="background:#fef2f2"><i class="bi bi-x-circle-fill text-danger"></i> <strong class="text-danger">Agotado</strong></div>@endif
</div></div></div>
@endsection
