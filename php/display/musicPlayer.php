<?php     
    $currentSong = getCurrentSong();    
    
    $CSS_FILE = CSS_DIR . "musicPlayer.css";
    echo "<link rel='stylesheet' type='text/css' href=$CSS_FILE>";
    
    echo "
    <h2>Currently playing: $currentSong</h2>
    ";
    
    $playSongButton = "";
    if ($currentSong == null) {
        $playSongButton = "<button class='playSongButton' disabled>Play Current Song</button>";
    }
    else {
        $playSongButton = "<button class='playSongButton' onClick=\"playSongFile('$currentSong')\">Play Current Song</button>" ;
    }
    
    $playShuffleButton = "<button class='playShuffleButton' onClick=\"playShuffle()\">Play All (Shuffle)</button>";
    
    
    echo "<div class='playButtonsContainer'>$playSongButton $playShuffleButton</div>";
    echo "<a class='settingsLink' href='php/display/settings.php'>Settings</a>";
?>






