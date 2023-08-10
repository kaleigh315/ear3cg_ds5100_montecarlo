# Monte Carlo Simulator

## Metadata

### Project Name: Monte Carlo Simulator
### UVA User ID: ear3cg
### Name: Kaleigh O'Hara

## Synopsis

This Python module can use multiple similar die of varying weights with numeric or string faces in the Die class. This die or these dice from the Die class can be used in the Game class to play a dice game and returns a data frame of the faces rolled. Additionally, in the Analyzer class, the module can analyze the outcomes by calculating the number of jackpots (a result in which all faces are the same), providing a data frame of the counts of each face and computing the distinction combinations and/or permutations of the dice rolls.

The classes are related in the following way: Game objects are initialized with a Die object, and Analyzer objects are initialized with a Game object.

To use this module, first download the setup.py and montecarlo folder from the repo. Then, on your local machine, navigate to the directory of the setup.py and montecarlo folder. Enter the following code into the bash command line:

`pip install -e.`

Next, in your Python file import the classes:

  `from montecarlo import Die`
  
  `from montecarlo import Game`
  
  `from montecarlo import Analyzer`

To create a traditional 6-sided die with faces: "1" "2" "3" "4" "5" "6," use the code below:
 
 `Die(np.array([1,2,3,4,5,6]))`

Please note that the faces passed to the Die class must be a numpy array.

All dies are initially fair; the weights of all die created are "1.0" However, to change the weights of the die, use the following code:

`die_object.change_weight(6,50)` 

where "die_object" is the die object created, "6" is the face of the die whose weight to be changed and "50" is the new weight of face "6" in "die_object." Weights of the die need to be changed one at a time.

To roll one die object once, use the below code:

`die_object.roll_die()`

where "die_object" is the die object created. To roll one die object four times, use the below code:

`die_object.roll_die(4)`

where "die_object" is the die object created and "4" is the number of rolls. (Notice that the number of rolls defaults to 1 if not otherwise specified.)

To return a copy of the dice data frame comprised of the faces of the die and the respective weights, use the following code:

`die_object.curr_state()`

where "die_object" is the die object created.

In the Game class, more than one similar die can be rolled. By similar dice, we mean that each die in a given game has the same number of sides and associated faces, but each die object may have its own weights.

To create a Game object, pass a list of all the die objects that you want to roll as a part of the game.

`Game([die_object1, die_object2, die_object3])`

where die_object1, die_object2 and die_object3 are die objects.

To roll every dice in the list of die objects passed to the Game class, use the code below:

`game_object.play(10000)`

where "game_object" is a game object and "10000" is the number of times each die will be rolled.

To display the faces rolled, use the function and code below:

`game_object.results()`

where "game_object" is a game object. This displays a data frame in the "wide" form with roll number as named index, die number as columns and face rolled in that instance in each cell. The code below will give the same display:

`game_object.results("wide")`

To display in a "narrow" form with a MultiIndex, comprising the roll number and the die number (in that order), and a single column with the outcomes use the following code:

`game_object.results("narrow")`

where "game_object" is a game object.

The Analyzer class provides information about the outcomes of the die rolled in the Game class.

To create an Analyzer object, pass a Game object to the Analyzer class.

`Analyzer(game_object)`

where "game_object" is a game object. Note that the "game_object" passed will have to have already used the "play()" method to roll the die or dice before the Analyzer class can provide any interpretable output.

To find out how many jackpots were rolled of the die and number of rolls, use the code below:

`analyzer_object.jackpot()`

where "analyzer_object" is an analyzer object.

To see a data frame of the counts of each face value, use the following code:

`analyzer_object.face_counts()`

where "analyzer_object" is an analyzer object.

The following code computes the distinct combinations of faces rolled, along with their counts:

`analyzer_object.combination()`

where "analyzer_object" is an analyzer object.

The following code computes the distinct combinations of faces rolled, along with their counts:

`analyzer_object.permutation()`

where "analyzer_object" is an analyzer object.

## API Description

See list of all classes with their public methods and attributes below.

```
`class Analyzer(builtins.object)`
     `|  Analyzer(game_object)`
     `|`  
     `|  An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it.`
     `|`  
     `|  Methods defined here:`
     `|`  
     `|  combination(self)`
     `|      PURPOSE: This function computes the distinct combinations of faces rolled, along with their counts.`
     `|`     
     `|      RETURN:`
     `|      combo_df  a data frame of the count of order-independent, distinct combinations with a MultiIndex of distinct combinations and a column for the associated counts`
     `|` 
     `|  face_counts(self)`
     `|      PURPOSE: This function computes how many times a given face is rolled in each event.`
     `|`      
     `|      RETURN:`
     `|      countval_df  a data frame with an index of the roll number, face values as columns, and count values in the cells (i.e. it is in wide format)`
     `|`      
     `|      OBJECT CHANGES:`
     `|      countval_df  creates a data frame with count of face values in the cells`
     `|`  
     `|  jackpot(self)`
     `|      PURPOSE: This function calculates how many jackpots (a result in which all faces are the same) are rolled in a game.`
     `|`      
     `|      RETURN:`
     `|      jackpot_count  integer for the number of jackpots`
     `|`  
     `|  permutation(self)`
     `|      PURPOSE: This function computes the distinct permutations of faces rolled, along with their counts.`
     `|`      
     `|      RETURN:`
     `|      combo_df  a data frame of the count of order-dependent, distinct permutations with a MultiIndex of distinct combinations and a column for the associated counts`
     `|`  
     `|  ----------------------------------------------------------------------`
     `|  Data descriptors defined here:`
     `|`
     `|  __dict__`
     `|      dictionary for instance variables (if defined)`
     `|`  
     `|  __weakref__`
     `|      list of weak references to the object (if defined)`
```
    
    class Die(builtins.object)
     |  Die(face)
     |  
     |  A die has a given number of sides, or "faces," and a given number of weights, and can be rolled to select a face.
     |  Each side contains a unique symbol. Symbols may be all alphabetic or all numeric.
     |  The weights are just numbers, not a normalized probability distribution.
     |  The die has one behavior, which is to be rolled one or more times.
     |  
     |  Methods defined here:
     |  
     |  change_weight(self, face_val, new_weight)
     |      PURPOSE: This functions checks if the face value to be changed exists in the initial array of face values.
     |               Then, it checks to see if the weight is a valid type, i.e. if it is numeric (integer or float) or castable as numeric.
     |      
     |      INPUTS
     |      face_val   numeric or string face value whose weight to change
     |      new_weight  numeric or castable as numeric weight to replace the existing weight of for face_val
     |      
     |      OBJECT CHANGES:
     |      dice        specified weight of given column updates
     |  
     |  curr_state(self)
     |      PURPOSE: This function provides the dice object data frame to users.
     |      
     |      RETURN: This function returns a copy of the dice object data frame.
     |  
     |  
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class Game(builtins.object)
     |  Game(dice)
     |  
     |  A game consists of rolling of one or more similar dice (Die objects) one or more times.
     |  Each game is initialized with a Python list that contains one or more dice.
     |  Game objects have a behavior to play a game, i.e. to roll all of the dice a given number of times.
     |  Game objects only keep the results of their most recent play.
     |  
     |  Methods defined here:
     |  
     | play(self, rolls_play)
     |      PURPOSE: This function plays the game by rolling the dice a specified number of times and returns an organized data frame of results for each dice rolled.
     |      
     |      INPUTS:
     |      rolls_play  integer parameter to specify how many times the dice should be rolled
     |      
     |      OBJECT CHANGES:
     |      result_df  data frame with results of the game with roll number as named index, die number as columns and face rolled in that instance in each cell
     |  
     |  results(self, form='wide')
     |      PURPOSE: This function shows the user the results in either "narrow" or "wide" form of the most recent play. A ValueError is raised if something other than "narrow" or "wide" is passed.
     |      
     |      INPUTS:
     |      form  a string parameter to specify to return the data frame in "narrow" or "wide" form which defaults to wide form
     |      
     |      RETURN: This function returns result_df, data frame with results of the game, in either "narrow" form 
     |              (with a MultiIndex, comprising the roll number and the die number (in that order), and a single column with the outcomes)
     |              or in "wide" form (with roll number as named index, die number as columns and face rolled in that instance in each cell)
     |      
     |      OBJECT CHANGES:
     |      result_df  a data frame with orientation of results will change to a MultiIndex, comprising the roll number and the die number (in that order), and a single column with the outcomes if "narrow" form is selected

