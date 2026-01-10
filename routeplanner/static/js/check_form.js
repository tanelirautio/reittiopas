function my_alert(title, message) {
	new Attention.Alert({
    title: title,
    content: message
	});
}

function required() {
	var originSelect = document.getElementById("origin");
	var origin = originSelect.options[originSelect.selectedIndex].text;


	var destSelect = document.getElementById("destination");
	var dest = destSelect.options[destSelect.selectedIndex].text;

	//var origin = document.forms["route_form"]["origin"].value;
	//var dest = document.forms["route_form"]["destination"].value;
	if(originSelect.selectedIndex == 0 && destinationSelect.selectedIndex == 0) {
		my_alert("Virhe", "Valitse lähtö- ja päätepysäkki.");
		return false;
	}
	else if(originSelect.selectedIndex == 0) {
		my_alert("Virhe", "Valitse lähtöpysäkki.");
		return false;
	}
	else if(destinationSelect.selectedIndex == 0) {
		my_alert("Virhe", "Valitse päätepysäkki.");
		return false;
	}

	/*
	origin = origin.toUpperCase();
	if(stops.indexOf(origin) < 0) {
		my_alert("Virhe", "Antamaasi lähtöpysäkkiä ei löytynyt järjestelmästä.");	
		return false;
	}

	dest = dest.toUpperCase();
	if(stops.indexOf(dest) < 0) {
		my_alert("Virhe", "Antamaasi päätepysäkkiä ei löytynyt järjestelmästä.");
		return false;
	}
	*/

	return true
}

