function my_alert(title, message) {
	new Attention.Alert({
    title: title,
    content: message
	});
}

function required() {
	var origin = document.forms["route_form"]["origin"].value;
	var dest = document.forms["route_form"]["destination"].value;
	if(origin == "" && dest == "") {
		my_alert("Virhe", "Valitse lähtö- ja päätepysäkki.");
		return false;
	}
	else if(origin == "") {
		my_alert("Virhe", "Valitse lähtöpysäkki.");
		return false;
	}
	else if(dest == "") {
		my_alert("Virhe", "Valitse päätepysäkki.");
		return false;
	}

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

	return true
}

