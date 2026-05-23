<?php
ob_start();
if (session_status() === PHP_SESSION_NONE) session_start();

include_once __DIR__ . '/../includes/db_connect.php';
require_once __DIR__ . '/../includes/error_handler.php';

// Redirect non-logged-in users
if (!isset($_SESSION['user'])) {
    $_SESSION['flash_message'] = [
        'type' => 'warning',
        'message' => 'You must be logged in to view orders.'
    ];
    ob_end_clean();
    header('Location: /grocery_store/templates/login.php');
    exit;
}

// Check admin status FIRST
$is_admin = false;
try {
    $stmt = $pdo->prepare("SELECT is_admin FROM users WHERE email = ?");
    $stmt->execute([$_SESSION['user']['email']]);
    $user = $stmt->fetch();
    $is_admin = $user['is_admin'] ?? false;
} catch (PDOException $e) {
    error_log("Admin check error: " . $e->getMessage());
}

// Redirect admins to admin page
if ($is_admin) {
    ob_end_clean();
    header('Location: /grocery_store/templates/admin_order.php');
    exit;
}

// Fetch regular user orders
try {
    $stmt = $pdo->prepare("SELECT * FROM orders WHERE customer_email = ? ORDER BY order_id DESC");
    $stmt->execute([$_SESSION['user']['email']]);
    $orders = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    error_log("Order fetch error: " . $e->getMessage());
    $orders = [];
}

// Correct header include (lowercase)
include_once __DIR__ . '/../includes/header.php';
?>

<div class="container">
    <h2>Your Orders</h2>
    <?php if (!empty($orders)): ?>
        <table border="1" cellpadding="10" cellspacing="0" id="products-table">
            <thead>
                <tr>
                    <th>Order ID</th>
                    <th>Product</th>
                    <th>Price (£)</th>
                    <th>Order Date</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($orders as $order): ?>
                    <tr>
                        <td><?= htmlspecialchars($order['order_id']) ?></td>
                        <td><?= htmlspecialchars($order['product_name']) ?></td>
                        <td><?= number_format($order['price'], 2) ?></td>
                        <td><?= date('d/m/Y H:i', strtotime($order['order_date'])) ?></td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    <?php else: ?>
        <p>You haven't placed any orders yet.</p>
    <?php endif; ?>
</div>

<?php include_once __DIR__ . '/../includes/footer.php'; ?>