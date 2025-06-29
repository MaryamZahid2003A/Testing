<?php
include 'db.php';
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
session_start();

$error = "";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $conn->real_escape_string($_POST['username']);
    $password = $_POST['password'];

    $sql = "SELECT * FROM users WHERE username='$username'";
    $result = $conn->query($sql);

    if ($result->num_rows === 1) {
        $user = $result->fetch_assoc();
        if (password_verify($password, $user['password'])) {
            $_SESSION['username'] = $username;
            header("Location: index.php");
            exit;
        } else {
            $error = "Invalid password";
        }
    } else {
        $error = "User not found";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Login</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(to right, #2980b9, #6dd5fa);
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .login-container {
      background: #ffffff;
      padding: 40px;
      border-radius: 12px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
      width: 350px;
    }
    h2 {
      text-align: center;
      color: #2980b9;
      margin-bottom: 25px;
    }
    input[type="text"], input[type="password"] {
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
    .signup-link {
      margin-top: 15px;
      text-align: center;
    }
    .signup-link a {
      color: #2980b9;
      text-decoration: none;
      font-weight: bold;
    }
    .signup-link a:hover {
      text-decoration: underline;
    }
    .error {
      color: red;
      text-align: center;
      margin-bottom: 10px;
    }
    .success {
      color: green;
      text-align: center;
      margin-bottom: 10px;
    }
  </style>
</head>
<body>
  <div class="login-container">
    <h2>User Login</h2>

    <?php if (!empty($error)): ?>
      <div class="error"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <?php if (isset($_GET['signup']) && $_GET['signup'] === 'success'): ?>
      <div class="success">Signup successful! Please log in.</div>
    <?php endif; ?>

    <form method="POST" id="loginForm">
      <input type="text" name="username" placeholder="Username" autocomplete="off" required />
      <input type="password" name="password" placeholder="Password" autocomplete="off" required />
      <button type="submit">Login</button>
    </form>

    <div class="signup-link">
      <p>Don't have an account? <a href="signup.php">Sign up here</a></p>
    </div>
  </div>
</body>
</html>
