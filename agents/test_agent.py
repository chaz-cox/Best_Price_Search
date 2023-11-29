#!/usr/bin/env python3

import gymnasium as gym
import best_price
import random
# from best_price.envs import BestPriceModel 
# from gym import envs
# from queue import Queue, LifoQueue, PriorityQueue
# import numpy as np

def agent_function(state,i):
    #go all the way right then down, attept to buy everythig on each location on the second row come, down
    right = [3] * 7
    down = [1]
    buy_left_combo = [4,5,6,2] * 7
    up = [0,0]
    actions = right + down + buy_left_combo + up
    # action = random.choice(best_price.BestPriceModel.ACTIONS(state))
    down_up = [1,0] * 7
    actions = down_up
    print(state)
    input("action "+str(actions[i]))
    return actions[i]

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
    i=0
    while not (terminated or truncated):
        action = agent_function(state,i)
        i+=1
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
    

