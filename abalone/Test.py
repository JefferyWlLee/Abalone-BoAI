import os
from copy import deepcopy
from enum import Enum

from enums import Marble, InitialPosition

import colorama
from colorama import Style


def generate_enum_from_file(file_path):
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
            case 'A': row_offset = 8
            case 'B': row_offset = 7
            case 'C': row_offset = 6
            case 'D': row_offset = 5
            case 'E': row_offset = 4
            case 'F': row_offset = 3
            case 'G': row_offset = 2
            case 'H': row_offset = 1
            case 'I': row_offset = 0
        col_index = int(col) - 1
        match row_offset:
            case 4: col_index -= 1
            case 3: col_index -= 2
            case 2: col_index -= 3
            case 1: col_index -= 4
            case 0: col_index -= 5
            case _: pass


        return row_offset, col_index

    # Fill the board with WHITE and BLACK marbles based on positions
    for pos in positions:
        row, col, color = pos[0], pos[1], pos[2].lower()
        row_offset, col_index = get_array_indices(row, col)
        print(row_offset, col_index, color, pos)
        board[row_offset][col_index] = Marble.WHITE if color == 'w' else Marble.BLACK

    # Dynamically generate an Enum class for the board state
    BoardState = {'BOARD': Enum(board), 'current_player': current_player}

    return BoardState

def strin(board) -> str:  # pragma: no cover
    board_lines = list(map(lambda line: ' '.join(map(str, line)), board))
    string = ''
    string += Style.DIM + '    I ' + Style.NORMAL + board_lines[0] + '\n'
    string += Style.DIM + '   H ' + Style.NORMAL + board_lines[1] + '\n'
    string += Style.DIM + '  G ' + Style.NORMAL + board_lines[2] + '\n'
    string += Style.DIM + ' F ' + Style.NORMAL + board_lines[3] + '\n'
    string += Style.DIM + 'E ' + Style.NORMAL + board_lines[4] + '\n'
    string += Style.DIM + ' D ' + Style.NORMAL + board_lines[5] + Style.DIM + ' 9\n' + Style.NORMAL
    string += Style.DIM + '  C ' + Style.NORMAL + board_lines[6] + Style.DIM + ' 8\n' + Style.NORMAL
    string += Style.DIM + '   B ' + Style.NORMAL + board_lines[7] + Style.DIM + ' 7\n' + Style.NORMAL
    string += Style.DIM + '    A ' + Style.NORMAL + board_lines[8] + Style.DIM + ' 6\n' + Style.NORMAL
    string += Style.DIM + '       1 2 3 4 5' + Style.NORMAL
    return string

def main():
    board = deepcopy(InitialPosition.DEFAULT.value)
    print(strin(board))
    file_path = input("Enter the path to the file: ")
    board_state = generate_enum_from_file(file_path)
    print(strin(board_state['BOARD']))

if __name__ == "__main__":
    main()