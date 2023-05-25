import search

#-----------------------------------------------------------------------------------------------------------------------------------------------

class RTBProblem(search.Problem):
    
    def __init__ (self):

        self.initial = None
        self.N = 0
        self.algorithm = None
        self.initial_tile, self.goal_tile = None, None
        self.solvable = True

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
            return False

        current_tile = state[index]

        #compatible current tile's input with previous tile's output
        opp = {'left': 'right', 'right': 'left', 'top': 'down', 'down': 'top'}
        input = opp[previous_output] 

        #initial tile  
        if 'initial' in current_tile:
            output = previous_output

        #checks if current tile contains the compatible input
        elif input in current_tile:
            current_tile_split = current_tile.split('-')
            
            #gets the current tile's output
            if current_tile_split[0] == input:
                output = current_tile_split[1]
            else:
                output = current_tile_split[0]

        else: return False
        
        #checks if current tile's output is compatible with tile's position on puzzle
        if output in possible_moves:
            #returns next tile's position and current tile's output
            index_operation = {'left': -1, 'right': +1, 'top': -self.N, 'down': +self.N}
            return (index + index_operation[output], output)
            
        else: return False

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
        if not self.solvable: return actions

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

        while 1:
            next_tile = self.next_tile(next_tile[0], next_tile[1], state)

            if not next_tile:
                return False

            #checks if goal tile was reached
            elif next_tile[0] == self.goal_tile[0]:
                #checks if next to last tile's output is compatible with goal tile
                if next_tile[1] == self.goal_tile[1]:
                    return True
                    
                else: return False

#-----------------------------------------------------------------------------------------------------------------------------------------------

    def setAlgorithm(self):
        self.algorithm = search.breadth_first_graph_search

#-----------------------------------------------------------------------------------------------------------------------------------------------

    def solve(self):
        return self.algorithm(self)

#-----------------------------------------------------------------------------------------------------------------------------------------------