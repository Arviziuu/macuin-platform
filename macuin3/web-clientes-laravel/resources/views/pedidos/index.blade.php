@extends('layouts.app')@section('title','Mis Pedidos - MACUIN')
@section('content')
<div class="d-flex justify-content-between align-items-center mb-4"><h4 class="fw-bold">Mis Pedidos</h4>
<a href="{{ route('pedidos.create') }}" class="btn btn-macuin"><i class="bi bi-cart-plus-fill"></i> Nuevo Pedido</a></div>
<div class="card"><table class="table table-hover mb-0" style="font-size:.9rem">
<thead style="background:#f8fafc"><tr><th>Folio</th><th>Fecha</th><th>Total</th><th>Estatus</th><th></th></tr></thead><tbody>
@forelse($pedidos as $p)<tr>
<td class="fw-600">{{ $p['folio'] }}</td><td>{{ substr($p['created_at']??'',0,10) }}</td>
<td class="fw-600">${{ number_format($p['total'],2) }}</td>
<td><span class="badge badge-{{ $p['estatus'] }}" style="font-size:.8rem">{{ strtoupper(str_replace('_',' ',$p['estatus'])) }}</span></td>
<td><a href="{{ route('pedidos.show',$p['id']) }}" class="btn btn-sm btn-outline-primary" style="border-radius:8px">Ver detalle</a></td>
</tr>@empty<tr><td colspan="5" class="text-center text-muted py-4">No tienes pedidos aún.</td></tr>@endforelse
</tbody></table></div>
@endsection
