import cardUtils, DominionPlayer, random


#A player that plays big money with a bit of randomness.  
#The rate of choosing a random action is determined by the explorationProb
class BadBigMoneyPlayer(DominionPlayer.DominionPlayer):
    def __init__(self, mdp, usingCachedWeights=False, cachingWeights=False, cacheStringKey="", explorationProb = 0.2):
        self.handSize = mdp.handSize
        self.maxTurns = mdp.maxTurns
        self.bigVPCard = max((cardUtils.getCardFromID(cardID).victoryPoints, cardUtils.getCardFromID(cardID)) for cardID in mdp.startKingdom)[1]
        self.usingCachedWeights = usingCachedWeights
        self.cachingWeights = cachingWeights
        self.cacheStringKey = cacheStringKey
        self.explorationProb = explorationProb
        
        return
    #Chooses a random action with likelihood explorationProb.  Otherwise...
    #Buys the biggest treasure card it can, unless it can buy the biggest victory point card
    def getAction(self, state, actions, otherPlayerStates = []):
        if random.random() < self.explorationProb:
            return random.choice(actions)
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        if phase == "buy":
            handValue = cardUtils.computeHandValue(hand)
            if handValue > self.bigVPCard.cardCost:
                return ("buy", self.bigVPCard.cardID)
            bestTreasureCard = None
            bestTreasureValue = float('-inf')
            for cardID in kingdom:
                card = cardUtils.getCardFromID(cardID)
                if "treasure" in card.cardType:
                    if card.cardCost <= handValue and card.treasureValue > bestTreasureValue:
                        bestTreasureCard = card
                        bestTreasureValue = card.treasureValue
            return ("buy", bestTreasureCard.cardID)
        if phase == "action":
            return ("play", -1)
            
    def incorporateFeedback(self, state, action, reward, newState, otherPlayerStates=[]):
        #Bad Big Money does not change strategy with feedback
        pass

    def endOfGame(self, reward):
        pass
    
    def getPlayerName(self):
        return "Bad Big Money Player"