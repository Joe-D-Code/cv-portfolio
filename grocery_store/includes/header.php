<?php
// MUST be at the very top (before any HTML/output)
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

$baseUrl = "/grocery_store";
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Your grocery store with fresh vegetables and quality meat products">
    <meta name="keywords" content="grocery, vegetables, meat, online store, fresh produce">
    <title><?= isset($pageTitle) ? htmlspecialchars($pageTitle) : 'Grocery Store' ?></title>
    <link rel="stylesheet" href="<?= $baseUrl ?>/assets/css/style.css">
    <link rel="icon" href="/grocery_store/assets/images/logo.png">
    <script src="https://unpkg.com/react@17.0.2/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@17.0.2/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/babel-standalone@6.26.0/babel.min.js"></script>
</head>

<body data-logged-in="<?= isset($_SESSION['user']) ? 'true' : 'false' ?>">
    <nav class="main-nav">
        <div class="nav-container">
            <!-- burger button -->
            <button id="burger-icon" class="burger-icon" aria-label="Toggle menu">
                <span class="line"></span>
                <span class="line"></span>
                <span class="line"></span>
            </button>

            <div class="logo-container">
                <a href="/grocery_store/templates/index.php">
                    <img src="/grocery_store/assets/images/logo.png" alt="Logo" class="logo">
                </a>
            </div>

            <div id="nav-links" class="nav-links">
                <a href="/grocery_store/templates/index.php"
                    class="<?= basename($_SERVER['PHP_SELF']) === 'index.php' ? 'active' : '' ?>">Home</a>
                <a href="/grocery_store/templates/login.php"
                    class="<?= basename($_SERVER['PHP_SELF']) === 'login.php' ? 'active' : '' ?>">Login</a>
                <a href="/grocery_store/templates/register.php"
                    class="<?= basename($_SERVER['PHP_SELF']) === 'register.php' ? 'active' : '' ?>">Register</a>
                <a href="/grocery_store/templates/order.php"
                    class="<?= basename($_SERVER['PHP_SELF']) === 'order.php' ? 'active' : '' ?>">Order</a>
            </div>

            <div class="user-status">
                <?php if (isset($_SESSION['user'])): ?>
                    <span class="user-greeting">Welcome, <?= htmlspecialchars($_SESSION['user']['name']) ?></span>
                    <a href="/grocery_store/api/logout.php" class="logout-btn">Logout</a>
                <?php else: ?>
                    <span class="guest-label">Guest</span>
                <?php endif; ?>
            </div>
        </div>
        <script src="/grocery_store/assets/js/burgerMenu.js" defer></script>
    </nav>

    <main class="container">
        <?php if (isset($flashMessage)): ?>
            <div class="alert alert-<?= htmlspecialchars($flashType) ?>">
                <?= htmlspecialchars($flashMessage) ?>
            </div>
        <?php endif; ?>