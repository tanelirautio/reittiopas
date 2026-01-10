from flask import Flask, request, render_template
from . import routeplanner
import os
import sys
import json

app = Flask(__name__, static_url_path='/static')
route_file = os.path.join(app.static_folder, 'json/reittiopas.json')

def get_page_template(routetable, selected_origin, selected_destination):
	if routetable is None:
		routetable = ""
	stops = routeplanner.get_stops(route_file)
	return render_template('results.html', title='Reittiopas', stops=stops, routetable=routetable, selected_origin=selected_origin, selected_destination=selected_destination)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		origin = request.form.get('origin')
		destination = request.form.get('destination')
		#print("Origin: {}, Destination: {}".format(origin, destination))

		routetable = routeplanner.search(route_file, origin, destination)
		return get_page_template(routetable, origin, destination)
		
	return get_page_template(None, "", "")

if __name__ == "__main__":
	app.run()