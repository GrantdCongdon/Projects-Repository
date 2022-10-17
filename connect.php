<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="style.css">
<style>
#map {
	height: 400px;
	width: 100%;
}
</style>
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
$hour = 12;
$time = (int)date("H");
$activate = 0;
// Create connection
$con = new mysqli($servername, $username, $password, $db);

// Check connection
if ($con->connect_error) {
    die("Connection failed: " . $con->connect_error);
}
//Trash Breaker
/*echo "Active: " . $stateCheck["on_off"];
if ($stateCheck["on_off"] == 0) {
$activate = 0;
}
else {
$activate = 1;
}
*/
$display = "SELECT * FROM students";
$result = $con->query("$display");
if ($result->num_rows > 0) {
	while($row = $result->fetch_assoc()) {
		if ($row["admin"]==1 && $_POST["pwd"]==$row["ID"] && $_POST["usr"]==$row["username"]) {
			echo "<h1 id='title'>Welcome SuperUser</h1>\n</div>\n";
			$pass=True;
			$admin = $con->query("SELECT students.ID, students.firstname, students.lastname, students.username, students.busIDam, students.busIDpm, students.busID2, buses.status, buses.sub, buses.latitude, buses.longitude, buses.on_off FROM students RIGHT JOIN buses ON students.busIDam = buses.busID");
			if ($admin->num_rows > 0) {
				echo "<br><form action='admin.php' method='post'>\n<p id='searchFirstname'>Firstname: <input type='username' name='frst'></p>\n<p id='searchLastname'>Lastname: <input type='username' name='lst'></p>\n<p id='secondPassword'> Password: <input type='password' name='pwd'>\n</p>\n<input class='submit' type='submit'>\n</form>";
				while($row = $admin->fetch_assoc()) {
					echo "<h3>ID: ".$row["ID"]." || Firstname: ". $row["firstname"]. " || Lastname: ".$row["lastname"]." || Username: ".$row["username"]." || BusIDam: ".$row["busIDam"]." || BusIDpm: ".$row["busIDpm"]." || BusID2: ".$row["busID2"]." || Status: ".$row["status"]." || Sub: ".$row["sub"]." || Latitude: ".$row["latitude"]." || Longitude: ".$row["longitude"]." || Active: ".$row["on_off"]."</h3>\n";
				}
			}
			else {
				echo "<h1>Admin Query Failed</h1>";
			}
		}
		elseif ($_POST["pwd"]==$row["ID"] && $_POST["usr"]==$row["username"] && $row["admin"]==0) {
			$pass = True;
			//$info = $con->query("SELECT students.firstname, students.lastname, students.busIDam, students.busIDpm, students.busID2, buses.status, buses.sub, buses.latitude, buses.longitude, buses.on_off FROM students RIGHT JOIN buses ON students.busIDam = buses.busID WHERE students.ID = " . $_POST["pwd"]);
			echo "<p id='name'>".$row["firstname"]." ".$row["lastname"];
			if ($hour <= $time) {
				$info = $con->query("SELECT students.firstname, students.lastname, students.busIDpm, buses.status, buses.sub, buses.longitude, buses.latitude, buses.on_off FROM students RIGHT JOIN buses ON students.busIDpm = buses.busID WHERE students.ID = ".$_POST["pwd"]);
				if ($info->num_rows > 0) {
					echo "\n<h1>Bus " . $row["busIDpm"]. " information</h1>\n</div>\n";
                			while ($row = $info->fetch_assoc()) {
						if ($row["on_off"] == 0) { echo "<h2>Bus Tracker System Offline</h2>"; }
						else {
                        				echo "<br><h2>Bus Status: " . $row["status"]. "</h2><h2 id='sub'>Sub: " . $row["sub"]. "</h2>\n";
							echo "<br><h4>Location</h4>\n";
							echo "<div id='map'></div>\n";
							echo "<script>\n";
							echo "function initMap() {\n";
							echo 'var uluru = {lat: '.$row["latitude"].', lng: '.$row["longitude"].'};\n';
							echo "var map = new google.maps.MAP(document.getElementById('map'), {zoom: 14, center: uluru});\n";
							echo "var marker = new google.maps.Marker({position:uluru, map: map});\n}\n";
							echo "</script>\n";
							echo "<script async defer\n src='https://maps.googleapis.com/maps/api/js?key='>\n</script>\n";
						}
					}
				}
				else { echo "<h2>Error with PM main query</h2>"; }
                	}
			else {
				$info = $con->query("SELECT students.firstname, students.lastname, students.busIDam, buses.status, buses.sub, buses.longitude, buses.latitude, buses.on_off FROM students RIGHT JOIN buses ON students.busIDam = buses.busID WHERE students.ID = ".$_POST["pwd"]);
				if ($info->num_rows > 0) {
					echo "\n<h1>Bus " . $row["busIDam"]. " information</h1>\n</div>\n";
					while ($row = $info->fetch_assoc()) {
						if ($row["on_off"] == 0) { echo "<h2>Bus Tracker System Offline</h2>"; }
						else {
							echo "<br><h2>Bus Status: " . $row["status"]. "</h2><h2 id='sub'>Sub: " . $row["sub"]. "</h2>\n";
                                        		echo "<br><h4>Location</h4>\n";
							echo "<br><p class='coords'>Longitude: " . $row["longitude"]. "<br>Latitude: " . $row["latitude"]. "</p>\n";
							echo "<div id='map'></div>\n";
							echo "<script>\n";
							echo "function initMap() {\n";
							echo "var uluru = {lat: ".$row['latitude'].", lng: ".$row['longitude']."};\n";
							echo "var map = new google.maps.MAP\n(document.getElementById('map'), {zoom: 14, center: uluru});\n";
							echo "var marker = new google.maps.Marker({position:uluru, map: map});\n}\n";
							echo "</script>\n";
							echo '<script async defer src="https://maps.googleapis.com/maps/api/js?key="></script>';
						}
					}
				}
				else { echo "<h2>Error with AM main query</h2>"; }
			}
        	}
	}
	if ($pass == False) {
		echo "<h1>Access Denied</h1>\n</div>\n";
	}
}
else {
	echo "<h1>Database Access Failed No Rows Detected</h1>";
}
$con->close();

?>

</body>
</html>
