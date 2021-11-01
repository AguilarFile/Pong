let cnv = document.getElementById("cnv");
let ctx = cnv.getContext("2d");
ctx.fillStyle = 'white';
const user = document.querySelector("body");
const game = new pongGame();
user.addEventListener("mousemove", e => {
    console.log(e);
    console.log(e.pageY || e.clientY)
    game.p1 = e.pageY || e.clientY;
    game.p2 = game.p1
})

function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0,0, 1920, 1080);

    let ballPos = game.getBallPosition();
    let p1 = game.getPlayer1Position();
    let p2 = game.getPlayer2Position();

    ctx.fillRect(ballPos[0], ballPos[1], game.ballSize, game.ballSize);
    ctx.fillRect(game.paddleOffSet, p1, game.paddleWidth, game.paddleHeight);
    ctx.fillRect(game.rightLine, p2,  game.paddleWidth, game.paddleHeight);
    game.nextFrame(0,0);
}
  
animate();