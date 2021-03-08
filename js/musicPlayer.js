function playSongFile(songFile) {	
	console.log("clicked play song file");
	let fetchURL = "php/util/playSongFile.php?songFile=" + encodeURIComponent(songFile);
	console.log(songFile);
	console.log(fetchURL);
	fetch(fetchURL).then((res) => {
		res.text().then((res) => {
			console.log(res);
		});
	});
}

function playShuffle() {   
   console.log("clicked play shuffle");
   let fetchURL = "php/util/playShuffle.php";
   fetch(fetchURL).then((res) => {
      res.text().then((res) => {
         console.log(res);
      });
   });
}