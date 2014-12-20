import collections, random
import cardUtils, util
import sys

# Perform |numGames| of the following:
# For each game, take the MDP |mdp| (for example, DominionMDP) and 
# a dominion player (eg backpropogateRewardsTDLearning) of the
# DominionPlayer class, that plays according to the dynamics of the
# MDP.
# Each game will run for at most |maxTurns|.
# Return the list of total rewards that each player got for each game.
# Note: This code was adapted from code we used in our assignments from CS221
def simulateDominion(mdp, players, numGames=10, maxTurns=100, verbose=False, printResults=True):
    # Return i in [0, ..., len(probs)-1] with probability probs[i].
    def sample(probs):
        target = random.random()
        accum = 0
        for i, prob in enumerate(probs):
            accum += prob
            if accum >= target: return i
        raise Exception("Invalid probs: %s" % probs)
  
    def computeOtherPlayerStates(allPlayerStates, playerID):
        otherPlayerStates = []
        for otherPlayerID in xrange(len(allPlayerStates)):
            if playerID != otherPlayerID:
                otherPlayerStates.append(allPlayerStates[otherPlayerID][-1])
        return otherPlayerStates

    def getPlayerRewards(allPlayerStates):
        playerRewards = []
        for playerID in xrange(len(allPlayerStates)):
            otherPlayerStates = computeOtherPlayerStates(allPlayerStates, playerID)
            playerRewards.append(mdp.computeReward(allPlayerStates[playerID][-1], otherPlayerStates))
        return playerRewards

    allGameRewards = [[] for _ in range(len(players))]  # The rewards each player gets on each game
    allGameVictoryPoints = [[] for _ in range(len(players))]
    allGameTurns = [[] for _ in range(len(players))]
    for game in range(numGames):
        print ".",
        sys.stdout.flush()
        if verbose:
            print "####################################"
            print "####################################"
            print "Game " + str(game) + ":"
        state = mdp.startState()
        gameRewards = [0 for _ in range(len(players))]
        gameVictoryPoints = [0 for _ in range(len(players))]
        #keep track of all states so that, for example, we can backpropagate end reward
        allPlayerStates = [[state] for _ in range(len(players))]
        allPlayerStatesAndActions = [[] for _ in range(len(players))] 
        currTurn = 0
        lastTurn = 0
        #for _ in range(maxTurns):
        gameFinished = False
        while not gameFinished: #keep playing until the end of the game - when it break out. (endOfGame is true of turn >= maxTurns)
#            playerStates = [state] * len(players)
            playersHistory = [[] for _ in range(len(players))]
            for playerID in xrange(len(players)):
                player = players[playerID]
                state = allPlayerStates[playerID][-1]
                turnNumber = currTurn
                while turnNumber == currTurn:
                    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
                    turnNumber = turn
                    if turnNumber != currTurn:
                        break
                    actions = mdp.actions(state)
                    otherPlayerStates = computeOtherPlayerStates(allPlayerStates, playerID)
                    if mdp.endOfGame(state):
                        print "END OF GAME AND CALLS GET ACTION"
                    action = player.getAction(state, mdp.actions(state), otherPlayerStates)
                    allPlayerStatesAndActions[playerID].append((state, action)) 
                    transitions = mdp.succAndProbs(state, action, otherPlayerStates)
                    if verbose:
                        print "#####################################"
                        print "Player",playerID, ":",players[playerID].getPlayerName()
                        print "Turn:", turn, "Money:", money,
                        cardUtils.printHand(hand)
                        actionType, cardID = action
                        cardName = cardUtils.getCardNameFromID(cardID)
                        print "Action:", actionType, cardName,
                        cardUtils.printCardEffects(cardID)
                    # Choose a random transition
                    i = sample([prob for newState, prob in transitions])
                    newState, prob = transitions[i]
                    playersHistory[playerID].append(action)
                    playersHistory[playerID].append(newState)
                    
                    #Update kingdoms of other players
                    newKingdom = newState[0]
                    if newKingdom != kingdom:
                        for otherPlayerID in xrange(len(players)):
                            if playerID != otherPlayerID:
                                kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = allPlayerStates[otherPlayerID][-1]
                                allPlayerStates[otherPlayerID][-1] = (util.HashableDict(newKingdom), deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed)

                    #if endOfGame(newState, allPlayerStates[playerID]):
                    if mdp.endOfGame(newState):
                        allPlayerStates[playerID].append(newState) 
                        playerRewards = getPlayerRewards(allPlayerStates)
                        player.incorporateFeedback(state, action, playerRewards[playerID], None, otherPlayerStates=computeOtherPlayerStates(allPlayerStates,playerID))
                        for playerID in xrange(len(players)):
                            gameRewards[playerID] = playerRewards[playerID]
                            #print "compute vic points for state:", allPlayerStates[playerID][-1]
                            gameVictoryPoints[playerID] = cardUtils.computeVPointsFromState(allPlayerStates[playerID][-1])
                            players[playerID].endOfGame(playerRewards[playerID]) #TODO: remove the last parameter??
                            
                        gameFinished = True
                        lastTurn = turn
                        break
                    state = newState
                    allPlayerStates[playerID].append(state) 
                if gameFinished:
                    break
                player.incorporateFeedback(state, action, 0, newState, otherPlayerStates=computeOtherPlayerStates(allPlayerStates,playerID))

                #player.endOfTurn(
            currTurn += 1
            
        for playerID in xrange(len(players)):
            allGameRewards[playerID].append(gameRewards[playerID])
            allGameTurns[playerID].append(lastTurn)
            allGameVictoryPoints[playerID].append(gameVictoryPoints[playerID])

        allGameTurns.append(lastTurn)

    if printResults:
        for playerID in xrange(len(players)):
            print "____________________"
            print "Player %d:" % playerID, ":", players[playerID].getPlayerName()
            print "Average Rewards:", sum(allGameRewards[playerID]) / (0.0 + len(allGameRewards[playerID]))
            print "All Rewards:", allGameRewards[playerID]
            print "Average Turns:", sum(allGameTurns[playerID]) / (0.0 + len(allGameTurns[playerID]))
            print "All Turns:", allGameTurns[playerID]
            print "Average Victory Points:", sum(allGameVictoryPoints[playerID]) / (0.0 + len(allGameRewards[playerID]))
            print "All Victory Points:", allGameVictoryPoints[playerID]
            print "____________________"


    return (allGameRewards, allGameTurns)
    
    
