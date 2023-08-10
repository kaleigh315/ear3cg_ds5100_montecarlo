# Monte Carlo Simulator
## UVA User ID: ear3cg
## Name: Kaleigh O'Hara

This Python module can use multiple similar die of varying weights with numeric or string faces in the Die class. This die or these dice from the Die class can be used in the Game class to play a dice game and returns a data frame of the faces rolled. Additionally, in the Analyzer class, the module can analyze the outcomes by calculating the number of jackpots (a result in which all faces are the same), providing a data frame of the counts of each face and computing the distinction combinations and/or permutations of the dice rolls.

To use this module, import the Die, Game and Analyzer classes from the "montecarlo" package. Please see the Python code below:

  from montecarlo import Die
  from montecarlo import Game
  from montecarlo import Analyzer

Die Class

  class Die:
  
    """
    A die has a given number of sides, or "faces," and a given number of weights, and can be rolled to select a face.
      Each side contains a unique symbol. Symbols may be all alphabetic or all numeric.
      The weights are just numbers, not a normalized probability distribution.
      The die has one behavior, which is to be rolled one or more times.
    """
    
    def __init__(self, face):
          """
          PURPOSE: This is the object initializer that is called when an instance of the Die class is created.
      
          INPUTS:
          face    numpy array of ints, floats or strings that indicate the face values of a die
          
          OBJECT CHANGES:
          dice    dataframe of faces and weights initialized with faces as the index and weights as the cell values
          """
    def change_weight(self, face_val, new_weight):
        """
        PURPOSE: This functions checks if the face value to be changed exists in the initial array of face values.
                 Then, it checks to see if the weight is a valid type, i.e. if it is numeric (integer or float) or castable as numeric.
    
        INPUTS
        face_val   face value whose weight to change
        new_weight  weight to replace the existing weight of for face_val
        
                
        OBJECT CHANGES:
        dice        specified weight of given column updates
        """
    def roll_die(self, num_rolls = 1):
        """
        PURPOSE: This function is a random sample with replacement, from the private die data frame, that applies the weights
    
        INPUTS
        num_rolls  how many times the die is to be rolled; defaults to 1
        
        RETURN: This function returns a list of specified number of outcomes of rolled dice
        """
    def curr_state(self):
        """
        PURPOSE: This function provides the dice object data frame to users.
        
        RETURN: This function returns a copy of the dice object data frame.
        """
        
Game Class:

  class Game: 
  
    """
    A game consists of rolling of one or more similar dice (Die objects) one or more times.
    Each game is initialized with a Python list that contains one or more dice.
    Game objects have a behavior to play a game, i.e. to roll all of the dice a given number of times.
    Game objects only keep the results of their most recent play.
    """
    
    def __init__(self, dice):
        """
        PURPOSE: This is the object initializer that is called when an instance of the Game class is created.
    
        INPUTS:
        dice    a list of already instantiated similar dice
        
        OBJECT CHANGES:
        dice    object of dataframe of faces and weights initialized with faces as the index and weights as the cell values defined for the class
        """
    def play(self, rolls_play):
        """
        PURPOSE: This function plays the game by rolling the dice a specified number of times and returns an organized data frame of results for each dice rolled.
        
        INPUTS:
        rolls_play  integer parameter to specify how many times the dice should be rolled
        
        OBJECT CHANGES:
        result_df  data frame with results of the game with roll number as named index, die number as columns and face rolled in that instance in each cell
        """
    def results(self, form = 'wide'):
        """
        PURPOSE: This function shows the user the results in either "narrow" or "wide" form of the most recent play. A ValueError is raised if something other than "narrow" or "wide" is passed.
        
        INPUTS:
        form  a parameter to specify to return the data frame in "narrow" or "wide" form which defaults to wide form
        
        RETURN: This function returns result_df, data frame with results of the game, in either "narrow" form 
                (with a MultiIndex, comprising the roll number and the die number (in that order), and a single column with the outcomes)
                or in "wide" form (with roll number as named index, die number as columns and face rolled in that instance in each cell)
        
        OBJECT CHANGES:
        result_df  orientation of data frame of results will change to a MultiIndex, comprising the roll number and the die number (in that order), and a single column with the outcomes if "narrow" form is selected
        """

Analyzer Class:

  class Analyzer: 
  
    """
    An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it.
    """
    
    def __init__(self, game_object):
        """
        PURPOSE: This function takes a game object as its input parameter. It throwa a ValueError if the passed value is not a Game object.
        
        INPUTS:
        game_object  an object of the Game class
        
        OBJECT CHANGES:
        game_object  data frame with results of the game
        """
    def jackpot(self):
        """
        PURPOSE: This function calculates how many jackpots (a result in which all faces are the same) are rolled in a game.
        
        RETURN:
        jackpot_count  integer for the number of jackpots
        """
    def face_counts(self):
        """
        PURPOSE: This function computes how many times a given face is rolled in each event.
        
        RETURN:
        countval_df  a data frame with an index of the roll number, face values as columns, and count values in the cells (i.e. it is in wide format)
        
        OBJECT CHANGES:
        countval_df  creates a data frame with count of face values in the cells
        """
    def combination(self):
        """
        PURPOSE: This function computes the distinct combinations of faces rolled, along with their counts.
        
        RETURN:
        combo_df  a data frame of the count of order-independent, distinct combinations with a MultiIndex of distinct combinations and a column for the associated counts
        """
    def permutation(self):
        """
        PURPOSE: This function computes the distinct permutations of faces rolled, along with their counts.
        
        RETURN:
        combo_df  a data frame of the count of order-dependent, distinct permutations with a MultiIndex of distinct combinations and a column for the associated counts
        """
