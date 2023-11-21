from Environment import Environment
from train import train
import numpy as np
import matplotlib.pyplot as plt

# Q-learning with an ϵ-greedy behavior policy

# Choose plot each step or not
Plot = True

# Parameters of SARSA
Epsilon = 0.8
Gamma = 0.95
Alpha = 0.2

# Parameter of Map (Size)
# please set cell_nums = 4 or cell_nums = 10
cell_nums = 10

# Define environment and trainer(agent, used for generating the action based on state and updating policy)
env = Environment(cell_nums)
trainer = train(cell_nums ,Epsilon)

# Initialize Q-table
Q_table=[[[0]*4 for _ in range(cell_nums)] for _ in range(cell_nums)]

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

    # Looping each step of episode
    while True:
        # Generate action based on state and policy
        state = next_state.copy()
        action = trainer.get_action(state)

        # Plot each step if Plot is True
        if Plot:
            env.render()

        # Generate next state based environment
        next_state, reward = env.step(action)

        # Generate next action based on next state and policy without exploring
        next_action = trainer.get_best_action(next_state)

        # Update Q table and policy
        Q_table[state[0]][state[1]][action] = Q_table[state[0]][state[1]][action] + Alpha*(reward + Gamma*(Q_table[next_state[0]][next_state[1]][next_action])-Q_table[state[0]][state[1]][action])
        trainer.update(state, Q_table[state[0]][state[1]])

        # if get positive or negative reward, break 
        if reward==-1:
            print("episode = ",episode,"  lose")
            break
        elif reward==1:
            if trainer.Epsilon > 0.2:
                trainer.Epsilon *= 0.8
            elif trainer.Epsilon > 0.02:
                trainer.Epsilon *= 0.98
            print("episode = ",episode,"  win")
            break

    # Record reward data
    reward_batch.append(reward)
    if len(reward_batch) == max_batch: 
        reward_nums.append(sum(reward_batch))
        reward_batch = []

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