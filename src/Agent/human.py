class Human:
    def __init__(self, name, params):
        self.name = name

    def Do_Action(self, observation):
        if observation['event_name'] == 'GameStart':
            print(observation)
        elif observation['event_name'] == 'NewRound':
            print(observation)
        elif observation['event_name'] == 'ChooseContrat':
            print(observation)
            contrat_dict = {"suit": observation["data"]["suit"],
                            "value":  observation["data"]["contrat"],
                            "newContrat": False}
            print('current contrat: ', contrat_dict)
            print("do you want to pass ? prompt 'yes' or 'no'")

            pass_bool = input()
            if pass_bool == 'no':
                contrat_dict["newContrat"]=True
                contrat_dict["suit"] = int(input('suit of the new contrat: '))
                contrat_dict["value"] = int(input('value of the new contrat: '))
                while contrat_dict["value"]%10!=0:
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
