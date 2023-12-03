from copy import deepcopy
import re
import sys
from ChessBoard import *
from Players import *
import numpy as np
from heuristics import baseline_1, baseline_3

if __name__ == '__main__':
    ori_stdout = sys.stdout
    f = open('log.txt', 'w')
    sys.stdout = f
    np.random.seed(10)
    # start game:    
    CDC_Board = Board()
    # CDC_Board.print_board_facedown()
    # CDC_Board.faceup = CDC_Board.facedown
    P1 = AI(baseline_3); P2 = AI(baseline_1)
    it = 0

    # we let Player1 make the first move
    act_str, _ = P1.think(CDC_Board)
    # we assume the first move is uncover
    first_piece = P1.action(act_str, CDC_Board)
    if first_piece>0:
        P1.role = 1; P2.role = -1 
    else:
        P1.role = -1; P2.role = 1 
    CDC_Board.print_board()
    
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
            
            CDC_Board.print_board()
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
            CDC_Board.print_board()
            
            # response = input("Debug mode? (y/n)")
            # if response.startswith('y'):
            #     # baseline_3(CDC_Board, action)
            #     P1.think(board_dup)
            continue
    
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
        
         
    sys.stdout = ori_stdout
    f.flush()
    f.close()