# -*- coding: utf-8 -*-


"""This module is a template for create AI player"""
from random import choice
from copy import deepcopy
from typing import List, Tuple, Union

from abstract_player import AbstractPlayer
from enums import Space, Direction, Player, Marble
from game import Game
from utils import line_from_to, line_to_edge, neighbor
import math



class AiPlayerKevin(AbstractPlayer):
    # 1. minimax with alpha-beta pruning
    # 2. heuristic evaluation function
    # 3. choice of:
    #   a. node ordering
    #   b. transposition tables
    #   c. quiescence search


    def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]], selection_lock: bool) \
            -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:

        return self._game_analytic(game)

        # ai_move = self._aplpha_beta_search(game, max_depth, 1, "all")
        # ai_move = self._aplpha_beta_search(game, max_depth, 2, "all")


    def _game_analytic(self, game):

        ai_move = ()
        max_depth = 0

        # if len(game.previous_boards) < 20:
        if len(game.previous_boards) < 0:
            # ai_move = self._aplpha_beta_search(game, max_depth, 1, "all")
            ai_move = self._aplpha_beta_search(game, max_depth, 1, "inline")
            # print("strategy 1")
        else:
            ai_move = self._aplpha_beta_search(game, 0, 2, "inline")
            # print("strategy 2")


        # ###### temp use attack
        # ai_move = self._aplpha_beta_search(game, 0, 2, "inline")
        # print("strategy 2")
        # #######

        return ai_move

    def _aplpha_beta_search(self, game, max_depth, strategy, tactic):
        tmp_score_move_list = []

        vgame = deepcopy(game)
        game.previous_scores = []
        game.previous_scores.append(game.get_score())
        move_list = self._sort_moves(list(game.generate_legal_moves()), game, tactic)
        for move in move_list:
            vgame = self._next_virtual_game(game, move)
            # score = self._max_value(vgame, move, max_depth, strategy, alpha=-math.inf, beta=math.inf)
            score = self._max_value(vgame, move, max_depth, strategy, tactic, alpha=-math.inf, beta=math.inf)

            # print(f"{score}: {move}")
            # del vgame

            tmp_score_move_list.append({"score": score, "move": move})



            # if score > current_score:
            #     best_move = move
            # current_score = score
        max_score = max(tmp_score_move_list, key=lambda x: x['score'])['score']
        higest_score_list = list(filter(lambda y: y['score'] == max_score, tmp_score_move_list))
        move_set = choice(higest_score_list)
        best_move = move_set['move']
        current_score = move_set['score']

        for a in tmp_score_move_list:
            print(a)
        print(f"best score: {current_score} - best move: {best_move}")
        return best_move

    def _max_value(self, vgame, move, max_depth, strategy, tactic, alpha, beta):
        # receive each move, evaluate the value of current move


        if max_depth == 0:
            return self.heuristic_strategies(strategy, move, vgame)

        max_depth -= 1
        score = -math.inf
        vgame.previous_scores.append(vgame.get_score())

        next_move_list = self._sort_moves(list(vgame.generate_legal_moves()), vgame, tactic)

        #minmax search
        for move in next_move_list:
            # print(f"max turn: {vgame.turn}, depth: {max_depth} - {move}")
            vgame.move(move[0], move[1])
            score = self._min_value(vgame, move, max_depth, strategy, tactic, alpha, beta)
            vgame.board = vgame.previous_boards.pop()
            score = max(score, alpha)
            if score > beta:
                # pruning
                # print(f"max pruned")
                return score

            alpha = max(alpha, score)
            # print(f"max_score: {score}, depth: {max_depth} move: {move}")
        return score

    def _min_value(self, vgame, move, max_depth, strategy, tactic, alpha, beta):
        # receive each move, evaluate the value of current move

        if max_depth == 0:
            return self.heuristic_strategies(strategy, move, vgame)

        max_depth -= 1
        score = math.inf
        vgame.previous_scores.append(vgame.get_score())

        next_move_list = self._sort_moves(list(vgame.generate_legal_moves()), vgame, tactic)

        # minmax search
        for move in next_move_list:
            # print(f"min turn: {vgame.turn} - {move}")
            vgame.move(move[0], move[1])
            score = self._max_value(vgame, move, max_depth, strategy, tactic, alpha, beta)
            vgame.board = vgame.previous_boards.pop()
            score = min(score, beta)
            if score < alpha:
                # pruning
                # print(f"min pruned")
                return score

            beta = min(beta, score)

        return score

    def heuristic_strategies(self, strategy_number, move, game):

        if strategy_number == 1:
            # defense first, score base on position
            # return score of each space
            score = {
                "I5": -100, "I6": -100, "I7": -100, "I8": -100, "I9": -100,
                "H4": -100, "H5": 1, "H6": 1, "H7": 1, "H8": 1, "H9": -100,
                "G3": -100, "G4": 1, "G5": 5, "G6": 5, "G7": 5, "G8": 1, "G9": -100,
                "F2": -100, "F3": 1, "F4": 25, "F5": 31, "F6": 31, "F7": 25, "F8": 1, "F9": -100,
                "E1": -100, "E2": 1, "E3": 25, "E4": 31, "E5": 31, "E6": 31, "E7": 31, "E8": 0, "E9": -100,
                "D1": -100, "D2": 1, "D3": 25, "D4": 31, "D5": 31, "D6": 25, "D7": 1, "D8": -100,
                "C1": -100, "C2": 1, "C3": 5, "C4": 5, "C5": 5, "C6": 1, "C7": -100,
                "B1": -100, "B2": 1, "B3": 1, "B4": 1, "B5": 1, "B6": -100,
                "A1": -100, "A2": -100, "A3": -100, "A4": -100, "A5": -100
                     }

            # boardside move, score are the sum of all marbles. For inline move, there is only one tuple
            sum = 0

            # tmp_sum=0
            # space_name = ['I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
            # for i, value in enumerate(game.board):
            #     for j in value:
            #             print(j)
            #         # if game.board[i][j].name == 'BLACK' or game.board[i][j].name == 'WHITE':
            #         #     space_modifier = j
            #         #     if space_name[i] == 'F':2
            #         #         space_modifier = j + 1
            #         #     elif space_name[i] == 'G':
            #         #         space_modifier = j + 2
            #         #     elif space_name[i] == 'H':
            #         #         space_modifier = j + 3
            #         #     elif space_name[i] == 'I':
            #         #         space_modifier = j + 4

            #             tmp_sum += score[space_name[i] + str(j)]

                        # print(f"{space_name[i] + str(space_modifier+1)}: {score[space_name[i] + str(space_modifier+1)]}")

                        # tmp_sum += score[space_name[i] + str(j)]

            for space in enumerate(Space):
                # print(type(space[1]))
                # print(str(space[1].name))
                test = str(space[1].name)
                # print(test)

                if test != "OFF" and game.get_marble(space[1]) != Marble.BLANK:
                    sum += score[test]

                # print(score[test])
                # tmp_sum += score[str(space[1].name)]



            # if isinstance(move[0], tuple):
            #     for marble in move[0]:
            #         # sum += score[marble.value[0] + marble.value[1]]
            #         sum += score[neighbor(marble, move[1]).name]

            #         # extra function to push marbles on rim to move to center
            #         # if game.turn == Player.BLACK and (marble.value[0] == 'A' or marble.value[0] == 'B'):
            #         #     sum += 80
            #         # elif game.turn == Player.WHITE and (marble.value[0] == 'I' or marble.value[0] == 'H'):
            #         #     sum += 80
            # else:
            #     sum = score[neighbor(move[0], move[1]).name]
            #     if game.turn == Player.BLACK and (move[0].value[0] == 'A' or move[0].value[0] == 'B'):
            #         if move[1].value == 'north-east' or move[1].value == 'north-west':
            #             sum += 1
            #     elif game.turn == Player.WHITE and (move[0].value[0] == 'I' or move[0].value[0] == 'H'):
            #         if move[1].value == 'south-east' or move[1].value == 'south-west':
            #             sum += 1



            # print(f"[STRATEGY] sum: {sum}, move: {move}")
            return sum

        elif strategy_number == 2:

            score = 0

            # Dodge Move
            # Priority just below killing move, score 8999. If there is a way to kill, kill first,
            # but if not prevent being kill is higher priority than others.
            # -----method-----
            # For current move:
            # 1. is the marble/marbles is on rim (possible being kill)? if not, skip
            # 2. are there opponent marbles in the line of move? if yes, skip (this move is blocked)
            # 3. are there 2+ opponent marbles lining up around us (possible being sumito)?
            #        Yes -> in danger chose this move
            #        No -> skip
            # (extra) more than one way to choice?
            third_rim = ["G5", "G6", "G7", "F4", "F7", "E3", "E7", "D3", "D6", "C3", "C4", "C5"]
            inner_rim = ["H5", "H6", "H7", "H8", "B2", "B3", "B4", "B5", "G4", "F3", "E2",
                         "D2", "C2", "G8", "F8", "E8", "D7", "C6"]
            outer_rim = ["I5", "I6", "I7", "I8", "I9", "A1", "A2", "A3", "A4", "A5",
                         "H4", "G3", "F2", "E1", "D1", "C1", "B1", "H9", "G9", "F9", "E9", "D8", "C7", "B6"]


            if move[0].name in outer_rim:     #1
                dodge_line = line_to_edge(move[0], move[1])
                if self.get_privous_board_marble(game, dodge_line[1]) == Marble.BLANK:  #2
                    # scan all directions
                    directions = [Direction.EAST, Direction.SOUTH_EAST, Direction.SOUTH_WEST, Direction.WEST, Direction.NORTH_WEST, Direction.NORTH_EAST]
                    for direction in directions:
                        dodge_line = line_to_edge(move[0], direction)
                        # next two spaces is opponent in this direction
                        if len(dodge_line) > 2 and (self._is_opponent_marble(game, dodge_line[1]) and self._is_opponent_marble(game, dodge_line[2])):  #3
                            score = 8999
                            print(f"Possible Dodge! {move}")
                            break






            # NOTE: EVEN depth=0, THE MOVE IS ALREADY MADE. AND ANY MORE DEPTH IS MOVING FURTHER!

            # hyper-aggressive, score base on push a marble to side
            # shortest distance to opponent two or smaller marbles



            # 1. right before any moves, if current move can kill. This is the first priority amoung all
            if (game.turn == Player.BLACK and game.previous_scores[0][1] > game.get_score()[1]) or \
                    (game.turn == Player.WHITE and game.previous_scores[0][0] > game.get_score()[0]):
                # there is a score differnece meaning an opponent marble is killed by this move
                score += 10000
                return score

            # 2. Second priority, arrange score according to how close the opponent marble to being kill
            # ANALYSIZING ON THE MOVE OF CURRENT DEPTH
            # if the opponent marble will be killed by next round score +6000
            # if the opponent marble will be killed by two round score +3000
            # if require three round score + 1500 (balance with defence strategy?)
            # if require four round, it is just random pushing marbles around, no addition score

            # if the move is 2 marbles only, deduct 1000. (3 marble move is more valuable than 2 marble moves
            if not isinstance(move[0], tuple):
                # check if the next position of the move contain opponent marble
                # third_rim = ["G5", "G6", "G7", "F4", "F7", "E3", "E7", "D3", "D6", "C3", "C4", "C5"]
                # inner_rim = ["H5", "H6", "H7", "H8", "B2", "B3", "B4", "B5", "G4", "F3", "E2",
                #              "D2", "C2", "G8", "F8", "E8", "D7", "C6"]
                # outer_rim = ["I5", "I6", "I7", "I8", "I9", "A1", "A2", "A3", "A4", "A5",
                #              "H4", "G3", "F2", "E1", "D1", "C1", "B1", "H9", "G9", "F9", "E9", "D8", "C7", "B6"]

                line = line_to_edge(move[0], move[1])
                own_marbles_num, opp_marbles_num = game._inline_marbles_nums(line[1:])
                if opp_marbles_num > 0:

                    # check if our marble outnumber opponent marble
                    if own_marbles_num > opp_marbles_num:
                        # check whether there is a blocking marble on the way, if not, this is a valuable sumito move
                        # example: after first white, there is another black on the road

                        # First find the empty space right after the opponent marble
                        possible_space_to_push = neighbor(line[own_marbles_num + opp_marbles_num-1], move[1])
                        # if possible_space_to_push is not None:
                        #     # case when it is not Space.OFF
                        #     score += 1000
                        if possible_space_to_push.name in third_rim:
                            score += 1500
                        if possible_space_to_push.name in inner_rim:
                            score += 3000
                        if possible_space_to_push.name in outer_rim:
                            score += 6000

                        if opp_marbles_num > 1:
                            score += 500

                        # two marbles move reduction
                        if own_marbles_num < 3:
                            score -= 1000
                    else:
                        # A space in between but meaningless move, it shouldn't be choosen
                        score -= 999

            else:
                # boardside moves
                distance_to_opp_marble = 99
                have_oppoment_marble = False
                for i in range(0, len(move[0])):
                    curr_distance_to_opp_marble = 0
                    exam_line = line_to_edge(move[0][i], move[1])
                    for space in exam_line:
                        if game.get_marble(space) == Marble.BLANK:
                            curr_distance_to_opp_marble += 1

                        if self._is_opponent_marble(game, space):
                            have_oppoment_marble = True

                    if curr_distance_to_opp_marble < distance_to_opp_marble:
                        distance_to_opp_marble = curr_distance_to_opp_marble

                if have_oppoment_marble:
                    # print(distance_to_opp_marble)
                    score = (10 - distance_to_opp_marble) * 100
                else:
                    score = -100

            if score <= 0:
                score = self.heuristic_strategies(1, move, game)

            return score

        else:
            pass

    def _sort_moves(self, moves, game, tactic="partial"):
        boardside_moves = []
        inline_multiple_marbles_moves = []
        single_marble_moves = []

        for legal_move in moves:
            if isinstance(legal_move[0], tuple):
                # (<Space.C4: ('C', '4')>, <Space.C5: ('C', '5')>), <Direction.NORTH_WEST: 'north-west'>)
                # boardside move only
                boardside_moves.append(legal_move)

            else:
                own_marbles_num, null = game._inline_marbles_nums(line_to_edge(legal_move[0], legal_move[1]))
                if isinstance(legal_move[0], Space) and own_marbles_num > 1:
                    # baseline move of 2 or 3 marbles. Possible Sumito moves
                    inline_multiple_marbles_moves.append(legal_move)

                else:
                    # single marble moves
                    single_marble_moves.append(legal_move)

        # for legal_move in moves:
        #     if not isinstance(legal_move[0], tuple):
                # (<Space.A1: ('A', '1')>, <Direction.NORTH_EAST: 'north-east'>
                # sorted_moves.append(legal_move)
                # inline_moves.append(legal_move)

        if tactic == "partial":
            # return boardside_moves[0:5]
            return boardside_moves + single_marble_moves
        elif tactic == "inline":
            return inline_multiple_marbles_moves + single_marble_moves
        else:
            return inline_multiple_marbles_moves + boardside_moves + single_marble_moves

    def _next_virtual_game(self, game, move):
            vitual_board = deepcopy(game)
            vitual_board.move(move[0], move[1])
            return vitual_board

    def _is_opponent_marble(self, game, space):
        if game.turn == Player.BLACK:
            if game.get_marble(space) == Marble.BLACK or game.get_marble(space) == Marble.BLANK:
                return False
            else:
                return True
        else:
            if game.get_marble(space) == Marble.WHITE or game.get_marble(space) == Marble.BLANK:
                return False
            else:
                return True

    def get_privous_board_marble(self, game, space: Space) -> Marble:

        xs = ['I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
        ys = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        if space is Space.OFF:
            raise Exception('Cannot get state of `Space.OFF`')

        x = xs.index(space.value[0])
        y = ys.index(space.value[1])

        if x <= 3:
            y -= 4 - x

        # x, y = _space_to_board_indices(space)

        return game.previous_boards[0][x][y]