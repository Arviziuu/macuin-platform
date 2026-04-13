<?php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\CatalogoController;
use App\Http\Controllers\PedidoController;

Route::get('/', fn() => redirect()->route('login'));
Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::get('/register', [AuthController::class, 'showRegister'])->name('register');
Route::post('/register', [AuthController::class, 'register']);
Route::get('/logout', [AuthController::class, 'logout'])->name('logout');

Route::middleware('api.auth')->group(function () {
    Route::get('/catalogo', [CatalogoController::class, 'index'])->name('catalogo');
    Route::get('/catalogo/{id}', [CatalogoController::class, 'show'])->name('catalogo.show');
    Route::get('/pedidos', [PedidoController::class, 'index'])->name('pedidos.index');
    Route::get('/pedidos/crear', [PedidoController::class, 'create'])->name('pedidos.create');
    Route::post('/pedidos', [PedidoController::class, 'store'])->name('pedidos.store');
    Route::get('/pedidos/{id}', [PedidoController::class, 'show'])->name('pedidos.show');
    Route::post('/pedidos/{id}/cancelar', [PedidoController::class, 'cancel'])->name('pedidos.cancel');
    Route::get('/pedidos/{id}/pdf', [PedidoController::class, 'pdf'])->name('pedidos.pdf');
    Route::get('/pedidos/{id}/excel', [PedidoController::class, 'excel'])->name('pedidos.excel');
    Route::get('/pedidos/{id}/docx', [PedidoController::class, 'docx'])->name('pedidos.docx');
});
