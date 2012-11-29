var clockTimerInterval = null;


var needle = new Image (10, 48);
needle.src = 'Images/NeedleSmall.png';
needle.onload = imageLoaded;

imageLoaded.numImages = 1;
imageLoaded.count = 0;


function imageLoaded(evt) {
	imageLoaded.count++;
	if (imageLoaded.numImages == imageLoaded.count) {
		onshow();
	}
}


function onshow() {
	if (clockTimerInterval == null) {
		startClockTimer();
	}
}

function onhide () {
    if (clockTimerInterval != null) {
        clearInterval(clockTimerInterval);
        clockTimerInterval = null;
    }
}


function startClockTimer()
{
	stopClockTimer();
	clockTimerInterval = setInterval("fetchWeather();", 5000);
}

function stopClockTimer()
{
	if (clockTimerInterval != null)
	{
		clearInterval(clockTimerInterval);
		clockTimerInterval = null;
	}
}



function drawNeedle (bearing)
{
	var canvas = document.getElementById("needleCanvas");
    var context = canvas.getContext("2d");
	
	//var needle = new Image (13, 64);
	//needle.src = 'Images/Needle.png';

	var pi = Math.PI;
	var bearingRad = ((bearing)*(pi/180));
	
	context.save();
	context.clearRect(0, 0, 76, 76);
	context.translate(38, 38);
	context.rotate(bearingRad);
	context.drawImage(needle, -5, -24, 10, 48);
	//context.fillStyle = "rgb(200,0,0)";
	//context.fillRect(-25, -25, 50, 50);
	context.restore();
	//context.translate(100/2, 100/2);
	//context.drawImage(needle, 0, 0, 13, 64);

}


//
// Function: load()
// Called by HTML body element's onload event when the widget is ready to start
//
function load()
{
    setupParts();
	fetchWeather();
}

//
// Function: remove()
// Called when the widget has been removed from the Dashboard
//
function remove()
{
    // Stop any timers to prevent CPU usage
    // Remove any preferences as needed
    // widget.setPreferenceForKey(null, createInstancePreferenceKey("your-key"));
}

//
// Function: hide()
// Called when the widget has been hidden
//
function hide()
{
    // Stop any timers to prevent CPU usage
    if (clockTimerInterval != null) {
        clearInterval(clockTimerInterval);
        clockTimerInterval = null;
    }
}

//
// Function: show()
// Called when the widget has been shown
//
function show()
{
    // Restart any timers that were stopped on hide
	if (clockTimerInterval == null) {
		startClockTimer();
	}
}

//
// Function: sync()
// Called when the widget has been synchronized with .Mac
//
function sync()
{
    // Retrieve any preference values that you need to be synchronized here
    // Use this for an instance key's value:
    // instancePreferenceValue = widget.preferenceForKey(null, createInstancePreferenceKey("your-key"));
    //
    // Or this for global key's value:
    // globalPreferenceValue = widget.preferenceForKey(null, "your-key");
}

//
// Function: showBack(event)
// Called when the info button is clicked to show the back of the widget
//
// event: onClick event from the info button
//
function showBack(event)
{
    var front = document.getElementById("front");
    var back = document.getElementById("back");

    if (window.widget) {
        widget.prepareForTransition("ToBack");
    }

    front.style.display = "none";
    back.style.display = "block";

    if (window.widget) {
        setTimeout('widget.performTransition();', 0);
    }
}

//
// Function: showFront(event)
// Called when the done button is clicked from the back of the widget
//
// event: onClick event from the done button
//
function showFront(event)
{
    var front = document.getElementById("front");
    var back = document.getElementById("back");

    if (window.widget) {
        widget.prepareForTransition("ToFront");
    }

    front.style.display="block";
    back.style.display="none";

    if (window.widget) {
        setTimeout('widget.performTransition();', 0);
    }
}

if (window.widget) {
    widget.onremove = remove;
    widget.onhide = hide;
    widget.onshow = show;
    widget.onsync = sync;
}
