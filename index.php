<?php 
    require_once "php/util/debugging.php";
    require_once "php/util/constants.php";
    require_once "php/util/session.php";
    
    session_start();
?>


<!DOCTYPE html>

<html>
	<head>
		<?php 
            $INDEX_CSS = CSS_DIR . "index.css";
            echo "<link rel='stylesheet' type='text/css' href=$INDEX_CSS>";
        ?>
		<script src="js/musicPlayer.js"></script>
	</head>

	<body class="mainPage">
		<h1>Music Player and LED Strip Visualizer</h1>
		
		<?php require "php/display/musicPlayer.php";?>
		<hr/>
		<?php require "php/display/savedMusicTable.php";?>
		
	</body>

</html>