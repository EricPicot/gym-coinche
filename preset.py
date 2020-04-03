from rl_coach.agents.soft_actor_critic_agent import SoftActorCriticAgentParameters
from rl_coach.core_types import EnvironmentSteps
from rl_coach.environments.gym_environment import GymEnvironmentParameters, GymVectorEnvironment
from rl_coach.graph_managers.basic_rl_graph_manager import BasicRLGraphManager
from rl_coach.graph_managers.graph_manager import ScheduleParameters
import coinche.gym

#########
# Agent #
#########
agent_params = SoftActorCriticAgentParameters()

###############
# Environment #
###############
env_params = GymVectorEnvironment(level='coinche-v0')

####################
# Graph Scheduling #
####################
num_tricks_in_round = 8

num_round_improve_steps = 80 * num_tricks_in_round
num_round_heatup = 8 * num_tricks_in_round
num_round_training = 300 * num_tricks_in_round
num_round_evaluation = 10 * num_tricks_in_round

schedule_params = ScheduleParameters()
schedule_params.improve_steps = EnvironmentSteps(num_round_improve_steps)
schedule_params.heatup_steps = EnvironmentSteps(num_round_heatup)
schedule_params.steps_between_evaluation_periods = EnvironmentSteps(num_round_training)
schedule_params.evaluation_steps = EnvironmentSteps(num_round_evaluation)

########################
# Create Graph Manager #
########################
# BasicRLGraphManager, créé un uniquement LevelManager entre l'Agent et l'Environnement
graph_manager = BasicRLGraphManager(agent_params=agent_params,
                                    env_params=env_params,
                                    schedule_params=schedule_params)
