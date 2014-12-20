import collections, util, math, random, copy, cardUtils
from DominionPlayer import DominionPlayer

#An action player that plays randomly.  Used as a baseline when testing our ExpectimaxActionPlayer
class RandomActionPlayer(DominionPlayer):
    def __init__(self, mdp):
        self.mdp = mdp
        
    def endOfGame(self, reward):
        pass
        
    def incorporateFeedback(self, state, action, reward, newState, otherPlayerStates=[]):
        pass

    def getPlayerName(self):
        return "RandomActionPlayer"

    def getAction(self, state, possibleActions, otherPlayerStates):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        if phase == "action":
            return random.choice(possibleActions)
        else:
            raise NotImplementedError("Action player should not be called during buy phase")    