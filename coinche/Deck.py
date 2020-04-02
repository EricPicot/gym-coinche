import random as rand

from coinche.Card import Card

numSuits = 4
minRank = 7
maxRank = 15

class Deck:
    def __init__(self):
        self.deck = []
        for suit in range(0, numSuits):
            for rank in range(minRank, maxRank):
                self.deck.append(Card(rank, suit))

    def __str__(self):
        deckStr = ''
        for card in self.deck:
            deckStr += card.__str__() + '\n'
        return deckStr

    def shuffle(self):
        rand.shuffle(self.deck, rand.random)

    def deal(self, numberOfCardsToDeal):
        cards = []
        for i in range(numberOfCardsToDeal):
            cards += [self.deck.pop(0)]
        return cards

    def sort(self):
        self.deck.sort()

    def size(self):
        return len(self.deck)

    def addCards(self, cards):
        self.deck += cards
        
    def addTrick(self, trick):
        for card in trick:
            self.deck.addCards(card)
            
    def joinTeamsSubDecks(self, teamA, teamB):
        self.deck = teamA.cardsInRound + teamB.cardsInRound
    
    def joinTeamsHands(self, teamA, teamB):
        self.deck = teamA.cardsInHand + teamB.cardsInHand
        
    def cut_deck(self):
        '''Randomly cuts the deck'''
        cut = rand.randint(2, len(self.deck)-3)
        self.deck = self.deck[-cut:] + self.deck[0:len(self.deck) - cut]
