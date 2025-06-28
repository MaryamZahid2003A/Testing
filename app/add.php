<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit;
}
include 'db.php';

$user = $_SESSION['username'];
$res = $conn->query("SELECT id FROM users WHERE username = '$user'");
$row = $res->fetch_assoc();
$user_id = $row['id'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = $conn->real_escape_string($_POST['title']);
    $description = $conn->real_escape_string($_POST['description']);

    $sql = "INSERT INTO tasks (title, description, user_id) VALUES ('$title', '$description', $user_id)";
    if ($conn->query($sql)) {
        header("Location: index.php");
        exit;
    } else {
        echo "Error: " . $conn->error;
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Add Task</title>
</head>
<body>
  <h2>Add New Task</h2>
  <form action="add.php" method="POST">
    <input type="text" name="title" placeholder="Task Title" required /><br><br>
    <textarea name="description" rows="5" placeholder="Task Description" required></textarea><br><br>
    <button type="submit">Add Task</button>
  </form>
  <br>
  <a href="index.php">Back to List</a>
</body>
</html>
