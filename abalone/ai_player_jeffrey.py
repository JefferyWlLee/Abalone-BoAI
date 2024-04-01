from collections.abc import Generator
from copy import deepcopy
from typing import List, Tuple, Union

import abstract_player
from utils import neighbor, line_to_edge
from enums import Space, Direction, Player, Marble
from game import Game, IllegalMoveException
from random import choice


sumito_weight = 1000

class AiPlayerJeffrey(abstract_player.AbstractPlayer):
    from typing import Optional

    def minimax(self, game: Game, depth: int, alpha: float, beta: float, maximizing_player: bool) -> Tuple[
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
            return self.heuristic_evaluation(game), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.generate_legal_moves(game):
                new_game = move[2]  # move[2] is the game state after the move
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, False)
                eval += self.check_inline(move[0], move[1], game)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (move[0], move[1])  # move[0] and move[1] are the space and direction
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.generate_legal_moves(game):
                new_game = move[2]  # move[2] is the game state after the move
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, True)
                eval -= self.check_inline(move[0], move[1], game)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (move[0], move[1])  # move[0] and move[1] are the space and direction
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def generate_legal_moves(self, game) -> Generator[Tuple[Union[Space, Tuple[Space, Space]], Direction], None, None]:
        """Generates all possible moves that the player whose turn it is can perform. The yielded values are intended\
        to be passed as arguments to `abalone.game.Game.move`.

        Yields:
            A tuple of 1. either one or a tuple of two `abalone.enums.Space`s and 2. a `abalone.enums.Direction`
        """
        for marbles in game.generate_own_marble_lines():
            for direction in Direction:
                copy = deepcopy(game)
                try:
                    copy.move(marbles, direction, False)

                except IllegalMoveException:
                    continue
                yield marbles, direction, copy

    def turn(self, game: Game, moves_history: List[Tuple[Union[Space, Tuple[Space, Space]], Direction]],
             selection_lock: bool) -> Tuple[Union[Space, Tuple[Space, Space]], Direction]:
        if len(moves_history) <= 1:
            return choice(list(game.generate_legal_moves()))

        _, best_move = self.minimax(game, depth=1, alpha=float('-inf'), beta=float('inf'),
                                    maximizing_player=game.turn == Player.WHITE)
        return best_move if best_move else choice(list(self.generate_legal_moves(game)))[0:2]

    def group_strength(self, game:Game):
        groups = list(self.check_for_groups(game))
        return sum([group for group in groups])




    @staticmethod
    def _space_to_board_indices(space: Space) -> Tuple[int, int]:
        """Returns the corresponding index for `self.board` of a given `abalone.enums.Space`.

        Args:
            space: The `abalone.enums.Space` for which the indices are wanted.

        Returns:
            An int tuple containing two indices for `self.board`.
        """

        xs = ['I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
        ys = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        x = xs.index(space.value[0])
        y = ys.index(space.value[1])
        # print("space to board")
        # print(space)
        # print(x,y)

        # offset because lines 'F' to 'I' don't start with '1'
        if x <= 3:
            y -= 4 - x

        # print(x,y)
        return x, y

    def get_marble(self, game, space: Space) -> Marble:
        """Returns the state of a `abalone.enums.Space`.

        Args:
            space: The `abalone.enums.Space` of which the state is to be returned.

        Returns:
            A `abalone.enums.Marble` representing the current state of `space`.

        Raises:
            Exception: Cannot get state of `abalone.enums.Space.OFF`
        """

        if space is Space.OFF:
            raise Exception('Cannot get state of `Space.OFF`')

        x, y = self._space_to_board_indices(space)
        # print("get_marble")
        # print(space)
        # print(x, y)
        # print(game.board[x][y])

        return game.board[x][y]

    def distence_to_center(self, game:Game):
        center = (4,4)
        total = 0
        if game.turn is Player.WHITE:
            for space in Space:
                if space is Space.OFF:
                    continue
                marble = game.get_marble(space)
                if marble == Marble.WHITE:
                    marble_index_x, marble_index_y = self._space_to_board_indices(space)
                    total += abs(center[0] - marble_index_x) + abs(center[1] - marble_index_y)
        else:
            for space in Space:
                if space is Space.OFF:
                    continue
                marble = game.get_marble(space)
                if marble == Marble.BLACK:
                    marble_index_x, marble_index_y = self._space_to_board_indices(space)
                    total += abs(center[0] - marble_index_x) + abs(center[1] - marble_index_y)

        # return 1000/total
        return total

    def score_heuristic (self, game:Game):
        white_marbles, black_marbles = game.get_score()
        if game.turn == Player.WHITE:
            return white_marbles - black_marbles
        else:
            return black_marbles - white_marbles


    def marble_of_player(self, player: Player) -> Marble:
        """Returns the corresponding `abalone.enums.Marble` for a given `abalone.enums.Player`.

        Args:
            player: The `abalone.enums.Player` whose `abalone.enums.Marble` is wanted.

        Returns:
            The `abalone.enums.Marble` which belongs to `player`.
        """

        return Marble.WHITE if player is Player.WHITE else Marble.BLACK


    def check_for_groups(self, game: Game) :
        """Generates all adjacent straight lines with up to three marbles of the player whose turn it is.

        Yields:
            0 for single marbles 1 for lines of 2 , 2 for lines of 3`.
        """
        marble = Marble.WHITE if game.turn is Player.WHITE else Marble.BLACK
        for space in Space:
            if space is Space.OFF or game.get_marble(space) is not marble:
                continue
            yield 0
            for direction in [Direction.NORTH_WEST, Direction.NORTH_EAST, Direction.EAST]:
                neighbor1 = neighbor(space, direction)
                if neighbor1 is not Space.OFF and game.get_marble(neighbor1) is marble:
                    yield 1
                    neighbor2 = neighbor(neighbor1, direction)
                    if neighbor2 is not Space.OFF and game.get_marble(neighbor2) is marble:
                        yield 2

    def scoring_potential(self, game: Game) -> int:
        """
        Calculate the potential for scoring points by pushing opponent's marbles off the board.

        Args:
            game: The current state of the game.

        Returns:
            An integer score representing the potential to push opponent marbles off the board.
        """
        # A simple heuristic can be the count of opponent marbles that are near the edge and can be pushed off
        # in the next move. For a more complex and accurate heuristic, you can analyze the board layout and
        # the positions of your marbles to see if pushing moves are possible.
        score_potential = 0
        opponent_marble = Marble.BLACK if game.turn == Player.WHITE else Marble.WHITE
        for space in Space:
            if space is Space.OFF or game.get_marble(space) != opponent_marble:
                continue
            for direction in Direction:
                if neighbor(space, direction) is Space.OFF:  # Potential to push off
                    score_potential += 1
                    break
        return score_potential

    def generate_sumito_moves(self, game: Game):
        """Generates all possible sumito moves that the player whose turn it is can perform. The yielded values are\
        intended to be passed as arguments to `abalone.game.Game.move`.

        Yields:
            A tuple of 1. either one or a tuple of two `abalone.enums.Space`s and 2. a `abalone.enums.Direction`
        """
        marble = Marble.WHITE if game.turn is Player.WHITE else Marble.BLACK
        opp_marble = Marble.BLACK if game.turn is Player.WHITE else Marble.WHITE
        for space in Space:
            if space is Space.OFF or game.get_marble(space) is not marble:
                continue
            for direction in Direction:
                neighbor1 = neighbor(space, direction)
                if neighbor1 is not Space.OFF and game.get_marble(neighbor1) is marble:
                    neighbor2 = neighbor(neighbor1, direction)
                    if neighbor2 is not Space.OFF and game.get_marble(neighbor2) is opp_marble:
                        neighbor3 = neighbor(neighbor2,direction)
                        if neighbor3 is Space.OFF or game.get_marble(neighbor3) is Marble.BLANK:
                            yield 500
                    if neighbor2 is not Space.OFF and game.get_marble(neighbor2) is marble:
                        neighbor3 = neighbor(neighbor2,direction)
                        if neighbor3 is opp_marble:
                            neighbor4 = neighbor(neighbor3,direction)
                            if neighbor4 is Space.OFF or game.get_marble(neighbor4) is Marble.BLANK:
                                yield 500

    def check_inline(self, marbles: Union[Space, Tuple[Space, Space]], direction: Direction, game:Game) -> int:
        """Check if the marbles are in a straight line in the given direction.

        Args:
            game: The current state of the game.
            marbles: The marbles to check.
            direction: The direction to check.

        Returns:
            True if the marbles are in a straight line in the given direction, False otherwise.
        """
        if isinstance(marbles, tuple):
            return 0

        return self.check_sumito(game, marbles, direction)

    @staticmethod
    def _marble_of_player(player: Player) -> Marble:
        """Returns the corresponding `abalone.enums.Marble` for a given `abalone.enums.Player`.

        Args:
            player: The `abalone.enums.Player` whose `abalone.enums.Marble` is wanted.

        Returns:
            The `abalone.enums.Marble` which belongs to `player`.
        """

        return Marble.WHITE if player is Player.WHITE else Marble.BLACK


    def _inline_marbles_nums(self, game, line: List[Space]) -> Tuple[int, int]:
        """Counts the number of own and enemy marbles that are in the given line. First the directly adjacent marbles\
        of the player whose turn it is are counted and then the subsequent directly adjacent marbles of the opponent.\
        Therefore only the marbles that are relevant for an inline move are counted. This method serves as an\
        helper method for `abalone.game.Game.move_inline`.

        Args:
            line: A list of `abalone.enums.Space`s that are in a straight line.

        Returns:
            A tuple with the number of 1. own marbles and 2. opponent marbles, according to the counting method\
            described above.
        """
        #print("inline marbles")
        own_marbles_num = 0
        # #print(line[own_marbles_num])
        # #print(game.get_marble(line[own_marbles_num]))
        # #print(game.board)
        marbles = [self.get_marble(game, space) for space in line]
        #print(line)
        #print(marbles)
        while own_marbles_num < len(line) and self.get_marble(game, line[own_marbles_num]) is self._marble_of_player(game.turn):
            # print("found own marble")
            own_marbles_num += 1
        opp_marbles_num = 0
        while opp_marbles_num + own_marbles_num < len(line) and game.get_marble(
                line[opp_marbles_num + own_marbles_num]) is self._marble_of_player(game.not_in_turn_player()):
            opp_marbles_num += 1
        return own_marbles_num, opp_marbles_num

    def check_sumito(self, game: Game, caboose: Union[Space], direction: Direction) -> int:
        line = line_to_edge(caboose, direction)
        own_marbles_num, opp_marbles_num = self._inline_marbles_nums(game, line)
        # #print(caboose, direction)
        if own_marbles_num > 3:
            #print("more than 3")
            return 0

        if own_marbles_num == len(line):
            #print("move own off board")
            return 0
        # sumito
        #print(own_marbles_num, opp_marbles_num)
        if opp_marbles_num > 0:
            if opp_marbles_num >= own_marbles_num:
                # print("opp more than own")
                return 0
            push_to = neighbor(line[own_marbles_num + opp_marbles_num - 1], direction)
            if push_to is not Space.OFF:
                if game.get_marble(push_to) is self._marble_of_player(game.turn):
                    # print("push to own")
                    return 0
            # print("#print sumito")
            return sumito_weight * 10000
        # print("no sumito")
        return 0



    def heuristic_evaluation(self, game: Game):
        sumito_potential_weight = 1000
        group_strength = self.group_strength(game)
        distence_to_center = self.distence_to_center(game)
        score_heuristic = self.score_heuristic(game)
        scoring_potential = self.scoring_potential(game)
        sumito_potential = sum(self.generate_sumito_moves(game))


        if group_strength > 40:
            group_strength_weight = 0
            scoring_potential_weight = 100000
            score_heuristic_weight = 100000
            distence_to_center_weight = 0
            global sumito_weight
            sumito_weight = 9999999
        else:
            sumito_weight = 1000
            group_strength_weight = 199999999
            distence_to_center_weight = 10999999
            score_heuristic_weight = 1000
            scoring_potential_weight = 1000
            global sumito_wheight
            sumito_weight = 1000
        #
        # if distence_to_center < 30:
        #     distence_to_center_weight = 0
        #     scoring_potential_weight = 100
        #     score_heuristic_weight = 100
        #
        if len(game.previous_boards) > 30:
            group_strength_weight = 0
            scoring_potential_weight = 100000
            score_heuristic_weight = 100000
            distence_to_center_weight = 0
            # global sumito_weight
            # sumito_weight = 9999999
        #
        # if sumito_potential > 0:
        #     sumito_potential_weight = 1000
        #     scoring_potential_weight = 0
        #     score_heuristic_weight = 0
        #     group_strength_weight = 0
        #     distence_to_center_weight = 0

        return (group_strength_weight * group_strength +
                distence_to_center_weight * distence_to_center +
                score_heuristic_weight * score_heuristic+
                scoring_potential_weight * scoring_potential+
                sumito_potential_weight * sumito_potential)