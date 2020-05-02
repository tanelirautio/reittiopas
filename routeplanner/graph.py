import sys

class Vertex:
    def __init__(self, node):
        self.__id = node
        self.__adjacent = {}
        self.__distance = sys.maxsize
        self.__visited = False
        self.__previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.__adjacent[neighbor] = weight

    @property
    def adjacent(self):
        return self.__adjacent
    
    @property
    def connections(self):
        return self.__adjacent.keys()
    
    @property
    def id(self):
        return self.__id
    
    def get_weight(self, neighbor):
        return self.__adjacent[neighbor]

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, dist):
        self.__distance = dist

    @property
    def previous(self):
        return self.__previous
    
    @previous.setter
    def previous(self, prev):
        self.__previous = prev

    @property
    def visited(self):
        return self.__visited
    
    @visited.setter
    def visited(self, visited):
        self.__visited = visited

    def __str__(self):
        return str(self.__id) + " adjacent: " + str([x.id for x in self.__adjacent])

    # Relative comparison for <
    def __lt__(self, other):
        return self.distance < other.distance

    # Relative comparison for <=
    def __le__(self, other):
        return self.distance <= other.distance

class Graph:
    def __init__(self):
        self.__vert_dict = {}
        self.__num_vertices = 0

    def __iter__(self):
        return iter(self.__vert_dict.values())

    def add_vertex(self, node):
        self.__num_vertices = self.__num_vertices + 1
        new_vertex = Vertex(node)
        self.__vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.__vert_dict:
            return self.__vert_dict[n]
        else:
            #print("Vertex {} not found in graph".format(n))
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.__vert_dict:
            self.add_vertex(frm)
        if to not in self.__vert_dict:
            self.add_vertex(to)

        self.__vert_dict[frm].add_neighbor(self.__vert_dict[to], cost)
        self.__vert_dict[to].add_neighbor(self.__vert_dict[frm], cost)

    def get_vertices(self):
        return self.__vert_dict.keys()

def create(data):
    g = Graph()

    for stop in data.stops:
        #print(stop)
        g.add_vertex(stop)

    for road in data.roads:
        g.add_edge(road.start, road.end, road.time)
    return g

###################

import heapq

def shortest(v, path):
    #print("Make shortest path from v.previous")
    if v.previous:
        path.append(v.previous.id)
        shortest(v.previous, path)
    return

def dijkstra(aGraph, start, target):
    #print("Dijkstra's shortest path")
    #Set the distance for the start node to zero
    start.distance = 0

    #Put tuple pair into the priority queue
    unvisited_queue = [(v.distance, v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        #Pops a vertex with smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.visited = True

        #for next in v.adjacent:
        for next in current.adjacent:
            #if visited, skip
            if next.visited:
                continue
            new_dist = current.distance + current.get_weight(next)

            if new_dist < next.distance:
                next.distance = new_dist
                next.previous = current
                #print("Updated: current = {}, next = {}, new_dist = {}".format(current.id, next.id, next.distance))
            #else:
                #print("Not updated : current = {}, next = {}, new_dist = {}".format(current.id, next.id, next.distance))

        #Rebuild heap
        #1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        #2. Put all vertices not visited into the queue
        unvisited_queue = [(v.distance, v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


  