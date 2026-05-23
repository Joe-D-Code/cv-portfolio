<?php
// Start session to manage user authentication and CAPTCHA verification
session_start();

// Include database connection and error handling utilities
require_once __DIR__ . '/../includes/db_connect.php';
require_once __DIR__ . '/../includes/error_handler.php';

try {
    // Ensure request is using POST method
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        throw new Exception('Invalid request method');
    }

    // Retrieve and sanitize form inputs
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';
    $captchaInput = strtolower($_POST['captcha'] ?? ''); // Make CAPTCHA case-insensitive

    // CAPTCHA validation process
    if (!isset($_SESSION['captcha'])) {
        throw new Exception('CAPTCHA expired or not generated');
    }

    // Compare user input with session-stored CAPTCHA value
    if ($_SESSION['captcha'] !== $captchaInput) {
        throw new Exception('CAPTCHA verification failed');
    }

    // Clear CAPTCHA value after validation (prevent reuse)
    unset($_SESSION['captcha']);

    // Database user verification
    $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
    $stmt->execute([$email]);
    $user = $stmt->fetch();

    // Verify password against stored hash
    if ($user && password_verify($password, $user['password'])) {
        // Set user session data (exclude sensitive information)
        $_SESSION['user'] = [
            'email' => $user['email'],
            'name' => $user['name'],
            'phone' => $user['phone']
        ];
        
        // Redirect to protected page after successful login
        header('Location: /grocery_store/templates/order.php');
        exit;
    } else {
        throw new Exception('Invalid credentials');
    }

} catch (Exception $e) {
    // Store error message in session for display on login page
    $_SESSION['flash_message'] = [
        'type' => 'warning',
        'message' => $e->getMessage()
    ];
    
    // Redirect back to login page with error message
    header('Location: /grocery_store/templates/login.php');
    exit;
}