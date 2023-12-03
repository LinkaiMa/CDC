from copy import deepcopy
from random import random

from ChessBoard import *
from Players import *
import numpy as np
from heuristics import baseline_0, baseline_1, baseline_2, baseline_3

N_RUNS = 25
PRINT = False

if __name__ == '__main__':
    # ori_stdout = sys.stdout
    # f = open('b1vsb0.txt', 'w')
    # sys.stdout = f
    
    
    test_result = {
        "n_runs": N_RUNS,
        "tie_count": 0,
        "P1_win_count": 0,
        "P2_win_count": 0,
        "P1_better_count": 0,
        "P2_better_count": 0,
        "games": [],
        "shuffle_seed": 456
    }
    
    while N_RUNS > 0:
        sd = np.random.randint(0, 100000)
        np.random.seed(sd)
        N_RUNS -= 1
        game_stats = {
            "seed": sd,
            "red": "",
            "black": "",
            "winner": "",
            "board_score": None,
            "action_counter": 0,
            "timer": None,
            "redpieces": None,
            "blackpieces": None,
        }
        # start game:    
        CDC_Board = Board()
        # CDC_Board.print_board(not PRINT)_facedown()
        # CDC_Board.faceup = CDC_Board.facedown
        P2 = AI(baseline_2); P1 = AI(baseline_1)
        it = 0

        # we let Player1 make the first move
        act_str, _ = P1.think(CDC_Board)
        # we assume the first move is uncover
        first_piece = P1.action(act_str, CDC_Board)
        if first_piece>0:
            P1.role = 1; P2.role = -1 
        else:
            P1.role = -1; P2.role = 1 
        CDC_Board.print_board(PRINT)
        
        game_stats["red"] = "P1" if P1.role > 0 else "P2"
        game_stats["black"] = "P1" if P2.role > 0 else "P2"
        
        action_counter = 0
        while CDC_Board.check_status() == None:
            action_counter += 1
            if it%2==0: # P2's turn
                print('P2 turn')
                it+=1
                while True:
                    current = 'Red' if P2.role>0 else 'Black'
                    print(current+"s turn")
                    act_str, _ = P2.think(CDC_Board)
                    res = P2.action(act_str,CDC_Board)
                    if res != False:
                        if res==100: # move
                            print('You have succesfully moved your piece.')
                        elif res==200: # eat
                            selup = CDC_Board.faceup[int(act_str[1])-1,int(act_str[2])-1]
                            tarup = CDC_Board.faceup[int(act_str[3])-1,int(act_str[4])-1]
                            print('You have succesfully captured a '+name_dic[CDC_Board.recent_dead[-1]]+' with your '+name_dic[tarup]+'!')
                        else: # uncover
                            print('You have succesfully uncovered a '+name_dic[res])
                        break
                print(f"Action {action_counter} | timer: {CDC_Board.timer} | facedown red sum: {np.sum(CDC_Board.facedown[CDC_Board.facedown>0])} | facedown black sum: {np.sum(CDC_Board.facedown[CDC_Board.facedown<0])}")
                
                CDC_Board.print_board(not PRINT)
                continue
            else: # P1's turn
                print('P1 turn')
                it+=1
                while True:
                    current = 'Red' if P1.role>0 else 'Black'
                    print(current+"s turn")
                    board_dup = deepcopy(CDC_Board)
                    act_str, action = P1.think(CDC_Board)
                    res = P1.action(act_str,CDC_Board)
                    
                    if res != False:
                        if res==100: # move
                            print('You have succesfully moved your piece.')
                        elif res==200: # eat
                            tarup = CDC_Board.faceup[int(act_str[3])-1,int(act_str[4])-1]
                            print('You have succesfully captured a '+name_dic[CDC_Board.recent_dead[-1]]+' with your '+name_dic[tarup]+'!')
                        else: # uncover
                            print('You have succesfully uncovered a '+name_dic[res])
                        break
                print(f"Action {action_counter} | timer: {CDC_Board.timer} | facedown red sum: {np.sum(CDC_Board.facedown[CDC_Board.facedown>0])} | facedown black sum: {np.sum(CDC_Board.facedown[CDC_Board.facedown<0])}")
                CDC_Board.print_board(not PRINT)
                
                # response = input("Debug mode? (y/n)")
                # if response.startswith('y'):
                #     # baseline_3(CDC_Board, action)
                #     P1.think(board_dup)
                continue
        game_stats["winner"] = "Red" if CDC_Board.check_status() > 0 else "Black" if CDC_Board.check_status() < 0 else "Tie"
        game_stats["action_counter"] = action_counter
        game_stats["timer"] = CDC_Board.timer
        # game_stats["redpieces"] = CDC_Board.redpieces
        # game_stats["blackpieces"] = CDC_Board.blackpieces
        
        stats = {}
        for rp in CDC_Board.redpieces:
            for bp in CDC_Board.blackpieces:
                if rp not in stats:
                    stats[rp] = 0.0
                if bp not in stats:
                    stats[bp] = 0.0
                if rp >= -bp or (rp == 1 and bp == -7):
                    stats[rp] += 1 / len(CDC_Board.blackpieces)
                if rp <= -bp or (rp == 7 and bp == -1):
                    stats[bp] -= 1 / len(CDC_Board.redpieces)
        print(f"Board score: {sum(stats.values())}.")
        game_stats["board_score"] = sum(stats.values())

        test_result["games"].append(game_stats)
        if game_stats["winner"] == "Tie":
            test_result["tie_count"] += 1
            if game_stats["board_score"] > 0 and game_stats["red"] == "P1" or game_stats["board_score"] < 0 and game_stats["black"] == "P1":
                test_result["P1_better_count"] += 1
            elif game_stats["board_score"] > 0 and game_stats["red"] == "P2" or game_stats["board_score"] < 0 and game_stats["black"] == "P2":
                test_result["P2_better_count"] += 1
                
        elif game_stats["winner"] == "Red" and game_stats["red"] == "P1" or game_stats["winner"] == "Black" and game_stats["black"] == "P1":
            test_result["P1_win_count"] += 1
        else:
            test_result["P2_win_count"] += 1
            
        # sys.stdout = ori_stdout
        # f.flush()
    # f.close()
    
    import json
    json.dump(test_result, open("test_result.json", "w"))