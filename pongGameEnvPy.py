import math
import random

import abc
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts


#A mutable class that represents the game Pong (Atari 1972 Game) with a 1920x1080 gameboard
class pongGameEnv(py_environment.PyEnvironment):

    screenWidth = 1920
    screenHeight = 1080
    shape = (screenHeight, screenWidth)

    paddleHeight = 140
    paddleWidth = 25
    paddleSpeed = 20
    paddleOffSet = math.floor(screenWidth/10) #distance from wall to bar
    maxBounceAngle = 5/12 * math.pi

    ballSize = 21
    #ballPos
    #ballVel

    leftLine = paddleOffSet + paddleWidth
    rightLine = screenWidth - paddleOffSet - paddleWidth - ballSize

    #p1
    #p2

    #Initializes the gameboard and returns two player types
    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=2, name='action')
        self._observation_spec = array_spec.BoundedArraySpec( 
            shape=(self.screenHeight,self.screenWidth), dtype=np.float32, 
            minimum=np.zeros(self.shape, dtype=np.float32), 
            maximum = np.full(self.shape, 255., dtype=np.float32), 
            name='observation')
        
        self._current_time_step = None
        self._episode_ended = False
        self._reset()

    def observation_spec(self):
        return self._observation_spec
    
    def action_spec(self):
        return self._action_spec

    #Resets the ball to its original position and gives it a random velocity [a,b]. 
    # -10 <= a,b <= 10
    # a,b != 0
    def _reset(self):
        self._episode_ended = False
        self.p1 = math.floor((self.screenHeight - self.paddleHeight)*random.random())
        self.p2 = math.floor((self.screenHeight - self.paddleHeight)*random.random())

        ballSpeed = 8
        maxStartingAngle = 5/12*math.pi
        angle = 2* maxStartingAngle* random.random() - maxStartingAngle +  (math.pi if random.random() > 0.5 else 0)
        self.ballVel = [ballSpeed*math.cos(angle), ballSpeed*math.sin(angle)]
        self.ballPos = [math.floor(self.screenWidth/2), math.floor(random.random()*(self.screenHeight - self.ballSize))] #[x,y] #math.floor

        return ts.restart(self.getObs())

    #parameters: action: the left paddle's action
    #action: 0 = up , 1 = remain, 2 = down
    def _step(self, action):

        if self._episode_ended:
            return self.reset()

        action = 1 - action

        offset = random.random()*self.paddleHeight - self.paddleHeight/2
        self.p1 +=  action * self.paddleSpeed
        self.p2 += self.paddleSpeed if (self.ballPos[1] + self.ballSize/2 + offset> self.p2 + self.paddleHeight/2) else -self.paddleSpeed
        

        #Paddle vertical boundaries
        self.p1 = max(0, self.p1)
        self.p1 = min(self.screenHeight - self.paddleHeight, self.p1)

        self.p2 = max(0, self.p2)
        self.p2 = min(self.screenHeight - self.paddleHeight, self.p2)


        self.ballPos[0] += self.ballVel[0]
        self.ballPos[1] += self.ballVel[1]
        

        #Crosses Top Boarder
        if (self.ballPos[1] < 0):
            self.ballVel =  [self.ballVel[0], -self.ballVel[1]]
            self.ballPos = [self.ballPos[0], -self.ballPos[1]]

        

        #Crosses Bottom Boarder
        if (self.ballPos[1] > self.screenHeight - self.ballSize):
            self.ballVel =  [self.ballVel[0], -self.ballVel[1]]
            self.ballPos = [self.ballPos[0], 2*self.screenHeight - 2*self.ballSize - self.ballPos[1]]

        ballPosBefore = [self.ballPos[0] - self.ballVel[0], self.ballPos[1] - self.ballVel[1]]

        #Crosses Player 1
        if (self.ballPos[0] <= self.leftLine and  self.leftLine <= ballPosBefore[0]):
            intersectY = self.findIntersectY(self.ballPos, self.ballVel, self.leftLine, self.p1)
            if (intersectY != None):
                self.ballPos = [self.leftLine, intersectY] 
                self.ballVel = self.findBounceAngle(intersectY, self.p1, self.ballVel)
            
        

        #Crosses Player 2
        if (ballPosBefore[0]  <= self.rightLine and self.rightLine <= self.ballPos[0]):
            intersectY = self.findIntersectY(self.ballPos, self.ballVel, self.rightLine  , self.p2)
            if (intersectY != None):
                self.ballPos = [self.rightLine, intersectY] 
                self.ballVel = self.findBounceAngle(intersectY, self.p2, self.ballVel)
                self.ballVel = [-self.ballVel[0], self.ballVel[1]]

        #Crosses Left Boarder
        if (self.ballPos[0] < 0):
            self._episode_ended = True
            reward = -100
            return ts.termination(np.array(self.getObs(), dtype=np.float32), reward)
        
        
        #Crosses Right Boarder
        if (self.ballPos[0] + self.ballSize > self.screenWidth) :
            self._episode_ended = True
            reward = 100
            return ts.termination(np.array(self.getObs(), dtype=np.float32), reward)

        return ts.transition(np.array(self.getObs(), dtype=np.float32), reward=0.0, discount=1.0)

    

    #With the line created from ballPos and ballVos, determine the intersection between 
    #such line and x = xLine, for any real number xLine
    #Return y-intersection iff paddlePosY <= y-intersection <= paddlePosY + paddleHeight , else Null
    def findIntersectY(self, ballPos, ballVel, xLine, paddlePos):
        m = ballVel[1]*1.0/ballVel[0]
        b = ballPos[1] - m*ballPos[0]
        intersectionY = math.floor(m*xLine + b)
        return intersectionY if (paddlePos - self.ballSize  <= intersectionY and intersectionY <= paddlePos + self.paddleHeight ) else None #paddle has greater range
    

    #return the resulting velocity of the ball after hits the paddle at intersectionY 
    #with the given ball's velocity ballVel
    def findBounceAngle(self, intersectY, paddlePos, ballVel):
        increaseInSpeed = 1/2
        relativeIntersectY = paddlePos + self.paddleHeight/2.0 - (intersectY + self.ballSize/2.0)
        normRelativeIntersectionY = (relativeIntersectY/(self.paddleHeight/2.0 + self.ballSize))
        bounceAngle = normRelativeIntersectionY * self.maxBounceAngle
        ballSpeed = math.sqrt(ballVel[0]**2 + ballVel[1]**2) + increaseInSpeed
        return [ballSpeed*math.cos(bounceAngle), -ballSpeed*math.sin(bounceAngle)]

    def getObs(self):
        xBall, yBall = math.floor(self.ballPos[0]), math.floor(self.ballPos[1])
        obs = np.zeros(self.shape, dtype = np.float32) #black canvas
        obs[self.p1: self.p1 + self.paddleHeight + 1, self.paddleOffSet : self.paddleOffSet + self.paddleWidth + 1] = 255. #paddle 1
        obs[self.p2: self.p2 + self.paddleHeight + 1, self.rightLine: self.rightLine + self.paddleWidth + 1] = 255. #paddle 2
        obs[yBall: yBall + self.ballSize + 1, xBall: xBall + self.ballSize + 1] = 255. #ball
        return obs

