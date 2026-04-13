@extends('layouts.app')@section('title','Pedido '.($pedido['folio']??''))
@section('content')
<div class="d-flex justify-content-between align-items-center mb-4"><h4 class="fw-bold">{{ $pedido['folio']??'' }}</h4>
<div class="d-flex gap-2">
<a href="{{ route('pedidos.pdf',$pedido['id']) }}" class="btn btn-outline-danger btn-sm" style="border-radius:8px"><i class="bi bi-file-earmark-pdf"></i> PDF</a>
<a href="{{ route('pedidos.excel',$pedido['id']) }}" class="btn btn-outline-success btn-sm" style="border-radius:8px"><i class="bi bi-file-earmark-excel"></i> Excel</a>
<a href="{{ route('pedidos.docx',$pedido['id']) }}" class="btn btn-outline-primary btn-sm" style="border-radius:8px"><i class="bi bi-file-earmark-word"></i> Word</a>
@if(($pedido['estatus']??'')==='recibido')<form method="POST" action="{{ route('pedidos.cancel',$pedido['id']) }}" onsubmit="return confirm('¿Cancelar?')">@csrf
<button class="btn btn-outline-danger btn-sm" style="border-radius:8px"><i class="bi bi-x-circle"></i> Cancelar</button></form>@endif
<a href="{{ route('pedidos.index') }}" class="btn btn-outline-secondary btn-sm" style="border-radius:8px">Volver</a></div></div>
<div class="row g-4"><div class="col-md-8">
<div class="card p-4 mb-3"><div class="row">
<div class="col-6"><span class="text-muted small">Folio</span><br><strong>{{ $pedido['folio'] }}</strong></div>
<div class="col-6"><span class="text-muted small">Estatus</span><br><span class="badge badge-{{ $pedido['estatus'] }}">{{ strtoupper(str_replace('_',' ',$pedido['estatus'])) }}</span></div>
<div class="col-6 mt-3"><span class="text-muted small">Fecha</span><br><strong>{{ substr($pedido['created_at']??'',0,10) }}</strong></div>
<div class="col-6 mt-3"><span class="text-muted small">Notas</span><br>{{ $pedido['notas']??'-' }}</div></div></div>
<div class="card p-4 mb-3"><h6 class="fw-bold mb-3">Productos</h6>
<table class="table table-sm mb-0"><thead><tr><th>SKU</th><th>Producto</th><th>Cant.</th><th>P.Unit.</th><th>Subtotal</th></tr></thead><tbody>
@foreach(($pedido['detalles']??[]) as $d)<tr><td><code>{{ $d['autoparte_sku']??'' }}</code></td><td>{{ $d['autoparte_nombre']??'' }}</td>
<td>{{ $d['cantidad'] }}</td><td>${{ number_format($d['precio_unitario'],2) }}</td><td>${{ number_format($d['subtotal'],2) }}</td></tr>@endforeach
</tbody><tfoot><tr><td colspan="4" class="text-end">Subtotal:</td><td>${{ number_format($pedido['subtotal'],2) }}</td></tr>
<tr><td colspan="4" class="text-end">IVA 16%:</td><td>${{ number_format($pedido['impuesto'],2) }}</td></tr>
<tr><td colspan="4" class="text-end fw-bold">Total:</td><td class="fw-bold">${{ number_format($pedido['total'],2) }}</td></tr></tfoot></table></div></div>
<div class="col-md-4"><div class="card p-4"><h6 class="fw-bold mb-3">Historial</h6>
@foreach(($pedido['historial']??[]) as $h)
<div class="border-start border-3 ps-3 mb-3" style="border-color:#3b82f6!important">
<span class="badge badge-{{ $h['estatus_nuevo'] }}">{{ strtoupper(str_replace('_',' ',$h['estatus_nuevo'])) }}</span>
@if($h['estatus_anterior'])<small class="text-muted ms-1">desde {{ $h['estatus_anterior'] }}</small>@endif
<br><small class="text-muted">{{ substr($h['created_at']??'',0,16) }}</small>
@if($h['comentario'])<br><small>{{ $h['comentario'] }}</small>@endif</div>@endforeach</div></div></div>
@endsection
