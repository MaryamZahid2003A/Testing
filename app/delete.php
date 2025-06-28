<?php
include 'db.php';

if (!isset($_GET['id'])) {
    header("Location: index.php");
    exit;
}

$id = (int)$_GET['id'];

$sql = "DELETE FROM tasks WHERE id=$id";
$conn->query($sql);

header("Location: index.php");
exit;
?>
