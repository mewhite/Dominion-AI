from card import Card
from collections import Counter

#Initializes the cards list from the given filename (cards.txt)
cardList = []
def initializeCardList(filename, verbose=False):
	cardsFile = open(filename, 'r')
	for line in cardsFile:
		if line == "" or line[0] == "#":
			pass
		else: 
			words = line.split()
			cardID = int(words[0])
			cardName = words[1]
			cardType = words[2].split(",")
			cardCost = int(words[3])
			treasureValue = int(words[4])
			victoryPoints = int(words[5])
			effects = parseEffects(words[6])
			cardList.append(Card(cardID, cardName, cardType, cardCost, treasureValue, victoryPoints, effects))
	if verbose:
		for card1 in cardList:
			print card1
	return cardList

def getCardFromID(id):
	return cardList[id]
	
#Effects is a dict of (+cards, +actions, +buys, +money)
def parseEffects(effectsString):
    effectsDict = Counter()
    effectsString = effectsString[1:-1]
    effectsList = effectsString.split(",")
    if len(effectsList) == 4:
        effectsDict["cards"] = int(effectsList[0])
        effectsDict["actions"] = int(effectsList[1])
        effectsDict["buys"] = int(effectsList[2])
        effectsDict["money"] = int(effectsList[3])
    return effectsDict

def computeVictoryPoints(deck):
    victoryPoints = 0
    for cardID in deck:
        card = getCardFromID(cardID)
        if "victory" in card.cardType:
            victoryPoints += card.victoryPoints * deck[cardID]
    return victoryPoints

def computeVPointsFromState(state):
    kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
    return computeVictoryPoints(deck)

def computeHandValue(hand):
    handValue = 0
    for cardID in hand:
        card = getCardFromID(cardID)
        if "treasure" in card.cardType:
            handValue += card.treasureValue
    return handValue

def computeDeckValue(deck):
    deckValue = 0
    for cardID in deck:
        card = getCardFromID(cardID)
        if "treasure" in card.cardType:
            deckValue += card.treasureValue * deck[cardID]
    return deckValue

def getNumProvinceCards(kingdom):
	return kingdom[5]

def getCardNameFromID(cardID):
    if cardID == -1:
        return "None"
    else:
        return cardList[cardID].cardName

def getCardEffectsFromCardID(cardID):
    if cardID == -1:
        return {}
    else:
        return cardList[cardID].effects
    
def getCardCostFromID(cardID):
    if cardID == -1:
        return 0
    else:
        return cardList[cardID].cardCost

def printDeck(deck):
    for cardID in deck:
        cardName = getCardFromID(cardID).cardName
        print deck[cardID], cardName,
    print

def printHand(hand):
    for cardID in hand:
        cardName = getCardFromID(cardID).cardName
        print cardName,
    print

def printCardEffects(cardID):
    if cardID == -1:
        print
    else: 
        card = getCardFromID(cardID)
        if "action" in card.cardType:
            print "[",
            cardEffects = card.effects
            for effect, number in cardEffects.iteritems():
                if number > 0:
                    print "+%d %s" % (number, effect),
            print "]",
        if "treasure" in card.cardType:
            print "[", card.treasureValue, "treasure ]",
        if "victory" in card.cardType:
            print "[", card.victoryPoints, "victory points ]",
        print