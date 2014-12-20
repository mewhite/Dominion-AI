import collections, util, math, random, copy, cardUtils
from DominionPlayer import DominionPlayer

class ExpensiveActionPlayer(DominionPlayer):
    def __init__(self, mdp):
        self.mdp = mdp
        
    def endOfGame(self, reward):
        pass
        
    def incorporateFeedback(self, state, action, reward, newState, otherPlayerStates=[]):
        pass

    def getPlayerName(self):
        return "ExpensiveActionPlayer"

    def getAction(self, state, possibleActions, otherPlayerStates):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        if phase == "action":
            cardID = max((cardUtils.getCardCostFromID(cardID), cardID) for actionType, cardID in possibleActions)[1]
            return ("play", cardID)
        else:
            #raise NotImplementedError("Action player should not be called during buy phase")
            return possibleActions[0]
    