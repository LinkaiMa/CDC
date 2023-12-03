from alpha_beta_strategy import find_best_action_by_ab
from helpers import action2cmd


class Player:
    def __init__(self):
        self.role = 0
    def action(self,act_str,B):
        if act_str[0]=='u': # choose to uncover
            if len(act_str) == 3: pass
            else:
                print('Wrong input!')
                return False
            if int(act_str[1])<=4 and int(act_str[2])<=8:
                return B.uncover((int(act_str[1]),int(act_str[2])))
            else:
                print('Out of boundary!')
                return False
        elif act_str[0]=='m': # choose to move
            if len(act_str) == 5: pass
            else:
                print('Wrong input!')
                return False
            if self.role*B.faceup[int(act_str[1])-1,int(act_str[2])-1]>=0: # chose the correct color
                return B.move((int(act_str[1]),int(act_str[2])), (int(act_str[3]),int(act_str[4])))
            else:
                print('You selected the opponents piece!')
                return False
    def think(self,B):
        raise NotImplementedError("Please Implement this method")

class Human(Player):
    def __init__(self):
        super().__init__()
    def think(self,B):
        act_str = input("How should I move?")
        return act_str, None
class AI(Player):
    def __init__(self, heuristic):
        super().__init__()
        self.heuristic = heuristic
    def think(self,B):
        action = find_best_action_by_ab(B, self.role, 3, self.heuristic)
        return action2cmd(action), action
