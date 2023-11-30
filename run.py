from ChessBoard import *
from Players import *
import numpy as np

if __name__ == '__main__':
    np.random.seed(0)
    # start game:    
    CDC_Board = Board()
    CDC_Board.print_board()
    P1 = Human(); P2 = AI()
    it = 0

    # we let Player1 make the first move
    act_str = P1.think(CDC_Board)
    # we assume the first move is uncover
    first_piece = P1.action(act_str, CDC_Board)
    if first_piece>0:
        P1.role = 1; P2.role = -1 
    else:
        P1.role = -1; P2.role = 1 
    CDC_Board.print_board()
        
    while CDC_Board.check_status() == None:
        if it%2==0: # P2's turn
            print('P2 turn')
            it+=1
            while True:
                current = 'Red' if P2.role>0 else 'Black'
                print(current+"s turn")
                act_str = P2.think(CDC_Board)
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
            CDC_Board.print_board()
            continue
        else: # P1's turn
            print('P1 turn')
            it+=1
            while True:
                current = 'Red' if P1.role>0 else 'Black'
                print(current+"s turn")
                act_str = P1.think(CDC_Board)
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
            CDC_Board.print_board()
            continue