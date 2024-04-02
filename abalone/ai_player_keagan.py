# -*- coding: utf-8 -*-


"""This module is a template for create AI player"""
from random import choice
from typing import List, Tuple, Union

from abstract_player import AbstractPlayer
from enums import Marble, Player, Space, Direction
from game import Game




class AiPlayerKeagan(AbstractPlayer):


    def minimax(self, game, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            # if there is more than 5 seconds remaining iterate another level
            return self.heuristic_evaluation(game)
        
        if maximizingPlayer:
            maxEval = float('-inf')
            for move in game.generate_legal_moves():
                eval = self.minimax(game, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for move in game.generate_legal_moves():
                eval = self.minimax(game, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
        
    def heuristic_evaluation(self, game):
        value = 0
        marble = Marble.WHITE if game.turn is Player.WHITE else Marble.BLACK
        enemy = Marble.BLACK if game.turn is Player.WHITE else Marble.WHITE
        for space in Space:
            if space is marble:
                value += 10
            elif space == enemy:
                value -= 10

        # move as many marbles per turn as possible
        
        return value
    
    def take_best_move(self, game, legal_moves):
        best_move = None
        best_value = float('-inf')
        for move in legal_moves:
            value = self.minimax(game, 1, float('-inf'), float('inf'), False)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move

    def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]], selection_lock: bool) \
            -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:

        legal_moves = list(game.generate_legal_moves())

        # for legal_move in legal_moves:
            # print(legal_move) # e.g. (<Space.I9: ('I', '9')>, <Direction.SOUTH_WEST: 'south-west'>)
            # print(legal_moves[0][0]) #Space.G5
            # print(legal_moves[0][1]) #Direction.EAST

            

        # our ai code is here....
        #1. minimax with alpha-beta pruning


        #2. heuristic evaluation function

        #3. choice of:
        #   a. node ordering
        #   b. transposition tables
        #   c. quiescence search
            
        hueristic_choice = self.take_best_move(game, legal_moves)

        return hueristic_choice
