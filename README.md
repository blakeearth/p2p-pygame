# p2p-pygame demonstration and explanation
## About
This project is a simple demonstration of how a turn-based peer-to-peer networked game (without any central server) might work. It was made by Cooper Urbec and Isaac Blake.

## Setup
Install pygame.

`pip3 install pygame`

Install ThorPy, the GUI engine for pygame.

`pip3 install thorpy`

Mastermind is already "installed"--it's in a folder in the root directory as a collection of modules.

## How to play
* Run two copies of `Main.py` to run the game locally. On each instance:
 * Enter a port to host your server on and press "Submit" to start listening for connections.
 * Enter your peer's IP (default to `localhost`) and the port their server is hosted on. Press "Submit" to connect as a client to their server.
 
Now, each instance is in charge of both their client of their peer's server and a server that a peer's client is connected to. The demo starts here.

The object of the game is to shoot the other player. Shoot by clicking in the game window (the angle and velocity of your bullet are calculated based on the mouse position). There is not a win condition, but the demonstration will keep score for you.

## How it works
 Both players maintain their own game state and do their own 
 calculations for the arks of the bullets, and only send messages 
 to their opponent containing new info. Meaning when one player shoots, 
 they send a message with the bullets starting x and y cords and the 
 bullets starting x and y velocities, and when the opponent gets this 
 message, they create a bullet object and do the calculation for the 
 bullet themselves. There is no central server doing all the 
 calculations for the game then sending each player an image of what 
 their screen should look like, because in p2p each computer is 
 responsible for its own screen.
 
 ## Sources and research
* [What Every Programmer Needs To Know About Game Networking (peer-to-peer lockstep)](http://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/)
  * Article description of structure: each "step" of the game, games "figure out" and sync everything that has to happen during that step
   * This is stuff like movements, bullets being fired, rotation, etc.
* [Peer-to-peer networked games](https://gamedevelopment.tutsplus.com/tutorials/building-a-peer-to-peer-multiplayer-networked-game--gamedev-10074)
  * It does not offer any way of preventing cheats using an approach without a given authority. In a peer-to-peer game without cheating, all other players would have to be authorities on the "current" player in some way.
* [Thorpy documentation (GUI engine)](http://www.thorpy.org/documentation.html)
* [Mastermind documentation (TCP message sending)](https://www.pygame.org/project-Mastermind+Networking+Lib-859-.html)
  * Contained in release in the form of a text file
* [pygame](https://www.pygame.org/)
