//A mutable class that represents the game Pong (Atari 1972 Game) with a 1920x1080 gameboard
class pongGame{

    screenWidth = 1920
    screenHeight = 1080

    paddleHeight = 150;
    paddleWidth = 20;
    paddleSpeed = 1;
    paddleOffSet = Math.floor(this.screenWidth/10) //distance from wall to bar
    maxBounceAngle = 5/12 * Math.PI;

    ballSize = 21;
    ballPos;
    ballVel;

    leftLine = this.paddleOffSet + this.paddleWidth;
    rightLine = this.screenWidth - this.paddleOffSet - this.paddleWidth - this.ballSize;

    p1;
    p2;
    scoreP1;
    scoreP2;

    wallAudio = new Audio("wallSound.wav");
    paddleAudio = new Audio("paddleSound.wav");


    //Initializes the gameboard and returns two player types
    constructor(){
        this.p1 = Math.floor((this.screenHeight - this.paddleHeight)/2);
        this.p2 = this.p1;
        this.scoreP1 = 0;
        this.scoreP2 = 0;
        this.ballReset();
    }

    //Resets the ball to its original position and gives it a random velocity [a,b]. 
    // -10 <= a,b <= 10
    // a,b != 0
    ballReset(){
        const maxSpeed = 100;
        const xSpeed = ((Math.random() < 0.5)? -1 : 1) * (Math.floor(Math.random()*maxSpeed) + 1);
        const ySpeed = ((Math.random() < 0.5)? -1 : 1) * (Math.floor(Math.random()*maxSpeed) + 1);
        this.ballVel = [xSpeed, ySpeed];
        this.ballPos = [Math.floor(this.screenWidth/2), Math.random()*(this.screenHeight - this.ballSize)]
    }

    //parameters: p1,p2 = -1,0,1
    nextFrame(actionP1, actionP2) { 

        this.p1 += actionP1 * this.paddleSpeed; //Fix bounded error
        this.p2 += actionP2 * this.paddleSpeed;
        this.ballPos[0] += this.ballVel[0];
        this.ballPos[1] += this.ballVel[1];

        //Crosses Left Boarder
        if (this.ballPos[0] < 0){
            this.scoreP2 += 1;
            this.ballReset();
            return false;
        }
        
        //Crosses Right Boarder
        if (this.ballPos[0] + this.ballSize > this.screenWidth) {
            this.scoreP1 += 1;
            this.ballReset();
            return false;
        }

        //Crosses Top Boarder
        if (this.ballPos[1] < 0){
            this.ballVel =  [this.ballVel[0], Math.abs(this.ballVel[1])];
            this.ballPos = [this.ballPos[0], -this.ballPos[1]];
            this.wallAudio.play()
        }

        //Crosses Bottom Boarder
        if (this.ballPos[1] > this.screenHeight - this.ballSize){
            this.ballVel =  [this.ballVel[0], - Math.abs(this.ballVel[1])];
            this.ballPos = [this.ballPos[0], 2*this.screenHeight - 2*this.ballSize - this.ballPos[1]];
            this.wallAudio.play();
        }

        const ballPosBefore = [this.ballPos[0] - this.ballVel[0], this.ballPos[1] - this.ballVel[1]];

        //Crosses Player 1
        if (this.ballPos[0] <= this.leftLine &&  this.leftLine <= ballPosBefore[0]){
            let intersectY = this.findIntersectY(this.ballPos, this.ballVel, this.leftLine, this.p1);
            if (intersectY != null){
                this.paddleAudio.play()
                this.ballPos = [this.leftLine, intersectY];
                this.ballVel = this.findBounceAngle(intersectY, this.p1, this.ballVel);
            }
        }

        //Crosses Player 2
        if (ballPosBefore[0]  <= this.rightLine && this.rightLine <= this.ballPos[0] ){
            let intersectY = this.findIntersectY(this.ballPos, this.ballVel, this.rightLine  , this.p2);
            if (intersectY != null){
                this.paddleAudio.play()
                this.ballPos = [this.rightLine, intersectY];
                this.ballVel = this.findBounceAngle(intersectY, this.p2, this.ballVel);
                this.ballVel = [-this.ballVel[0], this.ballVel[1]];
            }
        }

    }

    //With the line created from ballPos and ballVos, determine the intersection between 
    //such line and x = xLine, for any real number xLine
    //Return y-intersection iff paddlePosY <= y-intersection <= paddlePosY + paddleHeight , else Null
    findIntersectY(ballPos, ballVel, xLine, paddlePos){
        const m = ballVel[1]*1.0/ballVel[0];
        const b = ballPos[1] - m*ballPos[0];
        const intersectionY = Math.floor(m*xLine + b);
        return (paddlePos - this.ballSize  <= intersectionY && intersectionY <= paddlePos + this.paddleHeight )? intersectionY : null; //paddle has greater range
    }

    //return the resulting velocity of the ball after hits the paddle at intersectionY 
    //with the given ball's velocity ballVel
    findBounceAngle(intersectY, paddlePos, ballVel){
        const relativeIntersectY = paddlePos + this.paddleHeight/2.0 - (intersectY + this.ballSize/2.0);
        const normRelativeIntersectionY = (relativeIntersectY/(this.paddleHeight/2.0 + this.ballSize));
        const bounceAngle = normRelativeIntersectionY * this.maxBounceAngle;
        const ballSpeed = Math.sqrt(ballVel[0]**2 + ballVel[1]**2);
        return [ballSpeed*Math.cos(bounceAngle), -ballSpeed*Math.sin(bounceAngle)];
    }

    getBallPosition(){
        return this.ballPos;
    }

    getPlayer1Position() {
        return this.p1;
    }

    getPlayer2Position() {
        return this.p2;
    }

}

