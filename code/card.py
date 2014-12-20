#An implementation of a single Dominion card
class Card:
    def __init__(self, cardID, cardName, cardType, cardCost, treasureValue, victoryPoints, effects):
    	self.cardID = cardID
    	self.cardName = cardName
    	self.cardType = cardType
    	self.cardCost = cardCost
    	self.treasureValue = treasureValue
    	self.victoryPoints = victoryPoints
    	self.effects = effects
    def __repr__(self):
		return "ID: " + str(self.cardID) + " Name: " + self.cardName + " Type: " + str(self.cardType) + " Cost: " + str(self.cardCost) + " Value: " + str(self.treasureValue) + " Victory Points: " + str(self.victoryPoints) + " Effects: " + self.effects