import unittest
import pandas as pd
import numpy as np
import random
from itertools import permutations

class Die:
    '''
    A die has a given number of sides, or “faces”, and a given number of weights, and can be rolled to select a face.
    Each side contains a unique symbol. Symbols may be all alphabetic or all numeric.
    The weights are just numbers, not a normalized probability distribution.
    The die has one behavior, which is to be rolled one or more times.
    '''
    def __init__(self, face):
        '''
        PURPOSE: This is the object initializer that is called when an instance of the class is created.
    
        INPUTS
        face    numpy array of ints, floats or strings that indicate the face values of a die
        '''
        self.face = face
        if not isinstance(face, np.ndarray):
            raise TypeError("Face values must be a NumPy array.")
        if len(set(face)) != len(face):
            raise ValueError("Face values must be distinct.")
        self.dice = pd.DataFrame({'faces': face, 'weights': np.ones(len(face))}, columns=['faces', 'weights'])
    def change_weight(self, face_val, new_weight):
        '''
        PURPOSE: This functions checks if the face value to be changed exists in the initial array of face values.
                 Then, it checks to see if the weight is a valid type, i.e. if it is numeric (integer or float) or castable as numeric.
    
        INPUTS
        face_val   face value whose weight to change
        new_weight  weight to replace the existing weight of for face_val
        '''
        if not face_val in self.face:
            raise IndexError("Face value's weight to be changed must exist in the face array.")
        if not isinstance(new_weight, float): 
            if not isinstance(new_weight, int):
                try:
                    new_weight = pd.to_numeric(new_weight)
                except:
                    raise TypeError("New weight must be numeric.")
    def roll_die(self, num_rolls = 1):
        '''
        PURPOSE: This function is a random sample with replacement, from the private die data frame, that applies the   weights
    
        INPUTS
        num_rolls  how many times the die is to be rolled; defaults to 1
        '''
        return random.choices(self.dice['faces'], weights = self.dice['weights'], k = num_rolls)
    def curr_state(self):
        '''
        PURPOSE: This funciton returns a copy of the private die data frame.
        '''
        return self.dice
    
class Game: #revisit what is passed to the function (Die object? List?)
    def __init__(self, dice):
        self.dice = dice
    def play(self, rolls_play):
        result_list = []
        #result = Die(self.dice[1])
        for i in range(len(self.dice)):
            die = self.dice[i]
            result_list.append(die.roll_die(num_rolls = rolls_play))
        self.result_df = pd.DataFrame(data = result_list).T
        self.result_df.index.name = 'Roll Number'
        self.result_df = self.result_df.reset_index()
        self.result_df['Roll Number'] = self.result_df['Roll Number'] + 1
        self.result_df = self.result_df.set_index(['Roll Number'])
        self.result_df.columns = [x for x in range(1,len(self.dice)+1)]
        return(self.result_df)
    def results(self, form):
        if form == 'narrow':
            #reset - melt
            self.result_df = self.result_df.reset_index()#
            df_outcomes = pd.melt(self.result_df, id_vars = 'Roll Number', value_vars = list(range(1,(len(self.dice)+1))))
            df_outcomes = df_outcomes.rename({'variable':'Die Number', 'value':'Outcome'}, axis=1)
            df_outcomes = df_outcomes.set_index(['Roll Number','Die Number'])
            df_outcomes = pd.DataFrame(df_outcomes)
            #dice_num_list = [i for i in range(len(self.result_df.columns))]
            #print(dice_num_list)
            #index_list = list(self.result_df.index)
            #arrays = [index_list,dice_num_list]
            #print(arrays)
            #tuples = list(zip(*arrays))
            #index = pd.MultiIndex.from_tuples(tuples, names=["Roll Number", "Dice Number"])
            #print(index)
            #df_outcomes = pd.DataFrame(self.result_df, index=index)
        elif form != 'wide':
            raise ValueError("Form value must be 'narrow' or 'wide.'")
        else:
            df_outcomes = pd.DataFrame(self.result_df)
        return(df_outcomes)

class Analyzer: #how to access dice face values?
    def __init__(self, game_object):
        self.game_object = game_object
        if not isinstance(game_object, Game):
            raise ValueError("Passed value must be a Game object.")
        self.results = self.game_object.results(form = 'wide')
    def jackpot(self):
        count = 0
        jackpot_list = []
        for i in range(len(results)):
            count = 0
            for j in range(len(self.results.columns)):
                if j != 0:
                    if self.results.iloc[i,j] == results.iloc[i,j-1]:
                        count+=1
            if count == len(results.columns):
                jackpot_list.append(results.iloc[:,j])
        jackpot_df = pd.DataFrame(jackpot_list)
        return(jackpot_df)  
    def face_counts(self):
        faces = list(test.dice[0].dice['faces'])
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
        face_counts = self.face_counts()
        string_list = []
        unique_list = []
        count=[]
        for roll in range(len(face_counts)):
            combo = face_counts.iloc[roll,:]
            combo = [str(val) for val in combo]
            string = ""
            for val in combo:
                string += (val + "-") #creates an ID for the roll to see if this combination has been rolled before
            if string not in string_list:
                unique_list.append(combo)
                string_list.append(string)
                count.append(1)
            else:
                count[string_list.index(string)] +=1 #the index of the ID of the roll is the same as the index of the count for that roll
        face_val = face_counts.T
        face_val = face_val.reset_index()
        temp_df = pd.DataFrame(face_val['level_0']).T
        unique_df = pd.DataFrame(unique_list)
        id_list = []
        for row in range(len(unique_df)):
            combination_id = ""
            for col in range(len(unique_df.columns)):
                if pd.to_numeric(unique_df.iloc[row,col]) != 0:
                    part_id = str([temp_df.iloc[0,col]]*(pd.to_numeric(unique_df.iloc[row,col])))
                    part_id = part_id[1:-1]
                    combination_id += part_id + ", "
            id_list.append(combination_id[:-2])
        for roll in range(len(id_list)):
            id_list[roll] = pd.to_numeric(id_list[roll].split(","))
        combo_df = pd.DataFrame(id_list,count)
        combo_df.columns = [x for x in range(1,len(combo_df.columns)+1)]
        combo_df = combo_df.reset_index()
        combo_df = combo_df.rename(columns={'index':'Count'})
        combo_df = combo_df.set_index([x for x in range(1,len(combo_df.columns)+1)][:-1])
        return(combo_df)
    def permutation(self):
        unique_list = []
        string_list = []
        count = []
        for roll in range(len(self.results)):
            permute_list = list(self.results.iloc[roll,:])
            perm = [str(val) for val in permute_list]
            string = ""
            for val in perm:
                string += (val + "-") #creates an ID for the roll to see if this permutation has been rolled before
            if string not in string_list:
                unique_list.append(perm)
                string_list.append(string)
                count.append(1)
            else:
                count[string_list.index(string)] +=1
        index_list = []
        for lists in unique_list:
            index_list.append(list(map(int, lists)))
        perm_df = pd.DataFrame(index_list,count)
        perm_df.columns = [x for x in range(1,len(perm_df.columns)+1)]
        perm_df = perm_df.reset_index()
        perm_df = perm_df.rename(columns={'index':'Count'})
        perm_df = perm_df.set_index([x for x in range(1,len(perm_df.columns)+1)][:-1])
        return(perm_df)