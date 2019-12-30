import random
from datetime import datetime

class RandomAI:
    def __init__(self, name, params = None):
        random.seed(datetime.now())
        self.name = name

        if params != None:
            self.print_info = params['print_info']
        else:
            self.print_info = False

    def Do_Action(self, observation):
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
            makeACall = random.uniform(0,1) >=0.75
            if not makeACall or former_value==160:
                suit= ""
                contrat= ""
            else:
                suit = random.randint(0,3)
                contrat = random.randint(8,16)*10
            if suit != "":
                

            
                contrat_dict["newContrat"]=True
                contrat_dict["suit"] =int(suit)
                contrat_dict["value"] = int(contrat)
                while former_value >= contrat_dict["value"]:
                    contrat_dict["value"] = random.randint(former_value/10,16)*10

            return {
                    "event_name" : "ChooseContratAction",
                    "data" : {
                        'playerName': self.name,
                        'action': contrat_dict
                    }
                }
        
                
        elif observation['event_name'] == 'ChooseContrat':
            print(observation)
            contrat_dict = {"suit":None,
                       "value": None}
            for i, key in enumerate(contrat_dict):
                contrat_dict[key] = input('{0}: '.format(key
                                                        ))
                if key=="value":
                    while contrat_dict[key]%10!=0:
                        print("Must choose a multiple of 10")
                        contrat_dict[key] = input('{0}: '.format(key))

            print('contrat: ', contrat_dict)
            return {
                    "event_name" : "ChooseContrat_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'ChooseContrat': contrat_dict}
                    }
                }
        elif observation['event_name'] == 'PassCards':
            if self.print_info:
                print(observation)

            passCards = random.sample(observation['data']['hand'],3)

            if self.print_info:
                print(self.name, ' pass cards: ', passCards)

            return {
                    "event_name" : "PassCards_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'passCards': passCards}
                    }
                }

        elif observation['event_name'] == 'ShowPlayerHand':
            if self.print_info:
                print(observation)

        elif observation['event_name'] == 'PlayTrick':
            if self.print_info:
                print(observation)

            hand = observation['data']['hand']
            if '2c' in hand:
                choose_card = '2c'
            else:
                choose_card = random.choice(observation['data']['hand'])
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
