import cardUtils


#Implementation of a dominion player that allows a human to play.
#Uses python's raw_input() method to read in the player's move
class HumanPlayer():
    def __init__(self, mdp):
        self.mdp = mdp
    
    def endOfGame(self, reward):
        pass
        
    def incorporateFeedback(self, state, action, reward, newState, otherPlayerStates=[]):
        pass

    def getAction(self, state, possibleActions, otherPlayerStates):
        kingdom, deck, hand, drawPile, discardPile, phase, turn, buys, numActions, money, cardsPlayed = state
        print "#####################################"
        print "Money:", money
        print "Buys:", buys
        print "Actions:", numActions
        print "Hand:",
        cardUtils.printHand(hand)
        print "Possible actions:"
        for i in range(len(possibleActions)):
            action = possibleActions[i]
            actionType, cardID = action
            print "%d:" % i, actionType, cardUtils.getCardNameFromID(cardID),
            if actionType == "buy":
                print "(cost %d)" % cardUtils.getCardCostFromID(cardID),
                if cardID != -1:
                    print "{%d left}" % kingdom[cardID],
                cardUtils.printCardEffects(cardID)
            else:
                cardUtils.printCardEffects(cardID)

        if len(possibleActions) == 1:
            action = possibleActions[0]
            actionType, cardID = action
            print "No choice to be made: ", actionType, cardUtils.getCardNameFromID(cardID)
            return action
        else:
            while True:
                try:
                    actionChoice = raw_input("Enter the number of your choice (q to quit): ")
                    if "q" in actionChoice:
                        exit()
                    action = possibleActions[int(actionChoice)]
                    return action
                except IndexError:
                    print "That is not a valid action. Try again."
                except ValueError:
                    print "That is not a valid action. Try again."
    
    def getPlayerName(self):
       return "Human Player"
 