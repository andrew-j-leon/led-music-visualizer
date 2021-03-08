<?php     
    $hueRange = explode("-", $_POST["hueRange"]);
    $hueRange[0] = trim($hueRange[0]);
    $hueRange[1] = trim($hueRange[1]);

    $jsonArray = array(
        "visualizationType" => $_POST["visualizationType"],
        "brightness"        => $_POST["brightness"],
        "ampThreshold"      => $_POST["ampThreshold"],
        "ledPerAmp"         => $_POST["ledPerAmp"],
        "saturation"        => $_POST["saturation"],
        "lightness"         => $_POST["lightness"],
        "hueRange"          => $hueRange,
        "colorChangeType"   => $_POST["colorChangeType"]
    );
    
    $jsonObj = json_encode($jsonArray, JSON_PRETTY_PRINT);
    file_put_contents("../../json/config.json", $jsonObj);
    
    header("Location: ../../index.php");
?>