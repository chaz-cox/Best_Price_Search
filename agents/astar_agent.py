#!/usr/bin/env python3

import gymnasium as gym
import best_price
import random
# from best_price.envs import BestPriceModel 
# from gym import envs
# from queue import Queue, LifoQueue, PriorityQueue
# import numpy as np

def agent_function(state):
    """
    state: A best_price.BestPriceState object. The current state of the environment.
    
    returns: An integer, the item to turn over.
    """
    action = random.choice(best_price.BestPriceModel.ACTIONS(state))
    print(state)
    input("action "+str(action))
    return action

def main():
    # item_count = 9

    render_mode = None
    # render_mode = "ansi"
    # render_mode = "rgb_array"
    # render_mode = "human"

    env = gym.make('best_price/BestPrice-v0')
    observation, info = env.reset()
    state = best_price.BestPriceState()
    state.observation = observation
    
    terminated = truncated = False
    if render_mode == "ansi":
        print("Current state:", env.render())
    while not (terminated or truncated):
        action = agent_function(state)
        if render_mode == "ansi":
            print()
            print(f"Action: turn item {action}.")
        observation, reward, terminated, truncated, info = env.step(action)
        print("reward",reward)
        state.observation = observation
        if render_mode == "ansi":
            print("Current state:", env.render())

    env.close()
    return

if __name__ == "__main__":
    main()
    

