import unittest
import pandas as pd
import numpy as np
import random
from itertools import permutations

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
        self.face = face
        if not isinstance(face, np.ndarray):
            raise TypeError("Face values must be a NumPy array.")
        if len(set(face)) != len(face):
            raise ValueError("Face values must be distinct.")
        self.dice = pd.DataFrame({'faces': face, 'weights': np.ones(len(face))}, columns=['faces', 'weights'])
        self.dice = self.dice.set_index(['faces'])
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
        if not face_val in self.face:
            raise IndexError("Face value's weight to be changed must exist in the face array.")
        if not isinstance(new_weight, float): 
            if not isinstance(new_weight, int):
                try:
                    new_weight = pd.to_numeric(new_weight)
                except:
                    raise TypeError("New weight must be numeric.")
        for i in range(len(self.dice)):
            if self.dice.index[i] == face_val:
                self.dice.iloc[i,0] = new_weight
    def roll_die(self, num_rolls = 1):
        """
        PURPOSE: This function is a random sample with replacement, from the private die data frame, that applies the weights
    
        INPUTS
        num_rolls  how many times the die is to be rolled; defaults to 1
        
        RETURN: This function returns a list of specified number of outcomes of rolled dice
        """
        return(random.choices(self.dice.index, weights = self.dice['weights'], k = num_rolls))
    def curr_state(self):
        """
        PURPOSE: This function provides the dice object data frame to users.
        
        RETURN: This function returns a copy of the dice object data frame.
        """
        return(self.dice.copy())

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
        self.dice = dice
    def play(self, rolls_play):
        """
        PURPOSE: This function plays the game by rolling the dice a specified number of times and returns an organized data frame of results for each dice rolled.
        
        INPUTS:
        rolls_play  integer parameter to specify how many times the dice should be rolled
        
        OBJECT CHANGES:
        result_df  data frame with results of the game with roll number as named index, die number as columns and face rolled in that instance in each cell
        """
        result_list = []
        for i in range(len(self.dice)):
            die = self.dice[i]
            result_list.append(die.roll_die(num_rolls = rolls_play))
        self.result_df = pd.DataFrame(data = result_list).T
        self.result_df.index.name = 'Roll Number'
        self.result_df = self.result_df.reset_index()
        self.result_df['Roll Number'] = self.result_df['Roll Number'] + 1
        self.result_df = self.result_df.set_index(['Roll Number'])
        self.result_df.columns = [x for x in range(1,len(self.dice)+1)]
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
        if form == 'narrow':
            self.result_df = self.result_df.reset_index()#
            self.result_df = pd.melt(self.result_df, id_vars = 'Roll Number', value_vars = list(range(1,(len(self.dice)+1))))
            self.result_df = self.result_df.rename({'variable':'Die Number', 'value':'Outcome'}, axis=1)
            self.result_df = self.result_df.set_index(['Roll Number','Die Number'])
            self.result_df = pd.DataFrame(self.result_df)
        elif form != 'wide':
            raise ValueError("Form value must be 'narrow' or 'wide.'")
        else:
            self.result_df = pd.DataFrame(self.result_df)
        return(self.result_df)

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
        self.game_object = game_object
        if not isinstance(game_object, Game):
            raise ValueError("Passed value must be a Game object.")
        self.results = self.game_object.results(form = 'wide')
    def jackpot(self):
        """
        PURPOSE: This function calculates how many jackpots (a result in which all faces are the same) are rolled in a game.
        
        RETURN:
        jackpot_count  integer for the number of jackpots
        """
        count = 0
        jackpot_count = 0
        for i in range(len(self.results)):
            count = 0
            for j in range(len(self.results.columns)):
                if j != 0:
                    if self.results.iloc[i,j] == self.results.iloc[i,j-1]:
                        count+=1
            if count == (len(self.results.columns)-1):
                jackpot_count += 1
        return(jackpot_count)  
    def face_counts(self):
        """
        PURPOSE: This function computes how many times a given face is rolled in each event.
        
        RETURN:
        countval_df  a data frame with an index of the roll number, face values as columns, and count values in the cells (i.e. it is in wide format)
        
        OBJECT CHANGES:
        countval_df  creates a data frame with count of face values in the cells
        """
        faces = list(self.game_object.dice[0].dice.index)
        countval = []
        for i in faces:
            count_roll = []
            for j in range(len(self.results)):
                count_face = 0
                for k in range(len(self.results.columns)):
                    if self.results.iloc[j,k] == i:
                        count_face +=1
                count_roll.append(count_face)
            countval.append(count_roll)
        countval_df = pd.DataFrame(countval).T
        countval_df.index.name = 'Roll Number'
        countval_df = countval_df.reset_index()
        countval_df['Roll Number'] = countval_df['Roll Number'] + 1
        self.countval_df = countval_df.set_index(['Roll Number'])
        self.countval_df.columns = [faces]
        return(self.countval_df)
    def combination(self):
        """
        PURPOSE: This function computes the distinct combinations of faces rolled, along with their counts.
        
        RETURN:
        combo_df  a data frame of the count of order-independent, distinct combinations with a MultiIndex of distinct combinations and a column for the associated counts
        """
        results = self.results
        face_counts = self.face_counts()
        combo_list = []
        track_list = []
        for roll in range(len(results)):
            if list(face_counts.iloc[roll,:]) in track_list:
                index_results = track_list.index(list(face_counts.iloc[roll,:]))
                combo_list.append(results.iloc[index_results,:])
                track_list.append(list(face_counts.iloc[roll,:]))
            else:
                track_list.append(list(face_counts.iloc[roll,:]))
                combo_list.append(results.iloc[roll,:])
        combo_df = pd.DataFrame(combo_list)
        combo_df = pd.DataFrame(combo_df.value_counts())
        return(combo_df)
    def permutation(self):
        """
        PURPOSE: This function computes the distinct permutations of faces rolled, along with their counts.
        
        RETURN:
        combo_df  a data frame of the count of order-dependent, distinct permutations with a MultiIndex of distinct combinations and a column for the associated counts
        """
        results = self.results
        perm_list = []
        for roll in range(len(results)):
            perm = results.iloc[roll,:]
            perm_list.append([str(val) for val in perm])
        perm_df = pd.DataFrame(perm_list)
        perm_df = pd.DataFrame(perm_df.value_counts())
        return(perm_df)