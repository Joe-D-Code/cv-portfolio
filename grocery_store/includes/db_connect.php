<?php
// db_connect.php

$servername = "your_db_host";
$username   = "your_db_username";
$password   = "your_db_password";
$dbname     = "your_db_name";

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
} else {
    echo "Connection successful.";
}
?>
