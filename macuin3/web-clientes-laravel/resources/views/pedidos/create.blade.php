@extends('layouts.app')@section('title','Nuevo Pedido - MACUIN')
@section('content')
<h4 class="fw-bold mb-4">Crear Nuevo Pedido</h4>
<div class="card p-4" style="max-width:900px"><form method="POST" action="{{ route('pedidos.store') }}">@csrf
<div id="items-container">
<div class="row g-2 mb-2 item-row"><div class="col-md-7"><select name="autoparte_id[]" class="form-select" required>
<option value="">-- Seleccionar producto --</option>
@foreach($autopartes as $ap)@if(($ap['stock_actual']??0)>0)
<option value="{{ $ap['id'] }}">{{ $ap['sku'] }} — {{ $ap['nombre'] }} (${{ number_format($ap['precio'],2) }}) [{{ $ap['stock_actual'] }} disp.]</option>
@endif @endforeach</select></div>
<div class="col-md-3"><input type="number" name="cantidad[]" class="form-control" placeholder="Cantidad" min="1" value="1" required></div>
<div class="col-md-2"><button type="button" class="btn btn-outline-danger" onclick="this.closest('.item-row').remove()"><i class="bi bi-trash"></i></button></div></div></div>
<button type="button" class="btn btn-outline-primary btn-sm mb-3" onclick="addItem()" style="border-radius:8px"><i class="bi bi-plus"></i> Agregar producto</button>
<div class="mb-3"><label class="form-label small fw-500">Notas (opcional)</label>
<textarea name="notas" class="form-control" rows="2" placeholder="Instrucciones de entrega, horario, etc."></textarea></div>
<div class="d-flex gap-2"><button type="submit" class="btn btn-macuin"><i class="bi bi-check-lg"></i> Crear Pedido</button>
<a href="{{ route('catalogo') }}" class="btn btn-outline-secondary" style="border-radius:10px">Cancelar</a></div></form></div>
@endsection
@section('scripts')<script>function addItem(){const c=document.getElementById('items-container'),f=c.querySelector('.item-row'),cl=f.cloneNode(true);cl.querySelector('select').value='';cl.querySelector('input').value='1';c.appendChild(cl)}</script>@endsection
