import json

class Stop:
	def __init__(self, name):
		self.__name = name

	@property
	def name(self):
		return self.__name

	def __str__(self):
		return "[Stop: {}]".format(self.__name)

class Road:
	def __init__(self, start, end, time):
		self.__start = start
		self.__end = end
		self.__time = time
		self.__lines = []

	@property
	def start(self):
		return self.__start

	@property
	def end(self):
		return self.__end

	@property
	def time(self):
		return self.__time

	def add_line(self, line):
		self.__lines.append(line)

	@property
	def lines(self):
		return self.__lines

	def __str__(self):
		return "[From: {}, Where: {}, Time: {}]".format(self.__start, self.__end, self.__time) 

class Line:
	def __init__(self, name, stops):
		self.__name = name
		self.__stops = stops

	@property
	def name(self):
		return self.__name

	@property
	def stops(self):
		return self.__stops

	def __str__(self):
		return "[Line: {}, Stops: {}]".format(self.__name, self.__stops)

class Data:
	def __init__(self, stops, roads):
		self.__stops = stops
		self.__roads = roads

	@property
	def stops(self):
		return self.__stops

	@property
	def roads(self):
		return self.__roads

	def get_road(self, start, end):
		for road in self.__roads:
			if(road.start == start and road.end == end or road.start == end and road.end == start):
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
		start = road.start
		end = road.end
		time = road.time

		usedRoad = Road(start, end, time)
		addRoad = False
		for line in Lines:
			stops = line.stops
			if road.start in stops and road.end in stops:
				if(stops.index(start) == stops.index(end) + 1 or stops.index(start) == stops.index(end) - 1):
					#print("Adding line: {}: {} - {}".format(line.name, start, end))
					usedRoad.add_line(line)	
					addRoad = True

		if addRoad:
			UsedRoads.append(usedRoad)

	d = Data(Stops, UsedRoads)
	return d





