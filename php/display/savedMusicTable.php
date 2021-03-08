<?php 

    class MyFile {
        private $fileName;
        private $size;
        
        function __construct($fileName, $size) {
            $this->fileName = $fileName;
            $this->size = $size;
        }
        
        function getFilename() {
            return $this->fileName;
        }
        
        function getSize() {
            return $this->size;
        }
    }

    /**
     * 
     * @param {MyFile} $file1
     * @param {MyFile} $file2
     * @return number
     */
    function compareFiles($file1, $file2) {
        return strcmp($file1->getFilename(), $file2->getFilename());
    }
    
    /**
     * Creates a table of all songs stored in the given "$songDirectory".
     * 
     * @param {string} $songDirectory : The directory containing all the songs.
     * @return {string}               : A string that can be used to display a  table of all songs
     *                                  in the given "$songDirectory".
     */
    function createTableOfSongs($songDirectory) {
        // The table head
        $tableHead = "
            <thead>
                <tr>
                    <th></th>
                    <th>Title</th>
                    <th>Size (MB)</th>
                </tr>
            </thead>";
        
        // The table body
        $tableBody = "<tbody>";
        
        // Get each file in the provided song directory.
        $dirIterator = new DirectoryIterator($songDirectory);
        $files = array();
        foreach ($dirIterator as $file) {
            $fileName = $file->getFilename();
            $fileSize = $file->getSize();
            if ($fileName !== "." && $fileName !== "..")
                array_push($files, new MyFile($fileName, $fileSize));
        }
        // Sort by file name
        usort($files, "compareFiles");
        
        foreach ($files as $file) {
            $fileName = $file->getFilename();
            $fileSize_MB = round($file->getSize()/1000000.0, 3);
            
            // The filename might need to be encoded for use in the URL (e.g. if it contains spaces or &'s)
            $href = PHP_UTIL_DIR . "changeSong.php?newSong=" . urlencode($fileName);
            $tableRow = "
                <tr> 
                    <td><a href=\"$href\">Select</a></td>
                    <td>$fileName</td>
                    <td>$fileSize_MB</td>
                </tr>";
            
            $tableBody .= $tableRow;
        }
        $tableBody .= "</tbody>";
        
        return "<div class='musicTableContainer'><table class='musicTable'>" . $tableHead . $tableBody . "</table></div>";
    }
    
    // Add the CSS for the table
    $CSS_FILE = CSS_DIR . "savedMusicTable.css";
    echo "<link rel='stylesheet' type='text/css' href=$CSS_FILE>";
    
    // Display the table
    echo createTableOfSongs(MUSIC_DIR);
?>