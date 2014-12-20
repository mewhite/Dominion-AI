import collections, util, math, random, copy

# Performs Q-learning. 
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy returns a random action
class QLearningAlgorithm():
    def __init__(self, actions, discount, featureExtractor, explorationProb=1):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = collections.Counter()
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Uses the epsilon-greedy algorithm: returning a random action with probability
    # |explorationProb|.
    def getAction(self, state):
        self.numIters += 1
        #It assumes that it will always receive an acceptable
        #    action: if the end of the game, the only action should be "idle"
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return .1

    # This function is called with (s, a, r, s'), which is used to update the weights.
    # If s is a terminal state, then s' will be None.
    # Weights are updated using self.getStepSize().
    # Uses self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        residual = (reward + (self.discount * max(self.getQ(newState, nextAction) for nextAction in self.actions(newState)))) - self.getQ(state, action)
        for feature, value in self.featureExtractor(state, action):
            self.weights[feature] += self.getStepSize() * residual * value