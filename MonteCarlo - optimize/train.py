import random

class train():
    def __init__(self, cell_nums, Epsilon) -> None:
        # First-visit Monte Carlo control without exploring starts
        self.Epsilon = Epsilon
        self.height = cell_nums
        self.width = cell_nums

        # Initial Policy
        # Action Space: (# 0: Up, 1: Right, 2: Down, 3: Left)
        # PI_Action_table：action space of each state
        # PI_Possible_table: action possibility of each action in PI_Action_table：action
        self.PI_Action_table = [[[0, 1 ,2, 3] for _ in range(self.width)] for _ in range(self.height)]
        self.PI_Possible_table = [[[1/4, 1/4, 1/4, 1/4] for _ in range(self.width)] for _ in range(self.height)]

    def get_action(self, state):
        # Generate action based on state and policy
        action = random.choices(self.PI_Action_table[state[0]][state[1]], self.PI_Possible_table[state[0]][state[1]])[0]
        return action

    def get_best_action(self, state):
        # Generate best action based on state and policy
        # if there are more than 1 best action (same possibilities to choose them), random chooes one of them
        max_num = max(self.PI_Possible_table[state[0]][state[1]])
        best_actions = []
        
        for i in range(len(self.PI_Action_table[state[0]][state[1]])):
            if self.PI_Possible_table[state[0]][state[1]][i] == max_num:
                best_actions.append(self.PI_Action_table[state[0]][state[1]][i])
        best_action = random.choice(best_actions)

        return best_action

    def update(self, state, Q):
        # Update policy

        # Action space of state
        action_space = self.PI_Action_table[state[0]][state[1]]

        # Q value of each action
        Q_value=[]
        for i in action_space:
            Q_value.append(Q[i])

        # Choose best policy (with max Q value)
        # if there are more than 1 best action (same possibilities to choose them), they have same possibilities
        max_num = max(Q_value)
        best_actions = []
        for i in range(len(Q_value)):
            if Q_value[i] == max_num:
                best_actions.append(i)

        # ϵ-greedy min possibility
        Possible_min = self.Epsilon/len(action_space)
        Possible_max = (1 - (Possible_min * (len(action_space) - len(best_actions))))/len(best_actions)
        
        # Update policy
        for i in range(len(self.PI_Possible_table[state[0]][state[1]])):
            if Q_value[i] == max_num:
                self.PI_Possible_table[state[0]][state[1]][i] = Possible_max
            else:
                self.PI_Possible_table[state[0]][state[1]][i] = Possible_min
