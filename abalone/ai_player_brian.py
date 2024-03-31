import copy
from typing import List, Tuple, Union
from abstract_player import AbstractPlayer
from enums import Space, Direction, Player, Marble
from game import Game, IllegalMoveException


class AiPlayerBrian(AbstractPlayer):
    # def __init__(self):
    #     self.transposition_table = {}

    def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]],
             selection_lock: bool) \
            -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:

        legal_moves = list(game.generate_legal_moves())

        if game.turn == Player.BLACK:
            maximizing_player = True
        else:
            maximizing_player = False

        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move, direction in legal_moves:
            # Make the move
            try:
                # game.move(move, direction)

                # Create a deep copy of the game object
                game_copy = copy.deepcopy(game)
                game_copy.move(move, direction)
            except IllegalMoveException:
                continue

            # Evaluate the move using minimax with alpha-beta pruning
            # score = self.minimax(game, alpha, beta, maximizing_player, depth=1)
            score = self.minimax(game_copy, alpha, beta, maximizing_player, depth=1)

            # Revert the move
            # game.undo()

            # Update best move if necessary
            if maximizing_player and score > alpha:
                alpha = score
                best_move = (move, direction)
            elif not maximizing_player and score < beta:
                beta = score
                best_move = (move, direction)

        return best_move

    def minimax(self, game: Game, alpha: float, beta: float, maximizing_player: bool, depth: int) -> float:
        if depth == 0:
            return self.evaluate(game)

        if maximizing_player:
            return self.max_value(game, alpha, beta, depth)
        else:
            return self.min_value(game, alpha, beta, depth)

    def max_value(self, game: Game, alpha: float, beta: float, depth: int) -> float:
        max_eval = float('-inf')
        for move, direction in game.generate_legal_moves():
            game.move(move, direction)
            eval = self.minimax(game, alpha, beta, False, depth - 1)
            game.undo()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval

    def min_value(self, game: Game, alpha: float, beta: float, depth: int) -> float:
        min_eval = float('inf')
        for move, direction in game.generate_legal_moves():
            game.move(move, direction)
            eval = self.minimax(game, alpha, beta, True, depth - 1)
            game.undo()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval

    def evaluate(self, game: Game) -> float:
        # Get the number of black and white marbles
        black_marbles, white_marbles = game.get_score()

        # Calculate the difference in the number of marbles
        score = black_marbles - white_marbles

        # Define the weights for different positions on the board
        position_weights = {
            Space.I5: -1.0, Space.I6: -1.0, Space.I7: -1.0, Space.I8: -1.0, Space.I9: -1.0,
            Space.H4: -0.5, Space.H5: -0.5, Space.H6: -0.5, Space.H7: -0.5, Space.H8: -0.5, Space.H9: -0.5,
            Space.F4: 0.5, Space.F5: 0.5, Space.F6: 0.5, Space.F7: 0.5,
            Space.E3: 1.0, Space.E4: 1.0, Space.E5: 1.0, Space.E6: 1.0, Space.E7: 1.0,
            Space.D3: 0.5, Space.D4: 0.5, Space.D5: 0.5, Space.D6: 0.5,
            Space.B1: -0.5, Space.B2: -0.5, Space.B3: -0.5, Space.B4: -0.5, Space.B5: -0.5, Space.B6: -0.5,
            Space.A1: -1.0, Space.A2: -1.0, Space.A3: -1.0, Space.A4: -1.0, Space.A5: -1.0
        }

        # Evaluate central control
        for space, weight in position_weights.items():
            if game.get_marble(space) is Marble.BLACK:
                score += weight
            elif game.get_marble(space) is Marble.WHITE:
                score -= weight

        # Return the final score
        return score
