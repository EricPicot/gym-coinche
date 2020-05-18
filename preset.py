from rl_coach.agents.soft_actor_critic_agent import SoftActorCriticAgentParameters
from rl_coach.core_types import EnvironmentSteps, EnvironmentEpisodes
from rl_coach.environments.gym_environment import GymEnvironmentParameters, GymVectorEnvironment
from rl_coach.graph_managers.basic_rl_graph_manager import BasicRLGraphManager
from rl_coach.graph_managers.graph_manager import ScheduleParameters
from rl_coach.schedules import LinearSchedule, PieceWiseSchedule

import coinche.gym

#########
# Agent #
#########
agent_params = SoftActorCriticAgentParameters()

###############
# Environment #
###############
env_params = GymVectorEnvironment(level='coinche-v1')

####################
# Graph Scheduling #
####################
num_round_improve_steps = 100
num_round_heatup = 50
num_round_training = 50000
num_round_evaluation = 500

schedule_params = ScheduleParameters()
schedule_params.improve_steps = EnvironmentEpisodes(num_round_improve_steps)
schedule_params.heatup_steps = EnvironmentEpisodes(num_round_heatup)
schedule_params.steps_between_evaluation_periods = EnvironmentEpisodes(num_round_training)
schedule_params.evaluation_steps = EnvironmentEpisodes(num_round_evaluation)


# Politique d'exploration
agent_params.exploration.noise_schedule = LinearSchedule(1, 0.001, 50000)
# agent_params.exploration.noise_schedule = PieceWiseSchedule([(LinearSchedule(1, 0.01, 300), 300),
#                                                              (LinearSchedule(0.1, 0.005, 6000), 6000)])
# agent_params.exploration.noise_schedule = ExponentialSchedule(1, 0.05, 0.99)
print(agent_params.exploration)
print(agent_params.exploration.noise_schedule)

########################
# Create Graph Manager #
########################
# BasicRLGraphManager, créé un uniquement LevelManager entre l'Agent et l'Environnement
graph_manager = BasicRLGraphManager(agent_params=agent_params,
                                    env_params=env_params,
                                    schedule_params=schedule_params)
