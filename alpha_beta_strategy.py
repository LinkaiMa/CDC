from copy import deepcopy
from ChessBoard import Board
from ObjTypes import Action, MoveType
from helpers import apply_action, get_avaliable_actions, undo_action
from heuristics import placeholder_heuristic

def _minmax(board: Board, is_max_plr, depth, alpha, beta, utility_fn) -> float:
    if depth == 0 or len(get_avaliable_actions(board, not is_max_plr)) == 0 or board.check_status() != None:
        return utility_fn(board)
    
    if is_max_plr:
        max_eval = float('-inf')
        for action in get_avaliable_actions(board, not is_max_plr):
            eval = None
            if action[0] == MoveType.UNCOVER:
                # No searching if we immediately uncover a pawn
                eval = utility_fn(board)
            else:
                params = {
                    "board": board,
                    "is_max_plr": False,
                    "depth": depth-1 if depth > 0 else depth,
                    "alpha": alpha,
                    "beta": beta,
                    "utility_fn": utility_fn,
                }
                apply_action(board, action)
                eval = _minmax(**params)
                undo_action(board, action)
                
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    
    else:
        min_eval = float('inf')
        for action in get_avaliable_actions(board, not is_max_plr):
            eval = None
            if action[0] == MoveType.UNCOVER:
                # No searching if we immediately uncover a pawn
                eval = utility_fn(board)
            else:
                params = {
                    "board": board,
                    "is_max_plr": True,
                    "depth": depth-1 if depth > 0 else depth,
                    "alpha": alpha,
                    "beta": beta,
                    "utility_fn": utility_fn,
                }
                apply_action(board, action)
                eval = _minmax(**params)
                undo_action(board, action)
                
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_action_by_ab(currBoard: Board, currPlayer, depth=-1, utility_fn = placeholder_heuristic) -> Action:
    """Find the best move for the given piece on the given board using alpha-beta pruning.

    Args:
        currBoard (State): current state of the board
        currPlayer (_type_): _description_
        depth (int, optional): Depth of the search tree. Defaults to -1(no limit).
        utility_fn: Utility function. Defaults to placeholder_heuristic.

    Returns:
        Action: Next action suggested by the algorithm.
    """
    board_state = deepcopy(currBoard)
    alpha = float("-inf")
    beta = float("inf")
    is_max_plr = True if currPlayer == 1 else False
    
    params = {
        "board": board_state,
        "is_max_plr": is_max_plr,
        "depth": depth,
        "alpha": alpha,
        "beta": beta,
        "utility_fn": utility_fn,
    }
    
    best_action = None
    best_score = None
    for action in get_avaliable_actions(board_state, not is_max_plr):
        score = None
        if action[0] == MoveType.UNCOVER:
            # No searching if we immediately uncover a pawn
            score = utility_fn(board_state)
        else:
            apply_action(board_state, action)
            score = _minmax(**params)
            undo_action(board_state, action)
            
        # print(f"Action: {action}, score: {score}")
        
        if is_max_plr and (best_score is None or score > best_score):
            best_action = action
            best_score = score
        elif not is_max_plr and (best_score is None or score < best_score):
            best_action = action
            best_score = score
    print(f"Best action: {best_action}, score: {best_score}")
    return best_action
        
    