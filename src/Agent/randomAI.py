import random
from datetime import datetime
max_value = 11


class RandomAI:
    def __init__(self, name, params = None):
        random.seed(datetime.now())
        self.name = name

        if params != None:
            self.print_info = params['print_info']
        else:
            self.print_info = False

    def do_action(self, observation):
        if observation['event_name'] == 'GameStart':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'NewRound':
            if self.print_info:
                print(observation)
                
        elif observation['event_name'] == 'ChooseContrat':
            print(observation)
            former_value = observation["data"]["contrat"]
            contrat_dict = {"suit": int(observation["data"]["suit"]),
                            "value":  int(observation["data"]["contrat"]),
                            "newContrat": False}
            print('current contrat: ', contrat_dict)
#           Choose if RandomAI makes a call:
            make_a_call = random.uniform(0, 1) >= 0.75

            # If no bet or upper limit of bid already reached
            if not make_a_call or former_value == max_value*10:
                suit = ""
                contrat = ""
            else:
                suit = random.randint(0, 3)
                contrat = random.randint(8, max_value)*10
                # you must return "newContrat=True" if you change the value of the contrat
                contrat_dict["newContrat"] = True
                contrat_dict["suit"] = int(suit)
                contrat_dict["value"] = int(contrat)

                print('New contrat: ', contrat_dict)
            return {
                    "event_name": "ChooseContratAction",
                    "data": {
                        'playerName': self.name,
                        'action': contrat_dict
                    }
                }

        elif observation['event_name'] == 'ChooseContrat':
            print(observation)
            contrat_dict = {"suit": None,
                            "value": None}
            for i, key in enumerate(contrat_dict):
                contrat_dict[key] = input('{0}: '.format(key))

            print('contrat: ', contrat_dict)
            return {
                    "event_name": "ChooseContrat_Action",
                    "data": {
                        'playerName': self.name,
                        'action': {'ChooseContrat': contrat_dict}
                    }
                }

        elif observation['event_name'] == 'PassCards':
            if self.print_info:
                print(observation)

            pass_cards = random.sample(observation['data']['hand'], 3)

            if self.print_info:
                print(self.name, ' pass cards: ', pass_cards)

            return {
                    "event_name" : "PassCards_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'passCards': pass_cards}
                    }
                }

        elif observation['event_name'] == 'ShowPlayerHand':
            if self.print_info:
                print(observation)

        elif observation['event_name'] == 'PlayTrick':
            if self.print_info:
                print(observation)

            hand = observation['data']['hand']
            choose_card = random.choice(hand)
            if self.print_info:
                print(self.name, ' choose card: ', choose_card)

            return {
                    "event_name" : "PlayTrick_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'card': choose_card}
                    }
                }
        elif observation['event_name'] == 'ShowTrickAction':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'ShowTrickEnd':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'RoundEnd':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'GameOver':
            if self.print_info:
                print(observation)             
