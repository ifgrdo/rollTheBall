import search

#-----------------------------------------------------------------------------------------------------------------------------------------------

class RTBProblem(search.Problem):
    
    def __init__ (self):
        self.initial = None
        self.N = 0

#-----------------------------------------------------------------------------------------------------------------------------------------------

    def load(self, fh):
        count = 0
        puzzle_initial = []
        for line in fh.readlines():
            if len(line.split())==0 or line[0]=='#':
                count += 1

        fh.seek(0)
        self.N = int(fh.readlines()[count:count+1][0])
        fh.seek(0)

        for line in fh.readlines()[count+1:]:
            if len(line.split())>0 and line[0]!='#':
                line_splitted = line.split()
                puzzle_initial.append(line_splitted)
        
        self.initial = puzzle_initial

#-----------------------------------------------------------------------------------------------------------------------------------------------

    #checks possible tiles according to position in puzzle and respective boundaries
    def possibleTiles(self, row, column):
        if row == 0:                                                                                                  #top row
            if column == 0: return ['right', 'down']
            elif column == self.N-1: return ['down', 'left']
            else: return ['right', 'down', 'left']

        elif row == self.N-1:                                                                                         #bottom row
            if column == 0: return ['top', 'right']
            elif column == self.N-1: return ['top', 'left']
            else: return ['top', 'right', 'left']
        
        elif column == 0: return ['top', 'right', 'down']                                                             #left column

        elif column == self.N-1: return ['top', 'down', 'left']                                                       #right column

        elif row > 0 and row < self.N-1 and column > 0 and column < self.N-1: return ['top', 'right', 'down', 'left'] #middle

        else: return False

#-----------------------------------------------------------------------------------------------------------------------------------------------

    #returns next tile's position and current tile output
    def nextTile(self, row, column, prev_output):
        possible_tiles = self.possibleTiles(row, column)
        if possible_tiles == False: return False

        tile = self.initial[row][column]
        input = ''
        output = ''

        #compatible current tile's input with previous tile's output
        if prev_output == 'left':
            input = 'right'
        elif prev_output == 'right':
            input = 'left'
        elif prev_output == 'top':
            input = 'down'
        elif prev_output == 'down':
            input = 'top'

        #initial tile       
        if 'initial' in tile:
            output = prev_output
        
        #checks if current tile contains the compatible input
        elif input in tile:
            tile_split = tile.split('-')
            
            #gets the current tile's output
            if tile_split[0] == input:
                output = tile_split[1]
            elif tile_split[1] == input:
                output = tile_split[0]
        else: return False
        
        #checks if current tile's output is compatible with tile's position on puzzle
        if output in possible_tiles:
            #returns next tile's position and current tile's output
            if output == 'left': return [row, column-1, output]
            elif output == 'right': return [row, column+1, output]
            elif output == 'top': return [row-1, column, output]
            elif output == 'down': return [row+1, column, output]
        else: return False

#-----------------------------------------------------------------------------------------------------------------------------------------------

    def isSolution(self):
        initial_tile = []
        goal_tile = []

        #gets initial and goal tiles position
        for n_row, row in enumerate(self.initial):
            for n_column, tile in enumerate(row):
                if 'initial' in tile: initial_tile = [n_row, n_column, tile.split('-')[1]] 
                if 'goal' in tile: 
                    last_output = ''
                    goal_input = tile.split('-')[1]

                    #gets next to last tile's output compatible with goal tile
                    if goal_input == 'left': last_output = 'right'
                    elif goal_input == 'right': last_output = 'left'
                    elif goal_input == 'top': last_output = 'down'
                    elif goal_input == 'down': last_output = 'top'
                    
                    goal_tile = [n_row, n_column, last_output]

        current_tile = initial_tile

        while True:
            next_tile = self.nextTile(current_tile[0], current_tile[1], current_tile[2])
            if next_tile == False:
                return 0
                
            #checks if goal tile was reached
            elif next_tile[0] == goal_tile[0] and next_tile[1] == goal_tile[1]:
                #checks if next to last tile's output is compatible with goal tile
                if next_tile[2] == goal_tile[2]:
                    return 1
                    
                else:
                    return 0   

            else:
                current_tile = next_tile 

#-----------------------------------------------------------------------------------------------------------------------------------------------
