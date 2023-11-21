import pygame

class Environment:
    def __init__(self, cell_nums):

        # Define size of map
        self.cell_nums = cell_nums

        # Generate map, each number record reward of this position
        self.map = [[0 for _ in range(cell_nums)] for _ in range(cell_nums)]

        # Generate target point
        self.targets = [[cell_nums - 1, cell_nums -1]]
        for target in self.targets:
            self.map[target[0]][target[1]]=1

        # Generate holes
        self.holes = []
        if cell_nums==4:
            self.holes = [[1,1], [3,1], [3,2], [0,3]]
        elif cell_nums==10:
            self.holes = [[0,3], [0,5], [0,8], [1,5], [1,8], [2,4], [2,7], [3,0], [3,6], [3,9], [4,2], [4,6], 
                          [5,1], [5,5], [5,8], [5,9], [6,7], [6,8], [7,0], [7,1], [8,1], [8,9], [9,0], [9,4], [9,5]]
        for hole in self.holes:
            self.map[hole[0]][hole[1]]=-1

        # Generate initial state
        self.pos = [0, 0]

        # Generate render parameter
        self.init_render(cell_nums)

    def step(self,action):
        # Action Space: 
        # 0: Up, 1: Right, 2: Down, 3: Left

        # Generate the next state after action
        if action==0 and self.pos[1] > 0:
            self.pos[1]-=1
        elif action==1 and self.pos[0] < self.cell_nums - 1:
            self.pos[0]+=1
        elif action==2 and self.pos[1] < self.cell_nums - 1:
            self.pos[1]+=1
        elif action==3 and self.pos[0] > 0:
            self.pos[0]-=1

        reward = self.map[self.pos[0]][self.pos[1]]

        # if achieve holes or target point, return
        if reward == 1 or reward == -1: return self.pos, reward
        
        # # Time punish
        # reward -= 0.05
        
        # Distance reward
        reward -= (18 - self.pos[0] - self.pos[1]) * 0.003

        # return state and reward
        return self.pos, reward

    def init_render(self, cell_nums):
        # Generate render parameter

        # Initialize pygame
        pygame.init()

        # Define sizes
        self.screen_size = 720
        self.game_size, self.cell_nums = 640, cell_nums
        self.border_size = (self.screen_size - self.game_size) / 2
        self.cell_size = self.game_size / self.cell_nums
        self.line_width = 5
        self.character_size = self.cell_size/3
        self.target_size = self.cell_size - self.line_width

        # Define colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.background_color = (190, 231, 233)
        self.robot_color = (53, 51, 60)
        self.target_color = (230, 206, 172)
        self.hole_color = (244, 96 ,108)
        self.red = (255,0,0)

    def render(self):
        # Draw the board background
        pygame.display.set_caption("Path Planing")
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.draw.rect(self.screen, self.background_color, [0, 0, self.screen_size, self.screen_size])

        # Draw the grid lines
        for i in range(self.cell_nums + 1):
            pygame.draw.line(self.screen, self.black, [self.border_size + i * self.cell_size, self.border_size],
                              [self.border_size + i * self.cell_size, self.screen_size - self.border_size], self.line_width)
            pygame.draw.line(self.screen, self.black, [self.border_size, self.border_size + i * self.cell_size], 
                             [self.screen_size - self.border_size, self.border_size + i * self.cell_size], self.line_width)
        
        # Draw the holes
        for hole_x, hole_y in self.holes:
            pygame.draw.rect(self.screen, self.hole_color, (self.border_size + self.line_width/1.5 + hole_x * self.cell_size,
                self.border_size + self.line_width/1.5 + hole_y * self.cell_size, self.target_size, self.target_size))
        
        # Draw the target point
        pygame.draw.rect(self.screen, self.target_color, (self.border_size + self.line_width/1.5 + (self.cell_nums - 1) * self.cell_size,
                        self.border_size + self.line_width/1.5 + (self.cell_nums - 1) * self.cell_size, self.target_size, self.target_size))

        # Draw the robot
        pygame.draw.circle(self.screen, self.robot_color, [self.border_size + self.cell_size/2 + self.pos[0] * self.cell_size, 
                             self.border_size + self.cell_size/2+ self.pos[1] * self.cell_size], self.character_size, 0)
        
        # Update pygame and delay
        pygame.display.update()
        pygame.time.delay(50)


    def plot_Q_table(self, Q_table):
        # Draw the board background
        pygame.display.set_caption("Path Planing")
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.draw.rect(self.screen, self.background_color, [0, 0, self.screen_size, self.screen_size])
        
        # Draw the grid lines
        for i in range(self.cell_nums + 1):
            pygame.draw.line(self.screen, self.black, [self.border_size + i * self.cell_size, self.border_size],
                              [self.border_size + i * self.cell_size, self.screen_size - self.border_size], self.line_width)
            pygame.draw.line(self.screen, self.black, [self.border_size, self.border_size + i * self.cell_size], 
                             [self.screen_size - self.border_size, self.border_size + i * self.cell_size], self.line_width)

            # Draw the slash lines
            pygame.draw.line(self.screen, self.black, [self.border_size + i * self.cell_size, self.border_size],
                              [self.border_size, self.border_size + i * self.cell_size], int(self.line_width*1.2))
            pygame.draw.line(self.screen, self.black, [self.screen_size - self.border_size, self.border_size + i * self.cell_size],
                              [self.border_size + i * self.cell_size, self.screen_size - self.border_size], int(self.line_width*1.2))
            pygame.draw.line(self.screen, self.black, [self.border_size + i * self.cell_size, self.border_size],
                [self.screen_size - self.border_size, self.screen_size - self.border_size - i * self.cell_size], int(self.line_width*1.2))
            pygame.draw.line(self.screen, self.black, [self.border_size, self.screen_size - self.border_size - i * self.cell_size],
                            [self.border_size + i * self.cell_size, self.screen_size - self.border_size], int(self.line_width * 1.2))

        # Set font and font size
        if self.cell_nums==4:  
            font = pygame.font.Font(None, 35)
        else: 
            font = pygame.font.Font(None, 14)

        # Draw the Q value of each state and action
        for posx in range(self.cell_nums):
            for posy in range(self.cell_nums):
                for action_pos in range(4):

                    text_width, text_height = font.render(str(round(Q_table[posx][posy][action_pos],2)), True, self.black).get_size()
                    if action_pos == 0:
                        position = [self.border_size + (posx + 1/2) * self.cell_size - text_width/2, 
                                    self.border_size + (posy + 1/5) * self.cell_size - text_height/2]
                    elif action_pos == 1:
                        position = [self.border_size + (posx + 4/5) * self.cell_size - text_width/2, 
                                    self.border_size + (posy + 1/2) * self.cell_size - text_height/2]
                    elif action_pos == 2:
                        position = [self.border_size + (posx + 1/2) * self.cell_size - text_width/2, 
                                    self.border_size + (posy + 4/5) * self.cell_size - text_height/2]
                    else:
                        position = [self.border_size + (posx + 1/5 + 1/30) * self.cell_size - text_width/2,
                                    self.border_size + (posy + 1/2) * self.cell_size - text_height/2]
                    
                    if Q_table[posx][posy][action_pos] == max(Q_table[posx][posy]):
                        self.screen.blit(font.render(str(round(Q_table[posx][posy][action_pos],2)), True, self.red), position)
                    else:
                        self.screen.blit(font.render(str(round(Q_table[posx][posy][action_pos],2)), True, self.black), position)

        # Draw the holes, target point
        for hole_x, hole_y in self.holes:
            pygame.draw.rect(self.screen, self.hole_color, (self.border_size + self.line_width/1.5 + hole_x * self.cell_size,
                self.border_size + self.line_width/1.5 + hole_y * self.cell_size, self.target_size, self.target_size))
        pygame.draw.rect(self.screen, self.target_color, (self.border_size + self.line_width/1.5 + (self.cell_nums - 1) * self.cell_size,
                        self.border_size + self.line_width/1.5 + (self.cell_nums - 1) * self.cell_size, self.target_size, self.target_size))
        
        # Update, delay and save 
        pygame.display.update()
        pygame.image.save(self.screen, "./Figure/" + str(self.cell_nums)+"_Q_table.png")
        pygame.time.delay(3000)


    def plot_best_way(self, best_steps):
        # Draw the board background
        pygame.display.set_caption("Path Planing")
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.draw.rect(self.screen, self.background_color, [0, 0, self.screen_size, self.screen_size])

        # Draw the grid lines
        for i in range(self.cell_nums + 1):
            pygame.draw.line(self.screen, self.black, [self.border_size + i * self.cell_size, self.border_size],
                              [self.border_size + i * self.cell_size, self.screen_size - self.border_size], self.line_width)
            pygame.draw.line(self.screen, self.black, [self.border_size, self.border_size + i * self.cell_size], 
                             [self.screen_size - self.border_size, self.border_size + i * self.cell_size], self.line_width)
        
        # Draw the holes, target point
        for hole_x, hole_y in self.holes:
            pygame.draw.rect(self.screen, self.hole_color, (self.border_size + self.line_width/1.5 + hole_x * self.cell_size,
                self.border_size + self.line_width/1.5 + hole_y * self.cell_size, self.target_size, self.target_size))
        pygame.draw.rect(self.screen, self.target_color, (self.border_size + self.line_width/1.5 + (self.cell_nums - 1) * self.cell_size,
                        self.border_size + self.line_width/1.5 + (self.cell_nums - 1) * self.cell_size, self.target_size, self.target_size))

        # Draw the robot of best policy
        for best_step_x, best_step_y in best_steps:
            pygame.draw.circle(self.screen, self.red, [self.border_size + self.cell_size/2 + best_step_x * self.cell_size, 
                                self.border_size + self.cell_size/2+ best_step_y * self.cell_size], self.character_size, 0)

        # Update, delay and save 
        pygame.display.update()
        pygame.image.save(self.screen, "./Figure/" + str(self.cell_nums)+"_best_policy.png")
        pygame.time.delay(3000)
