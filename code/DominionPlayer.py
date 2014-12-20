#A superclass for all dominion player classes
class DominionPlayer():
    def __init__(self, mdp, discount, explorationProb=0.2, verbose=False, usingCachedWeights=False, cachingWeights=False, cacheStringKey=""):
        raise NotImplementedError("Override me")
    
    def endOfGame(self, reward):
        raise NotImplementedError("Override me")
        
    def incorporateFeedback(self, state, action, reward, newState, otherPlayerStates):
        raise NotImplementedError("Override me")

    def getAction(self, state, possibleActions, otherPlayerStates):
        raise NotImplementedError("Override me")
    
    def getPlayerName(self):
        raise NotImplementedError("Override me")
 