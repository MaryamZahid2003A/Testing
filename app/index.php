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
</head>
<body>
  <h1>Welcome, <?= htmlspecialchars($_SESSION['username']) ?></h1>
  <a href="logout.php">Logout</a> | 
  <a href="add.php"><button>Add New Task</button></a>

  <table border="1" cellpadding="10" cellspacing="0">
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
            <td>
              <a href="edit.php?id=<?= $row['id'] ?>">Edit</a>
              <a href="delete.php?id=<?= $row['id'] ?>" onclick="return confirm('Are you sure?')">Delete</a>
            </td>
          </tr>
        <?php endwhile; ?>
      <?php else: ?>
        <tr><td colspan="4">No tasks found.</td></tr>
      <?php endif; ?>
    </tbody>
  </table>
</body>
</html>
