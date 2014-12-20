import collections, util, math, random, copy
from DominionPlayer import DominionPlayer
import cardUtils
from ExpectimaxActionPhasePlayer import ExpectimaxActionPhasePlayer

# actions: a function that takes a state and returns a list of actions.
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action.
class FinalPlayer(DominionPlayer):
    def __init__(self, mdp, featureExtractor, explorationProb=0.2, usingCachedWeights=False, cachingWeights=False, cacheStringKey="", actionPlayer=None, learning=False):
        self.verbose = False
        self.mdp = mdp
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = {} #weights is a dict of feature to (timesVisited, weight), where weight is the average reward
        self.numIters = 0
        self.usingCachedWeights = usingCachedWeights
        self.cachingWeights = cachingWeights
        self.cacheStringKey = cacheStringKey
        self.actionPlayer = actionPlayer
        self.learning = learning
        self.allStates = []

    # Return the Value of the state associated with the weights and features
    def getV(self, state, otherPlayerStates):
        score = 0
        if state != None:
            features = self.featureExtractor(state, otherPlayerStates)
            for feature, v in features:
                if v == 0:
                    print "should not be in features?"
                if feature in self.weights:
                    timesVisited, weight = self.weights[feature]
                    score += (1.0 / len(features)) * weight * v    
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state, actions, otherPlayerStates=[]):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, numActions, money, cardsPlayed = state
        self.numIters += 1
        #if no more actions it means it's the end of the game
        if actions == ["idle"]:
            print state
            raise Exception("ERROR: SHOULD NEVER GET HERE!")
        if phase == "action":
            if self.actionPlayer != None:
                action = self.actionPlayer.getAction(state, actions, otherPlayerStates=[])
                return action
        if random.random() < self.explorationProb:
            if self.verbose:
                "Returning random action due to exploration"
            return random.choice(actions)
        else:
            bestAction = None
            bestActionScore = float('-inf')
            for action in actions:
                actionScore = 0
                statesAndProbs = self.mdp.succAndProbs(state, action, otherPlayerStates)
                for newState, prob in statesAndProbs:
                    if self.mdp.endOfGame(newState):
                        actionScore += self.mdp.computeReward(newState, otherPlayerStates) * prob
                    else:
                        actionScore += self.getV(newState, otherPlayerStates) * prob
                if self.verbose:
                    print "Action: ",action, "Score:",actionScore
                    
                if actionScore >= bestActionScore:
                    bestActionScore = actionScore
                    bestAction = action
            if bestAction == None:
                print state
                print actions
                print "ERROR"
            if self.verbose:
                print "Best action: ", bestAction
            return bestAction


    # Doesn't update the weights until the end of the game, when endOfGame is called
    def incorporateFeedback(self, state, action, reward, newState, otherPlayerStates=[]):
        self.allStates.append((state, otherPlayerStates))
        return

    def backpropagateReward(self, reward, allStates):
        for state, otherPlayerStates in allStates:
            for feature, value in self.featureExtractor(state, otherPlayerStates):
                if feature in self.weights:
                    timesVisited, weight = self.weights[feature]
                    newWeight = ((timesVisited + 0.0) / (timesVisited + 1)) * weight + (reward / (timesVisited + 1))
                    self.weights[feature] = (timesVisited + 1, newWeight)
                else:
                    self.weights[feature] = (1, reward)

    def endOfGame(self, reward):
        if self.learning:
            self.backpropagateReward(reward, self.allStates)
        self.allStates = []
        
    def getPlayerName(self):
        return "Final Player"
            

