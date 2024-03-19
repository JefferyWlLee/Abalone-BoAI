#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2020 Scriptim (https://github.com/Scriptim)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This module runs a `abalone.game.Game`."""
from enum import Enum
from traceback import format_exc
from typing import Generator, List, Tuple, Union
import time, threading, os

import inquirer

from abstract_player import AbstractPlayer
from enums import Direction, Player, Space, InitialPosition, Marble
from game import Game, IllegalMoveException
from utils import line_from_to
from human_player import HumanPlayer
from random_player import RandomPlayer
import Input_board


def _get_winner(score: tuple[int, int]) -> Union[Player, None]:
    """Returns the winner of the game based on the current score.

    Args:
        score: The score tuple returned by `abalone.game.Game.get_score`

    Returns:
        Either the `abalone.enums.Player` who won the game or `None` if no one has won yet.
    """
    if 8 in score:
        return Player.WHITE if score[0] == 8 else Player.BLACK
    return None


def _format_move(turn: Player, move: Tuple[Union[Space, Tuple[Space, Space]], Direction], moves: int, time_record) -> str:
    """Formats a player's move as a string with a single line.

    Args:
        turn: The `Player` who performs the move
        move: The move as returned by `abalone.abstract_player.AbstractPlayer.turn`
        moves: The number of total moves made so far (not including this move)
    """
    marbles = [move[0]] if isinstance(move[0], Space) else line_from_to(*move[0])[0]
    marbles = map(lambda space: space.name, marbles)

    if turn is Player.BLACK:
        return (f'BLACK\n'
                f'CURRENT MOVE TIME: {time_record["cur_spend_p1"]}s\n'
                f'AGGREGATE TIME FOR BLACK: {time_record["time_spend_p1"]}s\n'
                f'TOTAL TIME FOR BOTH PLAYERS: {time_record["agg_time_spend"]}s\n'
                f'{moves + 1}: {turn.name} moves {", ".join(marbles)} in direction {move[1].name}\n')
    else:
        return (f'WHITE\n'
                f'CURRENT MOVE TIME: {time_record["cur_spend_p2"]}s\n'
                f'AGGREGATE TIME FOR WHITE: {time_record["time_spend_p2"]}s\n'
                f'TOTAL TIME FOR BOTH PLAYERS: {time_record["agg_time_spend"]}s\n'
                f'{moves + 1}: {turn.name} moves {", ".join(marbles)} in direction {move[1].name}\n')


def write_move_history_to_files(game, move, moves_history, file, file2, file3, black_move_count, white_move_count, time_record):
    file.write(_format_move(game.turn, move, len(moves_history) - 1, time_record))
    file.write('\n')

    if game.turn is Player.BLACK:
        file2.write(_format_move(game.turn, move, black_move_count, time_record))
        file2.write('\n')
    else:
        file3.write(_format_move(game.turn, move, white_move_count, time_record))
        file3.write('\n')

def end_game(game):
    """
    create a end game function. Callback after certain period of time
    """
    score = game.get_score()
    winner = _get_winner(score)
    if winner is not None:
        print(f'Time is up. {winner.name} won!')
    else:
        print(f'Time is up. BLACK {score[0]} - WHITE {score[1]} result is even')
    os._exit(1)


def timer(time_event, controller_event, max_time, game, time_record_obj):
    """
    countdown clock, pause
    """
    global time_message
    countDown = max_time

    while controller_event.is_set():
        # if countDown <= 0:
            # time-up and end game
            # score = game.get_score()
            # winner = _get_winner(score)
            # if winner is not None:
            #     print(f'Time is up. {winner.name} won!')
            # else:
            #     print(f'Time is up. BLACK {score[0]} - WHITE {score[1]} result is tie')
            # os._exit(1)

        # countdown every second
        time_event.wait()  # control pause or resume
        if time_record_obj['reset']:
            countDown = max_time
            time_record_obj['reset'] = False
        if game.turn == player.BLACK:
            time_record_obj["cur_spend_p1"] += 1
            time_record_obj["time_spend_p1"] += 1
        else:
            time_record_obj["time_spend_p2"] += 1
            time_record_obj["cur_spend_p2"] += 1
        time_record_obj["agg_time_spend"] += 1

        sys.stdout.write(f"\r[Time left for {str(game.turn).split('.')[1]}: {int(countDown / 60)}:{countDown % 60:02d}]")
        time_message = f"{int(countDown / 60)}:{countDown % 60:02d}"  # for logging of time

        if countDown > 0:
            # print(f"{game.turn} is flushing")
            sys.stdout.flush()
            countDown -= 1
        else:
            # time-up and just on hold, resume in next round
            print(f"time for {str(game.turn).split('.')[1]} is up. Game is pause. "
                  f"Possible penalty. You can still make one move.")
            countDown = max_time
            time_spend_current_round = 0
            time_event.clear()

        time.sleep(1)


    # print("clock stop completely...")


def run_game(black: AbstractPlayer, white: AbstractPlayer, initial_position, move_limit, time_limit
             , player, **kwargs) \
        -> Generator[Tuple[Game, List[Tuple[Union[Space, Tuple[Space, Space]], Direction]]], None, None]:
    """Runs a game instance and prints the progress / current state at every turn.

    Args:
        black: An `abalone.abstract_player.AbstractPlayer`
        white: An `abalone.abstract_player.AbstractPlayer`
        initial_position: The initial position of the game. One of `abalone.enums.InitialPosition`
        move_limit: The maximum number of moves that can be made before the game ends
        **kwargs: These arguments are passed to `abalone.game.Game.__init__`

    Yields:
        A tuple of the current `abalone.game.Game` instance and the move history at the start of the game and after\
        every legal turn.
    """

    moves_limit = move_limit
    moves_made = 0
    black_move_count = 0
    white_move_count = 0
    game = Game(initial_position=initial_position, first_turn=player)
    moves_history = []
    yield game, moves_history

    # time feature
    ###### testing block
    lock_selection=False
    # player 1
    time_record = {
        "cur_spend_p1": 0,
        "cur_spend_p2": 0,
        "time_spend_p1": 0,
        "time_spend_p2": 0,
        "agg_time_spend": 0,
        "reset": False
    }
    time_event1 = threading.Event()
    controller_event1 = threading.Event()
    controller_event1.set()
    t1 = threading.Thread(target=timer, args=[time_event1, controller_event1, time_limit[0],
                                              game, time_record], daemon=True)
    t1.start()
    c1 = threading.Thread(daemon=True)
    c1.start()
    time_event1.set()
    # player 2 threads
    time_event2 = threading.Event()
    time_event2.set()
    controller_event2 = threading.Event()
    controller_event2.set()
    t2 = threading.Thread(target=timer, args=[time_event2, controller_event2, time_limit[1],
                                              game, time_record], daemon=True)
    t2.start()
    c2 = threading.Thread(daemon=True)
    c2.start()
    time_event2.clear() # pause the timer for player 2 when player 1 playing
    #####

    with open("moves.txt", 'w') as file, open("black_moves.txt", 'w') as file2, open("white_moves.txt", 'w') as file3:
        while True:
            score = game.get_score()
            score_str = f'BLACK {score[0]} - WHITE {score[1]}'
            print(score_str, game, '', sep='\n')

            winner = _get_winner(score)
            if winner is not None:
                print(f'{winner.name} won!')
                break

            try:
                move = black.turn(game, moves_history, lock_selection) if game.turn is Player.BLACK else \
                    white.turn(game, moves_history, lock_selection)


                # turn change. Timer for 2nd opponent create on first move only
                if not move == 'pause' and not move == 'resume':

                    # if turn is player1
                    if(game.turn == Player.WHITE):
                        time_event1.clear()
                        time_event2.set()
                        time_record["cur_spend_p1"] = 0
                    else:
                        time_event2.clear()
                        time_event1.set()
                        time_record["cur_spend_p2"] = 0
                    time_record['reset'] = True
                if move == 'undo':
                    if len(moves_history) == 0:
                        print('Cannot undo the first move\n')
                        continue
                    game.undo()
                    moves_history.pop()
                    moves_made -= 1
                    print('Undone last move\n')
                    continue
                if move == 'undo self':
                    if len(moves_history) < 2:
                        print('Cannot undo the first move\n')
                        continue
                    game.undo()
                    game.undo()
                    moves_history.pop()
                    moves_history.pop()
                    moves_made -= 2
                    print('Undone last two moves\n')
                    continue
                if move == 'pause':
                    time_event1.clear()
                    time_event2.clear()
                    lock_selection=True
                    print("The game has been paused!\n")
                    continue
                if move == 'resume':
                    if (game.turn == Player.WHITE):
                        time_event1.set()
                    else:
                        time_event2.set()
                    lock_selection = False
                    print("The game is resumed.\n")
                    continue

                print(_format_move(game.turn, move, len(moves_history), time_record), end='\n\n')

                moves_history.append(move)

                write_move_history_to_files(game, move, moves_history, file, file2, file3, black_move_count,
                                            white_move_count, time_record)

                if game.turn is Player.BLACK:
                    black_move_count += 1
                else:
                    white_move_count += 1

                # print(f"test show: {time_message}")  # can show time in anywhere of the code
                print(f"~~current time spend Black: {time_record['cur_spend_p1']}, "
                      f"agg time spend Black: {time_record['time_spend_p1']}, "
                      f"current time spend White: {time_record['cur_spend_p2']}, "
                      f"agg time spend White: {time_record['time_spend_p2']} "
                      f"agg time all players: {time_record['agg_time_spend']}~~")

                game.move(*move)
                game.switch_player()

                moves_made += 1
                if moves_made >= moves_limit:
                    print(f"Moves limit reached. {moves_limit} moves have been made.")
                    end_game(game)
                    break
                yield game, moves_history
            except IllegalMoveException as ex:
                print(f'{game.turn.name}\'s tried to perform an illegal move ({ex})\n')
                break
            except:
                print(f'{game.turn.name}\'s move caused an exception\n')
                print(format_exc())
                break


if __name__ == '__main__':  # pragma: no cover
    # Run a game from the command line with default configuration.
    import importlib
    import sys

    # if len(sys.argv) != 3:
    #     sys.exit(1)

    game_mode = inquirer.prompt([
        inquirer.List('game_mode',
                      message='What type layout do you want?',
                      choices=['Standard', 'German Daisy', 'Belgian Daisy', 'Test']
                      )
    ])['game_mode']

    player= Player.BLACK

    if game_mode == 'Standard':
        game = InitialPosition.DEFAULT
    elif game_mode == 'German Daisy':
        game = InitialPosition.GERMAN_DAISY
    elif game_mode == 'Belgian Daisy':
        game = InitialPosition.BELGIAN_DAISY
    else:
        file = input("Enter the file name to test from: ")
        board_state = Input_board.InputBoard(file)
        game = board_state
        if board_state.current_player == 'b':
            player = Player.BLACK
        else:
            player = Player.WHITE

    player1 = inquirer.prompt([
        inquirer.List('player1',
                      message='Who do you want to be Black?',
                      choices=['Player', 'Computer(Random)']
                      )
    ])['player1']

    if player1 == 'Player':
        black = HumanPlayer()
    else:
        black = RandomPlayer()

    player2 = inquirer.prompt([
        inquirer.List('player2',
                      message='Who do you want to be White?',
                      choices=['Player', 'Computer(Random)']
                      )
    ])['player2']


    if player2 == 'Player':
        white = HumanPlayer()
    else:
        white = RandomPlayer()



    while(True):
        try:
            move_limit = int(input("Enter the move limit per player: "))
            if move_limit > 0:
                move_limit = move_limit * 2
                break
            else:
                print("Invalid input, please enter a positive number")
        except:
            print("Invalid input, please enter number")

    while (True):
        try:
            black_time_limit = int(input("Enter the time limit for Black in minutes: "))
            white_time_limit = int(input("Enter the time limit for White in minutes: "))
            if white_time_limit > 0 or black_time_limit > 0:
                white_time_limit = white_time_limit * 60
                black_time_limit = black_time_limit * 60
                time_limit = (white_time_limit, black_time_limit)
                break
            else:
                print("Invalid input, please enter a positive number")
        except:
            print("Invalid input, please enter number")



    # Run the game with these player instances and an initial game position
    list(run_game(black, white, initial_position=game, move_limit=move_limit, time_limit=time_limit, player=player))