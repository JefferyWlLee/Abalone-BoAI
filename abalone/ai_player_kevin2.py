# -*- coding: utf-8 -*-


"""This module is a template for create AI player"""
from enum import Enum
from random import choice
from copy import deepcopy
import time
from typing import List, Tuple, Union

from abstract_player import AbstractPlayer
from enums import Space, Direction, Player, Marble
from game import Game
from utils import line_from_to, line_to_edge, neighbor
import math

class AiGame:
    def __init__(self, game: Union[Game, List], current_player: Player) -> None:
        # print(type(game))
        if (type(game) == Game):
            self.array = game.board
        else:
            self.array = game

        self.current_player = current_player

        self.current_marble = self.get_marble(current_player)
        self.opponent_marble = self.get_marble(self.get_other_player())

        self.opponent = self.get_other_player()

        # array looks like this
        # [
        #     [ M, M, M, M, M ],
        #     [ M, M, M, M, M, M ],
        #     [ M, M, M, M, M, M, M ],
        #     [ M, M, M, M, M, M, M, M ],
        #     [ M, M, M, M, M, M, M, M, M ],
        #     [ M, M, M, M, M, M, M, M ],
        #     [ M, M, M, M, M, M, M ],
        #     [ M, M, M, M, M, M ],
        #     [ M, M, M, M, M ]
        # ]
        self.current_player = current_player

    def get_other_player(self):
        if self.current_player == Player.BLACK:
            return Player.WHITE
        else:
            return Player.BLACK
        
    def get_marble(self, player):
        if player == Player.BLACK:
            return Marble.BLACK
        else:
            return Marble.WHITE

    def generate_marble_moves(self, space: Tuple):
        legal_moves = []
        row, col = space

        spaces = (
            (0,0), (0,1), (0,2), (0,3), (0,4),
            (1,0), (1,1), (1,2), (1,3), (1,4), (1,5),
            (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6),
            (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7),
            (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8),
            (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7),
            (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6),
            (7,0), (7,1), (7,2), (7,3), (7,4), (7,5),
            (8,0), (8,1), (8,2), (8,3), (8,4))

        modifications = [(-1, -1), (0, -1), (-1, 0), (1, 0), (-1, 1), (0, 1)]

        for mod in modifications:
            #check if the next space is on the board (M*)
            # print(f"row: {row}, col: {col}, mod: {mod}")
            if (row+mod[0], col+mod[1]) in spaces:
                # print("test")
                # check if empty, then move (M_)
                if self.array[row+mod[0]][col+mod[1]] == Marble.BLANK:
                    pass
                #     array = deepcopy(self.array)
                #     array[row+mod[0]][col+mod[1]] = self.current_marble
                #     array[row][col] = Marble.BLANK
                #     # print("test1")
                #     legal_moves.append(array)

                # # check if second own color marble (MM)
                elif self.array[row+mod[0]][col+mod[1]] == self.current_marble:
                #     # print("test2")
                #     #broadside move the two to empty, don't create dups, maybe call a function for this

                #     # check if the next space is on the board (MM*)
                    if (row+mod[0]*2, col+mod[1]*2) in spaces:
                #         #check if the next marble is empty (MM_)
                        if self.array[row+mod[0]*2][col+mod[1]*2] == Marble.BLANK:
                            pass
                #             array = deepcopy(self.array)
                #             array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                #             array[row+mod[0]][col+mod[1]] = self.current_marble
                #             array[row][col] = Marble.BLANK
                #             # print("test2")
                #             legal_moves.append(array)
                #         #check if the next marble contains an enemy marble (MME)
                #         elif self.array[row+mod[0]*2][col+mod[1]*2] == self.opponent:
                #             #check if we can push the enemy marble to another spot on the board (MME_)
                #             if (row+mod[0]*3, col+mod[1]*3) in spaces and self.array[row+mod[0]*3][col+mod[1]*3] == Marble.BLANK:
                #                 array = deepcopy(self.array)
                #                 array[row+mod[0]*3][col+mod[1]*3] = self.opponent
                #                 array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                #                 array[row+mod[0]][col+mod[1]] = self.current_marble
                #                 array[row][col] = Marble.BLANK
                #                 # print("test3")
                #                 legal_moves.append(array)
                #             #check if we can push the enemy marble off the board (MMEX)
                #             elif (row+mod[0]*3, col+mod[1]*3) not in spaces:
                #                 array = deepcopy(self.array)
                #                 array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                #                 array[row+mod[0]][col+mod[1]] = self.current_marble
                #                 array[row][col] = Marble.BLANK
                #                 # print("test4")
                #                 legal_moves.append(array)
                        #check if third own color marble (MMM)
                        elif self.array[row+mod[0]*2][col+mod[1]*2] == self.current_marble:
                            #broadsidemove the three to empty, don't create dups, maybe call a function for this

                            # check if we can consider the next marble in direction (MMM*)
                            if (row+mod[0]*3, col+mod[1]*3) in spaces:
                                #check if the next marble is empty (MMM_)
                                if self.array[row+mod[0]*3][col+mod[1]*3] == Marble.BLANK:
                                    array = deepcopy(self.array)
                                    array[row+mod[0]*3][col+mod[1]*3] = self.current_marble
                                    array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                                    array[row+mod[0]][col+mod[1]] = self.current_marble
                                    array[row][col] = Marble.BLANK
                                    # print("test5")
                                    legal_moves.append(array)
                                #check if the next marble contains an enemy marble (MMME)
                                elif self.array[row+mod[0]*3][col+mod[1]*3] == self.opponent:
                                    #check if the marble after 3 friendly's and an enemy exists (MMME*)
                                    if (row+mod[0]*4, col+mod[1]*4) in spaces:
                                        #check if it is empty (MMME_)
                                        if self.array[row+mod[0]*4][col+mod[1]*4] == Marble.BLANK:
                                            array = deepcopy(self.array)
                                            array[row+mod[0]*4][col+mod[1]*4] = self.opponent
                                            array[row+mod[0]*3][col+mod[1]*3] = self.current_marble
                                            array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                                            array[row+mod[0]][col+mod[1]] = self.current_marble
                                            array[row][col] = Marble.BLANK
                                            # print("test6")
                                            legal_moves.append(array)
                                        #check if it is another enemy marble and the marble after that is empty (MMMEE_)
                                        elif self.array[row+mod[0]*4][col+mod[1]*4] == self.opponent and (row+mod[0]*5, col+mod[1]*5) in AiSpace.spaces and self.array[row+mod[0]*5][col+mod[1]*5] == Marble.BLANK:
                                            array = deepcopy(self.array)
                                            array[row+mod[0]*5][col+mod[1]*5] = self.opponent
                                            array[row+mod[0]*4][col+mod[1]*4] = self.opponent
                                            array[row+mod[0]*3][col+mod[1]*3] = self.current_marble
                                            array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                                            array[row+mod[0]][col+mod[1]] = self.current_marble
                                            array[row][col] = Marble.BLANK
                                            # print("test7")
                                            legal_moves.append(array)
                                    #check if we can push the enemy marble off the board (MMMEEX)
                                    elif (row+mod[0]*4, col+mod[1]*4) not in spaces:
                                        array = deepcopy(self.array)
                                        array[row+mod[0]*3][col+mod[1]*3] = self.current_marble
                                        array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                                        array[row+mod[0]][col+mod[1]] = self.current_marble
                                        array[row][col] = Marble.BLANK
                                        # print("test8")
                                        legal_moves.append(array)

        # print(legal_moves)
        return legal_moves

                

    def generate_legal_moves(self):
        legal_moves = [] #list of boards
        for row in range(len(self.array)):
            for col in range(len(self.array[row])):
                # print(f"row: {row}, col: {col}")
                if self.array[row][col] == self.current_marble:
                    legal_moves += self.generate_marble_moves((row, col))
                    # self.generate_two_marble_moves_inline((row, col)) +
                    # self.generate_two_marble_moves_broadside((row, col)) +
                    # self.generate_three_marble_moves_inline((row, col)) +
                    # self.generate_three_marble_moves_broadside((row, col)))



        return legal_moves


class AiPlayerKevin(AbstractPlayer):
    # 1. minimax with alpha-beta pruning
    # 2. heuristic evaluation function
    # 3. choice of:
    #   a. node ordering
    #   b. transposition tables
    #   c. quiescence search


    def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]], selection_lock: bool) \
            -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:
        
        game = AiGame(game)

        return self._game_analytic(game)


    def _game_analytic(self, game):

        max_depth = 1

        ai_move = self._alpha_beta_search(game, max_depth)

        return game.create_formatted_move(game, ai_move)

    def _alpha_beta_search(self, game, max_depth):
        tmp_score_move_list = []

        vgame = deepcopy(game)
        move_list = self._sort_moves(list(game.generate_legal_moves()))
        for move in move_list:
            vgame = self._next_virtual_game(game, move)
            # score = self._max_value(vgame, move, max_depth, strategy, alpha=-math.inf, beta=math.inf)
            score = self._max_value(vgame, move, max_depth, alpha=-math.inf, beta=math.inf)

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

        # for a in tmp_score_move_list:
        #     print(a)
        # print(f"best score: {current_score} - best move: {best_move}")
        return best_move

    def _max_value(self, vgame, move, max_depth, strategy, tactic, alpha, beta):
        # receive each move, evaluate the value of current move


        if max_depth == 0:
            return self.heuristic_strategies(strategy, move, vgame)

        max_depth -= 1
        score = -math.inf

        next_move_list = self._sort_moves(list(vgame.generate_legal_moves()), tactic)

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

        next_move_list = self._sort_moves(list(vgame.generate_legal_moves()), tactic)

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

        # if strategy_number == 1:
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

            for space in enumerate(Space):
                # print(type(space[1]))
                # print(str(space[1].name))
                test = str(space[1].name)
                # print(test)

                if test != "OFF" and game.get_marble(space[1]) != Marble.BLANK:
                    sum += score[test]

                # print(score[test])
                # tmp_sum += score[str(space[1].name)]

            # print(f"[STRATEGY] sum: {sum}, move: {move}")
            # return sum

            # hyper-aggressive, score base on push a marble to side
            # shortest distance to opponent two or smaller marbles
            # score = 0
            if isinstance(move[0], tuple):
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
                    sum = (10 - distance_to_opp_marble) * 10
                else:
                    sum = -100
            else:
                # inline move
                # sumito possibility - higher priority for move
                # check if the next position of the move contain opponent marble
                inner_rim = ["H5", "H6", "H7", "H8", "B2", "B3", "B4", "B5", "G4", "F3", "E2",
                             "D2", "C2", "G8", "F8", "E8", "D7", "C6"]
                outer_rim = ["I5", "I6", "I7", "I8", "I9", "A1", "A2", "A3", "A4", "A5",
                             "H4", "G3", "F2", "E1", "D1", "C1","B1", "H9", "G9", "F9", "E9", "D8", "C7", "B6"]

                line = line_to_edge(move[0], move[1])
                own_marbles_num, opp_marbles_num = game._inline_marbles_nums(line)
                if opp_marbles_num > 0:
                    # check if our marble outnumber opponent marble
                    if own_marbles_num >= opp_marbles_num:
                        possible_space_to_push = neighbor(line[own_marbles_num + opp_marbles_num - 1], move[1])
                        if possible_space_to_push is not None:
                            sum += 200
                        if possible_space_to_push.value in inner_rim:
                            sum += 200
                        if possible_space_to_push.value in outer_rim:
                            sum += 300
                        if possible_space_to_push.value is Space.OFF:
                            sum += 1000

            # print(f"score: {score} - {move}")
            return sum

    def _sort_moves(self, moves):
        priority_1_moves = []
        priority_2_moves = []
        priority_3_moves = []
        priority_4_moves = []
        priority_5_moves = []
        priority_6_moves = []

        for legal_move in moves:
            if isinstance(legal_move[0], tuple):
                #broadside moves
                # (<Space.C4: ('C', '4')>, <Space.C5: ('C', '5')>), <Direction.NORTH_WEST: 'north-west'>)

                # if 3 marbles were moved
                if len(legal_move[0]) == 3:
                    priority_4_moves.append(legal_move)
                # if 2 marbles were moved
                elif len(legal_move[0]) == 2:
                    priority_5_moves.append(legal_move)
                # if 1 marble were moved
                else:
                    priority_6_moves.append(legal_move)
            else:
                pass
                #inline moves
                # (<Space.A1: ('A', '1')>, <Direction.NORTH_EAST: 'north-east'>
                # if 3 marbles were moved etc


        sorted_moves = priority_1_moves + priority_2_moves + priority_3_moves + priority_4_moves + priority_5_moves + priority_6_moves
        return sorted_moves

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
            

if __name__ == "__main__":
    game_original = Game()
    # print(type(game_original))

    game_new = AiGame(game_original, Player.BLACK)

    start_time = time.time()
    games = []
    
    for move in game_original.generate_legal_moves():
        game = deepcopy(game_original)
        game.move(move[0], move[1])
        games.append(game)
    game_original_time = time.time() - start_time
    print("--- original game took %s seconds ---" % (game_original_time))
    print(len(games))

    start_time = time.time()
    moves = game_new.generate_legal_moves()
    game_new_time = time.time() - start_time
    print("--- new game took %s seconds ---" % (game_new_time))
    print(len(moves))

    # print(moves[0].array)

    print("game new is %s times faster than game original" % (game_original_time/game_new_time))




