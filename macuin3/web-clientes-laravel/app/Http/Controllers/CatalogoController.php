<?php
namespace App\Http\Controllers;
use Illuminate\Http\Request;
use App\Services\ApiClient;

class CatalogoController extends Controller {
    protected ApiClient $api;
    public function __construct(ApiClient $api) { $this->api = $api; }

    public function index(Request $request) {
        $params = [];
        if ($request->search) $params['search'] = $request->search;
        if ($request->categoria_id) $params['categoria_id'] = $request->categoria_id;
        if ($request->marca) $params['marca'] = $request->marca;
        $r = $this->api->get('/autopartes', session('api_token'), $params);
        $autopartes = $r->successful() ? $r->json() : [];
        $cr = $this->api->get('/categorias', session('api_token'));
        $categorias = $cr->successful() ? $cr->json() : [];
        return view('catalogo.index', compact('autopartes', 'categorias'));
    }

    public function show(int $id) {
        $r = $this->api->get("/autopartes/{$id}", session('api_token'));
        if (!$r->successful()) return redirect()->route('catalogo')->with('error', 'Producto no encontrado.');
        return view('catalogo.show', ['autoparte' => $r->json()]);
    }
}
