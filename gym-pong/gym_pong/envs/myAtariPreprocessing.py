import gym
import numpy as np
import cv2

class myWrapper(gym.Wrapper):
    #Frame Skipping: 4 
    #Max pooling: last 2 frames 
    #Down Sample to square image: 84x84 
    #Increase dimension, from (height, width) -> (height, width, 1)
    def __init__(self, env):
        super().__init__(env)
        self.env = env
        self.frame_skip = 4
        self.screen_size = 84 #Just go with this for now
        s = (1080,1920,1)
        self.obs_buffer = [
            np.empty(s,dtype = np.float32),
            np.empty(s, dtype = np.float32)
             ]


    def step(self, action):
        R = 0.0
        for t in range(self.frame_skip):
            obs, reward, done, info = self.env.step(action)
            R += reward
            self.game_over = done

            if done:
                break

            if t == self.frame_skip - 2:
                self.obs_buffer[1] = obs
            elif t == self.frame_skip - 1:
                self.obs_buffer[0] = obs

        return self._get_obs(), R, done, info
    
    def reset(self):
        obs = self.env.reset()
        self.obs_buffer[0] = obs
        self.obs_buffer[1].fill(0)
        return self._get_obs()

    def _get_obs(self):
        np.maximum(self.obs_buffer[0], self.obs_buffer[1], out=self.obs_buffer[0])
        obs = cv2.resize(
            self.obs_buffer[0],
            (self.screen_size, self.screen_size),
            interpolation=cv2.INTER_AREA,
        )
        obs = np.asarray(obs, dtype=np.float32)
        return np.expand_dims(obs, axis = -1)
        
    

    

    