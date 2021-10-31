//A mutable class that represents the game Pong (Atari 1972 Game) with a 1920x1080 gameboard
class pongGame{

    screenWidth = 1920
    screenHeight = 1080

    paddleHeight = 170;
    paddleWdith = 10;
    paddleSpeed = 1;
    paddleOffSet = Math.floor(screenWidth/10) //distance from wall to bar
    maxBounceAngle = 5/12 * Math.PI;

    leftLine = paddleOffSet + paddleWdith;
    rightLine = screenWidth - paddleOffSet - paddleWdith;

    ballPos;
    ballVel;

    p1;
    p2;
    scoreP1;
    scoreP2;


    //Initializes the gameboard and returns two player types
    constructor(){
        this.p1 = Math.floor((screenHeight - paddleHeight)/2);
        this.p2 = Math.floor((screenHeight - paddleHeight)/2);
        scoreP1 = 0;
        scoreP2 = 0;
        this.ballReset();
    }

    //Resets the ball to its original position and gives it a random velocity [a,b]. 
    // -10 <= a,b <= 10
    // a,b != 0
    ballReset(){
        const maxSpeed = 10;
        const xSpeed = ((Math.random() < 0.5)? -1 : 1) * (Math.floor(Math.random()*maxSpeed) + 1);
        const ySpeed = ((Math.random() < 0.5)? -1 : 1) * (Math.floor(Math.random()*maxSpeed) + 1);
        this.ballVel = [xSpeed, ySpeed];
        this.ballPos = [math.floor(screenWidth/2), Math.random()*screenHeight]
    }

    //parameters: p1,p2 = -1,0,1
    nextFrame(actionP1, actionP2) {
        const originalX = this.ballPos[0];
        this.p1 = actionP1 * paddleSpeed;
        this.p2 = actionP2 * paddleSpeed;
        this.ballPos = [this.ballPos[0] + this.ballVel[0], this.ballPos[1] + this.ballVel[1]];

        //Crosses Left Boarder
        if (this.ballPos[0] < 0){
            this.scoreP2 += 1;
            this.ballReset()
            return False
        }
        
        //Crosses Right Boarder
        if (this.ballPos[0] > screenWidth) {
            this.scoreP1 += 1;
            this.ballReset();
            return False
        }

        //Crosses Top Boarder
        if (this.ballPos[1] < 0){
            this.ballVel =  [this.ballVel[0], -this.ballVel[1]]
            this.ballPos = [this.ballPos[0], -this.ballPos[1]];
        }

        //Crosses Bottom Boarder
        if (this.ballPos[1] > screenHeight){
            this.ballVel =  [this.ballVel[0], -this.ballVel[1]]
            this.ballPos = [this.ballPos[0], screenHeight - (this.ballPos[1] - screenHeight)]
        }

        //Crosses Player 1
        if (this.ballPos[0] < leftLine &&  leftLine < originalX){
            intersectY = this.findIntersectY(this.ballPos, this.ballVel, leftLine, this.p1);
            if (intersectY != Null){
                this.ballPos = [leftLine, intersectY];
                this.ballVel = this.findBounceAngle(intersectY, this.p2, this.ballVel);
            }
        }

        //Crosses Player 2
        if (originalX < rightLine && rightLine < this.ballPos[0]){
            intersectY = this.findIntersectY(this.ballPos, this.ballVel, rightLine, this.p2);
            if (intersectY != Null){
                this.ballPos = [rightLine, intersectY];
                this.ballVel = this.findBounceAngle(intersectY, this.p2, this.ballVel);
            }
        }

    }

    //With the line created from ballPos and ballVos, determine the intersection between 
    //such line and x = xLine, for any real number xLine
    //Return y-intersection iff paddlePosY <= y-intersection <= paddlePosY + paddleHeight , else Null
    findIntersectY(ballPos, ballVel, xLine, paddlePos){
        const m = ballVel[1]/ballVel[0];
        const b = ballPos[1] - m*ballPos[0];
        const intersectionY = Math.floor(m*xLine + b);
        return (paddlePos <= intersectionY && intersectionY <= paddlePos + paddleHeight)? intersectionY : Null;
    }

    //return the resulting velocity of the ball after hits the paddle at intersectionY 
    //with the given ball's velocity ballVel
    findBounceAngle(intersectY, paddlePos, ballVel){
        relativeIntersectY = (paddlePos + (paddleHeight/2)) - intersectY;
        normRelativeIntersectionY = (relativeIntersectY/(paddleHeight/2));
        bounceAngle = normRelativeIntersectionY * maxBounceAngle;
        ballSpeed = Math.sqrt(ballVel[0]**2 + ballVel[1]**2);
        return [ballSpeed*Math.cos(bounceAngle), ballSpeed*Math.sin(bounceAngle)];
    }
}