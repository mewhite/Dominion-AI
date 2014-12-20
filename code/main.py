import cardUtils, random
from collections import Counter
from DominionMDP import DominionMDP
from bigMoney import BigMoney
import cacheWeights
import cacheWeightsBackpropagate
from DominionGameSimulator import simulateDominion
from ExpectimaxActionPhasePlayer import ExpectimaxActionPhasePlayer
from ActionPhaseMDP import ActionPhaseMDP
from BuyListPlayer import BuyListPlayer
from BadBigMoneyPlayer import BadBigMoneyPlayer
from HumanPlayer import HumanPlayer
from ExpensiveActionPlayer import ExpensiveActionPlayer
from RandomActionPlayer import RandomActionPlayer
from FinalPlayer import FinalPlayer
import featureExtractor
import util
import testActionPlayer

#Constructs the list of cards used throughout our code
cardUtils.initializeCardList("cards.txt")


#The best weights that we trained for our player are in data.zip and are accessible with the cacheStringKey set to "" or "BestWeights(FullKingdom)"
defaultCacheStringKey = ""

defaultTrainingCacheStringKey = "Training"

# Below are various kingdoms that are available to play (easily editable)
# The "Full" kingdom
startKingdom = Counter({0:100, 1:100, 2:100, 3:8, 4:8, 5:8, 6:10, 7:10, 8:10, 9:10, 10:10, 11:10, 12:10, 13:10, 14:8, 15:8})

# Medium sized kingdom
# startKingdom = Counter({0:100, 1:100, 2:100, 3:8, 4:8, 5:8, 6:10, 7:10, 8:10, 9:10, 10:10, 11:10})

# Small kingdom with 4 provinces
# startKingdom = Counter({0:100, 1:100, 2:100, 3:8, 4:8, 5:4, 6:8, 7:8, 8:8})

# Very small kingdom contianing only money, VP cards and 1 province
#startKingdom = Counter({0:100, 1:100, 2:100, 3:8, 4:8, 5:1})

startDeck = Counter({0:7,3:3})
startHand = (0,0,0,3,3)
dominion = DominionMDP(maxTurns=100, startKingdom=startKingdom, startDeck=startDeck, startHand=startHand)

# Settings for training and testing
gamesPerTest = 50
trainingRuns = 5
gamesPerTrainingRun = 100
handsPerTest = 100

def playGameAgainstHuman():
    finalPlayer = FinalPlayer(dominion, featureExtractor.newestFeatureExtractor, explorationProb=0, usingCachedWeights=True, cacheStringKey=defaultCacheStringKey, actionPlayer=ExpectimaxActionPhasePlayer(dominion))
    cachedWeights = Counter()
    cacheWeightsBackpropagate.bpsetWeightsFromCache(dominion.startKingdom, cachedWeights, finalPlayer.cacheStringKey, 1)
    finalPlayer.weights = cachedWeights
    if cachedWeights == Counter():
        print "####NO WEIGHTS FOUND####"
    humanPlayer = HumanPlayer(dominion)

    players = []
    players.append(finalPlayer)
    players.append(humanPlayer)

    simulateDominion(dominion, players, numGames=1, maxTurns=100, verbose=True)

# Testing the action player generates |handsPerTest| hands 
# and then tests them with a random player to compute the average reward
# Next, it runs the same set of hands with the ExpectimaxActionPhasePlayer
# and again computes the average reward.
# Finally, it lets a human play with the set of hands and computes the average reward
def testTheActionPlayer():
    testActionPlayer.testActionPlayer(startKingdom, handsPerTest)

def testFinalPlayer():
    actionPlayer = ExpectimaxActionPhasePlayer(dominion)
    finalPlayer = FinalPlayer(dominion, featureExtractor.newestFeatureExtractor, explorationProb=0, usingCachedWeights=True, cacheStringKey="", actionPlayer=ExpectimaxActionPhasePlayer(dominion))
    bigMoneyPlayer = BigMoney(dominion)    
    finalPlayer.cacheStringKey = defaultCacheStringKey

    players = []
    players.append(finalPlayer)
    players.append(bigMoneyPlayer)

    tempRewardFunction = dominion.computeReward
    dominion.computeReward = util.learningComputeReward

    for playerID in range(len(players)):
        print "Player ", playerID, ":", players[playerID].getPlayerName()
        if (players[playerID].usingCachedWeights):
            cacheStringKey = players[playerID].cacheStringKey
            print "Using Cached Weights from", cacheStringKey 
            #Retrieve weights from cache so that it builds on already cached weights.
            cachedWeights = Counter()
            cacheReductionFactor = 1
            cacheWeightsBackpropagate.bpsetWeightsFromCache(dominion.startKingdom, cachedWeights, cacheStringKey, cacheReductionFactor)
            players[playerID].weights = cachedWeights
            if cachedWeights == Counter():
                print "####NO WEIGHTS FOUND####"

    results = simulateDominion(dominion, players, numGames=gamesPerTest, maxTurns=100, verbose=False)
    util.printGameSummary(results, players)
    allGameRewards, allGameTurns = results

    for playerID in range(len(players)):
        if (players[playerID].cachingWeights): 
            cacheWeightsBackpropagate.bpcacheWeights(dominion.startKingdom, players[playerID].weights, players[playerID].cacheStringKey)

def trainFinalPlayer():
    for _ in xrange(trainingRuns):
        actionPlayer = ExpectimaxActionPhasePlayer(dominion)
        finalPlayer = FinalPlayer(dominion, featureExtractor.newestFeatureExtractor, explorationProb=0.2, usingCachedWeights=True, cachingWeights=True, actionPlayer=actionPlayer, learning=True)
        finalPlayer2 = FinalPlayer(dominion, featureExtractor.newestFeatureExtractor, explorationProb=0.2, usingCachedWeights=True, cachingWeights=True, actionPlayer=actionPlayer, learning=True)
        finalPlayer.cacheStringKey = defaultTrainingCacheStringKey
        finalPlayer2.cacheStringKey = defaultTrainingCacheStringKey + "2"
    
        players = []
        players.append(finalPlayer)
        players.append(finalPlayer2)
    
        tempRewardFunction = dominion.computeReward
        dominion.computeReward = util.learningComputeReward
    
        for playerID in range(len(players)):
            print "Player ", playerID, ":", players[playerID].getPlayerName()
            if (players[playerID].usingCachedWeights):
                cacheStringKey = players[playerID].cacheStringKey
                print "Using Cached Weights from", cacheStringKey 
                #Retrieve weights from cache so that it builds on already cached weights.
                cachedWeights = Counter()
                cacheReductionFactor = 1
                cacheWeightsBackpropagate.bpsetWeightsFromCache(dominion.startKingdom, cachedWeights, cacheStringKey)
                players[playerID].weights = cachedWeights
                if cachedWeights == Counter():
                    print "####NO WEIGHTS FOUND####"
    
        results = simulateDominion(dominion, players, numGames=gamesPerTrainingRun, maxTurns=100, verbose=False)
        util.printGameSummary(results, players)
        allGameRewards, allGameTurns = results
    
        for playerID in range(len(players)):
            if (players[playerID].cachingWeights): 
                cacheWeightsBackpropagate.bpcacheWeights(dominion.startKingdom, players[playerID].weights, players[playerID].cacheStringKey)
print "########################################################"
print "Note: You can select the starting kingdom in main.py"
print "0: Play game against Human player"
print "1: Test Final version against Big Money"
print "2: Train Final version against itself"
print "3: Test the action player"
while True:
    actionChoice = raw_input("Enter the number of your choice (q to quit): ")
    if "q" in actionChoice:
        exit()
    if actionChoice == "0":
        playGameAgainstHuman()
        break
    if actionChoice == "1":
        testFinalPlayer()
        break
    if actionChoice == "2":
        trainFinalPlayer()
        break
    if actionChoice == "3":
        testTheActionPlayer()
        break
    else:
        print "That is not a valid action. Try again."