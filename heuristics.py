from ChessBoard import Board
def placeholder_heuristic(state):
    return 0

def naive_heuristic(state):
    B = state.faceup
    score = 0
    for i in range(4):
        for j in range(8):
            if B[i][j] != -9:
                score += B[i][j]
    # print("score naive", score)
    return score