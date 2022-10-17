<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<div class="header">
<a href="/">
<img src="westGeaugaLogo.jpg" alt="Logo">
</a>
<?php

$servername = "localhost";
$username = "root";
$password = "";
$db = "project";
$pass = False;

$con = new mysqli($servername, $username, $password, $db);

if ($con->connection_error) {
	die("Connection failed: " . $con->connect_error);
}

$select = "SELECT * FROM students WHERE ID = ".$_POST["pwd"];
$result = $con->query("$select");
if ($result->num_rows > 0) {
	while($row = $result->fetch_assoc()) {
		if ($row["ID"]==$_POST["pwd"]) {
			$find = "SELECT * FROM students WHERE firstname = '" . $_POST["frst"]. "' AND lastname = '". $_POST["lst"]. "'";
			$resultFind = $con->query("$find");
			$findGeneral = "SELECT * FROM students WHERE firstname = '" . $_POST["frst"]. "' OR lastname = '" . $_POST["lst"]. "'";
			$pass = True;
			if ($resultFind->num_rows > 0) {
				while ($row = $resultFind->fetch_assoc()) {
					echo "<h1>Bus information for: ".$row["firstname"]."</h1>\n</div>\n";
					echo "<h3>ID: ".$row["ID"]." || Firstname: ". $row["firstname"]." || Username: ".$row["username"]." || Latitude: ".$row["latitude"]." || Longitude: ".$row["longitude"]." || Status: ".$row["status"]." || Sub: ".$row["sub"]." || BusIDam: ".$row["busIDam"]." || BusIDpm: ".$row["busIDpm"]." || BusID2: ".$row["busID2"]."</h3>\n";
				}
			}
			elseif ($resultFind->num_rows == 0) {
				$getresult = $con->query("$findGeneral");
				if ($getresult->num_rows > 0) {
					while ($row = $getresult->fetch_assoc()) {
						echo "<h1>Bus information for: ".$row["firstname"]."</h1>\n</div>\n";
						echo "<h3>ID: ".$row["ID"]." || Firstname: ". $row["firstname"]." || Username: ".$row["username"]." || Latitude: ".$row["latitude"]." || Longitude: ".$row["longitude"]." || Status: ".$row["status"]." || Sub: ".$row["sub"]." || BusIDam: ".$row["busIDam"]." || BusIDpm: ".$row["busIDpm"]." || BusID2: ".$row["busID2"]."</h3>\n";
					}
				}
				else {
					echo "<h2>Person Not Found</h2>\n";
				}
			}
			else {
				echo "<h2>Person Not Found</h2>\n";
			}
		}
		elseif ($pass==False) {
			echo "<h2>Access Denied</h2>\n";
		}
	}
}
else {
	echo "<h2>Database Connection Fail</h2>\n";
}
?>
</body>
</html>
