var myData  = [];
var arr2;
var count = 0;

/*
 * Calulate pie chart score and initiliase canvas draw
 */
function calculateMatch(make, model, yom, door_plan){

	var score = 0;

	if(make !== "" || typeof make === 'undefined'){
		score += 5;
	}

	if(model !== "" || typeof model === 'undefined'){
		score += 55;
	}

	if(yom !== "" || typeof yom === 'undefined'){
		score += 30;
	}

	if(door_plan !== "" || typeof door_plan === 'undefined'){
		score += 7;
	}

	var percent_remaining = 100 - score;

	myData = [score, percent_remaining];

	//reset pie vars
	arr2 = null;
	count = 0;

	if (Modernizr.canvas){
		animatePie();
	}
}


/*
 * Calculate next slice ratio and trigger draw
 */
function animatePie() {

	// draw stuff
	var arr = calculateFrameValue(arr2);
	if(arr !== 'stop'){
		arr2 = arr;
		plotData(arr2);

		// request new frame
		requestAnimFrame(function() {
			animatePie();
		});
	}
}


/*
 * Set new array values for frame
 */
function calculateFrameValue(arr){

	var new_score;
	var remaining;

	if(count === 0 && arr2 == null){
		new_score = 1;
		remaining = 99;
		count ++;
		updateText(new_score);
		return [new_score, remaining];
	}else if(myData[0] !== arr[0] && myData[1] !== arr[1]){
		new_score = arr[0] + 1;
		remaining = arr[1] - 1;
		updateText(new_score);
		return [new_score, remaining];
	}else{
		//finished
		return 'stop';
	}
}


/*
 * Draw graph
 */
function plotData(arr) {
	
	var canvas;
	var ctx;
	var lastend = Math.PI / 180 * 270;
	var myTotal = getTotal();
	
	canvas = document.getElementById("canvas");
	ctx = canvas.getContext("2d");
	ctx.clearRect(0, 0, canvas.width, canvas.height);

	for (var i = 0; i < arr.length; i++) {

		ctx.fillStyle = pieColour[i];
		ctx.beginPath();
		ctx.moveTo(65,65);
		ctx.arc(65,65,65,lastend,lastend+(Math.PI*2*(arr[i]/myTotal)),false);
		ctx.lineTo(65,65);

		ctx.fill();
		lastend += Math.PI*2*(arr[i]/myTotal);
	}

	//Front-circle
	var context = canvas.getContext('2d');
	var centerX = canvas.width / 2;
	var centerY = canvas.height / 2;
	var radius  = 38;

	ctx.beginPath();
	ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
	ctx.fillStyle = pieCenterColour;
	ctx.fill();
}


/*
 * Get number of slices
 */
function getTotal(){
	var myTotal = 0;
	for (var j = 0; j < myData.length; j++) {
		myTotal += (typeof myData[j] == 'number') ? myData[j] : 0;
	}
	return myTotal;
}


/*
 * Update percent
 */
function updateText(percent){
	$('#match_percent').html(percent+'%');
}


/*
 * Get new animation frame
 */
window.requestAnimFrame = (function(callback) {
	return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
	function(callback) {
		window.setTimeout(callback, 1000 / 160);
	};
})();