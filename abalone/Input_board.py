import os
import re

from enums import Marble, Player
from state_space_generator import StateSpaceGenerator



class InputBoard:

    def __init__(self, file_path):
        self.value = None
        self.current_player = self.generate_enum_from_file(file_path)

    def generate_enum_from_file(self, file_path):
        # Ensure the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with open(file_path, 'r') as file:
            board_state_text = file.read()

        # Parse the input text
        lines = board_state_text.strip().split('\n')
        current_player = lines[0]
        positions = lines[1].split(',')

        # Initialize a 9x9 board with BLANK marbles
        board = [[Marble.BLANK for _ in range(5)]
            , [Marble.BLANK for _ in range(6)]
            , [Marble.BLANK for _ in range(7)]
            , [Marble.BLANK for _ in range(8)]
            , [Marble.BLANK for _ in range(9)]
            , [Marble.BLANK for _ in range(8)]
            , [Marble.BLANK for _ in range(7)]
            , [Marble.BLANK for _ in range(6)]
            , [Marble.BLANK for _ in range(5)]]

        # Helper function to translate board coordinates to array indices
        def get_array_indices(row, col):
            global row_offset
            match row:
                case 'A':
                    row_offset = 8
                case 'B':
                    row_offset = 7
                case 'C':
                    row_offset = 6
                case 'D':
                    row_offset = 5
                case 'E':
                    row_offset = 4
                case 'F':
                    row_offset = 3
                case 'G':
                    row_offset = 2
                case 'H':
                    row_offset = 1
                case 'I':
                    row_offset = 0
            col_index = int(col) - 1
            match row_offset:
                case 4:
                    col_index -= 0
                case 3:
                    col_index -= 1
                case 2:
                    col_index -= 2
                case 1:
                    col_index -= 3
                case 0:
                    col_index -= 4
                case _:
                    pass

            return row_offset, col_index

        # Fill the board with WHITE and BLACK marbles based on positions
        for pos in positions:
            row, col, color = pos[0], pos[1], pos[2].lower()
            row_offset, col_index = get_array_indices(row, col)
            board[row_offset][col_index] = Marble.WHITE if color == 'w' else Marble.BLACK

        self.value = board
        if current_player == 'b':
            player = Player.BLACK
        else:
            player = Player.WHITE
        file_names = self.get_file_names(file_path)
        state_space_generator = StateSpaceGenerator(self, player, file_names)
        list(state_space_generator.generate_legal_moves())

        return current_player



    def get_file_names(self, input_filename):
        """
        generate appropriate file names.

        :param filenames: the given filename.
        """



        # Extract the number from the filename using a regular expression
        match = re.search(r'(\d+)', input_filename)
        if match:
            number = int(match.group(1))
            # Increment the number
            new_number = number

            # Create new filenames as a tuple
            filenames = (f"test{new_number}.move", f"test{new_number}.board")

            return filenames




