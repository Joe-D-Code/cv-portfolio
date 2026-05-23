<?php
// Include database connection and error handling
require_once __DIR__ . '/../includes/db_connect.php';
require_once __DIR__ . '/../includes/error_handler.php';

// Set response content type to JSON
header('Content-Type: application/json');

// Retrieve the HTTP request method
$method = $_SERVER['REQUEST_METHOD'];

// Route request based on HTTP method
switch($method) {
    case 'GET':
        // Handle order retrieval requests
        if (isset($_GET['order_id'])) {
            // Get single order by ID
            getOrderById($_GET['order_id']);
        } else {
            // Configure pagination parameters
            $page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
            $limit = isset($_GET['limit']) ? (int)$_GET['limit'] : 10;
            $offset = ($page - 1) * $limit;
            
            // Prepare filters from query parameters
            $filters = [];
            if (isset($_GET['customer_email'])) {
                $filters['customer_email'] = $_GET['customer_email'];
            }
            
            // Get paginated and filtered orders
            getOrders($limit, $offset, $filters);
        }
        break;
        
    case 'POST':
        // Placeholder for order creation functionality
        createOrder();
        break;
        
    default:
        // Handle unsupported HTTP methods
        http_response_code(405);
        echo json_encode(['error' => 'Method not allowed']);
        break;
}

/**
 * Retrieves a single order by ID
 * @param int $order_id The order ID to retrieve
 */
function getOrderById($order_id) {
    global $pdo; // Access database connection from global scope
    
    try {
        // Prepare and execute parameterized query
        $stmt = $pdo->prepare("SELECT * FROM orders WHERE order_id = ?");
        $stmt->execute([$order_id]);
        $order = $stmt->fetch(PDO::FETCH_ASSOC);
        
        if ($order) {
            // Return found order
            echo json_encode(['data' => $order]);
        } else {
            // Handle order not found
            http_response_code(404);
            echo json_encode(['error' => 'Order not found']);
        }
    } catch (PDOException $e) {
        // Handle database errors
        http_response_code(500);
        echo json_encode(['error' => 'Database error']);
    }
}

/**
 * Retrieves paginated and filtered orders
 * @param int $limit Number of items per page
 * @param int $offset Pagination offset
 * @param array $filters Filters to apply
 */
function getOrders($limit, $offset, $filters = []) {
    global $pdo;
    
    try {
        // Base query
        $sql = "SELECT * FROM orders";
        $params = [];
        
        // Add filter clauses dynamically
        if (!empty($filters)) {
            $sql .= " WHERE ";
            $filterClauses = [];
            
            // Build safe filter conditions
            foreach ($filters as $key => $value) {
                $filterClauses[] = "$key = ?";
                $params[] = $value;
            }
            
            $sql .= implode(" AND ", $filterClauses);
        }
        
        // Add pagination to query
        $sql .= " ORDER BY order_id DESC LIMIT ? OFFSET ?";
        $params[] = $limit;
        $params[] = $offset;
        
        // Execute main query
        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        $orders = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        // Get total count for pagination metadata
        $countSql = "SELECT COUNT(*) FROM orders";
        $countParams = [];
        
        // Apply same filters to count query
        if (!empty($filters)) {
            $countSql .= " WHERE ";
            $filterClauses = [];
            
            foreach ($filters as $key => $value) {
                $filterClauses[] = "$key = ?";
                $countParams[] = $value;
            }
            
            $countSql .= implode(" AND ", $filterClauses);
        }
        
        // Execute count query
        $countStmt = $pdo->prepare($countSql);
        $countStmt->execute($countParams);
        $total = $countStmt->fetchColumn();
        
        // Return structured response with pagination info
        echo json_encode([
            'data' => $orders,
            'total' => $total,
            'page' => $offset / $limit + 1,
            'per_page' => $limit
        ]);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Database error']);
    }
}

?>