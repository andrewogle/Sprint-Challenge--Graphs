from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
reverese_directions = {'n':'s', 's':'n','e':'w','w':'e'}

reverse_path = []

visited = {}


#start with current room and get it exits
visited[player.current_room.id] = player.current_room.get_exits()

# travers the graph while the rooms visited are less than graph
while len(visited) < len(room_graph) -1:
	#if the current room is not in visited 
	if player.current_room.id not in visited:
		 # add it
		visited[player.current_room.id] = player.current_room.get_exits()
		# remove the exit one at a time so we dont traverse the same direction.
		visited[player.current_room.id].remove(reverse_path[-1]) 
	
	
    # while the room has no more exits 
	while len(visited[player.current_room.id]) == 0:
		# get the last direction w/ pop()
		reverse = reverse_path.pop()
		# update traversal Path
		traversal_path.append(reverse)
		#update player movement in the opisite direction 
		player.travel(reverse)
	
	#go to first available exit
	movement = visited[player.current_room.id].pop()

	#update the path 
	traversal_path.append(movement)
	#update the reverse path 
	reverse_path.append(reverese_directions[movement])
	#update player movement
	player.travel(movement)




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
	player.travel(move)
	visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
	print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
	print("TESTS FAILED: INCOMPLETE TRAVERSAL")
	print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
	cmds = input("-> ").lower().split(" ")
	if cmds[0] in ["n", "s", "e", "w"]:
		player.travel(cmds[0], True)
	elif cmds[0] == "q":
		break
	else:
		print("I did not understand that command.")
