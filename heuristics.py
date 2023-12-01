from ChessBoard import Board
from ObjTypes import MoveType
import numpy as np
def placeholder_heuristic(state):
    return 0

def naive_heuristic(state: Board, action) -> float:
    if state.check_status(vbose=False) == 1:
        return 52
    elif state.check_status(vbose=False) == -1:
        return -52
    elif state.check_status(vbose=False) == 0 or (state.timer >= 6 and np.sum((state.faceup == 0).flatten()) > 0):
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
    
def naive_heuristic_2(state: Board, action) -> float:
    if state.check_status(vbose=False) == 1:
        return 52
    elif state.check_status(vbose=False) == -1:
        return -52
    elif state.check_status(vbose=False) == 0 or (state.timer >= 6 and np.sum((state.faceup == 0).flatten()) > 0):
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
                    score += B[i][j]
        return vsum / count + score
    
    else:                    
        B = state.faceup
        score = 0
        for i in range(4):
            for j in range(8):
                if B[i][j] != -9:
                    score += B[i][j]
        # print("score naive", score)
        return score