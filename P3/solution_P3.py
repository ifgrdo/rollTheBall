import search
    """ For this assignment, you just need to import search.py,  
    which in turn imports utils.py; both files are available 
    in the AIMA repository (see Assignment 2)"""

class RTBProblem(search.Problem):
    def init (self, algorithm):
        """Method that instantiate your class.
        You can change the content of this.
        self.initial is where the initial state of the puzzle should be saved. 
        self.algorithm is where the chosen uninformed search algorithm should be saved."""
        self.initial = None
        self.algorithm = None
        
    def result (self, state, action):
        """Return the state that results from executing the given act"""
        pass
        
    def actions(self, state):
        """Return the actions that can be executed in the given state"""
        pass
    
    def goal_test(self, state):
        """Return True if the state is a goal."""
        pass
    
    def load(self, fh):
        """loads a RTB puzzle from the file object fh. You may initialize self.initial here."""
        pass
    
    def h(self, node):
        """This heuristic works like this:
        ...
        It is consistent/not consistent because ...
        It is admissible/not admissible because ..."""
        pass