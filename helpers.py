
from typing import List
from unittest import result
from ChessBoard import Board
from ObjTypes import Action, MoveType

def get_avaliable_actions(board: Board, is_black: bool) -> List[Action]:
    faceup_state = board.faceup
    result = []
    for i in range(faceup_state.shape[0]):
        for j in range(faceup_state.shape[1]):
            if faceup_state[i][j] == 0:
                result.append((MoveType.UNCOVER,i+1,j+1,-1,-1))
                continue
            elif faceup_state[i][j] == -9:
                continue
            elif is_black and faceup_state[i][j] < 0:
                # eat
                if i-1 >= 0 and faceup_state[i-1][j] > 0 and faceup_state[i-1][j] < 8 and board.is_eat_legal((i+1,j+1),(i,j+1)):
                    result.append((MoveType.EAT,i+1,j+1,i,j+1))
                elif i+1 < faceup_state.shape[0] and faceup_state[i+1][j] > 0 and faceup_state[i+1][j] < 8 and board.is_eat_legal((i+1,j+1),(i+2,j+1)):
                    result.append((MoveType.EAT,i+1,j+1,i+2,j+1))
                elif j-1 >= 0 and faceup_state[i][j-1] > 0 and faceup_state[i][j-1] < 8 and board.is_eat_legal((i+1,j+1),(i+1,j)):
                    result.append((MoveType.EAT,i+1,j+1,i+1,j))
                elif j+1 < faceup_state.shape[1] and faceup_state[i][j+1] > 0 and faceup_state[i][j+1] < 8 and board.is_eat_legal((i+1,j+1),(i+1,j+2)):
                    result.append((MoveType.EAT,i+1,j+1,i+1,j+2))
                # move
                if i-1 >= 0 and faceup_state[i-1][j] == -9 and board.is_move_legal((i+1,j+1),(i,j+1)):
                    result.append((MoveType.MOVE,i+1,j+1,i,j+1))
                elif i+1 < faceup_state.shape[0] and faceup_state[i+1][j] == -9 and board.is_move_legal((i+1,j+1),(i+2,j+1)):
                    result.append((MoveType.MOVE,i+1,j+1,i+2,j+1))
                elif j-1 >= 0 and faceup_state[i][j-1] == -9 and board.is_move_legal((i+1,j+1),(i+1,j)):
                    result.append((MoveType.MOVE,i+1,j+1,i+1,j))
                elif j+1 < faceup_state.shape[1] and faceup_state[i][j+1] == -9 and board.is_move_legal((i+1,j+1),(i+1,j+2)):
                    result.append((MoveType.MOVE,i+1,j+1,i+1,j+2))
            elif not is_black and faceup_state[i][j] > 0:
                # eat
                if i-1 >= 0 and faceup_state[i-1][j] < 0 and faceup_state[i-1][j] > -8 and board.is_eat_legal((i+1,j+1),(i,j+1)):
                    result.append((MoveType.EAT,i+1,j+1,i,j+1))
                elif i+1 < faceup_state.shape[0] and faceup_state[i+1][j]< 0 and faceup_state[i+1][j] > -8 and board.is_eat_legal((i+1,j+1),(i+2,j+1)):
                    result.append((MoveType.EAT,i+1,j+1,i+2,j+1))
                elif j-1 >= 0 and faceup_state[i][j-1] < 0 and faceup_state[i][j-1] > -8 and board.is_eat_legal((i+1,j+1),(i+1,j)):
                    result.append((MoveType.EAT,i+1,j+1,i+1,j))
                elif j+1 < faceup_state.shape[1] and faceup_state[i][j+1] < 0 and faceup_state[i][j+1] > -8 and board.is_eat_legal((i+1,j+1),(i+1,j+2)):
                    result.append((MoveType.EAT,i+1,j+1,i+1,j+2))
                # move
                if i-1 >= 0 and faceup_state[i-1][j] == -9 and board.is_move_legal((i+1,j+1),(i,j+1)):
                    result.append((MoveType.MOVE,i+1,j+1,i,j+1))
                elif i+1 < faceup_state.shape[0] and faceup_state[i+1][j] == -9 and board.is_move_legal((i+1,j+1),(i+2,j+1)):
                    result.append((MoveType.MOVE,i+1,j+1,i+2,j+1))
                elif j-1 >= 0 and faceup_state[i][j-1] == -9 and board.is_move_legal((i+1,j+1),(i+1,j)):
                    result.append((MoveType.MOVE,i+1,j+1,i+1,j))
                elif j+1 < faceup_state.shape[1] and faceup_state[i][j+1] == -9 and board.is_move_legal((i+1,j+1),(i+1,j+2)):
                    result.append((MoveType.MOVE,i+1,j+1,i+1,j+2))
    return result

def apply_action(board: Board, action: Action) -> None:
    faceup_state = board.faceup
    if action[0] == MoveType.UNCOVER:
        return board.uncover((action[1],action[2]))
    elif action[0] == MoveType.EAT:
        return board.move((action[1],action[2]),(action[3],action[4]))
    elif action[0] == MoveType.MOVE:
        return board.move((action[1],action[2]),(action[3],action[4]))
    else:
        raise ValueError(f"Invalid action type: {action[0]}.")
    
def undo_action(board: Board, action: Action) -> None:
    faceup_state = board.faceup
    if action[0] == MoveType.UNCOVER:
        raise Exception("An uncover action cannot be undone.")
    elif action[0] == MoveType.EAT:
        myPawn_x = action[1]-1
        myPawn_y = action[2]-1
        
        dest_x = action[3]-1
        dest_y = action[4]-1

        faceup_state[myPawn_x][myPawn_y],faceup_state[dest_x][dest_y] = \
        faceup_state[dest_x][dest_y],board.recent_dead[-1]

        if faceup_state[dest_x][dest_y]>0: # the dead piece is red
            board.redpieces.append(faceup_state[dest_x][dest_y])
        else:
            board.blackpieces.append(faceup_state[dest_x][dest_y])
        # del board.recent_dead[-1]
        board.recent_dead.pop(-1)
        # myPawn_x = action[1]
        # myPawn_y = action[2]
        # myPawn = faceup_state[myPawn_x][myPawn_y]
        
        # rival_x = action[3]
        # rival_y = action[4]
        # rival = faceup_state[rival_x][rival_y]
        
        # #TODO: undo eat
        # pass
    elif action[0] == MoveType.MOVE:
        myPawn_x = action[1]-1
        myPawn_y = action[2]-1
        
        dest_x = action[3]-1
        dest_y = action[4]-1

        faceup_state[myPawn_x][myPawn_y],faceup_state[dest_x][dest_y] = \
        faceup_state[dest_x][dest_y],faceup_state[myPawn_x][myPawn_y]

    
    else:
        raise ValueError(f"Invalid action type: {action[0]}.")
    
def action2cmd(action: Action) -> str:
    if action[0] == MoveType.UNCOVER:
        return f"u{action[1]}{action[2]}"
    elif action[0] == MoveType.MOVE or action[0] == MoveType.EAT:
        return f"m{action[1]}{action[2]}{action[3]}{action[4]}"
    else:
        raise ValueError(f"Invalid action type: {action[0]}.")
