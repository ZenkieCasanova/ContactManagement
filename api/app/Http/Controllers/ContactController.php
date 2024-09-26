<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Validator;
use App\Models\Contact; // Assuming you have a Contact model

class ContactController extends Controller
{
    // POST /upload
    public function upload(Request $request)
    {
        \Log::info('Upload method called'); // Log entry for method call
        \Log::info('Request Data: ', $request->all()); // Log all request data

        $validator = Validator::make($request->all(), [
            'file' => 'required|file|mimes:json|max:2048',
        ]);

        if ($validator->fails()) {
            \Log::error('Validation Errors: ', $validator->errors()->toArray());
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $filePath = $request->file('file')->store('contacts', 'local');

        // Call Python script to process the uploaded file
        $output = shell_exec("python3 C:/Users/Mark Renzkie/PycharmProjects/pythonProject12/mediatest/pythonProject/service/watcher.py $filePath");

        return response()->json(['message' => 'File uploaded successfully!', 'output' => $output], 200);
    }


    // GET /contacts
    public function index(Request $request)
    {
        $query = Contact::query();

        // Searching by name or email
        if ($request->has('search')) {
            $search = $request->input('search');
            $query->where('name', 'LIKE', "%$search%")
                  ->orWhere('email', 'LIKE', "%$search%");
        }

        // Pagination
        $contacts = $query->paginate(10);
        return response()->json($contacts);
    }

    // GET /contacts/{id}
    public function show($id)
    {
        $contact = Contact::findOrFail($id);
        return response()->json($contact);
    }

    // PUT /contacts/{id}
    public function update(Request $request, $id)
    {
        $contact = Contact::findOrFail($id);
        $contact->update($request->all());
        return response()->json(['message' => 'Contact updated successfully!']);
    }

    // DELETE /contacts/{id}
    public function destroy($id)
    {
        $contact = Contact::findOrFail($id);
        $contact->delete();
        return response()->json(['message' => 'Contact deleted successfully!']);
    }
}
