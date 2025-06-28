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
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(to right, #6dd5fa, #2980b9);
      margin: 0;
      padding: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
    }
    .add-container {
      background: #ffffff;
      padding: 40px;
      border-radius: 12px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
      width: 400px;
    }
    h2 {
      text-align: center;
      color: #2980b9;
      margin-bottom: 25px;
    }
    input[type="text"], textarea {
      width: 100%;
      padding: 12px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-size: 1em;
    }
    button {
      width: 100%;
      padding: 12px;
      background-color: #3498db;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 1em;
      font-weight: bold;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    button:hover {
      background-color: #2980b9;
    }
    .back-link {
      text-align: center;
      margin-top: 15px;
    }
    .back-link a {
      color: #2980b9;
      text-decoration: none;
      font-weight: bold;
    }
    .back-link a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="add-container">
    <h2>Add New Task</h2>
    <form action="add.php" method="POST">
      <input type="text" name="title" placeholder="Task Title" required />
      <textarea name="description" rows="5" placeholder="Task Description" required></textarea>
      <button type="submit">Add Task</button>
    </form>
    <div class="back-link">
      <p><a href="index.php">Back to List</a></p>
    </div>
  </div>
</body>
</html>
