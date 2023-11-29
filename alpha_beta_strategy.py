from copy import deepcopy
from Chinese_Dark_Chess import Board
from ObjTypes import Action, State, MoveType
from helpers import get_avaliable_actions
from heuristics import placeholder_heuristic

def find_best_move_by_ab(currBoard: Board, currPlayer, depth=-1, utility_fn = placeholder_heuristic) -> Action:
    """Find the best move for the given piece on the given board using alpha-beta pruning.

    Args:
        currBoard (State): current state of the board
        currPlayer (_type_): _description_
        depth (int, optional): Depth of the search tree. Defaults to -1(no limit).
        utility_fn: Utility function. Defaults to placeholder_heuristic.

    Returns:
        Action: Next action suggested by the algorithm.
    """
    board_state = deepcopy(currBoard.faceup)
    params = {
        "faceup_state": board_state,
        "board": currBoard,
        "currPlayer": currPlayer,
        "depth": depth,
        "utility_fn": utility_fn,
    }
    
    best_move = None
    best_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    
    for action in get_avaliable_actions(currBoard):
        pass
    