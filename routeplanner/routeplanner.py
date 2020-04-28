from routeplanner import parse
from routeplanner import graph
from routeplanner import finder

def get_stops(filename):
	stops = parse.get_stops(filename)   
	return stops
		
def search(filename, origin, destination):
	origin = origin.upper()
	destination = destination.upper()
	#print("origin: " + origin)
	#print("destination: " + destination)
	stops = get_stops(filename)
	#print(stops)

	if(origin in stops and destination in stops):
		if(origin == destination):
			return "<p>Lähtö- ja päätepysäkki ovat samat!</p>"
		else:
			data = parse.parse(filename)		
			g = graph.create(data)
			#print_graph(g)		

			dijkstra = graph.dijkstra(g, g.get_vertex(origin), g.get_vertex(destination))

			target = g.get_vertex(destination)
			path = [target.get_id()]
			graph.shortest(target, path)
			print("The shortest path: {}".format(path[::-1]))

			return finder.find_lines_from_route(path[::-1], data)
	else:
		return None

def print_graph(g):
	print("Graph data:")
	for v in g:
		for w in v.get_connections():
				vid = v.get_id()
				wid = w.get_id()
				print("({} , {}, {})".format( vid, wid, v.get_weight(w)))
