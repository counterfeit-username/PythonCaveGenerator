from random import randint
import sys, json

# Note that the map list is layed out as follows:
# map = [[tiles in row 1...], [tiles in row 2...]...]

# Also, 1 stands for a filled space and 0 stands for an empty space


# --------------------------------
# ------Function Definitions------
# --------------------------------


def print_map(map_list: list):
    """Prints the contents of list 'map_list' with '#' as wall and ' ' as void."""

    map = ""  # This represents the map with charaters.
    for row in map_list:
        # Loop through the rows in the map.
        for column in row:
            # Loop through the tiles in each row.
            tile = " "  # The character representation of the tile.

            if column == 1:  
                # Add a '#' for a wall or ' ' for an empty space.
                tile = "#"
            else:
                tile = " "

            map = map + tile
        
        map = map + "\n" # Add a newline after each row of tiles.
    print(map)


def get_num_neighbors(map: list, row: int, column: int) -> int:
    """Gets the number of a tile's neighbors. Neighbors are solid tiles which \
    are directly adjacent or diagonal to the tile at column, row.
    """
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            x = row + i
            y = column + j
            if (x > 0 and x < len(map[i]) and y > 0 and y < len(map[i])) \
                and map[y][x] == 1 and not (x == 0 and y == 0):

                # If the tile is filled and this is not the tile originally 
                #  being checked then add 1 to the sum.
                total += 1

    return total


def smoothen(map: list) -> list:
    """Takes a map of tiles and smoothens it."""
    # This loops through the tiles in the map and checks what needs to be filled.
    # Because the new map starts out filled with solid tiles, we only need to check 
    #  if the tile needs to be empty.

    smoothed = [[1 for _ in range(len(column))] for column in map] # Create a filled map.
    
    for row in range(1, len(map) - 1):
        for column in range(1, len(map[row]) - 1):
            # Loop through all tiles except for the edges.

            tile = map[row][column] # The tile being checked.
            neighbors = get_num_neighbors(map, row, column) # The number of neighbors.

            if neighbors < 5 and tile == 0:
                # The tile should be empty if it has < 5 neighbors and was
                #  originally empty.
                smoothed[row][column] = 0

            elif neighbors < 5 and tile == 1:
                # The tile should be empty if it has < 5 neighbors and was
                #  originally solid.
                smoothed[row][column] = 0

    return smoothed


# --------------------------------
# ------Function Use--------------
# --------------------------------


print("\n\n-----Cave System Generator v1.0-----")
print("Generates a map containing a cave system.\nPrints this to stdout and creates/writes to a json file.\n\n")

try: 
    height = int(sys.argv[1])  # Get the height of the map.
except IndexError:
    print("\nPlease provide a height for the map.")
    print("Program syntax is: python generator.py height width filepath\n")
    sys.exit()
except TypeError:
    print("\nMap height must be an integer")
    print("Program syntax is: python generator.py height width filepath\n")
    sys.exit()

try:
    width = int(sys.argv[2])  # Get the width of the map.
except IndexError:
    print("\nPlease provide a width for the map.")
    print("Program syntax is: python generator.py height width filepath\n")
    sys.exit()
except TypeError:
    print("\nMap width must be an integer")
    print("Program syntax is: python generator.py height width filepath\n")
    sys.exit()

try: # Get the file to write the map to.
    filepath = (sys.argv[3])
except:
    pass

map = [[randint(0, 1) for _ in range(width)] for i in range(height)] # Begin the map as noise.

for _ in range(6): # Repeatedly run the map through the smoothing algorithm.
    map = smoothen(map)

print_map(map)

try: # Write the map to a json file.
    with open(filepath, mode='x') as file:
        json.dump(map, file)
except FileExistsError:
    with open(filepath, mode='w') as file:
        json.dump(map, file)