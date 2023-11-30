import numpy as np
import tabulate
import pandas as pd 
name_list = ['General','Chariot','Horse','Cannon','Advisor','Elephant','Soldier']
name_dic = {}
for i,z in zip(np.arange(7,0,-1), name_list):
    name_dic[i] = 'Red '+z
    name_dic[-i] = 'Black '+z


class Board:
    def __init__(self):
        
        self.faceup = np.zeros((4,8),dtype=int)
        self.redpieces = ([1]*4+
            list(np.linspace(1,7,7,endpoint=True,dtype=int))
            +list(np.linspace(2,6,5,endpoint=True,dtype=int)))
        
        self.blackpieces = ([-1]*4+
            list(np.linspace(-7,-1,7,endpoint=True,dtype=int))
            +list(np.linspace(-6,-2,5,endpoint=True,dtype=int)) )
        all_chess = np.array(self.redpieces + self.blackpieces)
        np.random.shuffle(all_chess)
        
        self.facedown = all_chess.reshape((4,8))
        self.timer = 0
        self.recent_dead = []

    def print_board(self): 
        B = self.faceup 
        df = pd.DataFrame(B,index=['r'+str(i) for i in range(1,5)])
        for i in range(4):
            for j in range(8):
                if B[i,j]==-9:
                    df.iloc[i,j]=''
                if B[i,j]==0:
                    df.iloc[i,j]='?'
        print(tabulate.tabulate(df, tablefmt='grid', showindex=True, headers = ['c'+str(i) for i in range(1,9)]))  
    # def print_board(self):
    #     n,m = self.faceup.shape
    #     for row in range(n):
    #         print('\n')
    #         toprint=''
    #         for col in range(m):
    #             num = self.faceup[row,col]
    #             if num == -9:
    #                 toprint += '   '
    #             elif num == 0:
    #                 toprint += ' x'+' '
    #             else:
    #                 res = str(num) if num<0 else ' '+str(num)
    #                 toprint += res +' '
    #         print(toprint)
        
    def uncover(self,pos):
        # takes the position to uncover (starting from 1)
        i,j = pos[0]-1, pos[1]-1
        if i<4 and i>=0 and j<8 and j>=0:
            if self.facedown[i,j]==0:
                print('Error: the piece is already uncovered.')
                return False
            else:
                self.faceup[i,j],self.facedown[i,j] = self.facedown[i,j],0
                self.timer = 0
                # self.print_board()
                return self.faceup[i,j]
        else:
            print('Error: Out of the boundary')
            return False
    def is_move_legal(self,sel,tar):
        good_pos = [(sel[0]+1,sel[1]),(sel[0],sel[1]+1),
                    (sel[0]-1,sel[1]),(sel[0],sel[1]-1)]
        if (tar[0]<=4 and tar[1]<=8 and tar in good_pos):
            return True
        else:
            return False
        
    def is_eat_legal(self,sel,tar):
        selup,seldown = self.faceup[sel[0]-1,sel[1]-1], self.facedown[sel[0]-1,sel[1]-1]
        tarup,tardown = self.faceup[tar[0]-1,tar[1]-1], self.facedown[tar[0]-1,tar[1]-1]
        if tarup == -9: # target position is empty
            return True
        
        elif abs(selup)==1 and abs(tarup)==7:
            return True
        
        elif abs(selup)>=abs(tarup): # rank of selected piece is higher than target
            return True
        else:
            return False
        
    def move(self,sel,tar):
        if self.is_move_legal(sel, tar): pass
        else:
            print('You can only move to the immediate neighbor!')
            return False
        selup,seldown = self.faceup[sel[0]-1,sel[1]-1], self.facedown[sel[0]-1,sel[1]-1]
        tarup,tardown = self.faceup[tar[0]-1,tar[1]-1], self.facedown[tar[0]-1,tar[1]-1]
        if selup == 0:
            print('You cannot move a face-down piece!')
            return False
        if tarup == 0:
            print('You cannot capture a face-down piece!')
            return False
        if selup == -9:
            print('You selected an empty position!')
            return False
        if tarup == -9:
            print('You have succesfully moved your piece.')
            self.faceup[sel[0]-1,sel[1]-1],self.faceup[tar[0]-1,tar[1]-1] = -9,selup
            self.timer += 1
            # self.print_board()
            return True
        if selup*tarup>0:
            print('You cannot capture your own piece!')
            return False
        else:
            if self.is_eat_legal(sel, tar):
                print('You have succesfully captured a '+name_dic[tarup]+' with your '+name_dic[selup]+'!')
                self.faceup[sel[0]-1,sel[1]-1],self.faceup[tar[0]-1,tar[1]-1] = -9,selup
                self.timer = 0
                if tarup>0: # a red piece is captured
                    self.redpieces.remove(tarup)
                else: # a black piece is captured
                    self.blackpieces.remove(tarup)
                # self.print_board()
                self.recent_dead.append(tarup)
                return True
            else:
                print('You can not capture a piece of higher rank!')
                return False
    def check_status(self):
        if len(self.redpieces)==0:
            print('Black wins!')
            return -1
        if len(self.blackpieces)==0:
            print('Red wins!')
            return 1
        if self.timer>=50:
            print('Tie!')
            return 0
        return None
    
    
    
    
    