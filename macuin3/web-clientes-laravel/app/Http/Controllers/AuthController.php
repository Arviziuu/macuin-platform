<?php
namespace App\Http\Controllers;
use Illuminate\Http\Request;
use App\Services\ApiClient;

class AuthController extends Controller {
    protected ApiClient $api;
    public function __construct(ApiClient $api) { $this->api = $api; }

    public function showLogin() {
        if (session('api_token')) return redirect()->route('catalogo');
        return view('auth.login');
    }

    public function login(Request $request) {
        $request->validate(['email' => 'required|email', 'password' => 'required']);
        $response = $this->api->post('/auth/login', ['email' => $request->email, 'password' => $request->password]);
        if ($response->successful()) {
            $data = $response->json();
            if ($data['user']['rol']['nombre'] !== 'cliente_externo')
                return back()->with('error', 'Esta plataforma es solo para clientes.');
            session(['api_token' => $data['access_token'], 'user' => $data['user']]);
            return redirect()->route('catalogo');
        }
        return back()->with('error', 'Credenciales inválidas.');
    }

    public function showRegister() { return view('auth.register'); }

    public function register(Request $request) {
        $request->validate(['email' => 'required|email', 'password' => 'required|min:6', 'nombre' => 'required', 'apellido' => 'required']);
        $response = $this->api->post('/auth/register', $request->all());
        if ($response->successful()) {
            $data = $response->json();
            session(['api_token' => $data['access_token'], 'user' => $data['user']]);
            return redirect()->route('catalogo')->with('success', '¡Registro exitoso!');
        }
        return back()->withInput()->with('error', $response->json()['detail'] ?? 'Error en el registro.');
    }

    public function logout() { session()->flush(); return redirect()->route('login'); }
}
