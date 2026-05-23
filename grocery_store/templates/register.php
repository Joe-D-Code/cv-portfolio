<?php
// Must be at the VERY TOP before any output
require_once __DIR__ . '/../includes/logged_check.php';
require_once __DIR__ . '/../includes/error_handler.php';

// Now include header AFTER session management
include __DIR__ . '/../includes/header.php';
?>


<div class="container">
    <h2>Register</h2>

    <!-- Flash Message Display -->
    <?php if (isset($_SESSION['flash_message'])): ?>
        <div class="alert alert-<?= htmlspecialchars($_SESSION['flash_message']['type']) ?>">
            <?= htmlspecialchars($_SESSION['flash_message']['message']) ?>
        </div>
        <?php unset($_SESSION['flash_message']); ?>
    <?php endif; ?>

    <div id="register-form">
        <div class="loading-message">Loading registration form...</div>
    </div>
    <script type="text/babel" src="/grocery_store/assets/js/register.js"></script>
    <p class="login-link">Already have an account? <a href="login.php">Login here</a></p>
</div>

<?php include __DIR__ . '/../includes/footer.php'; ?>

