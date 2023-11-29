
from typing import List
from Chinese_Dark_Chess import Board
from ObjTypes import Action, MoveType


def get_avaliable_actions(board: Board) -> List[Action]:
    return []

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
        myPawn_x = action[1]
        myPawn_y = action[2]
        
        dest_x = action[3]
        dest_y = action[4]

        faceup_state[myPawn_x][myPawn_y],faceup_state[dest_x][dest_y] = \
        faceup_state[dest_x][dest_y],board.recent_dead[-1]

        # myPawn_x = action[1]
        # myPawn_y = action[2]
        # myPawn = faceup_state[myPawn_x][myPawn_y]
        
        # rival_x = action[3]
        # rival_y = action[4]
        # rival = faceup_state[rival_x][rival_y]
        
        # #TODO: undo eat
        # pass
    elif action[0] == MoveType.MOVE:
        myPawn_x = action[1]
        myPawn_y = action[2]
        
        dest_x = action[3]
        dest_y = action[4]

        faceup_state[myPawn_x][myPawn_y],faceup_state[dest_x][dest_y] = \
        faceup_state[dest_x][dest_y],faceup_state[myPawn_x][myPawn_y]

    
    else:
        raise ValueError(f"Invalid action type: {action[0]}.")