import collections, random


# Perform |numTrials| of the following:
# On each trial, take the MDP |mdp| (for example, DominionMDP) and 
# an TDLearning aglorithm |td| and simulates the
# TD Learning algorithm according to the dynamics of the MDP.
# Each trial will run for at most |maxIterations|.
# Return the list of the total rewards that we get and total number of 
# turns taken for each trial.
def tdSimulate(mdp, td, numTrials=10, maxIterations=50, verbose=False,
             sort=False):
    # Return i in [0, ..., len(probs)-1] with probability probs[i].
    def sample(probs):
        target = random.random()
        accum = 0
        for i, prob in enumerate(probs):
            accum += prob
            if accum >= target: return i
        raise Exception("Invalid probs: %s" % probs)

    totalRewards = []  # The rewards we get on each trial
    totalTurns = []
    for trial in range(numTrials):
        state = mdp.startState()
        sequence = [state]
        totalDiscount = 1
        totalReward = 0
        allStates = [] #keep track of all states so that we can backpropogate end reward
        for _ in range(maxIterations):
            allStates.append(state) 
            actions = mdp.actions(state)
            action = td.getAction(state, mdp.actions(state))
            transitions = mdp.succAndProbReward(state, action, otherPlayerStates = [])
            # Choose a random transition
            i = sample([prob for newState, prob, reward in transitions])
            newState, prob, reward = transitions[i]
            sequence.append(action)
            sequence.append(reward)
            sequence.append(newState)
            if mdp.endOfGame(newState):
                td.incorporateFeedback(state, action, reward, None)
            else:
                td.incorporateFeedback(state, action, reward, newState)
            totalReward += totalDiscount * reward
            totalDiscount *= mdp.discount()
            state = newState
        if verbose:
            print "Trial %d (totalReward = %s): %s" % (trial, totalReward, sequence)
        totalRewards.append(totalReward)
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        totalTurns.append(turn)

    if verbose:
        print "Total Rewards:", totalRewards
        print "Total Turns:", totalTurns
    return (totalRewards, totalTurns)
