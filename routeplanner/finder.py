from flask_table import Table, Col
import parse

class RouteTable(Table):
	icon = Col('Linja',  th_html_attrs={'scope': 'col'}, td_html_attrs={'data-label': 'Linja'},)
	line = Col('',  th_html_attrs={'scope': 'col'}, td_html_attrs={'data-label': ''},)
	start = Col('Lähtö', th_html_attrs={'scope': 'col'}, td_html_attrs={'data-label': 'Lähtö'},)
	end = Col('Kohde', th_html_attrs={'scope': 'col'}, td_html_attrs={'data-label': 'Kohde'},)
	time = Col('Aika', th_html_attrs={'scope': 'col'}, td_html_attrs={'data-label': 'Aika'},)
	intermediates = Col('Välipysäkit', th_html_attrs={'scope': 'col'}, td_html_attrs={'data-label': 'Välipysäkit'},)

class TableEntry:
	def __init__(self, line, start, end, time, intermediates):
		self.__line = line
		self.__start = start
		self.__end = end
		self.__time = time
		self.__intermediates = intermediates

	@property
	def icon(self):
		color = ""
		if self.__line == "keltainen":
			color = "yellow"
		elif self.__line == "punainen":
			color = "red"
		elif self.__line == "vihreä":
			color = "green"
		else:
			color = "blue"
		return "<img src=\"/static/images/bus_" + color + ".png\" width=\"40\" height=\"40\" alt=\""+ self.__line +"\"/>"


	@property
	def line(self):
		return self.__line

	@property
	def start(self):
		return self.__start
	
	@property
	def end(self):
		return self.__end
	
	@property
	def time(self):
		return self.__time

	@property
	def intermediates(self):
		if len(self.__intermediates) == 0:
			return "-"
		return ", ".join(self.__intermediates)
	
	def __str__(self):
		return "[Line: {} Start: {}, End: {}, Time: {}, Intermediate stops: {}]".format(self.__line, self.__start, self.__end, self.__time, self.__intermediates)

class RouteEntry:
	def __init__(self, start, end, time, line_names):
		self.__start = start
		self.__end = end
		self.__time = time
		self.__possible_lines = line_names
		self.__best_line = ""
	
	@property
	def start(self):
		return self.__start
	
	@property
	def end(self):
		return self.__end

	@property
	def time(self):
		return self.__time

	@property
	def possible_lines(self):
		return self.__possible_lines
	
	@property
	def best_line(self):
		return self.__best_line

	@best_line.setter
	def best_line(self, line):
		self.__best_line = line
	
	def __str__(self):
		return "[Start: {}, End: {}, Time: {}, Lines: {}, Best line: {}]".format(self.__start, self.__end, self.__time, self.__possible_lines, self.__best_line)

# Find the optimal lines that are serving the selected route
def find_lines_from_route(path, data):
	route_data = find_best_lines(path, data)
	route_table = process_route_data(route_data, path[0], path[-1])
	return route_table

# Find all the lines that run the given route. Note that there can be multiple lines serving some stops
def find_best_lines(path, data):
	route_data = []
	for (index, stop) in enumerate(path):
		if index < len(path)-1:
			start, end = stop, path[index + 1]
			
			line_names = []
			r = data.get_road(start, end)
			if r:
				for line in r.lines:
					line_names.append(line.name)
					#print("Line: {} - {}, Name: {}, Time: {}".format(start, end, line, r.time))
			entry = RouteEntry(start, end, r.time, line_names)
			route_data.append(entry)

	# Select best line if there are multiple options in a certain road
	current_line = ""
	previous_line = ""
	current_line_time = 0
	for (index, route) in enumerate(route_data):
		if len(route.possible_lines) == 1:
			current_line = route.possible_lines[0]
		else:
			current_line = choose_best_line(route_data, index, route.possible_lines, previous_line)
		route_data[index].best_line = current_line
		previous_line = current_line

	#for (index, route) in enumerate(route_data):
	#	print(str(index) + ": " + str(route))

	return route_data

def choose_best_line(route_data, index, possible_lines, previous_line):

	# Use same line as previous road did if it's an option
	if previous_line in possible_lines:
		return previous_line

	# Line change is required. Select best line from possible_lines by examining possible lines of next entry 
	if(index + 1 < len(route_data)):
		next_lines = route_data[index+1].possible_lines

		if len(next_lines) == 1:
			next_line = next_lines[0]
			if next_line in possible_lines:
				# Only one possible line continues in next road so use that
				return next_line
			else:
				# All possible lines are equally valid, just return first one from the list
				return possible_lines[0]
		else:
			# Multiple line options, check if only one option from possible_lines is available
			matching_lines = set(possible_lines) & set(next_lines)
			match_len = len(matching_lines)
			if match_len == 0:
				# All possible_lines are equal just return first one from the list
				return possible_lines[0]
			elif len(matching_lines) == 1:
				# Only one possible line in both possible_lines & next_lines
				return list(matching_lines)[0]
			else:
				# Multiple options, seatrch next roads recursively
				return choose_best_line(route_data, index+1, list(matching_lines), previous_line)
	else:		
		# If all else fails just return the first option from the possible lines list
		return possible_lines[0]

# Parse data to be represented in the html table
def process_route_data(route_data, origin, destination):
	table_entries = []

	# Variables for 'current' line
	c_line = route_data[0].best_line
	c_start = route_data[0].start
	c_end = ""
	c_time = route_data[0].time
	c_intermediates = []

	complete_time = 0
	for (index, route) in enumerate(route_data):
		complete_time += route.time
		if index < len(route_data):
			if(route.best_line != c_line):
				c_end = route.start
				#print("Creating TableEntry: " + c_line + ", " + c_start + ", " + c_end)
				t = TableEntry(c_line, c_start, c_end, c_time, c_intermediates)
				table_entries.append(t)

				c_line = route.best_line
				c_start = route.start
				c_end = ""
				c_time = route.time
				c_intermediates = []
			else:
				if route.start != c_start:
					c_time += route.time
					c_intermediates.append(route.start)	

	c_end = route.end
	#print("Creating TableEntry: " + c_line + ", " + c_start + ", " + c_end)
	t = TableEntry(c_line, c_start, c_end, c_time, c_intermediates)
	table_entries.append(t)


	table = RouteTable(table_entries)
	table_html = table.__html__()

	# Create caption and inject it into table html
	caption = "<caption>Reitti: " + origin + " - " + destination +"</caption>" 
	index = table_html.find('<thead>')
	table_html = table_html[:index] + caption + table_html[index:]

	# Create summary table row and inject it into table html
	summary = get_summary_table(len(table_entries)-1, complete_time)

	index = table_html.find('</table>')
	table_html = table_html[:index] + summary + table_html[index:]

	# Correct possible malformed tags
	table_html = table_html.replace('&lt;', '<').replace('&gt;', '>').replace('&#34;', '"')

	#print(table_html)
	return table_html

def get_summary_table(changes, time):
	change_txt = ""
	if changes == 0:
		change_txt = "Matkalla ei vaihtoja."
	elif changes == 1:
		change_txt = "Matkalla 1 vaihto."
	else:
		change_txt = "Matkalla " + str(changes) + " vaihtoa." 

	summary = "<tr><td colspan=\"6\">" + change_txt + " Matka-aika yhteensä " + str(time) + ".</td></tr>"
	#print(summary)

	return summary