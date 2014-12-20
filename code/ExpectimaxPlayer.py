import collections, util, math, random, copy, cardUtils
from DominionPlayer import DominionPlayer

class ExpectimaxActionPhasePlayer(DominionPlayer):
    def __init__(self, mdp, buyList, actionPlayer):
        self.mdp = mdp
        self.buyList = buyList
        self.actionPlayer = actionPlayer
        
    def endOfGame(self, reward, allStates):
        pass
        
    def incorporateFeedback(self, state, action, reward, newState):
        pass

    def getAction(self, state, possibleActions, otherPlayerStates):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        if phase == "action":
            return getBestActionFromExpectimax(state, possibleActions)
        else:
            return possibleActions[0]
    
    def expectimaxEval(state, maxDepth):
        if isGameOver(state):
            return scoreEvaluationFunction(state)
        elif depth == self.depth:
            return self.evaluationFunction(state)
        if agentIndex >= state.getNumAgents():
            agentIndex = 0
            actions = state.getLegalActions(agentIndex)
        if agentIndex == self.index:
            actions.remove(Directions.STOP)
            return max(expectimaxEval(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth) for action in actions)
        else:
            if agentIndex == state.getNumAgents() - 1:
                depth += 1
                total = sum(expectimaxEval(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth) for action in actions)
        return total / (0.0 + len(actions))
    
    def getBestActionFromExpectimax(state, possibleActions):
        bestActionValue = float(-"inf")
        bestAction = None
        for action in possibleActions:
            
        
        return bestAction
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        