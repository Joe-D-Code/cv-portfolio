<?php
// Start session properly
if (session_status() === PHP_SESSION_NONE) {
    session_start([
        'cookie_lifetime' => 86400,
        'read_and_close' => false
    ]);
}

// Hard-clear any previous output
if (ob_get_length()) ob_clean();

// CAPTCHA images with answers (store in lowercase for consistency)
$captchaImages = [
    'captcha1.jpg' => 'ecb4f',
    'captcha2.jpg' => 'Aeik2', 
    'captcha3.jpg' => '7plBJ8',
    'captcha4.jpg' => '24qUz'
];

// Verify images exist
$imageDir = realpath(__DIR__ . '/../assets/captcha_images/');
foreach ($captchaImages as $file => $answer) {
    if (!file_exists($imageDir . '/' . $file)) {
        http_response_code(500);
        die("Server error: CAPTCHA image missing");
    }
}

// Select random image
$selected = array_rand($captchaImages);
$imagePath = $imageDir . '/' . $selected;

// Store answer in lowercase for case-insensitive comparison
$_SESSION['captcha'] = strtolower($captchaImages[$selected]);


// Send appropriate headers
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Pragma: no-cache");
header('Content-Type: image/jpeg');

readfile($imagePath);
exit;