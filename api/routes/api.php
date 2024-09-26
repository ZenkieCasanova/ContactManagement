use App\Http\Controllers\ContactController;

Route::post('/upload', [ContactController::class, 'upload']);
Route::get('/contacts', [ContactController::class, 'index']);
Route::get('/contacts/{id}', [ContactController::class, 'show']);
Route::put('/contacts/{id}', [ContactController::class, 'update']);
Route::delete('/contacts/{id}', [ContactController::class, 'destroy']);
