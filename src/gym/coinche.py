from coinche import Deck, Player, Trick, AIPlayer, RandomPlayer
from gym import Env


class GymCoinche(Env):
    def __init__(self):
        self.observation_space = space.Box()
        self.action_space = space.Box()

        self.players = [
            RandomPlayer("N"), RandomPlayer("E"), AIPlayer("S"), RandomPlayer("W")
        ]
        self.deck = Deck()
        self.trick = None
        self.color = None
        self.value = None

    def reset(self):
        # Select color and value
        self.color = None
        self.value = None

        self.deck.shuffle()
        # TODO: deal for players in Deck
        # [ [card, card, card, card], [], [], [] ]
        cards = self.deck.deal()
        # TODO: add rotate
        for p, c in zip(self.players, cards):
            p.addCards(c)

        self.trick = Trick()

        self.play_until_ai_player()

    def play_until_ai_player(self):
        for p in self.players:
            if isinstance(p, AIPlayer):
                break

            # add random card
            if isinstance(p, RandomPlayer):
                while True:
                    card = p.getRandom()
                    try:
                        self.trick.addCard(card)
                        break
                    except PlayException:
                        pass

            # add random card
            probabilities = []  # shape(32)
            ## filter probabilities based on AI hand
            hand_probabilities = []  # shape(max 8)
            while True:
                card = p.getRandom()
                try:
                    self.trick.addCard(card)
                    break
                except Exception:
                    pass
