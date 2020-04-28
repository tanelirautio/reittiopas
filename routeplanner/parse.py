import json

class Stop:
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "[Stop: {}]".format(self.name)

class Road:
	def __init__(self, start, end, time):
		self.start = start
		self.end = end
		self.time = time
		self.lines = []

	def get_start(self):
		return self.start

	def get_end(self):
		return self.end

	def get_time(self):
		return self.time

	def add_line(self, line):
		self.lines.append(line)

	def get_lines(self):
		return self.lines

	def __str__(self):
		return "[From: {}, Where: {}, Time: {}]".format(self.start, self.end, self.time) 

class Line:
	def __init__(self, name, stops):
		self.name = name
		self.stops = stops

	def get_name(self):
		return self.name

	def get_stops(self):
		return self.stops

	def __str__(self):
		return "[Line: {}, Stops: {}]".format(self.name, self.stops)

class Data:
	def __init__(self, stops, roads):
		self.stops = stops
		self.roads = roads

	def get_stops(self):
		return self.stops

	def get_roads(self):
		return self.roads

	def get_road(self, start, end):
		for road in self.roads:
			if(road.get_start() == start and road.get_end() == end or road.get_start() == end and road.get_end() == start):
				return road
		return None

def get_stops(filename):
	with open(filename) as json_file:
		jsonStr = json.load(json_file)
		return jsonStr["pysakit"]
			
def parse(filename):
	#print("You passed filename " + filename)
	
	Stops = []
	Roads = []
	Lines = []

	with open(filename, encoding="utf-8") as json_file:
		#print("Opened json file")
		jsonStr = json.load(json_file)

		for pysakki in jsonStr["pysakit"]:
			p = Stop(pysakki)
			Stops.append(p)
		
		#print(*Stops)

		for tie in jsonStr["tiet"]:
			r = Road(tie["mista"], tie["mihin"], tie["kesto"])
			Roads.append(r) 
		#print(*Roads) 

		line = jsonStr["linjastot"]
		for name in line:
			stops = line[name]
			l = Line(name, stops)
			Lines.append(l)
		#print(*Lines)

	# Use only roads that have lines running, drop unused roads
	UsedRoads = []
	for road in Roads:
		start = road.get_start()
		end = road.get_end()
		time = road.get_time()

		usedRoad = Road(start, end, time)
		addRoad = False
		for line in Lines:
			stops = line.get_stops()
			if start in stops and end in stops:
				if(stops.index(start) == stops.index(end) + 1 or stops.index(start) == stops.index(end) - 1):
					#print("Adding line: {}: {} - {}".format(line.get_name(), start, end))
					usedRoad.add_line(line)	
					addRoad = True

		if addRoad:
			UsedRoads.append(usedRoad)

	d = Data(Stops, UsedRoads)
	return d





