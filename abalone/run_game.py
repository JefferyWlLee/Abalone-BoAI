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

from traceback import format_exc
from typing import Generator, List, Tuple, Union
import time, threading, os

import inquirer

from abstract_player import AbstractPlayer
from enums import Direction, Player, Space, InitialPosition
from game import Game, IllegalMoveException
from utils import line_from_to
from human_player import HumanPlayer
from random_player import RandomPlayer


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


def abalone_instructions():
    print("""
    ABALONE INSTRUCTIONS:
    
        OBJECTIVE
           The objective of Abalone is to push six of your opponent's marbles off the board.
        
        SETUP
           The game is played on a hexagonal board consisting of 61 circular spaces.
           Each player has 14 marbles of their color placed in a predetermined pattern at opposite ends of the board.
           Players can choose either black or white marbles.
        
        MOVEMENT
           Players take turns moving their marbles.
           A player can move one, two, or three adjacent marbles in a straight line in any direction (forward, backward, or sideways).
           A move can be made by pushing your own marbles or opponent's marbles.
           A single marble can push one or two marbles of the opponent's color.
           The direction of the push must be the same as the direction of the move.
           Diagonal movement is not allowed.
        
        WINNING
           The game is won by the player who first successfully pushes six of their opponent's marbles off the board.
           If a player has fewer than six marbles remaining, they lose the game.
        
        VARIATIONS
           Abalone can be played with different board sizes, variations in starting positions, and alternative rulesets.
    """)

    input("Enter any key to return to the main menu.")
    if input:
        abalone_menu()


def about_abalone():
    print("?")

    input("Enter any key to return to the main menu.")
    if input:
        abalone_menu()


def abalone_menu():
    print("""
           _           _                  
      __ _| |__   __ _| | ___  _ __   ___ 
     / _` | '_ \ / _` | |/ _ \| '_ \ / _ \\
    | (_| | |_) | (_| | | (_) | | | |  __/
     \__,_|_.__/ \__,_|_|\___/|_| |_|\___|
    
    Welcome to Abalone!
        
        1. Start Game
        2. Instructions
        3. About
        4. Exit
    """)

    option = None

    while option not in [1, 2, 3, 4]:
        try:
            option = int(input("Enter choice: "))
            print()
            if option == 1:
                # Run a game from the command line with default configuration.
                import importlib
                import sys

                if len(sys.argv) != 3:
                    sys.exit(1)
                black = sys.argv[1].rsplit('.', 1)
                black = getattr(importlib.import_module(black[0]), black[1])
                white = sys.argv[2].rsplit('.', 1)
                white = getattr(importlib.import_module(white[0]), white[1])
                list(run_game(black(), white()))
            elif option == 2:
                abalone_instructions()
            elif option == 3:
                about_abalone()
            elif option == 4:
                exit()
            else:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid option.\n")


def _format_move(turn: Player, move: Tuple[Union[Space, Tuple[Space, Space]], Direction], moves: int) -> str:
    """Formats a player's move as a string with a single line.

    Args:
        turn: The `Player` who performs the move
        move: The move as returned by `abalone.abstract_player.AbstractPlayer.turn`
        moves: The number of total moves made so far (not including this move)
    """
    marbles = [move[0]] if isinstance(move[0], Space) else line_from_to(*move[0])[0]
    marbles = map(lambda space: space.name, marbles)
    return f'{moves + 1}: {turn.name} moves {", ".join(marbles)} in direction {move[1].name}'


def write_move_history_to_files(game, move, moves_history, file, file2, file3, black_move_count, white_move_count):
    file.write(_format_move(game.turn, move, len(moves_history)))
    file.write('\n')

    if game.turn is Player.BLACK:
        file2.write(_format_move(game.turn, move, black_move_count))
        file2.write('\n')
    else:
        file3.write(_format_move(game.turn, move, white_move_count))
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


def timer(time_event, controller_event, max_time, game):
    """
    countdown clock, pause
    """
    countDown = max_time
    while controller_event.is_set():
        if countDown <= 1:
            # time-up and end game
            score = game.get_score()
            winner = _get_winner(score)
            if winner is not None:
                print(f'Time is up. {winner.name} won!')
            else:
                print(f'Time is up. BLACK {score[0]} - WHITE {score[1]} result is tie')
            os._exit(1)

        # countdown every second
        time_event.wait()  # control pause or resume
        sys.stdout.write(f"\r[Time left: {int(countDown / 60)}:{countDown % 60:02d}]")
        sys.stdout.flush()
        countDown -= 1
        time.sleep(1)
    print("clock stop completely...")


def run_game(black: AbstractPlayer, white: AbstractPlayer, initial_position, move_limit, time_limit, **kwargs) \
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
    black_count = 0
    white_count = 0
    game = Game(initial_position=initial_position)
    moves_history = []
    yield game, moves_history

    # time feature
    ###### testing block
    MAX_TIME = time_limit
    time_event = threading.Event()
    time_event.set()
    controller_event = threading.Event()
    controller_event.set()
    t = threading.Thread(target=timer, args=[time_event, controller_event, MAX_TIME, game])
    t.start()
    c = threading.Thread()
    c.start()
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
                move = black.turn(game, moves_history) if game.turn is Player.BLACK else white.turn(game, moves_history)

                write_move_history_to_files(game, move, moves_history, file, file2, file3, black_count, white_count)

                if game.turn is Player.BLACK:
                    black_count += 1
                else:
                    white_count += 1

                # reset the timer
                if not move == 'pause' and not move == 'resume':
                    controller_event.clear()
                    t.join()  # destroy the timer thread
                    controller_event.set()
                    # start another timer for opponent
                    t = threading.Thread(target=timer, args=[time_event, controller_event, MAX_TIME, game])
                    t.start()

                if move == 'undo':
                    if len(moves_history) == 0:
                        print('Cannot undo the first move\n')
                        continue
                    game.undo()
                    moves_history.pop()
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
                    print('Undone last two moves\n')
                    continue
                if move == 'pause':
                    time_event.clear()
                    print("The game has been paused!\n")
                    continue
                if move == 'resume':
                    time_event.set()
                    print("The game is resumed.\n")
                    continue

                print(_format_move(game.turn, move, len(moves_history)), end='\n\n')

                game.move(*move)
                game.switch_player()
                moves_history.append(move)
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
    # # Run a game from the command line with default configuration.
    # import importlib
    # import sys
    #
    # if len(sys.argv) != 3:
    #     sys.exit(1)
    # black = sys.argv[1].rsplit('.', 1)
    # black = getattr(importlib.import_module(black[0]), black[1])
    # white = sys.argv[2].rsplit('.', 1)
    # white = getattr(importlib.import_module(white[0]), white[1])
    # list(run_game(black(), white()))

    game_mode = inquirer.prompt([
        inquirer.List('game_mode',
                      message='What type layout do you want?',
                      choices=['Standard', 'German Daisy', 'Belgian Daisy']
                      )
    ])['game_mode']

    if game_mode == 'Standard':
        game = InitialPosition.DEFAULT
    elif game_mode == 'German Daisy':
        game = InitialPosition.GERMAN_DAISY
    else:
        game = InitialPosition.BELGIAN_DAISY

    versus_mode = inquirer.prompt([
        inquirer.List('versus_mode',
                      message='What type of game do you want?',
                      choices=['Player vs Player', 'Player vs Computer', 'Computer vs Computer']
                      )
    ])['versus_mode']

    if versus_mode == 'Player vs Player':
        black = HumanPlayer()
        white = HumanPlayer()
    elif versus_mode == 'Player vs Computer':
        black = HumanPlayer()
        white = RandomPlayer()
    else:
        black = RandomPlayer()
        white = RandomPlayer()

    while (True):
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
            time_limit = int(input("Enter the time limit per player in minutes: "))
            if time_limit > 0:
                time_limit = time_limit * 60
                break
            else:
                print("Invalid input, please enter a positive number")
        except:
            print("Invalid input, please enter number")

    # Run the game with these player instances and an initial game position
    list(run_game(black, white, initial_position=game, move_limit=move_limit, time_limit=time_limit))
