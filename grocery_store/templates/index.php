<?php 
include __DIR__ . '/../includes/header.php'; 
require_once __DIR__ . '/../includes/error_handler.php';

?>

<div class="container">

    <h1>Products</h1>
    <!-- Flash Message Display -->
    <?php if (isset($_SESSION['flash_message'])): ?>
        <div class="alert alert-<?= htmlspecialchars($_SESSION['flash_message']['type']) ?>">
            <?= htmlspecialchars($_SESSION['flash_message']['message']) ?>
        </div>
        <?php unset($_SESSION['flash_message']); ?>
    <?php endif; ?>
    
    <!-- Category Filter -->
    <div class="filter-container">
        <select id="category-filter">
            <option value="all">All Products</option>
            <option value="Meat">Meat</option>
            <option value="Vegetables">Vegetables</option>
        </select>
    </div>

    <!-- Product Table -->
    <table id="products-table">
        <thead>
            <tr>
                <th>Product</th>
                <th>Category</th>
                <th>Price</th>
                <th>Image</th>
                <?php if (isset($_SESSION['user'])): ?>
                    <th>Add to Order</th>
                <?php endif; ?>
            </tr>
        </thead>
        <tbody>
            
        </tbody>
    </table>
</div>

<!-- Include JavaScript -->
<script src="../assets/js/index.js"></script>

<?php include __DIR__ . '/../includes/footer.php'; ?>