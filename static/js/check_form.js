function required() {
	var origin = document.forms["route_form"]["origin"].value;
	var dest = document.forms["route_form"]["destination"].value;
	if(origin == "" && dest == "") {
		alert("Valitse lähtö- ja päätepysäkki.");
		return false;
	}
	else if(origin == "") {
		alert("Valitse lähtöpysäkki.");
		return false;
	}
	else if(dest == "") {
		alert("Valitse päätepysäkki.");
		return false;
	}

	origin = origin.toUpperCase();
	if(stops.indexOf(origin) < 0) {
		alert("Antamaasi lähtöpysäkkiä ei löytynyt järjestelmästä.");	
		return false;
	}

	dest = dest.toUpperCase();
	if(stops.indexOf(dest) < 0) {
		alert("Antamaasi päätepysäkkiä ei löytynyt järjestelmästä.");
	}

	return true
}