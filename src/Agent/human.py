class Human:
    def __init__(self, name, params):
        self.name = name

    def do_action(self, observation):
        if observation['event_name'] == 'GameStart':
            print(observation)
        elif observation['event_name'] == 'NewRound':
            print(observation)
        elif observation['event_name'] == 'ChooseContrat':
            print(observation)
            former_value = observation["data"]["contrat"]
            contrat_dict = {"suit": int(observation["data"]["suit"]),
                            "value":  int(observation["data"]["contrat"]),
                            "newContrat": False}
            print('current contrat: ', contrat_dict)

            suit = input('suit of the new contrat: ')
            contrat = input('value of the new contrat: ')
            if suit != "":
                
                contrat_dict["newContrat"]=True
                contrat_dict["suit"] = int(suit)
                contrat_dict["value"] = int(contrat)
                while former_value >= contrat_dict["value"]:
                    print("you must increase the value of the proposed contrat")
                    contrat_dict["value"] = input('value of the new contrat: ')

                while contrat_dict["value"]%10 != 0:
                    print("Must choose a multiple of 10")
                    contrat_dict["value"] = input('value of the new contrat: ')
            print(contrat_dict)
            return {
                    "event_name" : "ChooseContratAction",
                    "data" : {
                        'playerName': self.name,
                        'action': contrat_dict
                    }
                }

        elif observation['event_name'] == 'ShowPlayerHand':
            print(observation)

        elif observation['event_name'] == 'PlayTrick':
            print(observation)
            hand = observation['data']['hand']
#             if '2c' in hand:
#                 choose_card = '2c'
#             else:
            choose_card = input('choose card: ')
            playtrick_action = {
                    "event_name" : "PlayTrick_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'card': choose_card}
                    }
                }
            print("playtrick_action: ", playtrick_action)
            return playtrick_action

        elif observation['event_name'] == 'ShowTrickAction':
            print(observation)
        elif observation['event_name'] == 'ShowTrickEnd':
            print(observation)
        elif observation['event_name'] == 'RoundEnd':
            print(observation)
        elif observation['event_name'] == 'GameOver':
            print(observation)             
