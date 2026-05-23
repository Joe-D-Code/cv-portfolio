<?php
// Start session to manage user authentication and flash messages
session_start();

// Include database connection configuration
require_once __DIR__ . '/../includes/db_connect.php';

try {
    // Detect request content type (JSON vs traditional form submission)
    if (isset($_SERVER['CONTENT_TYPE']) && $_SERVER['CONTENT_TYPE'] === 'application/json') {
        $data = json_decode(file_get_contents('php://input'), true);
        header('Content-Type: application/json');
    } else {
        $data = $_POST;
    }

    // Validate required registration fields
    if (!isset($data['name'], $data['phone'], $data['email'], $data['password'])) {
        throw new Exception("Missing required registration fields.");
    }

    // Sanitize input data
    $name = trim($data['name']);
    $phone = trim($data['phone']);
    $email = trim($data['email']);
    $password = trim($data['password']);
    
    // Basic empty field validation
    if ($name === "" || $phone === "" || $email === "" || $password === "") {
        throw new Exception("Please fill in all required fields.");
    }
    
    // Validate email format using PHP filter
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        throw new Exception("Please enter a valid email address.");
    }
    
    // Check for existing email in database
    $checkEmailSql = "SELECT COUNT(*) FROM users WHERE email = :email";
    $checkStmt = $pdo->prepare($checkEmailSql);
    $checkStmt->execute([':email' => $email]);
    
    if ($checkStmt->fetchColumn() > 0) {
        // Handle duplicate email scenario
        $_SESSION['flash_message'] = [
            'type' => 'warning',
            'message' => "This email address is already registered. Please use a different email or login with your existing account."
        ];
        
        // Different response handling for JSON vs HTML
        if (isset($_SERVER['CONTENT_TYPE']) && $_SERVER['CONTENT_TYPE'] === 'application/json') {
            echo json_encode([
                'success' => false,
                'error' => "This email address is already registered. Please use a different email or login with your existing account.",
                'field' => 'email',
                'redirect' => '/grocery_store/templates/register.php'
            ]);
        } else {
            header('Location: /grocery_store/templates/register.php');
        }
        exit;
    }

    // Securely hash password before storage
    $passwordHash = password_hash($password, PASSWORD_DEFAULT);

    // Prepare SQL insert statement with named parameters
    $sql = "INSERT INTO users (name, phone, email, password) VALUES (:name, :phone, :email, :password)";
    $stmt = $pdo->prepare($sql);

    // Execute query with sanitized parameters
    $success = $stmt->execute([
        ':name'     => $name,
        ':phone'    => $phone,
        ':email'    => $email,
        ':password' => $passwordHash
    ]);

    if (!$success) {
        throw new Exception("Failed to register user.");
    }

    // Retrieve auto-incremented user ID
    $userId = $pdo->lastInsertId();

    // Set user session data (automatic login)
    $_SESSION['user'] = [
        'id'    => $userId,
        'name'  => $name,
        'email' => $email,
        'phone' => $phone
    ];

    // Set success notification
    $_SESSION['flash_message'] = [
        'type' => 'warning',
        'message' => 'Registration successful! You are now logged in.'
    ];

    // Handle response based on content type
    if (isset($_SERVER['CONTENT_TYPE']) && $_SERVER['CONTENT_TYPE'] === 'application/json') {
        echo json_encode([
            'success'  => true,
            'redirect' => '/grocery_store/templates/index.php'
        ]);
    } else {
        header('Location: /grocery_store/templates/index.php');
    }
    exit;

} catch (PDOException $e) {
    // Database error handling
    $errorMessage = "Database error occurred. ";
    
    // Detect MySQL duplicate entry errors
    if ($e->getCode() == 23000 && strpos($e->getMessage(), 'Duplicate entry') !== false) {
        $errorMessage = "This email address is already registered. Please use a different email or login with your existing account.";
    } else {
        $errorMessage .= "Please try again later.";
    }
    
    error_log("Registration PDO error: " . $e->getMessage());
    
    // Set error message in session
    $_SESSION['flash_message'] = [
        'type' => 'danger',
        'message' => $errorMessage
    ];
    
    // Handle different response types
    if (isset($_SERVER['CONTENT_TYPE']) && $_SERVER['CONTENT_TYPE'] === 'application/json') {
        header('Content-Type: application/json');
        echo json_encode([
            'success' => false,
            'error'   => $errorMessage,
            'redirect' => '/grocery_store/templates/register.php'
        ]);
    } else {
        header('Location: /grocery_store/templates/register.php');
    }
    exit;
    
} catch (Exception $e) {
    // General exception handling
    $errorMessage = $e->getMessage();
    error_log("Registration error: " . $errorMessage);

    // Store error message for display
    $_SESSION['flash_message'] = [
        'type' => 'danger',
        'message' => $errorMessage
    ];

    // Return appropriate response format
    if (isset($_SERVER['CONTENT_TYPE']) && $_SERVER['CONTENT_TYPE'] === 'application/json') {
        header('Content-Type: application/json');
        echo json_encode([
            'success' => false,
            'error'   => $errorMessage,
            'redirect' => '/grocery_store/templates/register.php'
        ]);
    } else {
        header('Location: /grocery_store/templates/register.php');
    }
    exit;
}