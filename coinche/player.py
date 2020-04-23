from random import choice


class Player:
    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.cards = []
        self.score = 0
        self.team = None
        self.teammate = None
        self.attacker = None

    def add_cards(self, cards):
        self.cards += cards

    def has_card(self, card):
        return card in self.cards

    def has_suit(self, suit):
        for card in self.cards:
            if card.suit == suit:
                return True
        return False

    def get_suit_card(self, suit):
        suit_cards = []

        for card in self.cards:
            if card.suit == suit:
                suit_cards.append(card)
        return suit_cards

    def remove_card(self, card):
        self.cards.remove(card)

    def reset_round(self):
        self.score = 0

    def is_ai(self):
        return False


class RandomPlayer(Player):
    def get_random(self):
        return choice(self.cards)


class DeterministicPlayer(RandomPlayer):
    def play_turn(self, trick):
        # If player is the first to start
        if trick.cardsInTrick == 0:
            # If player is an attacker
            if self.attacker == 1:
                # Try to play Atout or play random card
                if self.has_suit(trick.atout_suit):
                    suit_cards = self.get_suit_card(trick.atout_suit)
                    return choice(suit_cards)
                else:
                    return self.get_random()
        return self.get_random()


class AIPlayer(Player):
    def is_ai(self):
        return True
