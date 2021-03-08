<!DOCTYPE html>

<?php 
    $jsonDataStr = file_get_contents("../../json/config.json");
    $jsonDataArray = json_decode($jsonDataStr, true);
?>

<html>
	<head>
		<link rel='stylesheet' type='text/css' href=$INDEX_CSS>
		<link rel="stylesheet" type="text/css" href="../../js/jquery-ui-1.12.1/jquery-ui.min.css">
		<script src="../../js/jquery-ui-1.12.1/external/jquery/jquery.js"></script>
		<script src="../../js/jquery-ui-1.12.1/jquery-ui.min.js"></script>
		<script src="../../js/hueSlider.js"></script>
	</head>

	<body class="settingsPage">
		<h1>Settings</h1>	
		
		<form action="../util/updateSettings.php" method="post">
			<table>
				<thead></thead>
				
				<tbody>					
					<tr>
						<td>Visualization Type:</td>
						<td>
							<select name="visualizationType">
								<option value="centerDoubleBar">Center Double Bar</option>
							</select>
						</td>
					</tr>
					
					<tr>
						<td>Brightness (min=0.0 max=1.0 default=0.4):</td>
						<td><input type="text" name="brightness" value=<?php echo $jsonDataArray["brightness"];?> /></td>
					</tr>
					
					<tr>
						<td>Amplitude Threshold (default=45):</td>
						<td><input type="text" name="ampThreshold" value=<?php echo $jsonDataArray["ampThreshold"];?> /></td>
					</tr>
					
					<tr>
						<td>LEDs per Amplitude (default=3.8):</td>
						<td><input type="text" name="ledPerAmp" value=<?php echo $jsonDataArray["ledPerAmp"];?> /></td>
					</tr>
					
					<tr>
						<td> [&nbsp;<a href="http://www.google.com/search?q=Color+picker" target="_blank">Google's Color Picker</a>&nbsp;]
					</tr>
					
					<tr>
						<td>HSL Saturation (min=0 max=100 default=85):</td>
						<td><input type="number" name="saturation" min="0" max="100" value=<?php echo $jsonDataArray["saturation"];?> /></td>
					</tr>
					
					<tr>
						<td>HSL Lightness (min=0 max=100 default=45):</td>
						<td><input type="number" name="lightness" min="0" max="100" value=<?php echo $jsonDataArray["lightness"];?> /></td>
					</tr>
					
					<tr>
						<td>Hue Range Slider:</td>
						<td><div id="hueSlider"></div></td>
					</tr>
					
					<tr>
						<td></td>
						<td><input type="text" name="hueRange" id="hueRange" readonly></td>
					</tr>
					
					<tr>
						<td>Color Change Type:</td>
						<td>
							<select name="colorChangeType">
								<option value="loop">Loop</option>
								<option value="bounce">Bounce</option>
							</select>
						</td>
					</tr>
					
				</tbody>
				
				<input type="submit" value="Save Settings">
			</table>
		
		</form>	
	</body>

</html>