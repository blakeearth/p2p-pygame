# p2p-pygame
## About
See the [wiki](https://github.com/blakeearth/p2p-pygame/wiki) for now.

## How to play

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