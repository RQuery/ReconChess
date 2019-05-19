# CMSC 471 - Artificial Intelligence
# Project 5 - ReconChess

This is a repository to upload bots for the Reconchess project.

### Bots so far:
### BotOne.py:

Requirements: 

Stockfish executable, which is provided in the folder. You will need to make an environment variable for it.

Strategy:

Goes for the Scholar's Mate in the beginning - https://en.wikipedia.org/wiki/Scholar%27s_mate, once Black is 'checkmated', the king can't move, so we can capture it on the next turn. If Scholar's Mate fails, we use the best move suggested by Stockfish.

Performance: 

Beats TroutBot (Stockfish regular) most of the time - occasional engine crash - Needs fixing

Beats Random Bot every time (at least in the experiments) 

Beats Attacker Bot as white, loses as black, because attacker bot uses the same strategy as us for the first four moves, and since White starts first, Attacker Bot wins as white.

### BotTwo.py:

### Results:

### With White:

20-0 against AttackerBot

20-0 against RandomBot

20-1 against TroutBot (Stockfish)

### With Black:

20-0 against AttackerBot

20-0 against RandomBot

20-7 against TroutBot (Stockfish)

(Black results improved later too...we were 16-1 against Stockfish)
