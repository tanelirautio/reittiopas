from flask import Flask, request, render_template
from routeplanner import routeplanner
import os
import sys
import json

app = Flask(__name__, static_url_path='/static')
route_file = os.path.join(app.static_folder, 'json/reittiopas.json')

def get_page_template(routetable):
	if routetable is None:
		routetable = ""
	else:
		print(routetable)
	stops = routeplanner.get_stops(route_file)
	return render_template('results.html', title='Reittiopas', stops=stops, routetable=routetable)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		origin = request.form.get('origin')
		destination = request.form.get('destination')
		print("Origin: {}, Destination: {}".format(origin, destination))

		routetable = routeplanner.search(route_file, origin, destination)
		return get_page_template(routetable)
		#main.route_planner(json_file)

	return get_page_template(None)

@app.route('/hello')
def hello_world():
    return '<h1>Hello, World!</h1><ul><li>test1</li><li>test2</li></ul>'

#https://templated.co/transit

if __name__ == "__main__":
	app.run()