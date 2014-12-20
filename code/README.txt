AUTOMATIC DOMINION PLAYING AGENT
By Monisha White and Nolan Walsh


~~~~~~~~~~~~~~Steps to run the Player:~~~~~~~~~~~~~~~
1. Extract data.zip into the folder that contains main.py.  There should now be a folder called "data" in the same folder as the rest of the python code.
2. Run main.py and select "0" to play against the player on the full kingdom.

Note: You can change settings and configurations in main.py (including selecting the starting kingdom)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Background info on specific files:
cards.txt:
    This file contains the list of cards that we implemented along with their effects.  If someone wants to edit the available cards or add new ones, this is the file to edit.  Be warned however, there are still places in the code (mostly relating to Provinces) that rely on certain cards being associated with certain cardIDs.

DominionMDP.py:
    An implementation of the game of Dominion as an MDP.  Takes in a starting kingdom, starting deck, and starting hand along with a maximum number of turns.  This allows for customization of the cards available, or that players start with.

DominionGameSimulator.py:
    This file runs games of dominion between players.  It takes in an MDP (Almost always an instance of DominionMDP) and a list of players, along with the number of games to run, and a limit on number of turns per game. 
   
cacheWeightsBackPropagate.py:
    In order to save and use weights that we have learned across runs, we store files containing weights on the disk.  This file contains code that will cache and retrieve those weights.
 
FinalPlayer.py:
    The final version of our player.  Takes in a series of options related to caching, learning, and what action player it should rely on.

data.zip:
	The data folder contains a set of trained weights for four different sizes of kingdoms.  There are two copies of each trained set for ease of use.  Switching to a different starting kingdom should automatically switch our player to use the set of weights appropriate for that kingdom.   The weights for the full kingdom were created by running tens of thousands of games against itself, while the weights for the other kingdoms were created on only 1000-2000 games and so may not be the best possible play.   At the time of this writing, these weights led our player to win against Big Money on all four kingdoms over 90% of the time.  This can easily be tested by running main.py and selecting "Test Final player against Big Money"
