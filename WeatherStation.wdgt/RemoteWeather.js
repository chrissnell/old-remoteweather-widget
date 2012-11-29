function fetchWeather()
{

    var content;
    var req = new XMLHttpRequest();
	var url = "	";
        req.open("GET", "http://10.50.0.108:8000/wx", false);
	req.send(null);
	content = req.responseText;
	
	var outsideTemp        = content.match(/to=(\-*[\d\.]+)/)[1];
	var insideTemp         = content.match(/ti=(\-*[\d\.]+)/)[1];
	var windSpeed          = content.match(/ws=([\d\.]+)/)[1];
	var windDirection      = content.match(/wd=([\d\.]+)/)[1];
	var outsideHumidity    = content.match(/oh=([\d\.]+)/)[1];
	var insideHumidity     = content.match(/ih=([\d\.]+)/)[1];	
	var barometricPressure = content.match(/bp=([\d\.]+)/)[1];	
	var lastObservation    = content.match(/lo=([\d\.]+)/)[1];

	drawNeedle(windDirection);

	var outsideTempText = document.getElementById("outsideTempBox");
	outsideTempText.innerText = outsideTemp;

	var insideTempText = document.getElementById("insideTempBox");
	insideTempText.innerText = insideTemp;

	var outsideRelativeHumidityText = document.getElementById("outsideRelativeHumidityBox");
	outsideRelativeHumidityText.innerText = outsideHumidity;	
	
	var insideRelativeHumidityText = document.getElementById("insideRelativeHumidityBox");
	insideRelativeHumidityText.innerText = insideHumidity;	

	var windSpeedBox = document.getElementById("windSpeed");
	windSpeedBox.innerText = windSpeed;

}
