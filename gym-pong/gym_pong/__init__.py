import logging

# Third party
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(id="Pong-v0", entry_point="gym_pong.envs:PongEnv")