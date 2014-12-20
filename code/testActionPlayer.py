import collections, random, time
from collections import Counter
from ActionPhaseMDP import ActionPhaseMDP
from RandomActionPlayer import RandomActionPlayer
from ExpectimaxActionPhasePlayer import ExpectimaxActionPhasePlayer
from DominionGameSimulator import simulateDominion
from HumanPlayer import HumanPlayer
import cardUtils

def testActionPlayer(startKingdom, numTrials):
    def generateRandomState():
        #Generate deck
        totalIDs = len(startKingdom)
        startDeck = Counter()
        startDeck[0] += 1
        for i in range(totalIDs):
            startDeck[i] += random.randint(0,startKingdom[i])
        #Generate Hand
        handSize = 5
        deckSize = sum(startDeck.values())
        handList = []
        while len(handList) < handSize:
            randomID = random.randint(0,totalIDs)
            if startDeck[randomID] > 0:
                handList.append(randomID)
        return (startDeck, tuple(handList))

    playerRewards = 0
    baseRewards = 0
    hands = [generateRandomState() for _ in xrange(numTrials)]
    print "Done generating hands"
    startTime = time.time()
    for actionStartDeck, actionStartHand in hands:
        actionPhaseDominion = ActionPhaseMDP(maxTurns=1, startKingdom=startKingdom, startDeck=actionStartDeck, startHand=actionStartHand)
        actionPlayer = RandomActionPlayer(actionPhaseDominion)
        allGameRewards, allGameTurns = simulateDominion(actionPhaseDominion, [actionPlayer], numGames=1, maxTurns=100, verbose=False, printResults=False)
        playerRewards += sum(allGameRewards[0])
        print ".",
    endTime = time.time()
    print
    print "Random average rewards", playerRewards / (numTrials + 0.0),"Time:", endTime - startTime
    playerRewards = 0
    startTime = time.time()

    for actionStartDeck, actionStartHand in hands:
        actionPhaseDominion = ActionPhaseMDP(maxTurns=1, startKingdom=startKingdom, startDeck=actionStartDeck, startHand=actionStartHand)
        actionPlayer = ExpectimaxActionPhasePlayer(actionPhaseDominion, maxExplorationDepth=1)
        allGameRewards, allGameTurns = simulateDominion(actionPhaseDominion, [actionPlayer], numGames=1, maxTurns=100, verbose=False, printResults=False)
        playerRewards += sum(allGameRewards[0])
        print ".",
    endTime = time.time()
    print
    print "Expectimax average rewards", playerRewards / (numTrials + 0.0),"Time:", endTime - startTime
    playerRewards = 0
    startTime = time.time()

    for actionStartDeck, actionStartHand in hands:
        actionPhaseDominion = ActionPhaseMDP(maxTurns=1, startKingdom=startKingdom, startDeck=actionStartDeck, startHand=actionStartHand)
        actionPlayer = HumanPlayer(actionPhaseDominion)
        allGameRewards, allGameTurns = simulateDominion(actionPhaseDominion, [actionPlayer], numGames=1, maxTurns=100, verbose=False, printResults=False)
        playerRewards += sum(allGameRewards[0])
        print ".",
    endTime = time.time()
    print
    print "Human average rewards", playerRewards / (numTrials + 0.0),"Time:", endTime - startTime
    playerRewards = 0
    startTime = time.time()