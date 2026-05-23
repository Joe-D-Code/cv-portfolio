<?php
// Start a PHP session to access user session data
session_start();

// Include the database connection and custom error handler
require_once __DIR__ . '/../includes/db_connect.php';
require_once __DIR__ . '/../includes/error_handler.php';

// Set the response content type to JSON
header('Content-Type: application/json');

// Check if user is logged in by verifying session data
if (!isset($_SESSION['user'])) {
    http_response_code(401); // Unauthorized status code
    echo json_encode(['success' => false, 'error' => 'Not logged in']);
    exit; // Stop script execution
}

// Decode JSON input from request body
$data = json_decode(file_get_contents("php://input"), true);

// Validate input data structure
if (!$data || !isset($data['product_name']) || !isset($data['price'])) {
    http_response_code(400); // Bad Request status code
    echo json_encode(['success' => false, 'error' => 'Invalid input']);
    exit; // Stop script execution
}

try {
    // Prepare SQL statement to get user's phone number from database
    $stmt = $pdo->prepare("SELECT phone FROM users WHERE email = ?");
    $stmt->execute([$_SESSION['user']['email']]); // Execute with email from session
    $user = $stmt->fetch(); // Fetch the result

    // Check if user was found in database
    if (!$user) {
        throw new Exception('User not found');
    }

    // Prepare SQL statement to insert new order
    $stmt = $pdo->prepare("INSERT INTO orders 
                          (customer_name, customer_email, customer_phone, product_name, price) 
                          VALUES (?, ?, ?, ?, ?)");
    
    // Execute the insert statement with parameters from session and input data
    $success = $stmt->execute([
        $_SESSION['user']['name'],     // Customer name from session
        $_SESSION['user']['email'],     // Customer email from session
        $user['phone'],                 // Phone number from database query
        $data['product_name'],          // Product name from input
        $data['price']                  // Price from input
    ]);

    // Check if insert was successful
    if ($success) {
        // Return success response
        echo json_encode(['success' => true, 'message' => 'Item added to order']);
    } else {
        throw new Exception('Failed to add order');
    }
} catch (Exception $e) {
    // Handle any exceptions that occur
    http_response_code(500); // Internal Server Error status code
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}