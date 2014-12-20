import cardUtils, util, copy
from collections import Counter

#An implementation of the card game Dominion as a Markov Decision Process (MDP)
class DominionMDP:
    def __init__(self, maxTurns=5, startKingdom=Counter({0:100, 1:100, 2:100, 3:8, 4:8, 5:1}), startHand=(0,0,0,3,3), startDeck=Counter({0:7, 3:3})):
        # kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        # kingdom: possible cards in stock to buy (by ID)
        # NOTE: kingdom is now part of the state, not a constant for the MDP
        self.startKingdom = startKingdom
        self.handSize = 5
        self.maxTurns = maxTurns
        self.startHand = startHand
        self.startDeck = startDeck
        return

    def startState(self):
        #starting deck by ID, number of cards in that ID
        kingdom = self.startKingdom
        deck = self.startDeck
        hand = self.startHand
        drawPile = Counter(deck)
        for cardID in hand:
            drawPile[cardID] -= 1
        discardPile = Counter()
        phase = "action"
        turn = 0
        buys = 1
        actions = 1
        money = 0
        cardsPlayed = Counter()
        return (util.HashableDict(kingdom), util.HashableDict(deck), hand, util.HashableDict(drawPile), util.HashableDict(discardPile), phase, turn, buys, actions, money, util.HashableDict(cardsPlayed))

    def endOfGame(self, state):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        #Three pile ending
        emptyPiles = 0
        for cardID, quantity in kingdom.iteritems():
            if quantity == 0:
                emptyPiles += 1
        return cardUtils.getNumProvinceCards(kingdom) == 0 or emptyPiles >= 3 or turn >= self.maxTurns 
        
    # Return set of actions possible from |state|. Actions is a list of ("buy cardName") strings.
    def actions(self, state):
        results = []
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        if self.endOfGame(state):
            #Note: Most simulations should never get here. 
            #Returns an "idle" move if the game is over, so that getQ for qLearning doesn't break.
            return ["idle"]
            
        if phase == "buy":
            results.append(("buy", -1))
            handValue = cardUtils.computeHandValue(hand)
            for cardID in kingdom:
                if kingdom[cardID] > 0:
                    buyCard = cardUtils.getCardFromID(cardID)
                    if buyCard.cardCost <= money:
                        results.append(("buy", buyCard.cardID))
        
        if phase == "action":
            results.append(("play", -1))
            for cardID in set(hand):
                card = cardUtils.getCardFromID(cardID)
                if "action" in card.cardType:
                    results.append(("play", card.cardID))
                    
        return results

    def computeReward(self, state, otherPlayerStates=[]):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        myVPoints = cardUtils.computeVictoryPoints(deck)
        if self.endOfGame(state):
            maxVPoints = 0
            for otherPlayerState in otherPlayerStates:
                kingdom1, deck1, hand1, drawPile1, discardPile1, phase1, turn1, buys1, actions1, money1, cardsPlayed1 = otherPlayerState
                otherPlayerVPoints = cardUtils.computeVictoryPoints(deck1)
                if otherPlayerVPoints > maxVPoints:
                    maxVPoints = otherPlayerVPoints
            if len(otherPlayerStates) > 0:
                #MULTIPLAYER GAME, MOST VPOINTS WINS
                if maxVPoints > myVPoints:
                    return -100
                elif myVPoints > maxVPoints:
                    return 100
                else:
                    return 0
            else:
                #single player game
                if turn == self.maxTurns:
                    return -1
                    #reward is -1 if we go over the number of turns
                return 100 - 1 * turn
                    #the fewer turns, the higher the reward
        else:
            return 0

    # Return a list of (newState, prob) tuples corresponding to edges
    # coming out of |state|.
    #NOTE: succAndProbs assumes that it will not be called on an end state. (Thus is doesn't 
    #   deal with action type "idle".
    def succAndProbs(self, state, action, otherPlayerStates=[]):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, actions, money, cardsPlayed = state
        nextDeck = Counter(deck)
        nextDiscardPile = Counter(discardPile)
        nextKingdom = Counter(kingdom)
        nextPhase = phase
        nextBuys = buys
        nextActions = actions
        nextMoney = money
        actionType, cardID = action
        results = []
        newDrawPile = Counter(drawPile)
        nextCardsPlayed = Counter(cardsPlayed)
        if actionType == "play":
            #Not playing a card (i.e. Playing "None")
            if cardID == -1:
                nextMoney += cardUtils.computeHandValue(hand)
                nextPhase = "buy"
                newState = (util.HashableDict(nextKingdom), util.HashableDict(nextDeck), tuple(hand), util.HashableDict(newDrawPile), util.HashableDict(nextDiscardPile), nextPhase, turn, nextBuys, nextActions, nextMoney, util.HashableDict(nextCardsPlayed))
                prob = 1
                results.append((newState, prob))
            else:
                nextHand = list(hand)
                #Remove card from hand
                nextHand.remove(cardID)
                #Discard the card
                nextCardsPlayed[cardID] += 1
                #Play the card (Deal with the effects)
                nextActions -= 1
                cardEffects = cardUtils.getCardFromID(cardID).effects
                nextBuys += cardEffects["buys"]
                nextActions += cardEffects["actions"]
                nextMoney += cardEffects["money"]
                #Draw cards
                numCardsToDraw = cardEffects["cards"]
                if numCardsToDraw == 0:
                    if nextActions == 0:
                        nextMoney += cardUtils.computeHandValue(nextHand)
                        nextPhase = "buy"
                    newState = (util.HashableDict(nextKingdom), util.HashableDict(nextDeck), tuple(nextHand), util.HashableDict(newDrawPile), util.HashableDict(nextDiscardPile), nextPhase, turn, nextBuys, nextActions, nextMoney, util.HashableDict(nextCardsPlayed))
                    prob = 1
                    results.append((newState, prob))
                else:
                    newHand = list(nextHand)
                    if sum(newDrawPile.values()) + sum(nextDiscardPile.values()) < numCardsToDraw:

                        #Draw the rest of the deck 
                        for cardID in newDrawPile.keys():
                            for i in range(newDrawPile[cardID]):
                                newHand.append(cardID)
                                newDrawPile[cardID] -= 1
                                numCardsToDraw -= 1
                        #Draw the rest of the discard pile
                        for cardID in nextDiscardPile.keys():
                            for i in range(nextDiscardPile[cardID]):
                                newHand.append(cardID)
                                nextDiscardPile[cardID] -= 1
                                numCardsToDraw -= 1
                        nextHand = newHand
                        nextHand.sort()
                        nextDrawPile = Counter(newDrawPile)
                        if nextActions == 0:
                            nextMoney += cardUtils.computeHandValue(nextHand)
                            nextPhase = "buy"
                        newState = (util.HashableDict(nextKingdom), util.HashableDict(nextDeck), tuple(nextHand), util.HashableDict(nextDrawPile), util.HashableDict(nextDiscardPile), nextPhase, turn, nextBuys, nextActions, nextMoney, util.HashableDict(nextCardsPlayed))
                        prob = 1
                        results.append((newState, prob))
                    else:
                        if sum(newDrawPile.values()) < numCardsToDraw:
                            #Draw the rest of the deck 
                            for cardID in newDrawPile.keys():
                                for i in range(newDrawPile[cardID]):
                                    newHand.append(cardID)
                                    newDrawPile[cardID] -= 1
                                    numCardsToDraw -= 1
                            #Reshuffle
                            newDrawPile = nextDiscardPile
                            nextDiscardPile = Counter()
                        numHands = util.nchoosek(sum(newDrawPile.values()), numCardsToDraw)
                        handsAndProbs = []
                        computeHandsAndProbs(kingdom, [], numHands, handsAndProbs, Counter(newDrawPile), 0, numCardsToDraw)
                        results = []
                        tempMoney = nextMoney
                        for handAddition, prob in handsAndProbs:
                            nextMoney = tempMoney
                            nextHand = newHand + handAddition
                            nextHand.sort()
                            nextDrawPile = Counter(newDrawPile)
                            for cardID in handAddition:
                                nextDrawPile[cardID] -= 1
                            if nextActions == 0:
                                nextMoney += cardUtils.computeHandValue(nextHand)
                                nextPhase = "buy"
                            newState = (util.HashableDict(nextKingdom), util.HashableDict(nextDeck), tuple(nextHand), util.HashableDict(nextDrawPile), util.HashableDict(nextDiscardPile), nextPhase, turn, nextBuys, nextActions, nextMoney, util.HashableDict(nextCardsPlayed))
                            results.append((newState, prob))
                #
        if actionType == "buy":
            if cardID != -1:
                #Buy the card
                nextDeck[cardID] += 1
                nextDiscardPile[cardID] += 1
                nextKingdom[cardID] -= 1
                nextBuys -= 1
                nextMoney -= cardUtils.getCardFromID(cardID).cardCost
            #Start a new turn if we choose to buy nothing or only have one card to buy
            if buys == 1 or cardID == -1:
                #Discard the action cards we played
                nextDiscardPile += nextCardsPlayed
                nextCardsPlayed = Counter()
                turn += 1
                nextBuys = 1
                nextMoney = 0
                nextActions = 1
                nextPhase = "action"
                #Discard your hand
                for cardID in hand:
                    nextDiscardPile[cardID] += 1
                #Compute new hands and probabilities
                newHand = []
                handSize = self.handSize
                newDrawPile = Counter(drawPile)
                if sum(newDrawPile.values()) < self.handSize:
                    #Reshuffle. 
                    for cardID in newDrawPile.keys():
                        for i in range(newDrawPile[cardID]):
                            newHand.append(cardID)
                            newDrawPile[cardID] -= 1
                            handSize -= 1
                    newDrawPile = nextDiscardPile
                    nextDiscardPile = Counter()
                numHands = util.nchoosek(sum(newDrawPile.values()), handSize)
                handsAndProbs = []
                computeHandsAndProbs(kingdom, [], numHands, handsAndProbs, Counter(newDrawPile), 0, handSize)
                results = []
                for handAddition, prob in handsAndProbs:
                    nextHand = newHand + handAddition
                    nextHand.sort()
                    nextDrawPile = Counter(newDrawPile)
                    for cardID in handAddition:
                        nextDrawPile[cardID] -= 1
                    newState = (util.HashableDict(nextKingdom), util.HashableDict(nextDeck), tuple(nextHand), util.HashableDict(nextDrawPile), util.HashableDict(nextDiscardPile), nextPhase, turn, nextBuys, nextActions, nextMoney, util.HashableDict(nextCardsPlayed))
                    results.append((newState, prob))
            else:
                newState = (util.HashableDict(nextKingdom), util.HashableDict(nextDeck), tuple(hand), util.HashableDict(newDrawPile), util.HashableDict(nextDiscardPile), nextPhase, turn, nextBuys, nextActions, nextMoney, util.HashableDict(nextCardsPlayed))
                prob = 1
                results.append((newState, prob))
        return results
        # END_YOUR_CODE

    def computeStates(self, otherPlayerStates=[]):
        self.states = []
        queue = []
        self.states.append(self.startState())
        queue.append(self.startState())
        while len(queue) > 0:
            state = queue.pop()
            for action in self.actions(state):
                #NOTE: we only compute succAndProbs if it is NOT the end of the game
                if action != "idle":
                    for newState, prob in self.succAndProbs(state, action, otherPlayerStates):
                        self.states.append(newState)
                        queue.append(newState)
     
     
def computeHandsAndProbs(kingdom, hand, numHands, results, drawPile, drawIndex, handSize):
    if drawIndex > max(kingdom.keys()):
        return
    if len(hand) == handSize:
        prob = computeHandProbability(hand, drawPile, numHands)
        results.append((list(hand), prob))
        #print results
        return
    #print "drawPile: ",drawPile,"drawIndex: ",drawIndex   
    if drawPile[drawIndex] > 0:
        hand.append(drawIndex)
        drawPile[drawIndex] -= 1
        computeHandsAndProbs(kingdom, hand, numHands, results, drawPile, drawIndex, handSize)
        drawPile[drawIndex] += 1
        hand.pop()
    computeHandsAndProbs(kingdom, hand, numHands, results, drawPile, drawIndex + 1, handSize)

def computeHandProbability(hand, drawPile, numHands):
    prob = 1
    handCounter = util.HashableDict(Counter(hand))
    for cardID in handCounter.keys():
        prob *= util.nchoosek(drawPile[cardID] + handCounter[cardID], handCounter[cardID])
    prob /= (0.0 + numHands)
    return prob