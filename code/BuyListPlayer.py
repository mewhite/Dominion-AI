import collections, util, math, random, copy, cardUtils
from DominionPlayer import DominionPlayer

# An implementation of Mathew Fisher's "Buy List" player
class BuyListPlayer(DominionPlayer):
    # Buy list player determines its strategy from the buyList along with a set of vpParemeters which determine when it buys various vp cards
    def __init__(self, mdp, buyList, actionPlayer, vpParemeters):
        self.mdp = mdp
        self.defaultBuyList = copy.copy(buyList)
        self.actionPlayer = actionPlayer
        self.buyList = buyList
        self.vpParemeters = vpParemeters
        self.usingCachedWeights = False
        self.cachingWeights = False
        
    def endOfGame(self, reward):
        self.buyList = copy.copy(self.defaultBuyList)
        pass
        
    def incorporateFeedback(self, state, action, reward, newState, otherPlayerStates=[]):
        pass

    def getActionPhaseAction(self, state, possibleActions, otherPlayerStates=[]):
        return self.actionPlayer.getAction(state, possibleActions, otherPlayerStates)

    def getBestCardToBuy(self, money, kingdom):
        #Deal with buying VP cards
        if money >= 8:
            return 5 #CardID of province
        if kingdom[5] <= self.vpParemeters[0]:
            if money >= 5:
                return 4
        if kingdom[5] <= self.vpParemeters[1]:
            if money >= 2:
                return 3

        for i in range(len(self.buyList)):
            cardID, numberToBuy = self.buyList[i]
            if numberToBuy > 0 and kingdom[cardID] > 0:
                cardCost = cardUtils.getCardFromID(cardID).cardCost
                if cardCost <= money:
                    self.buyList[i] = (cardID, numberToBuy - 1)
                    return cardID
        return -1

    def getAction(self, state, possibleActions, otherPlayerStates=[]):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        if phase == "buy":
            return ("buy", self.getBestCardToBuy(money,kingdom))
        if phase == "action":
            return self.getActionPhaseAction(state, possibleActions, otherPlayerStates)

    def getPlayerName(self):
        return "Buy List Player"
        
#Note: The best buy list created by Fisher's Provincial is below:
#    buyList = [(2,1),(15,8),(2,99),(11,4),(10,10),(11,2),(7,1),(1,99)]
#    vpParemeters = (3,1)