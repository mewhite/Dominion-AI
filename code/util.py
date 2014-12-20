import collections, random, time
from collections import Counter
import cardUtils


#Implementation of nchoosek found on StackOverflow
def nchoosek(n, k):
    result = 1
    for x in range(n - k + 1, n + 1):
        result *= x
    for x in range(1, k + 1):
        result /= x
    return result


#A subclass of dict that is hashable, must be sure not to change dicts after making them part of a state.
class HashableDict(Counter):
    def __hash__(self):
        return hash(frozenset(self))
    def __setitem__(self, key, value):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def __delitem__(self, key):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def clear(self):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def pop(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def popitem(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def setdefault(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))

#A reward function used for training our player.  Takes into account how much a player loses/wins by in calculating a reward
def learningComputeReward(state, otherPlayerStates=[]):
    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
    myVPoints = cardUtils.computeVictoryPoints(deck)
    maxVPoints = 0
    for otherPlayerState in otherPlayerStates:
        kingdom1, deck1, hand1, drawPile1, discardPile1, phase1, turn1, buys1, actions1, money1, cardsPlayed1 = otherPlayerState
        otherPlayerVPoints = cardUtils.computeVictoryPoints(deck1)
        if otherPlayerVPoints > maxVPoints:
            maxVPoints = otherPlayerVPoints
    vPointDif = myVPoints - maxVPoints
    if maxVPoints > myVPoints:
        return -50 + vPointDif
    elif myVPoints > maxVPoints:
        return 50 + vPointDif
    else:
        return 0

#Prints a summary of results from a series of games
def printGameSummary(results, players):
    allGameRewards, allGameTurns = results
    for playerID in range(len(players)):
        numGames = len(allGameRewards[playerID])
        numWins = 0
        numTies = 0
        numLosses = 0
        for reward in allGameRewards[playerID]:
            if reward > 0:
                numWins += 1
            elif reward < 0:
                numLosses += 1
            else:
                numTies += 1
        print "_________________________________"
        print "Player:", playerID, ":", players[playerID].getPlayerName()
        print "Number of Games Played: ", numGames
        print "NumWins:", numWins, "Win Percentage: ", numWins / (0.0 + numGames)
        print "NumLosses:", numLosses, "Loss Percentage: ", numLosses / (0.0 + numGames)
        print "NumTies:", numTies, "Tie Percentage: ", numTies / (0.0 + numGames)
        return 0


