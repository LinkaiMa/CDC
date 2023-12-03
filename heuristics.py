from typing import Tuple
from ChessBoard import Board
from ObjTypes import Action, MoveType
import numpy as np

FACTOR = 1000

def placeholder_heuristic(state: Board, action) -> float:
    return 0

def baseline_0(state: Board, action) -> float:
    if action[0] == MoveType.UNCOVER:
        return 0
    elif state.check_status(vbose=False) == 1:
        return 52 * FACTOR
    elif state.check_status(vbose=False) == -1:
        return -52 * FACTOR
    else:
        return 0

def baseline_1(state:Board, action) -> float:
    if action[0] == MoveType.UNCOVER:
        return 0
    elif state.check_status(vbose=False) == 1:
        return 52 * FACTOR
    elif state.check_status(vbose=False) == -1:
        return -52 * FACTOR
    elif state.check_status(vbose=False) == 0:
        return 0
    else:
        return np.sum( np.multiply(state.faceup, state.faceup!= -9).flatten() )

def baseline_2(state: Board, action, unique_uncover=False) -> float:
    if state.check_status(vbose=False) == 1:
        return 52 * FACTOR
    elif state.check_status(vbose=False) == -1:
        return -52 * FACTOR
    # elif state.check_status(vbose=False) == 0 or (state.timer >= 6 and np.sum((state.faceup == 0).flatten()) > 0):
    elif state.check_status(vbose=False) == 0:
        return 0
        
    if action[0] == MoveType.UNCOVER:
        vsum = 0.0
        count = 0
        for i in range(4):
            for j in range(8):
                if state.faceup[i][j] == 0:
                    vsum += state.facedown[i][j]
                    count += 1
        B = state.faceup
        score = 0
        for i in range(4):
            for j in range(8):
                if B[i][j] != -9:
                    if B[i][j] == 1 or B[i][j] == -1:
                        score += B[i][j] * 6.5
                    else:
                        score += B[i][j]
        return vsum / count + score
    
    else:                    
        B = state.faceup
        score = 0
        for i in range(4):
            for j in range(8):
                if B[i][j] != -9:
                    if B[i][j] == 1 or B[i][j] == -1:
                        score += B[i][j] * 6.5
                    else:
                        score += B[i][j]
        # print("score naive", score)
        return score
    
    
def eatable_neighbour(state: Board, coord: Tuple[int, int], k=2) -> float:
    # check up, down, left, right
    x, y = coord
    B = state.faceup
    is_black = B[x][y] < 0
    neighbours = []
    for i in range(x-k, x+k+1):
        for j in range(y-k, y+k+1):
            if i < 0 or i >= state.faceup.shape[0] or j < 0 or j >= state.faceup.shape[1]:
                continue
            if i == x and j == y:
                continue
            if B[i][j] == -9 or B[i][j] == 0:
                continue
            if abs(i-x) + abs(j-y) > k:
                continue
            if ((B[i][j] < 0 and not is_black) or (B[i][j] > 0 and is_black)) and ((abs(B[x][y]) == 1 and abs(B[i][j]) == 7) or abs(B[x][y]) >= abs(B[i][j])):
                neighbours.append((i, j, abs(i-x) + abs(j-y)))
    temp = {i: (0,0.0) for i in range(1, k+1)}
    for neighbour in neighbours:
        nx, ny, distance = neighbour
        temp[distance] = (temp[distance][0] + 1, temp[distance][1]-B[nx][ny])
    score = 0
    for coef, value in zip([0.1**i for i in range(k)], temp.values()):
        score += coef * (0 if value[0] == 0 else (value[1] / value[0]))
    return score

def baseline_3(state: Board, action: Action) -> float:
    # if action[0] == MoveType.UNCOVER:
    #     return 0
    result = 0
    result += 10 * baseline_2(state, action)
    for i in range(state.faceup.shape[0]):
        for j in range(state.faceup.shape[1]):
            if state.faceup[i][j] != -9 and state.faceup[i][j] != 0:
                result += 2 * eatable_neighbour(state, (i, j))
                
    return result
    
    


