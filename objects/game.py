import os
import sys
from copy import deepcopy
import random

from config import BOARD_SIZE_EDGES, PIECES, PlayerActions


class Game:
    def __init__(self) -> None:
        self.__board: list = self.__init_board()
        self.__curr_block: list = []
        self.__block_pos: list = []
        self.__init_block()
        self.__do_move_down: bool = False
        self.__error_message: str = ''
        self.__print_board()
        self.__available_actions: dict = {
            PlayerActions.MOVE_LEFT.value: self.__move_left,
            PlayerActions.MOVE_RIGHT.value: self.__move_right,
            PlayerActions.ROTATE_ANTICLOCKWISE.value: self.__rotate_anticlockwise,
            PlayerActions.ROTATE_CLOCKWISE.value: self.__rotate_clockwise,
            PlayerActions.NO_MOVE.value: self.__move_down,
            PlayerActions.QUIT_GAME.value: self.__end_game
        }

    @staticmethod
    def __init_board() -> list:
        board = [[0 for _ in range(BOARD_SIZE_EDGES)] for _ in range(BOARD_SIZE_EDGES)]
        for i in range(BOARD_SIZE_EDGES):
            board[i][0] = 1
        for i in range(BOARD_SIZE_EDGES):
            board[BOARD_SIZE_EDGES - 1][i] = 1
        for i in range(BOARD_SIZE_EDGES):
            board[i][BOARD_SIZE_EDGES - 1] = 1
        return board

    def __init_block(self) -> None:
        self.__curr_block = self.__get_random_block()
        self.__block_pos = self.__get_random_position()

    @staticmethod
    def __get_random_block() -> list:
        idx = random.randrange(len(PIECES))
        return PIECES[idx]

    def __get_random_position(self) -> list:
        curr_block_size = len(self.__curr_block)
        x = 0
        y = random.randrange(1, BOARD_SIZE_EDGES - curr_block_size)
        return [x, y]

    def __print_board(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("TETRIS (practically)\n\n")

        board_copy = deepcopy(self.__board)
        curr_block_size_x = len(self.__curr_block)
        curr_block_size_y = len(self.__curr_block[0])
        for i in range(curr_block_size_x):
            for j in range(curr_block_size_y):
                pos_x = self.__block_pos[0] + i
                pos_y = self.__block_pos[1] + j
                board_copy[pos_x][pos_y] = self.__curr_block[i][j] | self.__board[pos_x][pos_y]

        for i in range(BOARD_SIZE_EDGES):
            for j in range(BOARD_SIZE_EDGES):
                if board_copy[i][j] == 1:
                    print("*", end='')
                else:
                    print(" ", end='')
            print("")

        print("Instructions:\n")
        print(" - a: move block left")
        print(" - d: move block right")
        print(" - w: rotate block counter clockwise")
        print(" - s: rotate block clockwise")
        print(" - e: just move the block downwards as is")
        print(" - q: to quit the game anytime")

        if self.__error_message:
            print(self.__error_message)
        print("Your move:", )
        self.__error_message = ''

    def __overlap_check(self, curr_block: list, block_pos: list) -> bool:

        curr_block_size_x = len(curr_block)
        curr_block_size_y = len(curr_block[0])
        for i in range(curr_block_size_x):
            for j in range(curr_block_size_y):
                if self.__board[block_pos[0] + i][block_pos[1] + j] == 1 and curr_block[i][j] == 1:
                    return False
        return True

    def __get_rotate_clockwise(self) -> list:
        block_copy = deepcopy(self.__curr_block)
        reverse_block = block_copy[::-1]
        return list(list(elem) for elem in zip(*reverse_block))

    def __can_rotate_clockwise(self) -> bool:
        curr_block = self.__get_rotate_clockwise()
        return self.__overlap_check(curr_block, self.__block_pos)

    def __rotate_clockwise(self) -> None:
        if self.__can_rotate_clockwise():
            self.__curr_block = self.__get_rotate_clockwise()
            self.__do_move_down = True
        else:
            self.__error_message = "Cannot rotate clockwise!"

    def __get_rotate_anticlockwise(self) -> list:
        block_copy = deepcopy(self.__curr_block)
        zip_block = list(list(elem) for elem in zip(*block_copy))
        return zip_block[::-1]

    def __can_rotate_anticlockwise(self) -> bool:
        curr_block = self.__get_rotate_anticlockwise()
        return self.__overlap_check(curr_block, self.__block_pos)

    def __rotate_anticlockwise(self) -> None:
        if self.__can_rotate_anticlockwise():
            self.__curr_block = self.__get_rotate_anticlockwise()
            self.__do_move_down = True
        else:
            self.__error_message = "Cannot rotate anti-clockwise !"

    def __get_right_move(self) -> list:
        new_block_pos = [self.__block_pos[0], self.__block_pos[1] + 1]
        return new_block_pos

    def __can_move_right(self) -> bool:
        block_pos = self.__get_right_move()
        return self.__overlap_check(self.__curr_block, block_pos)

    def __move_right(self) -> None:
        if self.__can_move_right():
            self.__block_pos = self.__get_right_move()
            self.__do_move_down = True
        else:
            self.__error_message = "Cannot move right!"

    def __get_left_move(self) -> list:
        new_block_pos = [self.__block_pos[0], self.__block_pos[1] - 1]
        return new_block_pos

    def __can_move_left(self) -> bool:
        block_pos = self.__get_left_move()
        return self.__overlap_check(self.__curr_block, block_pos)

    def __move_left(self) -> None:
        if self.__can_move_left():
            self.__block_pos = self.__get_left_move()
            self.__do_move_down = True
        else:
            self.__error_message = "Cannot move left!"

    def __get_down_move(self) -> list:
        new_block_pos = [self.__block_pos[0] + 1, self.__block_pos[1]]
        return new_block_pos

    def __can_move_down(self) -> bool:
        block_pos = self.__get_down_move()
        return self.__overlap_check(self.__curr_block, block_pos)

    def __move_down(self) -> None:
        self.__block_pos = self.__get_down_move()

    @staticmethod
    def __end_game() -> None:
        print("Bye Thank you for playing!")
        sys.exit(0)

    def is_game_over(self) -> bool:
        if not self.__can_move_down() and self.__block_pos[0] == 0:
            return True
        return False

    def __merge_board_and_block(self) -> None:
        curr_block_size_x = len(self.__curr_block)
        curr_block_size_y = len(self.__curr_block[0])
        for i in range(curr_block_size_x):
            for j in range(curr_block_size_y):
                pos_x = self.__block_pos[0] + i
                pos_y = self.__block_pos[1] + j
                self.__board[pos_x][pos_y] = self.__curr_block[i][j] | self.__board[pos_x][pos_y]

        empty_row = [0] * BOARD_SIZE_EDGES
        empty_row[0] = 1
        empty_row[BOARD_SIZE_EDGES - 1] = 1
        filled_row = [1] * BOARD_SIZE_EDGES
        filled_rows = 0
        for row in self.__board:
            if row == filled_row:
                filled_rows += 1

        filled_rows -= 1

        for i in range(filled_rows):
            self.__board.remove(filled_row)

        for i in range(filled_rows):
            self.__board.insert(0, empty_row)

    def player_move(self, player_input: str) -> None:
        if player_input in self.__available_actions.keys():
            self.__available_actions[player_input]()
        else:
            self.__error_message = "That is not a valid move!"

        if self.__do_move_down and self.__can_move_down():
            self.__move_down()

        if not self.__can_move_down():
            self.__merge_board_and_block()
            self.__init_block()
        self.__print_board()
