from random import randint, choice
from coinche.Card import Suit


clubs = 0
diamonds = 1
spades = 2
hearts = 3
suits = ["c", "d", "s", "h"]


class Hand:
    def __init__(self):

        self.clubs = []
        self.diamonds = []
        self.spades = []
        self.hearts = []
        
        # create hand of cards split up by suit
        self.hand = [self.clubs, self.diamonds,
                     self.spades, self.hearts]

    def size(self):
        return len(self.clubs) + len(self.diamonds) + len(self.spades) + len(self.hearts)

    def hasCard(self, card):
        return self.containsCard(card.rank.rank, card.suit.iden)

    def hasHigherCard(self, suit, suit_rank, current_highest_card):
        suit_cards = self.hand[suit.iden]
        rank = 0
        for card in suit_cards:
            if suit_rank[card.rank.rank] > rank:
                rank = suit_rank[card.rank.rank]
        return rank > current_highest_card

    def hasAtout(self, atout):
        return len(self.hand[atout.iden]) > 0

    def hasSuit(self, suit):
        return len(self.hand[suit.iden]) > 0

    def addCards(self, cardsToAdd):
        for card in cardsToAdd:
            if card.suit == Suit(clubs):
                self.clubs.append(card)
            elif card.suit == Suit(diamonds):
                self.diamonds.append(card)
            elif card.suit == Suit(spades):
                self.spades.append(card)
            elif card.suit == Suit(hearts):
                self.hearts.append(card)
            else:
                print ('Invalid card')

        if self.size() == 8:
                for suit in self.hand:
                    suit.sort()

    def updateHand(self):
        self.hand = [self.clubs, self.diamonds, self.spades, self.hearts]

    def getRandomCard(self):
        return choice(self.all_cards())


    @classmethod
    def strToCard(self, card):
        if len(card) == 0: return None
        
        suit = card[len(card)-1].lower() # get the suit from the string
        
        try:
            suitIden = suits.index(suit)
        except Exception as e:
            print ('Invalid suit')
            print(e)
            return None

        cardRank = card[0:len(card)-1] # get rank from string
        
        try:
            cardRank = cardRank.upper()
        except AttributeError:
            pass

        # convert rank to int
        if cardRank == "T":
            cardRank = 10
        elif cardRank == "J":
            cardRank = 11
        elif cardRank == "Q":
            cardRank = 12
        elif cardRank == "K":
            cardRank = 13
        elif cardRank == "A":
            cardRank = 14
        else:
            try:
                cardRank = int(cardRank)
            except Exception as e:
                print ("Invalid card rank.")
                print(e)
                return None

        return cardRank, suitIden

    def containsCard(self, cardRank, suitIden):
        for card in self.hand[suitIden]:
            if card.rank.rank == cardRank:
                cardToPlay = card

                return cardToPlay
        return None

    def playCard(self, card):
        cardInfo = self.strToCard(card)

        if cardInfo is None:
            return None
        else:
            cardRank, suitIden = cardInfo[0], cardInfo[1]

        # see if player has that card in hand
        return self.containsCard(cardRank, suitIden)

    def removeCard(self, card):
        suitId = card.suit.iden
        initLen = self.size()
        for c in self.hand[suitId]:
            if c == card:

                self.hand[card.suit.iden].remove(c)
                self.updateHand()

        finalLen = self.size()
        # TODO: remove
        assert finalLen == initLen - 1


    def all_cards(self):
        return [card for suit in self.hand for card in suit]


    def __str__(self):
        handStr = ''
        for suit in self.hand:
            for card in suit:
                handStr += card.__str__() + ' '
        return handStr


