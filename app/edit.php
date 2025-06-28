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

if (!isset($_GET['id'])) {
    header("Location: index.php");
    exit;
}
$id = (int)$_GET['id'];

// Ensure task belongs to logged-in user
$sql = "SELECT * FROM tasks WHERE id = $id AND user_id = $user_id";
$result = $conn->query($sql);
if ($result->num_rows !== 1) {
    header("Location: index.php");
    exit;
}
$task = $result->fetch_assoc();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = $conn->real_escape_string($_POST['title']);
    $description = $conn->real_escape_string($_POST['description']);

    $sql = "UPDATE tasks SET title='$title', description='$description' WHERE id=$id AND user_id=$user_id";
    if ($conn->query($sql)) {
        header("Location: index.php");
        exit;
    } else {
        echo "Error updating record: " . $conn->error;
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Edit Task</title>
</head>
<body>
  <h2>Edit Task</h2>
  <form action="edit.php?id=<?= $task['id'] ?>" method="POST">
    <input type="text" name="title" value="<?= htmlspecialchars($task['title']) ?>" required /><br><br>
    <textarea name="description" rows="5" required><?= htmlspecialchars($task['description']) ?></textarea><br><br>
    <button type="submit">Update Task</button>
  </form>
  <br>
  <a href="index.php">Back to List</a>
</body>
</html>
