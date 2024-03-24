# -*- coding: utf-8 -*-


"""This module is a template for create AI player"""
from random import choice
from typing import List, Tuple, Union

from abstract_player import AbstractPlayer
from enums import Space, Direction
from game import Game


class AiPlayerJeffrey(AbstractPlayer):
    def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]], selection_lock: bool) \
            -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:

        legal_moves = list(game.generate_legal_moves())

        for legal_move in legal_moves:
            print(legal_move) # e.g. (<Space.I9: ('I', '9')>, <Direction.SOUTH_WEST: 'south-west'>)
            print(legal_moves[0][0]) #Space.G5
            print(legal_moves[0][1]) #Direction.EAST

        # our ai code is here....
        #1. minimax with alpha-beta pruning
        #2. heuristic evaluation function
        #3. choice of:
        #   a. node ordering
        #   b. transposition tables
        #   c. quiescence search

        return choice(legal_moves)
