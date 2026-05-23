<?php
session_start();

// Redirect non-logged-in users
if (isset($_SESSION['user'])) {
    $_SESSION['flash_message'] = [
        'type' => 'warning',
        'message' => 'Please Logout First!'
    ];
    ob_end_clean();
    header('Location: /grocery_store/templates/index.php');
    exit;
}

?>