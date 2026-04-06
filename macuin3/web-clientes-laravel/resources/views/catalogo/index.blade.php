@extends('layouts.app')@section('title','Catálogo - MACUIN')
@section('content')
<div class="d-flex justify-content-between align-items-center mb-4"><h4 class="fw-bold">Catálogo de Autopartes</h4>
<a href="{{ route('pedidos.create') }}" class="btn btn-macuin"><i class="bi bi-cart-plus-fill"></i> Nuevo Pedido</a></div>
<div class="card p-3 mb-4"><form method="GET" action="{{ route('catalogo') }}" class="row g-2">
<div class="col-md-5"><input type="text" name="search" class="form-control" placeholder="Buscar por nombre, SKU, vehículo..." value="{{ request('search') }}"></div>
<div class="col-md-3"><select name="categoria_id" class="form-select"><option value="">Todas las categorías</option>
@foreach($categorias as $cat)<option value="{{ $cat['id'] }}" {{ request('categoria_id')==$cat['id']?'selected':'' }}>{{ $cat['nombre'] }}</option>@endforeach</select></div>
<div class="col-md-2"><input type="text" name="marca" class="form-control" placeholder="Marca" value="{{ request('marca') }}"></div>
<div class="col-md-2"><button class="btn btn-macuin w-100"><i class="bi bi-search"></i> Buscar</button></div></form></div>
<div class="row">@forelse($autopartes as $ap)
<div class="col-md-4 col-lg-3 mb-4"><div class="card product-card h-100"><div class="card-body d-flex flex-column">
<span class="category-badge mb-2" style="width:fit-content">{{ $ap['categoria_nombre'] ?? 'General' }}</span>
<h6 class="fw-bold mb-1">{{ $ap['nombre'] }}</h6>
<small class="text-muted">{{ $ap['sku'] }} · {{ $ap['marca'] ?? '' }}</small>
<p class="mt-2 small text-muted flex-grow-1">{{ \Illuminate\Support\Str::limit($ap['descripcion'] ?? '',80) }}</p>
<div class="mt-auto"><div class="price mb-1">${{ number_format($ap['precio'],2) }}</div>
@if(($ap['stock_actual']??0)>0)<span class="stock-available"><i class="bi bi-check-circle-fill"></i> En stock ({{ $ap['stock_actual'] }})</span>
@else<span class="stock-unavailable"><i class="bi bi-x-circle-fill"></i> Agotado</span>@endif
<div class="mt-2"><a href="{{ route('catalogo.show',$ap['id']) }}" class="btn btn-outline-primary btn-sm w-100" style="border-radius:8px">Ver detalle</a></div>
</div></div></div></div>
@empty<div class="col-12"><div class="alert alert-info">No se encontraron autopartes.</div></div>@endforelse</div>
@endsection
