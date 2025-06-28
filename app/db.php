<?php
$servername = "db"; // service name in docker-compose
$username = "root";
$password = "rootpassword";
$dbname = "task_manager";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
