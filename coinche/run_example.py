import gym

from coinche import *
from Agent.human import Human
from Agent.randomAI import RandomAI

NUM_EPISODES = 5
MAX_SCORE = 1000

playersNameList = ['Nord', 'Est', 'Sud', 'Ouest']
agent_list = [0, 0, 0, 0]

# Human vs Random

# agent_list[0] = Human(playersNameList[0], {'print_info': True})
# agent_list[1] = Human(playersNameList[1], {'print_info': True})
# agent_list[2] = Human(playersNameList[2], {'print_info': True})
# agent_list[3] = Human(playersNameList[3], {'print_info': True})


# Random play

agent_list[0] = RandomAI(playersNameList[0], {'print_info': False})
agent_list[1] = RandomAI(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAI(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAI(playersNameList[3], {'print_info': False})


env = gym.make('Coinche_Game-v0')
env.__init__(playersNameList, maxScore=MAX_SCORE)

for i_episode in range(NUM_EPISODES):
    
    observation = env.reset()
    
    while True:
        env.render()

        now_event = observation['event_name']
        IsBroadcast = observation['broadcast']
        action = None
        if IsBroadcast == True:
            for agent in agent_list:
                agent.do_action(observation)
        else:
            playName = observation['data']['playerName']
            for agent in agent_list:
                if agent.name == playName:
                    action = agent.do_action(observation)

        observation, reward, done, info = env.step(action)

        if reward != None:
            print('\nreward: {0}\n'.format(reward))

        if done:
            print('\nGame Over!!\n')
            break


