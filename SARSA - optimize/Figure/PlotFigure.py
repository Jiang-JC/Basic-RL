import numpy as np
import matplotlib.pyplot as plt

# Load Reward Figure
reward_nums1 = np.loadtxt("./Figure/10_reward_nums_original.dat")
reward_nums2 = np.loadtxt("./Figure/10_reward_nums_distancepunish.dat")



# Create a figure and axis object
fig, ax = plt.subplots()


# Plot the first curve
ax.plot(np.arange(400), reward_nums1, label='Original')

# Plot the second curve
ax.plot(np.arange(400), reward_nums2, label='Distance Punish')

ax.set_xlabel("50 Episodes")
ax.set_ylabel("Reward")

# Add a legend to the plot
ax.legend()

plt.savefig("./Figure/10_reward_plot_compare.png")
plt.show()