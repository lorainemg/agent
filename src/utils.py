from enum import Enum

class FinalState(Enum):
    WON = 0
    FIRED = 1
    TIMEOUT = 2

def in_range(matrix, x, y):
    return x >= 0 and x < len(matrix) and y >= 0 and y < len(matrix[x])

def empty_positions(map_):
    'Returns all the empty positions in the map'
    result = []
    for i in range(len(map_)):
        for j in range(len(map_[i])):
            if map_[i][j].is_empty:
                result.append((i, j))
    return result     