<?php
// Start session to access current session data
session_start();

// Clear all session variables
session_unset();

// Destroy the session completely
session_destroy();

// Include error handling utilities
require_once __DIR__ . '/../includes/error_handler.php';

// Redirect user to login page with clean session state
header("Location: /grocery_store/templates/login.php");
exit; // Ensure no further code execution after redirect
?>