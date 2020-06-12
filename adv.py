from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

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

# Used when current room already visited to go back to previous room
reverse = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

# Depth first (basically travels down EVERY path and back)
def traverse(starting_room, visited=None):
    # Initial run
    if visited == None:
        visited = set()
    # Create list path to return path followed
    path = []
    current = player.current_room

    # Iterate through possible directions (exits from current room)
    for choice in current.get_exits():
        # Travel that way
        player.travel(choice)
        current = player.current_room
        # If we've already visited this room, return to previous room
        if current in visited:
            player.travel(reverse[choice])
        # Otherwise, add the room to visited and to path
        else:
            visited.add(current)
            path.append(choice)
            # Recursively call function again on this room and add to path
            path = path + traverse(current, visited)
            player.travel(reverse[choice])
            path.append(reverse[choice])

    return path

# def traverse(starting_room, visited=None):
#     if visited is None:
#         visited = set()
    
#     s = Stack()
#     options = starting_room.get_exits()
#     current_room = starting_room
#     path = []
#     for i in options:
#         s.push(i)
#     # iterate through queue
#     while s.size() > 0:
#         direction = s.pop()
#         print(direction)
#         path.append(direction)
#         current_room = current_room.get_room_in_direction(direction)
#         print(current_room)
#         if current_room not in visited:
#             visited.add(current_room)
#             for directions in current_room.get_exits():
#                 s.push(directions)
#     return path

# # Create a stack
# stack = []
# direction = []
# visited = set()
# possible_directions = {}
# traversal_path = []
# stack.append(player.current_room)
# # visited.add(player.current_room)


# while len(visited) != len(room_graph):
#     v = stack.pop()
#     if direction:
#         direct = direction.pop()
#         traversal_path.append(direct)
#         prev_room = v.get_room_in_direction(reverse[direct])
#         if possible_directions[prev_room.id]:
#             possible_directions[prev_room.id].remove(direct)
#     print(v.id)
#     if v.id not in possible_directions:
#         possible_directions[v.id] = v.get_exits()
#     # if possible_directions[v.id] is None:
#     #     exits = v.get_exits()
#     #     possible_directions[v.id] = exits
#     # else:
#     #     exits = possible_directions[v.id]  
#     print(possible_directions[v.id])
         
#     for i in possible_directions[v.id]:
#         room = v.get_room_in_direction(i)
#         if room not in visited:
#             stack.append(room)
#             direction.append(i)
#             visited.add(room)
#         else:
#             if v.get_room_in_direction(i) == prev_room:
#                 if len(possible_directions[v.id]) == 1:
#                     stack.append(room)
#                     direction.append(i)
#                 else:
#                     for j in possible_directions[v.id][:-1]:
#                         room = v.get_room_in_direction(j)
#                         stack.append(room)
#                         direction.append(j)
#             else:
#                 if len(possible_directions[v.id]) == 2:
#                     x = possible_directions[v.id][0]
#                     room = v.get_room_in_direction(x)
#                     stack.append(room)
#                     direction.append(x)
#                 else:
#                     stack.append(room)
#                     direction.append(i)

# traversal_path.append(direction.pop())


        
traversal_path = traverse(player.current_room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
    # print(f'{traversal_path}')
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
    # print(f'{traversal_path}')



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
