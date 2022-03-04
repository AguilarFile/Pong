import math
import tensorflow as tf
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec

    
#A mutable class that represents the game Pong (Atari 1972 Game) with a 1920x1080 gameboard
class pongGameEnv(py_environment.PyEnvironment):

    screenWidth = 1920
    screenHeight = 1080

    paddleHeight = 140
    paddleWidth = 25
    paddleSpeed = 10
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
            shape=(), dtype=np.int32, minimum=0, maximum=1, name='action')

        self.p1 = math.floor((self.screenHeight - self.paddleHeight)/2)
        self.p2 = self.p1
        self.scoreP1 = 0
        self.scoreP2 = 0
        self.ballReset()
    

    #Resets the ball to its original position and gives it a random velocity [a,b]. 
    # -10 <= a,b <= 10
    # a,b != 0
    def ballReset(self):
        ballSpeed = 8
        maxStartingAngle = 5/12*math.pi
        angle = 2* maxStartingAngle*math.random() - maxStartingAngle +  (math.pi if math.random() > 0.5 else 0)
        self.ballVel = [ballSpeed*math.cos(angle), ballSpeed*math.sin(angle)]
        self.ballPos = [math.floor(self.screenWidth/2), math.random()*(self.screenHeight - self.ballSize)]
    
    

    def frame(self):
        frame, step  = [], 4
        for y in range(0, self.screenHeight, step):
            for x in range(0, self.screenWidth, step):
                #paddle 1
                if (self.p1 <= y and y <= self.p1 + self.paddleHeight and self.paddleOffSet <= x and x <= self.paddleOffSet + self.paddleWidth):
                    frame.push(255)

                #paddle 2
                elif (self.p2 <= y and y <= self.p2 + self.paddleHeight and self.rightLine <= x and x <= self.rightLine + self.paddleWidth):
                    frame.push(255)
                
                #b
                elif (self.ballPos[1] <= y and  y <= self.ballPos[1] + self.ballSize and self.ballPos[0] <= x and x <= self.ballPos[0] + self.ballSize):
                    frame.push(255)

                #black space
                else:
                    frame.push(0)

        return frame
    

    #parameters: p1,p2 = -1,0,1
    def step(self, actionP2, actionP1 = 0, hardcoded = False):

        if (hardcoded):
            offset = math.random()*self.paddleHeight - self.paddleHeight/2
            self.p1 += self.paddleSpeed if (self.ballPos[1] + self.ballSize/2 + offset> self.p1 + self.paddleHeight/2) else -self.paddleSpeed
            self.p2 += actionP2 * self.paddleSpeed
        else:
            self.p1 += actionP1 * self.paddleSpeed
            self.p2 += actionP2 * self.paddleSpeed
        

        #Paddle vertical boundaries
        self.p1 = math.max(0, self.p1)
        self.p1 = math.min(self.screenHeight, self.p1)

        self.p2 = math.max(0, self.p2)
        self.p2 = math.min(self.screenHeight - self.paddleHeight, self.p2)


        self.ballPos[0] += self.ballVel[0]
        self.ballPos[1] += self.ballVel[1]

        #Crosses Left Boarder
        if (self.ballPos[0] < 0):
            self.gameOver.play()
            self.scoreP2 += 1
            self.ballReset()
            return False
        
        
        #Crosses Right Boarder
        if (self.ballPos[0] + self.ballSize > self.screenWidth) :
            self.gameOver.play()
            self.scoreP1 += 1
            self.ballReset()
            return False
        

        #Crosses Top Boarder
        if (self.ballPos[1] < 0):
            self.ballVel =  [self.ballVel[0], -self.ballVel[1]]
            self.ballPos = [self.ballPos[0], -self.ballPos[1]]
            self.wallAudio.play()
        

        #Crosses Bottom Boarder
        if (self.ballPos[1] > self.screenHeight - self.ballSize):
            self.ballVel =  [self.ballVel[0], -self.ballVel[1]]
            self.ballPos = [self.ballPos[0], 2*self.screenHeight - 2*self.ballSize - self.ballPos[1]]
            self.wallAudio.play()
        

        ballPosBefore = [self.ballPos[0] - self.ballVel[0], self.ballPos[1] - self.ballVel[1]]

        #Crosses Player 1
        if (self.ballPos[0] <= self.leftLine and  self.leftLine <= ballPosBefore[0]):
            intersectY = self.findIntersectY(self.ballPos, self.ballVel, self.leftLine, self.p1)
            if (intersectY != None):
                self.paddleAudio.play()
                self.ballPos = [self.leftLine, intersectY] 
                self.ballVel = self.findBounceAngle(intersectY, self.p1, self.ballVel)
            
        

        #Crosses Player 2
        if (ballPosBefore[0]  <= self.rightLine and self.rightLine <= self.ballPos[0]):
            intersectY = self.findIntersectY(self.ballPos, self.ballVel, self.rightLine  , self.p2)
            if (intersectY != None):
                self.paddleAudio.play()
                self.ballPos = [self.rightLine, intersectY] 
                self.ballVel = self.findBounceAngle(intersectY, self.p2, self.ballVel)
                self.ballVel = [-self.ballVel[0], self.ballVel[1]]
            
        
        return self.frame()

    

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
    

    def getBallPosition(self):
        return self.ballPos
    

    def getPlayer1Position(self):
        return self.p1
    

    def getPlayer2Position(self): 
        return self.p2
    


