<?php

/**
 * Displays the provided $data to the browser console.
 * @param {object} $data : The thing to display to the browser console.
 */
function consoleLog($data) {
    $js_code = "console.log(" . json_encode($data, JSON_PRETTY_PRINT) . ");";
    
    echo "<script>$js_code</script>";
}
?>