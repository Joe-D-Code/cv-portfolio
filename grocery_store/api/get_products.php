<?php
// Include database connection and error handling utilities
require_once __DIR__ . '/../includes/db_connect.php';
require_once __DIR__ . '/../includes/error_handler.php';

// Set response content type to JSON
header('Content-Type: application/json');

try {
    // 1. Verify database connection exists
    if (!$pdo) {
        throw new RuntimeException("Database connection not established");
    }

    // 2. Build dynamic query based on category filter
    $category = isset($_GET['category']) ? trim($_GET['category']) : '';
    $sql = "SELECT * FROM products";
    $params = [];
    
    // Add category filter if valid category is provided
    if ($category) {
        // Define allowed categories to prevent invalid inputs
        $validCategories = ['Meat', 'Vegetables'];
        if (!in_array($category, $validCategories)) {
            throw new InvalidArgumentException("Invalid category");
        }
        $sql .= " WHERE category = ?";
        $params[] = $category; // Add parameter to array for prepared statement
    }

    // 3. Execute prepared statement with parameter binding
    $stmt = $pdo->prepare($sql);
    $executed = $stmt->execute($params);
    
    // Handle query execution errors
    if (!$executed) {
        $errorInfo = $stmt->errorInfo(); // Get PDO error details
        error_log("SQL Error: " . json_encode($errorInfo)); // Log to server error log
        throw new RuntimeException("Query failed: " . $errorInfo[2]);
    }

    // 4. Process and return results
    $products = $stmt->fetchAll(PDO::FETCH_ASSOC); // Get results as associative array
    
    // Handle empty result set
    if (empty($products)) {
        echo json_encode(['notice' => 'No products found']);
    } else {
        // Return success with numerical values preserved in JSON
        echo json_encode([
            'success' => true,
            'data' => $products
        ], JSON_NUMERIC_CHECK); // Maintain number types in JSON output
    }

} catch (PDOException $e) {
    // Handle database-specific exceptions
    error_log("PDO Exception: " . $e->getMessage());
    http_response_code(500); // Internal Server Error
    echo json_encode([
        'success' => false,
        'error' => 'Database error',
    ]);
} catch (Exception $e) {
    // Handle general exceptions (e.g., invalid category)
    http_response_code(400); // Bad Request
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}
?>