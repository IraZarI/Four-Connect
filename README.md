# Four-Connect
Board for the Programming-AI-Gym-Challenge

This small python script includes some basic Backend for our 4-connect challenge. 
It follows the simple rules, that one can extract from the wiki article:
https://en.wikipedia.org/wiki/Connect_Four

if you want to participate in the challenge, download this board.py and start programming. 


optionally available is a very stupid dummy bot that just randomly throws in coins on different columns. Download bob.py


the board software (at this state) operates as follows:

start board.py in console
board waits for number of games to play (int value). Enter it!
board waits for player 1 to connect (start bob.py in another console)
board waits for player 2 to connect (yourself, or also bob)
board randomly let one player start by sending him the boardStatus np.array: (empty board)

#game loop
board waits for this player to respond.
response could be: \n
int: 1-7  #move of the player \n
int: -10  #Player wants to end the whole session

boards checks input from player and checks if the move is legit.
if move is not legit, the game-round will be cancelt, the player with the wrong move will get an int: -1 sent, the other player a int: 0
if move is legit, board applies it
board checks if any player has won or if the game is remis.
if remis, both player get send int: 0 and a new game is started (reset boardStatus, new random start player)
if one player won, the player gets int: 1 sent, the other player gets send int: 0 and a new game is started.
if remis or won, game count goes up by 1. 
if game count is over number of max games, both players get send a int: -20 and board kills itself.
repeat @ game loop.





for connection a tcp protocol is used. Port 4001, passwort: 'secret password'

as an example please look into bob.py


