from enum import Enum

BOARD_SIZE = 20
BOARD_SIZE_EDGES = BOARD_SIZE + 2
PIECES = [

    [[1], [1], [1], [1]],

    [[1, 0],
     [1, 0],
     [1, 1]],

    [[0, 1],
     [0, 1],
     [1, 1]],

    [[0, 1],
     [1, 1],
     [1, 0]],

    [[1, 1],
     [1, 1]]

]
class PlayerActions(Enum):
    MOVE_LEFT = 'a'
    MOVE_RIGHT = 'd'
    ROTATE_ANTICLOCKWISE = 'w'
    ROTATE_CLOCKWISE = 's'
    NO_MOVE = 'e'
    QUIT_GAME = 'q'

