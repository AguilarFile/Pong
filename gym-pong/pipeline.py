# %%
import gym
import gym_pong
import cv2
import numpy as np
import matplotlib.pyplot as plt

from tf_agents.environments import suite_gym
from tf_agents.environments.atari_preprocessing import AtariPreprocessing
from tf_agents.environments.atari_wrappers import FrameStack4
from gym_pong.envs.myAtariPreprocessing import myWrapper

environment_name = "Pong-v0"
max_episode_steps = 27000 

env = suite_gym.load(
    environment_name,
    max_episode_steps = max_episode_steps,
    gym_env_wrappers=[myWrapper, FrameStack4]
)

# %%
for _ in range(4):
    time_step = env.step(1)


# %%
def plot_observation(obs):
    # Since there are only 3 color channels, you cannot display 4 frames
    # with one primary color per frame. So this code computes the delta between
    # the current frame and the mean of the other frames, and it adds this delta
    # to the red and blue channels to get a pink color for the current frame.
    obs = obs.astype(np.float32)
    img = obs[..., :3]
    current_frame_delta = np.maximum(obs[..., 3] - obs[..., :3].mean(axis=-1), 0.)
    img[..., 0] += current_frame_delta
    img[..., 2] += current_frame_delta
    img = np.clip(img / 150, 0, 1)
    plt.imshow(img)
    plt.axis("off")


plt.figure(figsize=(6, 6))
plot_observation(time_step.observation)
plt.show()


# %%
