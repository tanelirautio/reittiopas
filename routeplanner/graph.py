import sys

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.distance = sys.maxsize
        self.visited = False
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + " adjacent: " + str([x.id for x in self.adjacent])

    # Relative comparison for <
    def __lt__(self, other):
        return self.distance < other.distance

    # Relative comparison for <=
    def __le__(self, other):
        return self.distance <= other.distance

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            print("Vertex {} not found in graph".format(n))
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

def create(data):
    g = Graph()

    for stop in data.get_stops():
        #print(stop)
        g.add_vertex(stop)

    for road in data.get_roads():
        #print(road)
        start = road.get_start()
        end = road.get_end()
        time = road.get_time()
        g.add_edge(start, end, time)
    return g

###################

import heapq

def shortest(v, path):
    print("Make shortest path from v.previous")
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return

def dijkstra(aGraph, start, target):
    #print("Dijkstra's shortest path")
    #Set the distance for the start node to zero
    start.set_distance(0)

    #Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        #Pops a vertex with smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        #for next in v.adjacent:
        for next in current.adjacent:
            #if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                #print("Updated: current = {}, next = {}, new_dist = {}".format(current.get_id(), next.get_id(), next.get_distance()))
            #else:
                #print("Not updated : current = {}, next = {}, new_dist = {}".format(current.get_id(), next.get_id(), next.get_distance()))

        #Rebuild heap
        #1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        #2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


  