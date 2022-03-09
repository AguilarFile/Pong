document.body.style.cursor = 'none';
let cnv = document.getElementById("cnv");
let ctx = cnv.getContext("2d");
ctx.fillStyle = 'white';
const user = document.querySelector("body");
const game = new pongGameEnv();

user.addEventListener("mousemove", e => {
    game.p2 = e.pageY || e.clientY;
})
/*
user.addEventListener("keydown", function(event)  {
    if (event.defaultPrevented) {
        return; // Do nothing if event already handled
      }

    switch (event.code) {
        case "ArrowDown":
            game.p2 += 2*game.paddleSpeed;
            break;
        case "ArrowUp":
            game.p2 -= game.paddleSpeed;
            break;
   }
   event.preventDefault();
}, true);
*/
//One solution would be to just continuously run the move function in a loop until keyup happens: 
// https://stackoverflow.com/questions/29279805/keydown-doesnt-continuously-fire-when-pressed-and-hold
// DO NOT WORK ON THIS - WASTE OF TIME

let oldballPos = game.ballPos;
let oldballVel = game.ballVel;

function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0,0, 1920, 1080);

    let ballPos = game.getBallPosition();
    let p1 = game.getPlayer1Position();
    let p2 = game.getPlayer2Position();

    ctx.fillRect(ballPos[0], ballPos[1], game.ballSize, game.ballSize);
    ctx.fillRect(game.paddleOffSet, p1, game.paddleWidth, game.paddleHeight);
    ctx.fillRect(game.rightLine + game.ballSize, p2,  game.paddleWidth, game.paddleHeight);

    game.step(0,0, true)

    // let frame = game.step(0,0, true);
    // for (let y = 0; y < game.screenHeight; y++){
    //     for (let x = 0; x < game.screenWidth; x++){
    //         paint = frame[y*game.screenWidth + x]
    //         if (paint != 0){
    //             ctx.fillRect(x,y,1,1);
    //         }
    //     }
    // }
}


animate();