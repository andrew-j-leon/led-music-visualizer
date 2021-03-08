<?php
    $songFile = $_GET["songFile"]; // Just the song name (e.g. "Minuet of Forest.wav").
    system("START python ../../python/mainClient.py ../../music/\"$songFile\" ../../json/config.json");
?>