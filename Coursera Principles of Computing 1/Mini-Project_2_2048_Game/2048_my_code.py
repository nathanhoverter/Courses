"""
2048 game.
"""

import poc_2048_gui
from random import randint

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    #Initialize an empty line, slide tiles, and match numbers
    board = empty_board(line)
    move = slide_tiles(line)
    matches = match(move)
    #If legitimate matches are made, double the score in the "first" position
    for ind in range(len(matches)):
        if matches[ind] == True:
            board[ind] = move[ind]*2
        elif matches[ind-1] == True:
            board[ind] = 0
        else:
            board[ind] = move[ind]
    return slide_tiles(board)
    
def empty_board(line):
    """
    Function that returns an empty row based on the number of tiles
    """
    empty = []
    for dummy_num in range(len(line)):
        empty.append(0)
    return empty

def slide_tiles(line):
    """
    Function that slides tiles according to the rules of 2048
    """
    slide = []
    zeros = []
    for tile in line:
        if tile != 0:
            slide.append(tile)
        else:
            zeros.append(tile)
             
    return slide + zeros

def match(line):
    """
    Returns a list of booleans where True indicates legitimate paired matches according to the rules of 2048
    """
    matches = []
    #Legitimate matches can only be found in pairs of tiles, i.e the sequence 2, 2, 2, 0 only has one legitimate match
    for ind in range(len(line)-1):
        if line[ind] == line[ind+1]:
            matches.append(True)
        else:
            matches.append(False)
    matches.append(False)
    for ind, val in enumerate(matches):
        if val == True and matches[ind-1] == True:
            matches[ind] = False
    return matches

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        top_ind = []
        bottom_ind = []
        left_ind = []
        right_ind = []
        #Get indices of the edges of the board and store in dictionary for later use with the move method
        top_ind = [(0, col) for col in range(grid_width)]
        bottom_ind = [(grid_height-1, col) for col in range(grid_width)] 
        left_ind = [(row, 0) for row in range(grid_height)]
        right_ind = [(row, grid_width-1) for row in range(grid_height)]
        self._indices = {UP: top_ind, DOWN: bottom_ind, LEFT: left_ind, RIGHT: right_ind}     
        
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._board = [[0 for dummy_var in range(self._grid_width)] for dummy_var in range(self._grid_height)]
        #Add two new tiles
        self.new_tile()
        self.new_tile()
   
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        board_str = ""
        for row in self._board:
            board_str = board_str + str(row)
        return board_str

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in a given direction and add
        a new tile if any tiles moved.
        """
        #Get the list of indices of the edge being moved towards
        direct_ind = self._indices[direction]
        offset = OFFSETS[direction]
        #Make a deep copy of the initial board so that it can be determined if the board has changed later
        initial_board = [tile[:] for tile in self._board]
        #Need to know direction so that board of any dimmensions will work
        if direction == UP or direction == DOWN:
            length = self._grid_height
        elif direction == LEFT or direction == RIGHT:
            length = self._grid_width
        #For each tile in the edge being moved towards, get the values of the row or column that is moving towards that tile
        #Then apply the merge function on that row or column
        for tile in direct_ind:
            temp_ind = []
            temp_values = []
            for unit in range(length):
                if unit == 0: 
                    temp_ind.append(tile)
                else:
                    row_ind = offset[0] + temp_ind[unit-1][0]
                    col_ind = offset[1] + temp_ind[unit-1][1]
                    temp_ind.append((row_ind, col_ind))
            for index in temp_ind:
                temp_values.append(self._board[index[0]][index[1]])
            #Apply the merge function on the values of the row or column being moved
            #Then add the results of the merged function back onto the board
            merged = merge(temp_values)
            for index, value in enumerate(temp_ind):
                self._board[value[0]][value[1]] = merged[index]
        #If the board state has changed after a move, add a new file
        if initial_board != self._board:
            self.new_tile()
             

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        rand_tile_choice = randint(1, 10)
        if rand_tile_choice == 1:
            tile = 4
        else:
            tile = 2
        rand_row_index = randint(0, self._grid_height-1)
        rand_col_index = randint(0, self._grid_width-1)
        if self._board[rand_row_index][rand_col_index] == 0:
            self._board[rand_row_index][rand_col_index] = tile
        else:
            self.new_tile()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._board[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(6, 6))