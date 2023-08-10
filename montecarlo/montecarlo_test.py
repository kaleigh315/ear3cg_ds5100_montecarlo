import statistics
import unittest
import pandas as pd
import numpy as np
import random
from montecarlo import Die
from montecarlo import Game
from montecarlo import Analyzer

class DieTestSuite(unittest.TestCase):
    
    def test_1_change_weight(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        mydie.change_weight(1,3)
        self.assertTrue(3 in mydie.dice['weights'])
    def test_1_roll_die(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        self.assertTrue(isinstance(mydie.roll_die(5), list))
    def test_1_curr_state(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        self.assertTrue(mydie.curr_state().shape == (len(faces), 1))

class GameTestSuite(unittest.TestCase):
    
    def test_1_play(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        mydie2 = Die(faces)
        mydie3 = Die(faces)
        list_die = [mydie,mydie2,mydie3]
        test = Game(list_die)
        roll_number = 2
        test.play(roll_number)
        self.assertTrue(test.result_df.shape == (roll_number, len(list_die)))
    def test_1_results(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        mydie2 = Die(faces)
        mydie3 = Die(faces)
        test = Game([mydie,mydie2,mydie3])
        roll_number = 2
        test.play(roll_number)
        testresults = test.results(form="narrow")
        self.assertTrue(isinstance(testresults.index, pd.MultiIndex))
    def test_2_results(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        mydie2 = Die(faces)
        mydie3 = Die(faces)
        list_die = [mydie,mydie2,mydie3]
        test = Game(list_die)
        roll_number = 2
        test.play(roll_number)
        testresults = test.results(form="wide")
        self.assertTrue(testresults.shape == (roll_number, len(list_die)))

class AnalyzerTestSuite(unittest.TestCase):    
    def test_1_jackpot(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        mydie2 = Die(faces)
        mydie3 = Die(faces)
        test = Game([mydie,mydie2,mydie3])
        roll_number = 2
        test.play(roll_number)
        anatest = Analyzer(test)
        self.assertTrue(isinstance(anatest.jackpot(), int))
    def test_1_face_counts(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        mydie2 = Die(faces)
        mydie3 = Die(faces)
        test = Game([mydie,mydie2,mydie3])
        roll_number = 2
        test.play(roll_number)
        anatest = Analyzer(test)
        self.assertTrue(anatest.face_counts().shape[0] == roll_number)
    def test_2_face_counts(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        mydie2 = Die(faces)
        mydie3 = Die(faces)
        test = Game([mydie,mydie2,mydie3])
        roll_number = 2
        test.play(roll_number)
        anatest = Analyzer(test)
        self.assertTrue(anatest.face_counts().shape[1] == len(faces))
    def test_1_combination(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        mydie2 = Die(faces)
        mydie3 = Die(faces)
        test = Game([mydie,mydie2,mydie3])
        roll_number = 2
        test.play(roll_number)
        anatest = Analyzer(test)
        combo = anatest.combination()
        self.assertTrue(isinstance(combo.index, pd.MultiIndex))
    def test_1_permutation(self):
        faces = np.array([1,2,3,4,5,6])
        mydie = Die(faces)
        mydie2 = Die(faces)
        mydie3 = Die(faces)
        test = Game([mydie,mydie2,mydie3])
        roll_number = 2
        test.play(roll_number)
        anatest = Analyzer(test) 
        perm = anatest.permutation()
        self.assertTrue(isinstance(perm.index, pd.MultiIndex))
        
if __name__ == '__main__':

    unittest.main(verbosity=3)
