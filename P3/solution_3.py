import search
#-----------------------------------------------------------------------------------------------------------------------------------------------

class RTBProblem(search.Problem):
    
    def __init__ (self):

        self.initial = None
        self.N = 0
        self.algorithm = None
        self.initial_tile, self.goal_tile = None, None
        self.solvable = True
        self.start = True #set to True at the beggining of the loops to go through the puzzle (goal test and h functions)
        self.out = False #set to True if tile's indexes are out of the board

#-----------------------------------------------------------------------------------------------------------------------------------------------

    def load(self, fh):

        puzzle_initial = ()
        initialized = 0

        for line in fh.readlines(): 
            line_split = line.split()
            if len(line_split)>0 and not line.startswith("#"):           #ignore empty lines and comments
                if initialized == 0:                                     #first line with size of puzzle
                    self.N = int(line); 
                    initialized = 1

                else: 
                    puzzle_initial += tuple(line_split)

        self.initial = puzzle_initial
    
        opp = {'left': 'right', 'right': 'left', 'top': 'down', 'down': 'top'}

        #gets initial and goal tiles position
        for index, tile in enumerate(self.initial):
            if 'initial' in tile:
                self.initial_tile = (index, tile.split('-')[1])
                
            if 'goal' in tile:
                #gets next to last tile's output compatible with goal tile
                last_output = opp[tile.split('-')[1]] 
                self.goal_tile = (index, last_output)

        self.check_solvable_puzzle()

#-----------------------------------------------------------------------------------------------------------------------------------------------

    #checks if the initial and goal tiles' position and orientation allow the puzzle to be solvable
    def check_solvable_puzzle(self):

        if 'left' in self.initial[self.initial_tile[0]] and self.initial_tile[0] % self.N == 0:
            self.solvable = False

        elif 'right' in self.initial[self.initial_tile[0]] and self.initial_tile[0] % self.N == self.N-1:
            self.solvable = False

        elif 'top' in self.initial[self.initial_tile[0]] and self.initial_tile[0] < self.N:
            self.solvable = False

        elif 'down' in self.initial[self.initial_tile[0]] and self.initial_tile[0] > (self.N)**2-self.N-1:
            self.solvable = False


        elif 'left' in self.initial[self.goal_tile[0]] and self.goal_tile[0] % self.N == 0:
            self.solvable = False

        elif 'right' in self.initial[self.goal_tile[0]] and self.goal_tile[0] % self.N == self.N-1:
            self.solvable = False

        elif 'top' in self.initial[self.goal_tile[0]] and self.goal_tile[0] < self.N:
            self.solvable = False

        elif 'down' in self.initial[self.goal_tile[0]] and self.goal_tile[0] > (self.N)**2 - self.N - 1:
            self.solvable = False

#-----------------------------------------------------------------------------------------------------------------------------------------------
    
    #checks possible moves according to position in puzzle and respective boundaries
    def possible_moves(self, index):

        possible_moves = ['top','down','left','right']

        if index < self.N:  
            possible_moves.remove('top')                                                                                                 

        if index > (self.N)**2 - self.N - 1:       
            possible_moves.remove('down')
        
        if index % self.N == 0: 
            possible_moves.remove('left')                                                           

        if index % self.N == self.N-1: 
            possible_moves.remove('right')     

        if index < 0 or index > (self.N)**2 - 1:
            return False                                         

        return tuple(possible_moves)
       
#-----------------------------------------------------------------------------------------------------------------------------------------------

    #returns next tile's position and current tile output
    def next_tile(self, index, previous_output, state):

        possible_moves = self.possible_moves(index)
        
        if not possible_moves: 
            self.out = True
            return False

        current_tile = state[index]

        #compatible current tile's input with previous tile's output
        opp = {'left': 'right', 'right': 'left', 'top': 'down', 'down': 'top'}
        input = opp[previous_output] 

        #initial tile 
        if self.start == True:
            if 'initial' in current_tile:
                output = previous_output
                self.start = False
        
        #for heuristic function h, when it goes through the puzzle starting at the goal tile
            elif 'goal' in current_tile:
                output = input
                self.start = False

        #checks if current tile contains the compatible input
        elif input in current_tile:
            current_tile_split = current_tile.split('-')
            
            #gets the current tile's output
            if current_tile_split[0] == input:
                output = current_tile_split[1]
            else:
                output = current_tile_split[0]

        else:
            return False
        
        #checks if current tile's output is compatible with tile's position on puzzle
        if output in possible_moves:
            #returns next tile's position and current tile's output
            index_operation = {'left': -1, 'right': +1, 'top': -self.N, 'down': +self.N}
            return (index + index_operation[output], output)
            
        else: 
            self.out = True
            return False

#-----------------------------------------------------------------------------------------------------------------------------------------------

    def result(self, state, action):

        state = list(state)
        index, move = action[0], action[1]

        index_operation = {'left': -1, 'right': +1, 'top': -self.N, 'down': +self.N}
        
        #swaps empty tile with neighbouring tile according to action
        state[index], state[index + index_operation[move]] = state[index + index_operation[move]], state[index]      #state[index] is empty cell
             
        return tuple(state)

#-----------------------------------------------------------------------------------------------------------------------------------------------

    #finds position of empty tiles in current state
    def find_empty_tiles(self, state):

        return (index for index, tile in enumerate(state) if 'empty' in tile)
        
#-----------------------------------------------------------------------------------------------------------------------------------------------

    def actions(self, state):

        actions = ()

        #if puzzle not solvable return empty actions and end search
        if not self.solvable: 
            return actions

        empty_tiles = self.find_empty_tiles(state)

        forbidden_words = ('not', 'empty', 'initial', 'goal')
        index_operation = {'left': -1, 'right': +1, 'top': -self.N, 'down': +self.N}
                     
        for index_empty_tiles in empty_tiles:
            #checks possible actions according to each empty tiles' position
            possible_moves = self.possible_moves(index_empty_tiles)
            indexes = ()

            for move in possible_moves:
                #adds only actions that don't swap an empty cell with another empty cell, with an unmovable tile, or with the initial/goal tiles
                if not any (word in state[index_empty_tiles + index_operation[move]] for word in forbidden_words):
                   actions += ([index_empty_tiles, move],)
        
        return actions

#-----------------------------------------------------------------------------------------------------------------------------------------------
    
    def goal_test(self, state):

        next_tile = self.initial_tile
        self.start = True

        while 1:
            next_tile = self.next_tile(next_tile[0], next_tile[1], state)
            
            if not next_tile:
                return False

            elif next_tile[0] == self.goal_tile[0]:
                if next_tile[1] == self.goal_tile[1]:
                    return True
                    
                else:
                    return False

#-----------------------------------------------------------------------------------------------------------------------------------------------

    def setAlgorithm(self):
        
        self.algorithm = search.astar_search

#-----------------------------------------------------------------------------------------------------------------------------------------------

    def solve(self):
        
        return self.algorithm(self, self.h)

#-----------------------------------------------------------------------------------------------------------------------------------------------

    def h(self, node):
        '''
        This heuristic calculates the Manhattan distance between the last tile that the ball reaches from the initial tile 
        (index_forward) and the last tile the ball reaches from the goal tile (index_backwards)

        This heuristic is admissible because it underestimates the cost. It assumes that there are only empty tiles in the shortest path
        between index_forward and the index_backwards tiles and that it takes one move (cost=1 per move) to replace each of the empty 
        tiles by the fitting tile (i.e. fitting tile is assumed to be right next to the empty cell where it fits). Therefore, 
        heuristics = number of moves needed x cost = Manhattan distance between index_forward and index_backwards tiles - 1.
        Subtracting 1 is because we only want to count what's in between the index_forward and index_backwards tiles.

        This heuristic is consistent because in each step, the heuristic can only increase/decrease by one and the cost per move is
        one. Therefore, h(next step) <= cost(=1) + h(current step)
        Note that when a solution is found, this functions automatically returns zero.

        Since this is a graph-search, and h is consistent, then A* is optimal and complete.
        '''

        index_operation = {'left': -1, 'right': +1, 'top': -self.N, 'down': +self.N}
        opp = {'left': 'right', 'right': 'left', 'top': 'down', 'down': 'top'}

        #finds last reachable tile from initial tile
        next_tile = self.initial_tile
        self.start = True
 
        while 1:
            current_tile = next_tile
            index_forward = current_tile[0]
            next_tile = self.next_tile(next_tile[0], next_tile[1], node.state)

            if not next_tile:
                #in case the last reachable tile is not a puzzle's boundaries, next_tile returns index of a not compatible tile, so we need to get the index of the previous tile
                if self.out == False:
                    index_forward -= index_operation[current_tile[1]]
                break 

            #heuristic returns 0 if a solution is found
            if next_tile[0] == self.goal_tile[0] and next_tile[1] == self.goal_tile[1]:
                return 0
        
        #convert index_forward tile to matrix representation
        row_forward, column_forward = int(index_forward / self.N), index_forward % self.N
 
        #finds last reachable tile from goal tile
        next_tile = self.goal_tile
        self.start = True
        self.out = False

        while 1:
            current_tile = next_tile
            index_backwards = current_tile[0]
            next_tile = self.next_tile(next_tile[0], next_tile[1], node.state)

            if not next_tile:
                if self.out == False:

                    #goal tile has opposite output
                    if current_tile[0] == self.goal_tile[0]:
                        output = opp[current_tile[1]]
            
                    else: 
                        output = current_tile[1]
                        
                    #in case the last reachable tile is not a puzzle's boundaries, next_tile returns index of a not compatible tile, so we need to get the index of the previous tile
                    index_backwards -= index_operation[output]

                break 
  
        #convert index_backwards tile to matrix representation                        
        row_backwards, column_backwards = int(index_backwards / self.N), index_backwards % self.N

        #returns manhattan distance - 1
        return abs(row_forward - row_backwards) + abs(column_forward - column_backwards) - 1

#-----------------------------------------------------------------------------------------------------------------------------------------------