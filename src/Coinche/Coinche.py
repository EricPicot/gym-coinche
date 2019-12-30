from .Deck import Deck
from .Card import Card, Suit, Rank
from .Player import Player, Team
from .Trick import Trick
from.CardsOrder import *
import random
from gym import Env

'''Change auto to False if you would like to play the game manually.'''
'''This allows you to make all passes, and plays for all four players.'''
'''When auto is True, passing is disabled and the computer plays the'''
'''game by "guess and check", randomly trying moves until it finds a'''
'''valid one.'''



class CoincheEnv(Env):

    def __init__(self, playersName, maxScore=100):
        
        self.maxScore = maxScore
        
        self.roundNum = 0
        self.trickNum = 0  # initialization value such that first round is round 0
        self.dealer = -1  # so that first dealer is 0
        self.passes = [1, -1, 2, 0]  # left, right, across, no pass
        self.currentTrick = Trick()
        self.trickWinner = -1

        # Make four players
        self.players = [Player(playersName[0]),
                        Player(playersName[1]),
                        Player(playersName[2]),
                        Player(playersName[3])]
        
        # Make two teams
        self.teams = [Team(0,self.players[0], self.players[2]),
                      Team(1,self.players[1], self.players[3])]
        
        # Linking players to a team
        self.players[0].team = self.teams[0]
        self.players[2].team = self.teams[0]
        self.players[1].team = self.teams[1]
        self.players[3].team = self.teams[1]
        
        # Linking players to their teammate
        self.players[0].teammate = self.players[2]
        self.players[2].teammate = self.players[0]
        self.players[1].teammate = self.players[3]
        self.players[3].teammate = self.players[1]
        
        

        '''
        Player physical locations:
        Game runs clockwise

            p3
        p2        p4
            p1

        '''
        
        self.event = None
        self.round = 0
        
        self.renderInfo = {'printFlag': False, 'Msg': ""}
        
    def _countTrickValue(self):
        """ 
        This function computes the value of the trick given if the cards are atout cards or not
        ex:
        if atout_suit is heart and the trick is [Ad, Td, 9h, 7d]:
        --> the trickValue is 11(Ad) + 10(Td) + 14(9h) + 0(7d) = 35 for player "Sud"
        """
        trickValue = 0
        for card in self.currentTrick.trick:

            if card !=Card(0,-1):
                if card.suit.iden == self.atout_suit:
                    trickValue += atout_values[card.rank.rank]
                else:

                    trickValue += generic_values[card.rank.rank]
        return trickValue
                
    
    @classmethod
    def _handsToStrList(self, hands):
        """
        This function helps to print a hand of a player
        """
        output = []
        for card in hands:
            output += [str(card)]
        return output

    def _getFirstTrickStarter(self):
        for i, p in enumerate(self.players):
            if p.hand.contains2ofclubs:
                self.trickWinner = i

    def _dealCards(self):
        """
        This function deals the deck
        TODO: deal card the coinche way !!!
        """
        i = 0
        while(self.deck.size() > 0):
            self.players[i % len(self.players)].addCard(self.deck.deal())
            i += 1

    def _evaluateTrick(self):
        self.trickWinner = self.currentTrick.winner
        p = self.players[self.trickWinner]
        p.trickWon(self.currentTrick.trick)



    # print player's hand
    def _printPlayer(self, i):
        p = self.players[i]
        print (p.name + "'s hand: " + str(p.hand))

    # print all players' hands
    def _printPlayers(self):
        for p in self.players:
            print (p.name + ": " + str(p.hand))

    # show cards played in current trick
    def _printCurrentTrick(self):
        trickStr = '\nCurrent table:\n'
        trickStr += "Atout suit of the round: " + Suit(self.atout_suit).__str__() + "\n"
        trickStr += "Trick suit: " + self.currentTrick.suit.__str__() + "\n"
        for i, card in enumerate(self.currentTrick.trick):
            if self.currentTrick.trick[i] is not 0:
                trickStr += self.players[i].name + ": " + str(card) + "\n"
            else:
                trickStr += self.players[i].name + ": None\n"
        
        return trickStr

    
    def _getCurrentTrickStrList(self):
        trick_list = []
        for i, card in enumerate(self.currentTrick.trick):
            if self.currentTrick.trick[i] is not 0:
                trick_list += [{'playerName': self.players[i].name, 'card': str(card) }]
        
        return trick_list
        
    
    def _event_GameStart(self):
        self.event_data_for_server = {}
        self.event_data_for_client \
        = {'event_name': self.event
           , 'broadcast': True
           , 'data': {
               "players" : [
                   {'playerName': self.players[0].name},
                   {'playerName': self.players[1].name},
                   {'playerName': self.players[2].name},
                   {'playerName': self.players[3].name}
                   ]
               }
           }
        
        for p in self.players:
            p.score = 0
        self.round = 0
    
        self.renderInfo = {'printFlag': False, 'Msg': ""}
        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = '\n*** Hearts Start ***\n'
    
    def _event_NewRound(self):

        self.deck = Deck()
        self.deck.shuffle()
        self.roundNum += 1
        self.trickNum = 0
        self.trickWinner = -1
        self.dealer = (self.dealer + 1) % len(self.players)
        self._dealCards()
        self.currentTrick = Trick()
        self.round += 1
        self.atout_suit = -1
        self.contrat = 0
        self.leadingTeam = None
        for p in self.players:
            p.resetRound()
            p.discardTricks()

        for t in self.teams:
            t.score = 0
            
        self.event_data_for_client \
        = {'event_name': self.event
           , 'broadcast': True
           , 'data': {
               "Teams" : [
                   {'teamName': self.teams[0].name,
                    'score': self.teams[0].score},
                   {'teamName': self.teams[1].name,
                    'score': self.teams[1].score},
                   ]
               }
           }
        
        self.event = 'ShowPlayerHand'
        self.event_data_for_server = {'now_player_index': 0}
        

        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = '\n*** Start Round {0} ***\n'.format(self.round)
        for p in self.players:
            self.renderInfo['Msg'] += '{0}: {1}\n'.format(p.name, p.score)
            self.renderInfo['Msg'] += 'Leading team: {0}\n'.format(self.leadingTeam)

    
    def _event_ShowPlayerHand(self):

        if self.event_data_for_server['now_player_index'] < 4:
            now_player_index = self.event_data_for_server['now_player_index']
            self.event_data_for_client \
            =   {"event_name" : self.event,
                 "broadcast" : False,
                 "data" : {
                     'playerName': self.players[now_player_index].name,
                     'hand': self._handsToStrList(sum(self.players[now_player_index].hand.hand, []))
                    }
                }
            self.event_data_for_server['now_player_index'] += 1
        
        else:
            self.event = 'ChooseContrat'
            self.event_data_for_server = {'shift': 0}
            self.numTurnOfAnnounce= 0
            

    def _event_ChooseContrat(self):
        shift = self.event_data_for_server['shift']
        
        if shift == 0 and self.numTurnOfAnnounce==0:
            self.playerToStartAnnounce = (self.dealer + 1)%4
            self.current_player = self.players[self.playerToStartAnnounce]
        else:
            self.current_player_i = (self.playerToStartAnnounce+shift)%4
            self.current_player = self.players[self.current_player_i]


        self.event_data_for_client \
            =   {"event_name" : self.event,
                 "broadcast" : False,
                 "data" : {
                     'playerName': self.current_player.name,
                     'hand': self._handsToStrList(sum(self.current_player.hand.hand, [])),
                     'contrat': self.contrat,
                     'suit': self.atout_suit,
                     'shift': shift}
                }


    def _event_ChooseContratAction(self, actionData):
        
        shift = self.event_data_for_server['shift']
        
        if shift == 0 and self.numTurnOfAnnounce==0:
            self.playerToStartAnnounce = (self.dealer + 1)%4
            self.current_player = self.players[self.playerToStartAnnounce]
            
        else:
            self.current_player_i = (self.playerToStartAnnounce+shift)%4
            self.current_player = self.players[self.current_player_i]

            
        self.contrat = actionData["data"]["action"]["value"]
        self.atout_suit = actionData["data"]["action"]["suit"]
        
#         if there is a modification of the previous contrat, new turn of announce starting after the current player
        if actionData["data"]["action"]["newContrat"]:
            self.playerToStartAnnounce = self.current_player_i
            self.numTurnOfAnnounce = 1
            self.event_data_for_server['shift'] =0
            self.leadingTeam = self.current_player.team.teamNumber

            
        if self.event_data_for_server['shift'] <3:

            self.event_data_for_server['shift'] += 1
            self.event = "ChooseContrat"
            self._event_ChooseContrat()
        else:
            
            self.event_data_for_server['shift'] += 1
            if self.contrat == 0 and self.atout_suit== -1:
                self.renderInfo['printFlag'] = True

                self.renderInfo['Msg'] += "everybody passed - New round is comming"

                self.event = 'RoundEnd'
                self._event_ChooseContrat()
                self.event_data_for_server = {}
    
            # if everyone had the opportunity to announce, let's play !
            else:
                self.event = 'PlayTrick'
                self.renderInfo['Msg'] += 'Leading team: {0}\n'.format(self.leadingTeam)
                self._event_PlayTrick()
      
            
            
    def _event_PlayTrick(self):
                
        shift = self.event_data_for_server['shift']
        print("shift", shift, "trickNum", self.trickNum)
        if self.trickNum == 0 and shift == 0:
            
            current_player = self.players[self.dealer + 1]
            
        else:
            current_player_i = (self.trickWinner + shift)%4
            current_player = self.players[current_player_i]
            
        self.event_data_for_client \
        =   { "event_name" : self.event,
                "broadcast" : False,
                "data" : {
                    'playerName': current_player.name,
                    'hand': self._handsToStrList(sum(current_player.hand.hand, [])),
                    'trickNum': self.trickNum+1,
                    'trickSuit': self.currentTrick.suit.__str__(),
                    'currentTrick': self._getCurrentTrickStrList(),
                    'contrat': self.contrat,
                    'suit': self.atout_suit
                }
            }

    def _event_PlayTrick_Action(self, action_data):

        shift = self.event_data_for_server['shift']
        current_player_i = (self.trickWinner + shift)%4
        current_player = self.players[current_player_i]
        addCard = current_player.play(action_data['data']['action']['card'])

        if shift==0:
            self.currentTrick.setTrickSuit(addCard) 
        # If suit is atout, you must go higher if you can
        if (addCard is not None and 
            addCard.suit == Suit(self.atout_suit) and 
            self.currentTrick.suit == Suit(self.atout_suit)):
        
            if (current_player.hasHigherAtout(self.atout_suit, self.currentTrick.highest_rank) and
                atout_rank[addCard.rank.rank] < self.currentTrick.highest_rank):
                print("Must put a higher atout")
                addCard = None
                
            # player tries to play off suit but has trick suit
            if addCard is not None and addCard.suit != self.currentTrick.suit:
                if current_player.hasSuit(self.currentTrick.suit):
                    print ("Must play the suit of the current trick.")
                    addCard = None
                elif current_player.hasAtout(Suit(self.atout_suit)) and addCard.suit != Suit(self.atout_suit):
                    print ("Must play Atout.")
                    addCard = None
                elif (current_player.hasAtout(Suit(self.atout_suit)) and
                      addCard.suit == Suit(self.atout_suit)):
                    # Player can play a higher atout but doesn't do so --> forced to play a higher atout
                    if (self.currentTrick.highest_is_atout and
                        current_player.hasHigherAtout(self.atout_suit, self.currentTrick.highest_rank) and
                        atout_rank[addCard.rank.rank] < self.currentTrick.highest_rank):
                        print("Must put a higher atout")
                        addCard = None


        if addCard is not None:
            current_player.removeCard(addCard)
            self.currentTrick.addCard(addCard, current_player_i, Suit(self.atout_suit))
            self.event_data_for_server['shift'] += 1
            self.event = 'ShowTrickAction'
            self._event_ShowTrickAction()
        else:
            self.event = 'PlayTrick'
            self._event_PlayTrick()
    
            
    def _event_ShowTrickAction(self):

        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = "\n" + self._printCurrentTrick()
        self.renderInfo['Msg'] += 'Leading team: {0}\n'.format(self.leadingTeam)
        self.event_data_for_client \
        =   { "event_name" : self.event,
                "broadcast" : True,
                "data" : {
                    'trickNum': self.trickNum+1,
                    'trickSuit': self.currentTrick.suit.__str__(),
                    'currentTrick': self._getCurrentTrickStrList(),
                    'trickValue': self._countTrickValue(),
                    'contrat': self.contrat,
                    'suit': self.atout_suit
                }
            }
        
        if self.currentTrick.cardsInTrick < 4:
            self.event = 'PlayTrick'
        else:
            
            self.event = 'ShowTrickEnd'
            self._evaluateTrick()
        
            self.players[self.trickWinner].score += self._countTrickValue()
            [t.updateRoundScore() for t in self.teams]
        
    def _event_ShowTrickEnd(self):
        

        cards = []
        for card in self.currentTrick.trick:
            cards += [str(card)]
                 
        self.event_data_for_client \
        =   { "event_name" : self.event,
                "broadcast" : True,
                "data" : {
                    'trickNum': self.trickNum+1,
                    'trickWinner': self.players[self.trickWinner].name,
                    'cards': cards,
                    'contrat': self.contrat,
                    'suit': self.atout_suit
                }
            }

        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = '\n*** Trick {0} ***\n'.format(self.trickNum+1)
        self.renderInfo['Msg'] += 'Winner: {0}\n'.format(self.players[self.trickWinner].name)
        self.renderInfo['Msg'] += 'ValueTrick: {0}\n'.format(self._countTrickValue())

        for i in range(2):
            self.renderInfo['Msg'] += '{}:{}\n'.format(self.teams[i].name, self.teams[i].score)

        self.renderInfo['Msg'] += 'Winning team: {0}\n'.format(self.players[self.trickWinner].team.name)
        self.renderInfo['Msg'] += 'cards: {0}\n'.format(cards)

        self.renderInfo['Msg'] += 'AtoutIs: {0}\n'.format(Suit(self.atout_suit).string)
        
        self.currentTrick = Trick()
             
        self.trickNum += 1
        if self.trickNum < 8:
            self.event = 'PlayTrick'
            self.event_data_for_server = {'shift': 0}
        else:
            self.event = 'RoundEnd'
            self.event_data_for_server = {}
                
    def _event_RoundEnd(self):


        self.event_data_for_client \
        =   { "event_name" : self.event,
                "broadcast" : True,
                "data" : {
                    "teams" : [
                       {'TeamName': self.teams[0].name,
                        'score': self.teams[0].score},
                       {'TeamName': self.teams[1].name,
                        'score': self.teams[1].score},
                       ],
                    'Round': self.round,
                    'contrat': self.contrat,
                    'suit': self.atout_suit
                }
            }

        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = '\n*** Round {0} End ***\n'.format(self.round)
        for t in self.teams:
            self.renderInfo['Msg'] += 'round Score {0}: {1}\n'.format(t.name, t.score)
            self.renderInfo['Msg'] += 'global score {0}: {1}\n'.format(t.name, t.globalScore)

            
        roundScore_list_for_teams = [0,0]
        if self.contrat == 0 and self.atout_suit==-1:
            self.renderInfo['Msg'] += 'Everybody passed'

        elif self.teams[self.leadingTeam].score >= self.contrat:
            self.teams[self.leadingTeam].globalScore += self.contrat
            roundScore_list_for_teams[self.leadingTeam] = self.contrat

        else:
            self.teams[self.leadingTeam-1].globalScore += self.contrat
            roundScore_list_for_teams[self.leadingTeam -1] = self.contrat

        roundScore_list_for_players = roundScore_list_for_teams*2
        max_score_team = max(self.teams, key=lambda x:x.globalScore)
        # new round if no one has lost
        if max_score_team.globalScore < self.maxScore:
            self.event = 'NewRound'
            self.event_data_for_server = {}
        else:
            self.event = 'GameOver'
            self.event_data_for_server = {}
        
        reward = {}
        for current_player_i in range(len(self.players)):
            reward[self.players[current_player_i].name] = roundScore_list_for_players[current_player_i]
        return reward
        
    def _event_GameOver(self):
        
        winner = min(self.teams, key=lambda x:x.globalScore)
        
        self.event_data_for_client \
        =   { "event_name" : self.event,
                "broadcast" : True,
                "data" : {
                    "teams" : [
                        {'TeamName': self.teams[0].name,
                        'score': self.teams[0].globalScore},
                       {'TeamName': self.teams[1].name,
                        'score': self.teams[1].globalScore},
                       ],
                    'Round': self.round,
                    'Winner': winner.name
                }
            }

        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = '\n*** Game Over ***\n'
        for p in self.teams:
            self.renderInfo['Msg'] += 'round score {0}: {1}\n'.format(p.name, p.score)
            self.renderInfo['Msg'] += '{0}: {1}\n'.format(p.name, p.globalScore)
        
        self.renderInfo['Msg'] += '\nRound: {0}\n'.format(self.round)
        self.renderInfo['Msg'] += 'Winner: {0}\n'.format(winner.name)
        
        self.event = None

    def reset(self):
        
        # Generate a full deck of cards and shuffle it
        self.event = 'GameStart'
        self._event_GameStart()
        observation = self.event_data_for_client
        self.event = 'NewRound'
        self.event_data_for_server = {}
        
        return observation
                
    def render(self):
        
        if self.renderInfo['printFlag']:
            print(self.renderInfo['Msg'])
            self.renderInfo['printFlag'] = False
            self.renderInfo['Msg'] = ""
    

        
    def step(self, action_data):
        observation, reward, done, info = None, None, None, None
        print("\n \ntype of event in env.step: ",self.event)
        if self.event == 'NewRound':
            self._event_NewRound()
                      
        elif self.event == 'ShowPlayerHand':
            self._event_ShowPlayerHand()

        elif self.event == 'ChooseContrat' or self.event == 'ChooseContratAction':
            if action_data != None:
                self._event_ChooseContratAction(action_data)
            else:
                if self.event == 'ChooseContrat':
                    self._event_ChooseContrat()
            
        elif self.event == 'PlayTrick' or self.event == 'ShowTrickAction' or self.event == 'ShowTrickEnd':
            print(self.event)
            if action_data != None and action_data['event_name'] == "PlayTrick_Action":

                self._event_PlayTrick_Action(action_data)
            else:
                if self.event == 'PlayTrick':
                    self._event_PlayTrick()
                elif self.event == 'ShowTrickEnd':
                    self._event_ShowTrickEnd()
                    reward = self._countTrickValue()

        
        elif self.event == 'RoundEnd':
            reward = self._event_RoundEnd()
            
        elif self.event == 'GameOver':
            self._event_GameOver()

        elif self.event == None:
            self.event_data_for_client = None
            done = True

        print(reward)
        observation = self.event_data_for_client
        return observation, reward, done, info
