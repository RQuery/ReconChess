import argparse
import datetime
import chess
from reconchess import load_player, play_local_game

firstBot = 0
secondBot = 0


parser = argparse.ArgumentParser()
parser.add_argument('white_bot_path', help='path to white bot source file')
parser.add_argument('black_bot_path', help='path to black bot source file')
args = parser.parse_args()

for i in range(100):        
    white_bot_name, white_player_cls = load_player(args.white_bot_path)
    black_bot_name, black_player_cls = load_player(args.black_bot_path)

    winner_color, win_reason, history = play_local_game(white_player_cls(), black_player_cls())

    print('Game Over!')
    if winner_color is not None:
        print('{} won because of {}!'.format(white_bot_name if winner_color else black_bot_name, win_reason))
    else:
        print('Draw!')

    winner = 'Draw' if winner_color is None else chess.COLOR_NAMES[winner_color]
    
    print()
    print()
    
    if (winner_color == chess.WHITE and (i % 2 == 0)) or (winner_color == chess.BLACK and i % 2):
        firstBot += 1
        if winner_color == chess.WHITE:
            print("{} wins: {}".format(white_bot_name, firstBot))
            print("{} wins: {}".format(black_bot_name, secondBot))
        else:
            print("{} wins: {}".format(black_bot_name, firstBot))
            print("{} wins: {}".format(white_bot_name, secondBot))            
                
    elif (winner_color == chess.BLACK and (i % 2 == 0)) or (winner_color == chess.WHITE and i % 2):
        secondBot += 1
        if winner_color == chess.BLACK:
            print("{} wins: {}".format(white_bot_name, firstBot))
            print("{} wins: {}".format(black_bot_name, secondBot))
        else:
            print("{} wins: {}".format(black_bot_name, firstBot))
            print("{} wins: {}".format(white_bot_name, secondBot)) 
    
    print()
    print()
    
    temp = args.white_bot_path
    args.white_bot_path = args.black_bot_path
    args.black_bot_path = temp
    '''
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')

    replay_path = 'games/{}-{}-{}-{}.json'.format(white_bot_name, black_bot_name, winner, timestamp)
    print('Saving replay to {}...'.format(replay_path))
    history.save(replay_path)
    '''
white_bot_name, white_player_cls = load_player(args.white_bot_path)
black_bot_name, black_player_cls = load_player(args.black_bot_path)

print("{} Bot wins: {}".format(white_bot_name, firstBot))
print("{} Second Bot wins: {}".format(black_bot_name, secondBot))
# import sys
# sys.argv = ['test',replay_path]
# exec(open('rc-replay.py').read())