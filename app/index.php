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

$sql = "SELECT * FROM tasks WHERE user_id = $user_id ORDER BY id DESC";
$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Task Manager</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f0f8ff;
      margin: 0;
      padding: 20px;
    }
    .container {
      max-width: 800px;
      margin: auto;
      background: white;
      padding: 25px 40px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      border-radius: 10px;
    }
    h1 {
      color: #2c3e50;
      text-align: center;
      margin-bottom: 10px;
    }
    .top-links {
      text-align: center;
      margin-bottom: 20px;
    }
    .top-links a {
      margin: 0 10px;
      text-decoration: none;
      color: #3498db;
      font-weight: bold;
    }
    .top-links a:hover {
      text-decoration: underline;
    }
    button {
      background-color: #3498db;
      color: white;
      padding: 10px 20px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      font-size: 1em;
      transition: background-color 0.3s ease;
    }
    button:hover {
      background-color: #2980b9;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    th, td {
      padding: 12px 15px;
      border-bottom: 1px solid #ddd;
      text-align: left;
    }
    th {
      background-color: #3498db;
      color: white;
    }
    tr:hover {
      background-color: #eef6ff;
    }
    .actions a {
      margin-right: 10px;
      color: #2980b9;
      text-decoration: none;
      font-weight: 500;
    }
    .actions a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Welcome, <?= htmlspecialchars($_SESSION['username']) ?></h1>
    <div class="top-links">
      <a href="logout.php">Logout</a> | 
      <a href="add.php"><button>Add New Task</button></a>
    </div>

    <table>
      <thead>
        <tr><th>ID</th><th>Title</th><th>Description</th><th>Actions</th></tr>
      </thead>
      <tbody>
        <?php if ($result->num_rows > 0): ?>
          <?php while($row = $result->fetch_assoc()): ?>
            <tr>
              <td><?= $row['id'] ?></td>
              <td><?= htmlspecialchars($row['title']) ?></td>
              <td><?= htmlspecialchars($row['description']) ?></td>
              <td class="actions">
                <a href="edit.php?id=<?= $row['id'] ?>">Edit</a>
                <a href="delete.php?id=<?= $row['id'] ?>" onclick="return confirm('Are you sure?')">Delete</a>
              </td>
            </tr>
          <?php endwhile; ?>
        <?php else: ?>
          <tr><td colspan="4" style="text-align:center;">No tasks found.</td></tr>
        <?php endif; ?>
      </tbody>
    </table>
  </div>
</body>
</html>
