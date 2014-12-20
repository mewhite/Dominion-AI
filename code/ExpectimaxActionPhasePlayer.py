import collections, util, math, random, copy, cardUtils
from DominionPlayer import DominionPlayer

class ExpectimaxActionPhasePlayer(DominionPlayer):
    def __init__(self, mdp, maxExplorationDepth=1):
        self.mdp = mdp
        self.maxDepth = maxExplorationDepth
        
    def endOfGame(self, reward):
        pass
        
    def incorporateFeedback(self, state, action, reward, newState, otherPlayerStates=[]):
        pass
    
    def heuristicStateEvaluation(self, state):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        return money + actions
        
    def turnReward(self, state):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        return money + ((buys - 1) * money / 4)  
    
    def isActionPhaseOver(self, state):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        return phase != "action"
    
    def expectimaxEval(self, statesAndProbs, depth):
        stateSum = 0
        for newState, prob in statesAndProbs:
            if self.isActionPhaseOver(newState):
                reward = self.turnReward(newState)
                stateSum += reward * prob
            elif depth == self.maxDepth:
                stateSum += self.heuristicStateEvaluation(newState) * prob
            else:
                actions = self.mdp.actions(newState)
                stateSum += max(self.expectimaxEval(self.mdp.succAndProbs(newState, action), depth + 1) for action in actions) * prob
        value = stateSum
        return value
    
    def getBestActionFromExpectimax(self, state, possibleActions):
        #Computes best expected value over actions
        return max((self.expectimaxEval(self.mdp.succAndProbs(state, action), 0), action) for action in possibleActions)[1]

    def getPlayerName(self):
        return "Expectimax Action Phase Player"

    def getAction(self, state, possibleActions, otherPlayerStates):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        if phase == "action":
            return self.getBestActionFromExpectimax(state, possibleActions)
        else:
            raise NotImplementedError("Action player should not be called during buy phase")
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        