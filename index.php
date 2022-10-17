<!DOCTYPE html>

<html>
<head>
<title>Login</title>
<script type="text/javascript" src="jquery.min.js"></script>
<script type="text/javascript">
function connectdb() {
	$.get("connect.php");
	return false;
}
</script>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<div class="header">
<a href="/">
<img src="westGeaugaLogo.jpg" alt="Logo">
</a>
<h1>WGMS Bus Locator Website</h1>
</div>
<br><form action="connect.php" method="post" id="login">
Username: <input type="username" name="usr"><br>
StudentID: <input type="password" name="pwd"><br>
<input class="submit" type="submit">
</form>
<img id="mainImage" src="bus.png" alt="bus">
</body>
</html>
