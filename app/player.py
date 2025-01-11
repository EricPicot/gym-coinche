class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def receive_cards(self, cards):
        self.hand.extend(cards)
        
    def reset_hand(self):
        self.hand = []

    def __repr__(self):
        return f"{self.name}: {self.hand}"