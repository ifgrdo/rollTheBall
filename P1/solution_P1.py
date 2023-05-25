import search

class RTBProblem(search.Problem):
    def __init__ (self):
        ”””Method that instantiate your class .
            You can change the content of this .
            self.initial is where the initial state of
            the puzzle should be saved . ”””
        
        self.initial = None


    def load(self , fh):
        ”””loads a RTB puzzle from the file object fh.
            You may initialize self . initial here.”””
            
        pass
    
    
    def isSolution(self ):
        ”””returns 1 if the loaded puzzle is a solution , 0 otherwise.””” 
        
        pass