from __future__ import print_function
import cv2
import numpy as np
import pandas as pd

map = cv2.imread('Lekagul Roadways.bmp')
colors = {"general-gate": [0, 255, 255], "entrance": [76, 255, 0], "ranger-stop": [255, 216, 0],
			"gate": [255, 0, 0], "ranger-base": [255, 0, 220], "camping": [255, 106, 0]}
places = {"general-gates": {}, "entrances": {}, "ranger-stops": {}, "gates": {},
			"ranger-bases": {}, "campings": {}}
camping_order = [0, 8, 1, 2, 3, 4, 5, 7, 6]

# Find distances between all interconnected nodes
for x, line in enumerate(map):
	for y, px in enumerate(line):
		spot = [map[x][y][2], map[x][y][1], map[x][y][0]]
		if (spot == colors["general-gate"]):
			n = str(len(places["general-gates"]))
			places["general-gates"]["general-gate" + n] = [y, x]

		if (spot == colors["entrance"]):
			n = str(len(places["entrances"]))
			places["entrances"]["entrance" + n] = [y, x]

		if (spot == colors["ranger-stop"]):
			n = str(len(places["ranger-stops"]))
			places["ranger-stops"]["ranger-stop" + n] = [y, x]

		if (spot == colors["gate"]):
			n = str(len(places["gates"]))
			places["gates"]["gate" + n] = [y, x]

		if (spot == colors["ranger-base"]):
			n = str(len(places["ranger-bases"]))
			places["ranger-bases"]["ranger-base"] = [y, x]
			print ("ranger-base found")

		if (spot == colors["camping"]):
			n = camping_order[len(places["campings"])]
			places["campings"]["camping" + str(n)] = [y, x]

#print places

def color(node): #x,y
	x = node[0]
	y = node[1]
	#print "Finding color for", node
	if x >= 200 or y >= 200 or x < 0 or y < 0:
		return [0, 0, 0]
	"hey!"
	return [map[y][x][2], map[y][x][1], map[y][x][0]]

def adjacent(node): # x,y
	x = node[0]
	y = node[1]

	candidates = [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]
	adj = []
	for n in candidates:
		#print "candidates are:", candidates
		if color(n) != [0, 0, 0]:
			adj.append(n)

		#else:
		#	print color(n)
	#print "adjacent to", node, ":", adj
	return adj

def search(source, dest):
	# Source is in x, y ordering.
	S = []
	Q = []
	P = {} # each node should be visited once, so parent is also saved once...

	S.append(source)
	Q.append(source)
	P[str(source)] = "root"
	iter = 0

	while len(Q) > 0:
		current = Q.pop(0)
		#print "Current queue:",Q,"Now looking at node:", current
		if current == dest:
			distance = -1
			child = dest

			while str(child) in P: #distance
				distance += 1
				child = P[str(child)] # the parent is now the child, search grandpa

			return distance # has a parent that we can search
		#print "current node examined is:", current
		#print "adjacent:", adjacent(current)
		for n in adjacent(current):
			if n not in S:
				S.append(n)
				P[str(n)] = current
				Q.append(n)
		#print "current Q: ", Q
		#iter += 1

	#print "Oh my god Rick what has happened"
	return float("Infinity")

# Run a search from each checkpoint
# For all reachable checkpoint

# Distances in miles, each square 0.06 miles
shortest_distances = { }
counter = 1
print()

for category_source in places:
	for i, specific_location_source in enumerate(places[category_source]):
		current_source  = places[category_source][specific_location_source] # coordinates
		for category_dest in places:
			for k, specific_location_dest in enumerate(places[category_dest]):
				current_dest = places[category_dest][specific_location_dest] # coordinates
				# now see if these can be united by a string of white points
				try:
					val = shortest_distances[specific_location_source][specific_location_source]
				except KeyError, e:
					min_distance = search(current_source, current_dest)
					#print "The distance between", current_source, "and", current_dest, "is", min_distance
					if specific_location_source not in shortest_distances:
						shortest_distances[specific_location_source] = {}
					if specific_location_dest not in shortest_distances:
						shortest_distances[specific_location_dest] = {}

					shortest_distances[specific_location_source][specific_location_dest] = min_distance
					shortest_distances[specific_location_dest][specific_location_source] = min_distance

					print ("\rFinding paths...", counter * 100/780, "%", end="")
					counter += 1

print(shortest_distances)
# Now calculate the speeds!
res_file = open("distances.csv", "w+")
res_file.write("checkpoint1,checkpoint2,distance\n")
for source in shortest_distances:
	for dest in shortest_distances:
		res_file.write(source + "," + dest + "," + str(shortest_distances[source][dest]) + "\n")
