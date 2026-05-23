<?php
// includes/admin_auth.php
if (session_status() === PHP_SESSION_NONE) session_start();

if (!isset($_SESSION['user'])) {
    header('Location: /grocery_store/templates/login.php');
    exit;
}

require_once __DIR__ . '/../includes/db_connect.php';

$stmt = $pdo->prepare("SELECT is_admin FROM users WHERE email = ?");
$stmt->execute([$_SESSION['user']['email']]);
$user = $stmt->fetch();

if (!$user || !$user['is_admin']) {
    header('Location: /grocery_store/templates/order.php');
    exit;
}
?>