from Environment import Environment
from train import train
import numpy as np
import matplotlib.pyplot as plt

# First-visit Monte Carlo control without exploring starts

# Choose plot each step or not
Plot = True

# Parameters of SARSA
Epsilon = 0.2
Gamma = 0.95
Alpha = 0.2

# Parameter of Map (Size)
# please set cell_nums = 4 or cell_nums = 10
cell_nums = 10

# Define environment and trainer(agent, used for generating the action based on state and updating policy)
env = Environment(cell_nums)
trainer = train(cell_nums ,Epsilon)

# Initialize Q-table and Return table
Q_table=[[[0]*4 for _ in range(cell_nums)] for _ in range(cell_nums)]
Return_table=[[[[] for _ in range(4)] for _ in range(cell_nums)] for _ in range(cell_nums)]

# Initialize reward nums and used for ploting reward figure
reward_nums = []
reward_batch = []
max_batch = 50

# Define episode nums
max_episodes = 20000
for episode in range(max_episodes):
    # Initialize initial state
    next_state = [0,0]
    env.pos = next_state

    # Record trajectory
    Traj=[]
    Traj_state=[]

    # Looping each step of episode
    while True:
        state = next_state.copy()
        
        # Generate action based on state and policy
        action = trainer.get_action(state)
        
        # Plot each step if Plot is True
        if Plot:
            env.render()

        # Generate next state based environment
        next_state, reward = env.step(action)

        # Record trajectory
        Traj.append([state, action, reward])
        Traj_state.append([state])

        # if get positive or negative reward, break 
        if reward==-1:
            print("episode = ",episode,"  lose")
            break
        elif reward==1:
            print("episode = ",episode,"  win")
            break

    # Record reward data
    reward_batch.append(reward)
    if len(reward_batch) == max_batch: 
        reward_nums.append(sum(reward_batch))
        reward_batch = []

    # Loop through each step of the episode (t = T-1, T-2, ..., 0)
    G=0
    for k, pair in enumerate(Traj[::-1]):

        # Update return G
        G = Gamma * G + pair[2]
        if pair[0] not in Traj_state[:len(Traj)-k-1]:
            
            # Update return table
            Return_table[pair[0][0]][pair[0][1]][pair[1]].append(G)

            # Update Q table and policy
            Q_table[pair[0][0]][pair[0][1]][pair[1]] = sum(Return_table[pair[0][0]][pair[0][1]][pair[1]]) / len(Return_table[pair[0][0]][pair[0][1]][pair[1]])
            trainer.update(pair[0], Q_table[pair[0][0]][pair[0][1]])

# Plot reward figure and save it as PNG file
np.savetxt("./Figure/" + str(cell_nums) + "_reward_nums.dat", reward_nums)
plt.plot(np.arange(max_episodes / max_batch), reward_nums)

plt.xlabel("50 Episodes")
plt.ylabel("Reward")
plt.title("Reward Figure")

plt.savefig("./Figure/" + str(cell_nums) + "_reward_plot.png")

plt.show()

# Plot Q table and save it as PNG file
env.plot_Q_table(Q_table)

# Plot best policy and save it as PNG file
next_state = [0, 0]
env.pos = next_state
best_steps = []
best_steps.append(next_state.copy())
for _ in range(20):
    state = next_state.copy()
    # Generate best action based on state and policy
    action = trainer.get_best_action(state)
    next_state, reward = env.step(action)
    best_steps.append(next_state.copy())
    if reward == -1 or reward == 1:
        break
env.plot_best_way(best_steps)