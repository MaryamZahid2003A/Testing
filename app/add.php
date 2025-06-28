<?php
include 'db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = $conn->real_escape_string($_POST['title']);
    $description = $conn->real_escape_string($_POST['description']);

    $sql = "INSERT INTO tasks (title, description) VALUES ('$title', '$description')";
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
    /* Paste same CSS, add small adjustments for form */
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f5f7fa;
      margin: 0;
      padding: 20px;
    }
    .container {
      max-width: 500px;
      margin: auto;
      background: white;
      padding: 25px 40px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      border-radius: 10px;
    }
    h2 {
      color: #2c3e50;
      text-align: center;
      margin-bottom: 20px;
    }
    input[type="text"], textarea {
      width: 100%;
      padding: 10px 15px;
      margin-bottom: 15px;
      border-radius: 6px;
      border: 1px solid #ccc;
      font-size: 1em;
    }
    button {
      background-color: #3498db;
      color: white;
      padding: 12px 25px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      font-size: 1em;
      transition: background-color 0.3s ease;
      width: 100%;
    }
    button:hover {
      background-color: #2980b9;
    }
    a {
      display: block;
      margin-top: 15px;
      text-align: center;
      color: #2980b9;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Add New Task</h2>
    <form action="add.php" method="POST">
      <input type="text" name="title" placeholder="Task Title" required />
      <textarea name="description" rows="5" placeholder="Task Description" required></textarea>
      <button type="submit">Add Task</button>
    </form>
    <a href="index.php">Back to List</a>
  </div>
</body>
</html>
