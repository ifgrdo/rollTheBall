import search
    """ For this assignment, you just need to import search.py,  
    which in turn imports utils.py; both files are available 
    in the repository mentioned on page 2 of the Assignment"""

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
    
    def setAlgorithm(self):
        """Sets the uninformed search algorithm chosen."""
        
        self.algorithm = search. ...
        # example: self.algorithm = search.breadth_first_tree search 
        # substitute by the function in search.py that implements the chosen algorithm.
        # You can only use the algorithms defined in search.py

    
    def solve(self):
        """Calls the uninformed search algorithm chosen."""

        return algorithm(self, ...)
        #
        # You have to provide the arguments for the chosen algorithm if any.
        # For instance, for the Depth Limited Search you need to provide a value for the limit L, otherwise the default value (50) will be used.
        