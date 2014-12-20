import cardUtils, util, copy
from collections import Counter

class ValueIteration():

    # Value iteration firsts computes V_opt. Once V_opt is computed, computes
    # the optimal policy pi.
    def solve(self, mdp, epsilon=0.001):
        mdp.computeStates()
        def computeActionValue(state, action, vPrevious):
            total = 0.0
            for newState, prob, reward in mdp.succAndProbReward(state, action):
                total += prob * (reward + (mdp.discount() * vPrevious[newState]))
            return total
        def maxDiff(v, vPrevious):
            m = max(abs(v[state] - vPrevious[state]) for state in mdp.states)
            return m
        pi = {}
        v = {state:0.0 for state in mdp.states}
        while True:
            vPrevious = copy.copy(v)
            for state in mdp.states:
                if mdp.actions(state) == ["idle"]:
                    pi[state] = "idle"
                else:
                    actionValues = {action:computeActionValue(state, action, vPrevious) for action in mdp.actions(state)}
                    optAction, optValue = max(actionValues.iteritems(), key=lambda pair: pair[1])
                    v[state] = optValue
                    pi[state] = optAction
            if maxDiff(v, vPrevious) <= epsilon:
                break
        self.V = v
        self.pi = pi