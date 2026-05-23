<?php
// Include header and DB connection
include_once '../includes/Header.php';
include_once '../includes/db_connect.php';
require_once __DIR__ . '/../includes/admin_auth.php';
require_once __DIR__ . '/../includes/error_handler.php';

try {
    // Fetch orders from the database using PDO
    $sql = "SELECT * FROM orders ORDER BY order_id DESC";
    $stmt = $pdo->query($sql);
    $orders = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    echo "Error: " . $e->getMessage();
}
?>


<div class="container">
    <div class="search-container">
        <input type="text" id="orderSearchBox" class="search-box" placeholder="Search by Order ID...">
      </div>
      
      <div id="noResults" class="no-results">No orders found matching your search.</div>
    <h2>All Orders - Admin View</h2>
    <?php if (!empty($orders)): ?>
        <table border="1" cellpadding="10" cellspacing="0" id="products-table">
            <thead>
                <tr>
                    <th>Order ID</th>
                    <th>Customer Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Product</th>
                    <th>Price (£)</th>
                    <th>Order Date</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($orders as $order): ?>
                    <tr>
                        <td><?= htmlspecialchars($order['order_id']) ?></td>
                        <td><?= htmlspecialchars($order['customer_name']) ?></td>
                        <td><?= htmlspecialchars($order['customer_email']) ?></td>
                        <td><?= htmlspecialchars($order['customer_phone']) ?></td>
                        <td><?= htmlspecialchars($order['product_name']) ?></td>
                        <td><?= number_format($order['price'], 2) ?></td>
                        <td><?= date('d/m/Y H:i', strtotime($order['order_date'])) ?></td>
                        
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    <?php else: ?>
        <p>No orders found.</p>
    <?php endif; ?>
</div>

<?php include_once '../includes/footer.php'; ?>
<script>
    // Direct implementation
    document.addEventListener('DOMContentLoaded', function() {
      const searchBox = document.getElementById('orderSearchBox');
      const tableRows = document.querySelectorAll('#products-table tbody tr');
      const noResultsMessage = document.getElementById('noResults');
      
      searchBox.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        let hasVisibleRows = false;
        
        tableRows.forEach(row => {
          const orderId = row.cells[0].textContent.toLowerCase().trim();
          
          if (searchTerm === '' || orderId.includes(searchTerm)) {
            row.style.display = '';
            hasVisibleRows = true;
          } else {
            row.style.display = 'none';
          }
        });
        
        noResultsMessage.style.display = hasVisibleRows ? 'none' : 'block';
      });
    });
    </script>
