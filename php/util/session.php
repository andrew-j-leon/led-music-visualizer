<?php
    session_start();

    /**
     * Sets the current song (in the $_SESSION["currentSong"])
     * to $newSong.
     * 
     * @param {string} $newSong : The location of the new song
     * that the music player should play.
     */
    function setCurrentSong($newSong) {
        if (!is_string($newSong))
            throw new InvalidArgumentException("Argument must be a string value");
        
        $_SESSION["currentSong"] = $newSong;
    }
    
    /**
     * @return string : The name of the currently selected song
     *                  (e.g. "Minuet of Forest.wav"). If no song is currently selected,
     *                  returns null.
     */
    function getCurrentSong() {
        if (is_string($_SESSION["currentSong"]))
            return $_SESSION["currentSong"];
        else 
            return null;
    }

?>