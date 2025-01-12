class Player:
    def __init__(self, name, is_llm=False):
        self.name = name
        self.hand = []
        self.is_llm = is_llm

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def reset_hand(self):
        self.hand = []

    def make_annonce(self, current_contract_value, current_contract_holder):
        # Placeholder for making an annonce
        pass
    
    def organize_hand(self):
        self.hand.sort(key=lambda card: (card.suit, card.value))