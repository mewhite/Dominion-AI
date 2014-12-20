import cardUtils
import collections
from collections import Counter

#Various feature extractors for DominionMDP
def newestFeatureExtractor(state, otherPlayerStates=[]):
    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
    features = []
    vPoints = cardUtils.computeVictoryPoints(deck)
    maxOtherPlayerVPoints = 0
    for state in otherPlayerStates:
        playerVPoints = cardUtils.computeVPointsFromState(state)
        if playerVPoints > maxOtherPlayerVPoints:
            maxOtherPlayerVPoints = playerVPoints
    vPointsDif = vPoints - maxOtherPlayerVPoints
    #NUMBER OF EACH CARD AND TURN
    for cardID in deck:
        features.append(("numOfCardsInDeckOfType" + str(cardID) + "=" + str(deck[cardID]) + "turndiv3:" + str(turn / 3), 1))
    
    #AVERAGE TREASURE VALUE AND TURN
    averageMoneyValue = (deck[0] + deck[1] * 2 + deck[2] * 3) / (deck[0] + deck[1] + deck[2] + 0.0)
    roundedAverageMoneyValue = round(averageMoneyValue, 1)
    features.append(("averageMoneyValue:" + str(roundedAverageMoneyValue) + "turndiv3:" + str(turn / 3), 1))
    
    #NUM PROVINCES AND VPOINTSDIF
    numProvinces = cardUtils.getNumProvinceCards(kingdom)
    features.append(("vPointsDif" + str(vPointsDif) + "provinces:" + str(numProvinces), 3))
    return features

def deckProvinceFeatureExtractor(state, otherPlayerStates=[]):
    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
    features = []
    numProvinces = cardUtils.getNumProvinceCards(kingdom)
    features.append(("provinces:" + str(numProvinces) + "deck:" + str(deck), 1))
    return features


def backpropagateFeatureExtractor(state):
    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
    features = []
    vPoints = cardUtils.computeVictoryPoints(deck)
    #NUMBER OF EACH CARD AND TURN
    for cardID in deck:
       features.append(("numOfCardsInDeckOfType" + str(cardID) + "=" + str(deck[cardID]) + "turndiv3:" + str(turn / 3), 1))
    #DECK VALUE AND TURN
    deckValue = cardUtils.computeDeckValue(deck)
    features.append(("deckValue:" + str(deckValue) + "turn:" + str(turn), 1))
    #NUM PROVINCES AND TURN
    numProvinces = cardUtils.getNumProvinceCards(deck)
    features.append(("provincesInDeck:" + str(deck) + "turn:" + str(turn), 1))
    return features
    
def gameStageFeatureExtractor(state, otherPlayerStates=[]) :
    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
    features = []
    #Compute "Stage" of game
    opponentState = otherPlayerStates[0]
    oppkingdom, oppdeck, opphand, oppdrawPile, oppdiscardPile, oppphase, oppturn, oppbuys, oppactions, oppmoney, oppcardsPlayed = opponentState
    gameStage = "Start"
    if deck[5] > 0 or oppdeck[5] > 0:
        gameStage = "Middle"
    if deck[5] + oppdeck[5] > 6:
        gameStage = "End"

    deckValue = cardUtils.computeDeckValue(deck)
    treasureCount = 0
    for cardID in deck:
        if "treasure" in cardUtils.getCardFromID(cardID).cardType:
            treasureCount += deck[cardID]
    averageMoneyValue =  (deckValue + 0.0) / treasureCount
    roundedMoneyValue = round(averageMoneyValue, 1)
    features.append(("AverageMoneyValue:" + str(roundedMoneyValue) + "Stage" + gameStage, 1))

    numProvinces = cardUtils.getNumProvinceCards(deck)
    features.append(("provincesInDeck:" + str(numProvinces) + "Stage:" + gameStage, 1))

    for cardID in deck:
        features.append(("numOfCardsInDeckOfType" + str(cardID) + "=" + str(deck[cardID]) + "Stage:" + gameStage, 1))

    vPoints = cardUtils.computeVictoryPoints(deck)
    maxOtherPlayerVPoints = 0
    for state in otherPlayerStates:
        playerVPoints = cardUtils.computeVPointsFromState(state)
        if playerVPoints > maxOtherPlayerVPoints:
            maxOtherPlayerVPoints = playerVPoints
    vPointsDif = vPoints - maxOtherPlayerVPoints
    features.append(("vPointsDif" + str(vPointsDif) + "Stage" + gameStage, 1))
    return features

def monishaFeatureExtractor(state, otherPlayerStates=[]):
    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
    features = []
    vPoints = cardUtils.computeVictoryPoints(deck)
    maxOtherPlayerVPoints = 0
    for state in otherPlayerStates:
        playerVPoints = cardUtils.computeVPointsFromState(state)
        if playerVPoints > maxOtherPlayerVPoints:
            maxOtherPlayerVPoints = playerVPoints
    vPointsDif = vPoints - maxOtherPlayerVPoints
    #NUMBER OF EACH CARD AND TURN
    for cardID in deck:
        features.append(("numOfCardsInDeckOfType" + str(cardID) + "=" + str(deck[cardID]) + "turndiv3:" + str(turn / 3), 1))
    #DECK VALUE AND TURN
    deckValue = cardUtils.computeDeckValue(deck)
    goldConcentration = (deck[2] * 3) / (deckValue + 0.0)
    features.append(("goldConcentration:" + str(goldConcentration) + "turndiv3:" + str(turn / 3), 1))
    #NUM PROVINCES AND TURN
    numProvinces = cardUtils.getNumProvinceCards(kingdom)
    features.append(("vPointsDif" + str(vPointsDif) + "provinces:" + str(numProvinces), 3))
    return features

def testFeatureExtractor(state, otherPlayerStates=[]):
    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
    features = []
    vPoints = cardUtils.computeVictoryPoints(deck)
    maxOtherPlayerVPoints = 0
    for state in otherPlayerStates:
        playerVPoints = cardUtils.computeVPointsFromState(state)
        if playerVPoints > maxOtherPlayerVPoints:
            maxOtherPlayerVPoints = playerVPoints
    vPointsDif = vPoints - maxOtherPlayerVPoints
    #NUMBER OF EACH CARD AND TURN
    for cardID in deck:
        features.append(("numOfCardsInDeckOfType" + str(cardID) + "=" + str(deck[cardID]) + "turndiv3:" + str(turn / 3), 1))
    #DECK VALUE AND TURN
    deckValue = cardUtils.computeDeckValue(deck)
    goldConcentration = (deck[2] * 3) / (deckValue + 0.0)
    features.append(("goldConcentration:" + str(round(goldConcentration,1)) + "turndiv3:" + str(turn / 3), 1))
    #NUM PROVINCES AND TURN
    numProvinces = cardUtils.getNumProvinceCards(kingdom)
    features.append(("vPointsDif" + str(vPointsDif) + "provinces:" + str(numProvinces), 3))

    return features
    
    
def tdDominionFeatureExtractor(state):
    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
    features = []
    handValue = cardUtils.computeHandValue(hand)
    #features.append(("handValue" + str(handValue), 1))
    
    #VICTORY POINTS AND TURN
    vPoints = cardUtils.computeVictoryPoints(deck)
    #NUMBER OF EACH CARD AND TURN
    for cardID in deck:
       features.append(("numOfCardsInDeckOfType" + str(cardID) + "=" + str(deck[cardID]) + "turndiv3:" + str(turn / 3), 1))
    
    #DECK VALUE AND TURN
    deckValue = cardUtils.computeDeckValue(deck)
    features.append(("deckValue:" + str(deckValue) + "turn:" + str(turn), 1))


    #NUM PROVINCES AND TURN
    numProvinces = cardUtils.getNumProvinceCards(kingdom)
    features.append(("provinces:" + str(numProvinces) + "turn:" + str(turn), 1))

    return features
    
def qDominionFeatureExtractor(state, action):
    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
    features = []
    features.append(("action:" + str(action), turn))
    
    #FEATURES: how many cards of each type in your hand, action
    handCounts = Counter()
    for cardID in hand:
        handCounts[cardID] += 1
    for cardID in handCounts:
        featureKey = "numInHandOf" + str(cardID) + "=" + str(handCounts[cardID]) + "action:" + str(action)
    return features
 