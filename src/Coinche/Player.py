from .Hand import Hand

class Player:
    def __init__(self, name):
            self.name = name
            self.hand = Hand()
            self.score = 0
            self.tricksWon = []
            self.CardsInRound = []
            self.team = None

    def addCard(self, card):
        self.hand.addCard(card)

    def play(self, card):
        return self.hand.playCard(card)


    def trickWon(self, cards):
        self.CardsInRound += cards

    def hasAtout(self, atout):
        return len(self.hand.hand[atout.iden]) > 0
    
    def hasSuit(self, suit):
        return len(self.hand.hand[suit.iden]) > 0

    def removeCard(self, card):
        self.hand.removeCard(card)

    def discardTricks(self):
        self.tricksWon = []

    def resetRound(self):
        self.CardsInRound = []
        self.score = 0


    
class Team:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.name = self.player1.name + " " + self.player2.name
        self.score = 0
        self.globalScore = 0
        self.tricksWon = []
        self.CardsInRound = []
        

    def updateRoundScore(self):
        self.score = self.player1.score + self.player2.score
    
    def discardTricks(self):
        self.tricksWon = []

    def resetRoundCards(self):
        self.CardsInRound = []
        
    def teamScore(self):
        return None

        