from copy import deepcopy
from ChessBoard import Board
from ObjTypes import Action, MoveType
from helpers import apply_action, get_avaliable_actions, undo_action
from heuristics import placeholder_heuristic

def _minmax(board: Board, is_max_plr, depth, alpha, beta, utility_fn) -> float:
    if depth == 0 or len(get_avaliable_actions(board, not is_max_plr)) == 0 or board.check_status(vbose=False) != None:
        return utility_fn(board, [None])
    
    if is_max_plr:
        max_eval = float('-inf')
        max_action = None
        for action in get_avaliable_actions(board, not is_max_plr):
            eval = None
            if action[0] == MoveType.UNCOVER:
                # No searching if we immediately uncover a pawn
                eval = utility_fn(board, action)
            else:
                params = {
                    "board": board,
                    "is_max_plr": False,
                    "depth": depth-1 if depth > 0 else depth,
                    "alpha": alpha,
                    "beta": beta,
                    "utility_fn": utility_fn,
                }
                # print(f"Red Turn: applying action {action}")
                old_timer = board.timer
                apply_action(board, action)
                eval = _minmax(**params)
                undo_action(board, action)
                board.timer = old_timer
                
            if eval > max_eval:
                max_action = action
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        # print(f"Max action: {max_action}, score: {max_eval}")
        return max_eval
    
    else:
        min_eval = float('inf')
        min_action = None
        for action in get_avaliable_actions(board, not is_max_plr):
            eval = None
            if action[0] == MoveType.UNCOVER:
                # No searching if we immediately uncover a pawn
                # eval = utility_fn(board, action)
                eval = 0
            else:
                params = {
                    "board": board,
                    "is_max_plr": True,
                    "depth": depth-1 if depth > 0 else depth,
                    "alpha": alpha,
                    "beta": beta,
                    "utility_fn": utility_fn,
                }
                # print(f"Black Turn: action {action}")
                old_timer = board.timer
                apply_action(board, action)
                eval = _minmax(**params)
                undo_action(board, action)
                board.timer = old_timer
            
            if eval < min_eval:
                min_action = action
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        # print(f"Min action: {min_action}, score: {min_eval}")
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
        "is_max_plr": not is_max_plr,
        "depth": depth,
        "alpha": alpha,
        "beta": beta,
        "utility_fn": utility_fn,
    }
    
    best_action = None
    best_score = None
    # print(f"Avaliable actions: {get_avaliable_actions(board_state, not is_max_plr)}")
    debug_list = []
    for action in get_avaliable_actions(board_state, not is_max_plr):
        score = None
        # print(f"Start probing {action}")
        if action[0] == MoveType.UNCOVER:
            # No searching if we immediately uncover a pawn
            score = utility_fn(board_state, action)
        else:
            old_timer = board_state.timer
            apply_action(board_state, action)
            score = _minmax(**params)
            undo_action(board_state, action)
            board_state.timer = old_timer
            
            debug_list.append((action, score))
            
        # print(f"Action: {action}, score: {score}")
        
        if is_max_plr and (best_score is None or score > best_score):
            best_action = action
            best_score = score
        elif not is_max_plr and (best_score is None or score < best_score):
            best_action = action
            best_score = score
            
        # input(f"finished probing on action {action} with score {score}, press enter to continue.")
    print(f"Best action: {best_action}, score: {best_score}")
    return best_action
        
    