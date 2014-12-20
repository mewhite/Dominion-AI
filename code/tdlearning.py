import collections, util, math, random, copy
from monteCarloSimulate import tdMonteCarloSimulate


# Performs TD-learning.
# actions: a function that takes a state and returns a list of possible actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action.
class TDLearningAlgorithm():
    def __init__(self, mdp, discount, featureExtractor, usingMonteCarlo=False, explorationProb=0.2, verbose=False):
        self.verbose = verbose
        self.mdp = mdp
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = collections.Counter()
        self.numIters = 0
        self.usingMonteCarlo = usingMonteCarlo

    # Return the value V associated with the weights and features
    def getV(self, state):
        score = 0
        if state != None:
            for f, v in self.featureExtractor(state):
                score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # We use the epsilon-greedy algorithm, taking a random 
    # action with probability |explorationProb|.
    def getAction(self, state, actions, otherPlayerStates=[]):
        self.numIters += 1
        #if no more actions it means it's the end of the game
        if actions == ["idle"]:
            if self.verbose:
                "Returning idle"
            return "idle" #don't compute succAndProbReward
        if random.random() < self.explorationProb:
            if self.verbose:
                "Returning random action due to exploration"
            return random.choice(actions)
        else:
            bestAction = None
            bestActionScore = float('-inf')
            for action in actions:
                actionScore = 0
                probAndRewards = self.mdp.succAndProbReward(state, action, otherPlayerStates)
                for newState, prob, reward in probAndRewards:
                    if self.mdp.endOfGame(newState):
                        actionScore += self.mdp.computeReward(newState, otherPlayerStates) * prob
                    else:
                        actionScore += self.getV(newState) * prob
                if self.verbose:
                    print "Action: ",action, "Score:", actionScore
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

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 0.1

    # We call this function with (s, a, r, s'), which we use to update the weights.
    # If s is a terminal state, then s' will be None.
    # Updates the weights using self.getStepSize()
    # Uses self.getV() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        residual = (reward + (self.discount * self.getV(newState))) - self.getV(state)
        for feature, value in self.featureExtractor(state):
            self.weights[feature] += self.getStepSize() * residual 

        def normalize(weights):
            total = 0
            for feature in weights:
                total += math.fabs(weights[feature])
            if total != 0: 
                for feature in weights:
                    weights[feature] /= total

