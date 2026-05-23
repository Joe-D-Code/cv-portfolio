<?php
// includes/error_handler.php

// At the beginning of your error_handler.php file
$logDir = dirname(__DIR__) . '/logs';
if (!is_dir($logDir)) {
    mkdir($logDir, 0777, true);
}

// Error logging function
function logError($level, $message, $context = []) {
    // Log to file
    $timestamp = date('Y-m-d H:i:s');
    $logMessage = "[{$timestamp}] [{$level}] {$message} " . 
                  (!empty($context) ? json_encode($context) : '');
    
    error_log($logMessage . PHP_EOL, 3, __DIR__ . '/../logs/app.log');
}

// Display friendly error message to user
function showError($type, $message) {
    $_SESSION['flash_message'] = [
        'type' => $type,
        'message' => $message
    ];
}

// Database error handler
function handleDbError($e, $redirect = null) {
    logError('ERROR', 'Database error: ' . $e->getMessage());
    showError('error', 'A database error occurred. Please try again later.');
    
    if ($redirect) {
        header("Location: {$redirect}");
        exit;
    }
}

// API error response
function apiError($statusCode, $message, $details = null) {
    http_response_code($statusCode);
    echo json_encode([
        'success' => false,
        'error' => $message,
        'details' => $details
    ]);
    exit;
}

// Set global error handler
set_error_handler(function($errno, $errstr, $errfile, $errline) {
    if (!(error_reporting() & $errno)) {
        // This error code is not included in error_reporting
        return false;
    }
    
    $error_type = match($errno) {
        E_USER_ERROR, E_ERROR, E_CORE_ERROR, E_COMPILE_ERROR => 'FATAL',
        E_USER_WARNING, E_WARNING => 'WARNING',
        E_USER_NOTICE, E_NOTICE => 'NOTICE',
        default => 'UNKNOWN'
    };
    
    logError($error_type, $errstr, [
        'file' => $errfile,
        'line' => $errline
    ]);
    
    // Don't execute PHP internal error handler
    return true;
});

// Set exception handler
set_exception_handler(function($e) {
    logError('EXCEPTION', $e->getMessage(), [
        'file' => $e->getFile(),
        'line' => $e->getLine(),
        'trace' => $e->getTraceAsString()
    ]);
    
    // For API requests
    if (strpos($_SERVER['REQUEST_URI'], '/api/') !== false) {
        apiError(500, 'An unexpected error occurred');
    } else {
        showError('error', 'An unexpected error occurred. Please try again later.');
        include __DIR__ . '/../templates/error.php';
    }
    
    exit;
});
?>