<?php
    /**
     * Uses the URL query variable "newSong" to
     * set the current song played by the audio player, then redirects
     * to index.php.
     */
    require_once "session.php";
    require_once "debugging.php";
    require_once "constants.php";

    $newSong = urldecode($_GET["newSong"]);
    
    setCurrentSong($newSong);    
    header("Location: ../../index.php");
?>