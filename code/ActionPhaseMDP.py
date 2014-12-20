import cardUtils, util, copy
from collections import Counter
from DominionMDP import DominionMDP

#An MDP that represents a single action phase.  Used for testing action players
class ActionPhaseMDP(DominionMDP):
    
    def endOfGame(self, state):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        return phase == "buy"
        
    def computeReward(self, state, otherPlayerStates=[]):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        return money