# -*- coding: utf-8 -*-


"""This module is a template for create AI player"""
from random import choice
from copy import deepcopy
import sys
from typing import List, Optional, Tuple, Union

from abstract_player import AbstractPlayer
from enums import Space, Direction, Player, Marble
from game import Game
import math

class AiGame:
    def __init__(self, game: Union[Game, List], current_player: Player, kill: bool=False, value=0) -> None:
        # print(type(game))
        if (type(game) == Game):
            self.array = game.board
        else:
            self.array = game

        self.kill = kill

        self.value = value

        self.current_player = current_player

        self.current_marble = self.get_marble(current_player)
        self.opponent_marble = self.get_marble(self.get_other_player())

        self.opponent = self.get_other_player()

        self.score = self.get_score()

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

    def get_score(self):
        black_score = 0
        white_score = 0
        for row in range(len(self.array)):
            for col in range(len(self.array[row])):
                if self.array[row][col] == Marble.BLACK:
                    black_score += 1
                elif self.array[row][col] == Marble.WHITE:
                    white_score += 1

        return (black_score, white_score)

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
        
    def get_position_score(self, location):
        farthest_ring = (
            (0,0), (0,1), (0,2), (0,3), (0,4),
            (1,0), (1,4),
            (2,0), (2,5),
            (3,0), (3,6),
            (4,0), (4,7),
            (5,0), (5,6),
            (6,0), (6,5),
            (7,0), (7,4),
            (8,0), (8,1), (8,2), (8,3), (8,4))
        
        second_farthest_ring = (
            (1,1), (1,2),(1,3), (1,4),
            (2,1), (2,5),
            (3,1), (3,6),
            (4,1), (4,7),
            (5,1), (5,6),
            (6,1), (6,5),
            (7,1), (7,2), (7,3), (7,4))
        
        third_farthest_ring = (
            (2,2), (2,3), (2,4),
            (3,2), (3,5),
            (4,2), (4,6),
            (5,2), (5,5),
            (6,2), (6,3), (6,4))
        
        fourth_farthest_ring = (
            (3,3), (3,4),
            (4,3), (4,5),
            (5,3), (5,4))
        
        if location in farthest_ring:
            return 210
        elif location in second_farthest_ring:
            return 105
        elif location in third_farthest_ring:
            return 50
        elif location in fourth_farthest_ring:
            return 20

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

        if row < 4: 
            modifications = [(0, -1), (-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0)]
        elif row == 4:
            modifications = [(0, -1), (-1, -1), (-1, 0), (0, 1), (1, 0), (1, -1)]
        else:
            modifications = [(0, -1), (-1, 0), (-1, +1), (0, 1), (1, 0), (1, -1)]

        for mod in modifications:
            #check if the next space is on the board (M*)
            # print(f"row: {row}, col: {col}, mod: {mod}")
            if (row+mod[0], col+mod[1]) in spaces:
                # print("test")
                # check if empty, then move (M_)
                if self.array[row+mod[0]][col+mod[1]] == Marble.BLANK:
                    # pass
                    array = deepcopy(self.array)
                    array[row+mod[0]][col+mod[1]] = self.current_marble
                    array[row][col] = Marble.BLANK
                    # print("test1")
                    legal_moves.append(AiGame(array, self.opponent))

                # # check if second own color marble (MM)
                elif self.array[row+mod[0]][col+mod[1]] == self.current_marble:
                    # print("test2")
                #     #broadside move the two to empty, don't create dups, maybe call a function for this

                #     # check if the next space is on the board (MM*)
                    if (row+mod[0]*2, col+mod[1]*2) in spaces:
                #         #check if the next marble is empty (MM_)
                        if self.array[row+mod[0]*2][col+mod[1]*2] == Marble.BLANK:
                            # pass
                            array = deepcopy(self.array)
                            array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                            array[row+mod[0]][col+mod[1]] = self.current_marble
                            array[row][col] = Marble.BLANK
                            # print("test2")
                            legal_moves.append(AiGame(array, self.opponent))
                        #check if the next marble contains an enemy marble (MME)
                        elif self.array[row+mod[0]*2][col+mod[1]*2] == self.opponent:
                            self.value += 20
                            #check if we can push the enemy marble to another spot on the board (MME_)
                            if (row+mod[0]*3, col+mod[1]*3) in spaces and self.array[row+mod[0]*3][col+mod[1]*3] == Marble.BLANK:
                                array = deepcopy(self.array)
                                array[row+mod[0]*3][col+mod[1]*3] = self.opponent
                                array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                                array[row+mod[0]][col+mod[1]] = self.current_marble
                                array[row][col] = Marble.BLANK
                                # print("test3")
                                self.value += self.get_position_score(Tuple(row+mod[0]*3,col+mod[1]*3))

                                legal_moves.append(AiGame(array, self.opponent, value=self.value))
                            #check if we can push the enemy marble off the board (MMEX)
                            elif (row+mod[0]*3, col+mod[1]*3) not in spaces:
                                array = deepcopy(self.array)
                                array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                                array[row+mod[0]][col+mod[1]] = self.current_marble
                                array[row][col] = Marble.BLANK
                                # print("test4")
                                legal_moves.append(AiGame(array, self.opponent, True))
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
                                    legal_moves.append(AiGame(array, self.opponent))
                                #check if the next marble contains an enemy marble (MMME)
                                elif self.array[row+mod[0]*3][col+mod[1]*3] == self.opponent:
                                    #check if the marble after 3 friendly's and an enemy exists (MMME*)
                                    if (row+mod[0]*4, col+mod[1]*4) in spaces:
                                        #check if it is empty (MMME_)
                                        if self.array[row+mod[0]*4][col+mod[1]*4] == Marble.BLANK:
                                            self.value += 20
                                            array = deepcopy(self.array)
                                            array[row+mod[0]*4][col+mod[1]*4] = self.opponent
                                            array[row+mod[0]*3][col+mod[1]*3] = self.current_marble
                                            array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                                            array[row+mod[0]][col+mod[1]] = self.current_marble
                                            array[row][col] = Marble.BLANK
                                            # print("test6")

                                            self.value += self.get_position_score(Tuple(row+mod[0]*4,col+mod[1]*4))

                                            legal_moves.append(AiGame(array, self.opponent, value=self.value))
                                        #check if it is another enemy marble and the marble after that is empty (MMMEE_)
                                        elif self.array[row+mod[0]*4][col+mod[1]*4] == self.opponent:
                                            if (row+mod[0]*5, col+mod[1]*5) in spaces and self.array[row+mod[0]*5][col+mod[1]*5] == Marble.BLANK:
                                                array = deepcopy(self.array)
                                                array[row+mod[0]*5][col+mod[1]*5] = self.opponent
                                                array[row+mod[0]*4][col+mod[1]*4] = self.opponent
                                                array[row+mod[0]*3][col+mod[1]*3] = self.current_marble
                                                array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                                                array[row+mod[0]][col+mod[1]] = self.current_marble
                                                array[row][col] = Marble.BLANK
                                                # print("test7")
                                                legal_moves.append(AiGame(array, self.opponent))
                                            #check if we can push the enemy marble off the board (MMMEEX)
                                            elif (row+mod[0]*5, col+mod[1]*5) not in spaces:
                                                array = deepcopy(self.array)
                                                array[row+mod[0]*4][col+mod[1]*4] = self.current_marble
                                                array[row+mod[0]*3][col+mod[1]*3] = self.current_marble
                                                array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                                                array[row+mod[0]][col+mod[1]] = self.current_marble
                                                array[row][col] = Marble.BLANK
                                                # print("test8")
                                                legal_moves.append(AiGame(array, self.opponent, True))
                                    #check if we can push the enemy marble off the board (MMMEX)
                                    else:
                                        array = deepcopy(self.array)
                                        array[row+mod[0]*3][col+mod[1]*3] = self.current_marble
                                        array[row+mod[0]*2][col+mod[1]*2] = self.current_marble
                                        array[row+mod[0]][col+mod[1]] = self.current_marble
                                        array[row][col] = Marble.BLANK
                                        # print("test8")
                                        legal_moves.append(AiGame(array, self.opponent, True))

        # print(legal_moves)
        return legal_moves

                

    def generate_legal_moves(self):
        # print("current player is: ", self.current_player)
        legal_moves = [] #list of boards
        for row in range(len(self.array)):
            for col in range(len(self.array[row])):
                # print(f"row: {row}, col: {col}")
                if self.array[row][col] == self.current_marble:
                    # print("current marble is: ", self.current_marble)
                    # print("position is", row, col)
                    legal_moves += self.generate_marble_moves((row, col))
                    # self.generate_two_marble_moves_inline((row, col)) +
                    # self.generate_two_marble_moves_broadside((row, col)) +
                    # self.generate_three_marble_moves_inline((row, col)) +
                    # self.generate_three_marble_moves_broadside((row, col)))



        return legal_moves
    
    def convert_to_space(self, space):
        mapping = {
            (0,0): Space.I5, (0,1): Space.I6, (0,2): Space.I7, (0,3): Space.I8, (0,4): Space.I9,
            (1,0): Space.H4, (1,1): Space.H5, (1,2): Space.H6, (1,3): Space.H7, (1,4): Space.H8, (1,5): Space.H9,
            (2,0): Space.G3, (2,1): Space.G4, (2,2): Space.G5, (2,3): Space.G6, (2,4): Space.G7, (2,5): Space.G8, (2,6): Space.G9,
            (3,0): Space.F2, (3,1): Space.F3, (3,2): Space.F4, (3,3): Space.F5, (3,4): Space.F6, (3,5): Space.F7, (3,6): Space.F8, (3,7): Space.F9,
            (4,0): Space.E1, (4,1): Space.E2, (4,2): Space.E3, (4,3): Space.E4, (4,4): Space.E5, (4,5): Space.E6, (4,6): Space.E7, (4,7): Space.E8, (4,8): Space.E9,
            (5,0): Space.D1, (5,1): Space.D2, (5,2): Space.D3, (5,3): Space.D4, (5,4): Space.D5, (5,5): Space.D6, (5,6): Space.D7, (5,7): Space.D8,
            (6,0): Space.C1, (6,1): Space.C2, (6,2): Space.C3, (6,3): Space.C4, (6,4): Space.C5, (6,5): Space.C6, (6,6): Space.C7,
            (7,0): Space.B1, (7,1): Space.B2, (7,2): Space.B3, (7,3): Space.B4, (7,4): Space.B5, (7,5): Space.B6,
            (8,0): Space.A1, (8,1): Space.A2, (8,2): Space.A3, (8,3): Space.A4, (8,4): Space.A5
        }

        return mapping[space]
    
    def create_formatted_move(self, previous_game):
        starting_marble = None
        ending_marble = None
        direction = None

        for row in range(len(self.array)):
            for col in range(len(self.array[row])):
                if previous_game.array[row][col] == previous_game.current_marble and self.array[row][col] == Marble.BLANK:
                    starting_marble = (row, col)
                elif (self.array[row][col] == previous_game.current_marble and (previous_game.array[row][col] == Marble.BLANK or previous_game.array[row][col] == previous_game.opponent_marble)):
                    ending_marble = (row, col)
        
        if starting_marble[0] == ending_marble[0]:
            if starting_marble[1] < ending_marble[1]:
                direction = Direction.EAST
            else:
                direction = Direction.WEST

        elif starting_marble[0] < ending_marble[0]:
            if starting_marble[0] < 4:
                print("yes")
                if starting_marble[1] <= ending_marble[1]:
                    direction = Direction.SOUTH_WEST
                else:
                    direction = Direction.SOUTH_EAST
            else:
                print("no")
                if starting_marble[1] <= ending_marble[1]:
                    direction = Direction.SOUTH_EAST
                else:
                    direction = Direction.SOUTH_WEST
        
        elif starting_marble[0] > ending_marble[0]:
            print(starting_marble[0], starting_marble[1])
            print(ending_marble[0], ending_marble[1])
            if starting_marble[0] < 4:
                print("yes")
                if starting_marble[1] < ending_marble[1]:
                    direction = Direction.NORTH_WEST
                else:
                    direction = Direction.NORTH_EAST
            else:
                print("no")
                if starting_marble[1] < ending_marble[1]:
                    direction = Direction.NORTH_EAST
                else:
                    direction = Direction.NORTH_WEST


        starting_marble = self.convert_to_space(starting_marble)
        ending_marble = self.convert_to_space(ending_marble)

        print("direction", direction)
        print("starting_marble", starting_marble)
        print("ending_marble", ending_marble)

        return (starting_marble, direction)


class AiPlayerKevin(AbstractPlayer):
    # 1. minimax with alpha-beta pruning
    # 2. heuristic evaluation function
    # 3. choice of:
    #   a. node ordering
    #   b. transposition tables
    #   c. quiescence search
    def __init__(self):
        self.turns = 0


    def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]], selection_lock: bool) \
            -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:
        
        game = AiGame(game, game.turn)

        self.turns += 1

        print(self._game_analytic(game))
        # sys.exit()
        return self._game_analytic(game)


    def _game_analytic(self, game):

        ai_move = ()
        max_depth = 2

        # # if len(game.previous_boards) < 20:
        # if self.turns < 10:
        #     # ai_move = self._aplpha_beta_search(game, max_depth, 1, "all")
        #     ai_move = self._alpha_beta_search(game, max_depth, 1, "inline")
        #     # print("strategy 1")
        # else:
        #     ai_move = self._alpha_beta_search(game, 0, 2, "inline")
        #     # print("strategy 2")

        #as the game goes on will prioritize agressive more and more


        # 1-(1/self.turns)
        ai_move = self.minimax(game, max_depth, alpha=float('-inf'), beta=float("inf"), maximizing_player=game.current_player != Player.WHITE)[1]

        return ai_move.create_formatted_move(game)


    def minimax(self, game: AiGame, depth: int, alpha: float, beta: float, maximizing_player: bool) -> Tuple[
        float, Optional[Tuple[Union[Space, Tuple[Space, Space]], Direction]]]:
        """
        Perform a minimax search to determine the best move.

        Args:
            game: The current state of the game.
            depth: The maximum depth to search to.
            alpha: Alpha value for alpha-beta pruning.
            beta: Beta value for alpha-beta pruning.
            maximizing_player: True if the current turn is for the maximizing player, False otherwise.

        Returns:
            A tuple containing the heuristic value of the best move and the best move itself (or None if no move is found).
        """
        if depth == 0:
            return self.heuristic_strategies(game), None

        if maximizing_player:
            max_eval = float('-inf')
            best_board = None
            for game in game.generate_legal_moves():
                eval, _ = self.minimax(game, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_board = game
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_board
        else:
            min_eval = float('inf')
            best_board = None
            for game in game.generate_legal_moves():
                eval, _ = self.minimax(game, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_board = game
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_board
        

    def heuristic_strategies(self, game: AiGame):

        # zero is earlier in the game, gets higher as the game goes on
        strategy_number = 1-(1/self.turns)
        
        position_score = {
            (0, 0): -100, (0, 1): -100, (0, 2): -100, (0, 3): -100, (0, 4): -100,
            (1, 0): -100, (1, 1): 1, (1, 2): 1, (1, 3): 1, (1, 4): 1, (1, 5): -100,
            (2, 0): -100, (2, 1): 1, (2, 2): 5, (2, 3): 5, (2, 4): 5, (2, 5): 1, (2, 6): -100,
            (3, 0): -100, (3, 1): 1, (3, 2): 25, (3, 3): 31, (3, 4): 31, (3, 5): 25, (3, 6): 1, (3, 7): -100,
            (4, 0): -100, (4, 1): 1, (4, 2): 25, (4, 3): 31, (4, 4): 31, (4, 5): 31, (4, 6): 25, (4, 7): 1, (4, 8): -100,
            (5, 0): -100, (5, 1): 1, (5, 2): 25, (5, 3): 31, (5, 4): 31, (5, 5): 25, (5, 6): 1, (5, 7): -100,
            (6, 0): -100, (6, 1): 1, (6, 2): 5, (6, 3): 5, (6, 4): 5, (6, 5): 1, (6, 6): -100,
            (7, 0): -100, (7, 1): 1, (7, 2): 1, (7, 3): 1, (7, 4): 1, (7, 5): -100,
            (8, 0): -100, (8, 1): -100, (8, 2): -100, (8, 3): -100, (8, 4): -100
        }


        # boardside move, score are the sum of all marbles. For inline move, there is only one tuple
        sum = 0

        for row in range(len(game.array)):
            for col in range(len(game.array[row])):
                if game.array[row][col] == game.current_marble:
                    # print("position score",position_score[(row, col)])
                    sum += position_score[(row, col)] #* strategy_number


        if (game.kill):
            # there is a score difference meaning an opponent marble is killed by this move
            sum += 350
            sys.exit()
            # return score

        # 2. Second priority, arrange score according to how close the opponent marble to being kill
        # ANALYSIZING ON THE MOVE OF CURRENT DEPTH
        # if the opponent marble will be killed by next round score +6000
        # if the opponent marble will be killed by two round score +3000
        # if require three round score + 1500 (balance with defence strategy?)
        # if require four round, it is just random pushing marbles around, no addition score

        # print("game value", game.value)
        sum += game.value

        # print("total game sum",sum)
        return sum

    def _sort_moves(self, moves, game, tactic="partial"):
        broadside_moves = []
        inline_multiple_marbles_moves = []
        single_marble_moves = []

        # for legal_move in moves:
        #     if isinstance(legal_move[0], tuple):
        #         # (<Space.C4: ('C', '4')>, <Space.C5: ('C', '5')>), <Direction.NORTH_WEST: 'north-west'>)
        #         # boardside move only
        #         broadside_moves.append(legal_move)

        #     else:
        #         single_marble_moves.append(legal_move)
        return moves

        # for legal_move in moves:
        #     if not isinstance(legal_move[0], tuple):
                # (<Space.A1: ('A', '1')>, <Direction.NORTH_EAST: 'north-east'>
                # sorted_moves.append(legal_move)
                # inline_moves.append(legal_move)

        if tactic == "partial":
            # return boardside_moves[0:5]
            return broadside_moves + single_marble_moves
        elif tactic == "inline":
            return inline_multiple_marbles_moves + single_marble_moves
        else:
            return inline_multiple_marbles_moves + broadside_moves + single_marble_moves

    # def _next_virtual_game(self, game, move):
    #         vitual_board = deepcopy(game)
    #         vitual_board.move(move[0], move[1])
    #         return vitual_board

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
