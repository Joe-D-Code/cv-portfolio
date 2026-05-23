<?php
// Must be at the VERY TOP before any output
require_once __DIR__ . '/../includes/logged_check.php';
require_once __DIR__ . '/../includes/error_handler.php';

// Now include header AFTER session management
include __DIR__ . '/../includes/header.php';
?>

<div class="container">
    <h2>Login</h2>

    <!-- Flash Message Display -->
    <?php if (isset($_SESSION['flash_message'])): ?>
        <div class="alert alert-<?= htmlspecialchars($_SESSION['flash_message']['type']) ?>">
            <?= htmlspecialchars($_SESSION['flash_message']['message']) ?>
        </div>
        <?php unset($_SESSION['flash_message']); ?>
    <?php endif; ?>

    <!-- Login Form Container -->
    <div id="login-form-container">
        <form action="/grocery_store/api/login.php" method="POST">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" id="password" placeholder="Password" required>
            <div class="show-password-toggle">
                <label for="show-password-checkbox">Show Password:</label>
                <input type="checkbox" id="show-password-checkbox" onchange="toggleShowPassword(this)" />
            </div>
            <!-- CAPTCHA Section -->
            <div class="captcha">
                <img src="/grocery_store/includes/captcha.php?<?= time() ?>" alt="CAPTCHA" id="captcha-image"
                    onclick="refreshCaptcha()" style="cursor: pointer">
                <input type="text" name="captcha" placeholder="Enter CAPTCHA" required>
            </div>

            <button type="submit">Login</button>
        </form>
    </div>

    <p>Don't have an account? <a href="register.php">Register here</a></p>
</div>

<script>
    // CAPTCHA refresh function
    function refreshCaptcha() {
        const captchaImg = document.getElementById('captcha-image');
        captchaImg.src = '/grocery_store/includes/captcha.php?' + Date.now();
    }

    function toggleShowPassword(checkbox) {
    const passwordInput = document.getElementById("password");
    if (passwordInput) {
      passwordInput.type = checkbox.checked ? "text" : "password";
    }
  }
</script>

<?php include __DIR__ . '/../includes/footer.php'; ?>