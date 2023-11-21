# Basic-RL

The project primarily involves solving a path planning problem using three reinforcement learning algorithms. The algorithms used in this project are:
1.	First-visit Monte Carlo control without exploring starts. 
2.	SARSA with an ϵ-greedy behavior policy. 
3.	Q-learning with an ϵ-greedy behavior policy

## Monte Carlo Control

<img src="MonteCarlo\Figure\10_best_policy_original.png" width="300">

<img src="MonteCarlo\Figure\10_reward_plot_orginal.png" width="300">

On the 10 * 10 map, we limited the loop to 2000 episodes for the "First-visit Monte Carlo control without exploring starts" algorithm. This is because obtaining positive rewards on this map is challenging, causing the agent to prefer moving towards the wall or spinning to avoid negative rewards. We set the exploration rate to ϵ = 0.2, which means the probability of exploring new actions is only 15%. As a result, completing an episode can take thousands of steps, making the learning process time-consuming.
Furthermore, the discount factor γ = 0.95 results in moving towards the wall or spinning behavior having slightly higher Q values compared to other behaviors. Since the agent only receives negative rewards, moving towards the wall or spinning is always one step ahead of other exploratory behaviors. As a result, the agent prefers moving toward the wall or spinning, and the best policy learned by the algorithm is simply to move toward the wall.

## SARSA

<img src="SARSA\Figure\10_best_policy_original.png" width="300">

<img src="SARSA\Figure\10_reward_plot_orginal.png" width="300">

From the Q table and the best policy, it is evident that SARSA is capable of learning the 10 * 10 map effectively. However, it may take a considerable amount of time for SARSA to learn the map, despite achieving positive rewards several times. 
Moreover, even after learning the map proficiently, the agent still tends to wander or walk against the wall. This can be observed in the Q table where the difference between the Q values for the agent walking against the wall or wandering on the ground and the Q values for the agent moving towards the target point is very small in many positions.

## Q-Learning

<img src="Qlearning\Figure\10_best_policy_original.png" width="300">

<img src="Qlearning\Figure\10_reward_plot_orginal.png" width="300">

It is evident that Q-learning can learn the 10 * 10 map rapidly and effectively, with a fantastic outcome that surpasses SARSA's performance. In the following part, we will discuss the reasons for this superior performance of Q-learning.
