<?php
namespace App\Http\Controllers;
use Illuminate\Http\Request;
use App\Services\ApiClient;

class PedidoController extends Controller {
    protected ApiClient $api;
    public function __construct(ApiClient $api) { $this->api = $api; }

    public function index() {
        $r = $this->api->get('/pedidos', session('api_token'));
        return view('pedidos.index', ['pedidos' => $r->successful() ? $r->json() : []]);
    }

    public function show(int $id) {
        $r = $this->api->get("/pedidos/{$id}", session('api_token'));
        if (!$r->successful()) return redirect()->route('pedidos.index')->with('error', 'Pedido no encontrado.');
        return view('pedidos.show', ['pedido' => $r->json()]);
    }

    public function create() {
        $r = $this->api->get('/autopartes', session('api_token'));
        return view('pedidos.create', ['autopartes' => $r->successful() ? $r->json() : []]);
    }

    public function store(Request $request) {
        $items = []; $ids = $request->input('autoparte_id', []); $cantidades = $request->input('cantidad', []);
        for ($i = 0; $i < count($ids); $i++) {
            if (!empty($ids[$i]) && !empty($cantidades[$i]) && $cantidades[$i] > 0)
                $items[] = ['autoparte_id' => (int)$ids[$i], 'cantidad' => (int)$cantidades[$i]];
        }
        if (empty($items)) return back()->with('error', 'Agrega al menos un producto.');
        $r = $this->api->post('/pedidos', ['items' => $items, 'notas' => $request->input('notas', '')], session('api_token'));
        if ($r->successful()) return redirect()->route('pedidos.show', $r->json()['id'])->with('success', 'Pedido creado.');
        return back()->with('error', $r->json()['detail'] ?? 'Error al crear pedido.');
    }

    public function cancel(int $id) {
        $r = $this->api->post("/pedidos/{$id}/cancelar", [], session('api_token'));
        return redirect()->route('pedidos.show', $id)->with($r->successful() ? 'success' : 'error',
            $r->successful() ? 'Pedido cancelado.' : ($r->json()['detail'] ?? 'Error.'));
    }

    public function pdf(int $id) {
        $r = $this->api->getRaw("/pedidos/{$id}/pdf", session('api_token'));
        if ($r->successful()) return response($r->body(), 200)->header('Content-Type', 'application/pdf')
            ->header('Content-Disposition', "attachment; filename=pedido-{$id}.pdf");
        return redirect()->route('pedidos.show', $id)->with('error', 'Error al descargar PDF.');
    }
}
