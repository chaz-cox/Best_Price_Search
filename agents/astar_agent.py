#!/usr/bin/env python3

import gymnasium as gym
import best_price
import random
from best_price_search import BestPriceSearch, Node, stateIndex
import enum
# from best_price.envs import BestPriceModel 
# from gym import envs
# from queue import Queue, LifoQueue, PriorityQueue
# import numpy as np
class ActionIndex(enum.IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    BUYAPPLE = 4
    BUYORANGE = 5
    BUYBANNANA = 6

def get_index(x, y, width,height):
    if x >=width or x < 0 or y >= height or y < 0:
        # print("ERR: INVALID POSITION",x,y)
        #invalid coordinates return none
        return None
    return y*width+ x 
   
def get_coordinates(pos,width):
    x = pos % width
    y = pos // width
    return x,y


def model_search_actions(node, goal,width=7, height=5):
    # input("goal="+str(goal))
    actions = []
    direction = ActionIndex
    # state = best_price.BestPriceState()
    pos = node._state[stateIndex.POSITION]
    # input("current pos="+str(pos))
    x, y = get_coordinates(pos, width)

    if get_index(x,y+1,width,height) != None:
        actions.append(direction.DOWN)
        if get_index(x,y+1,width, height) == goal:
            return [direction.DOWN]
    if get_index(x,y-1,width,height) != None:
        actions.append(direction.UP)
        if get_index(x,y-1,width, height) == goal:
            return [direction.UP]
    if get_index(x+1,y,width, height) != None:
        actions.append(direction.RIGHT)
        if get_index(x+1,y,width,height) == goal:
            return [direction.RIGHT]
    if get_index(x-1,y,width,height) != None:
        actions.append(direction.LEFT)
        if get_index(x-1,y,width, height) == goal:
            return [direction.LEFT]
    return actions



def model_search_result(node, action, goal, width=7, height=5):
    # input("action = "+str(action))
    # state = best_price.BestPriceState()
    keepStuff = node._state[stateIndex.BAG:]
    direction = ActionIndex
    new_pos = node._state[stateIndex.POSITION] 
    x, y = get_coordinates(new_pos,width)
    if action == direction.UP:
        # input("action = up y-1")
        new_pos = get_index(x,y-1, width, height)
    elif action == direction.DOWN:
        # print(state.get_index(x,y+1))
        # input("action = down y+1")
        new_pos = get_index(x,y+1, width,height)
    elif action == direction.RIGHT:
        # input("action = right x+1")
        new_pos = get_index(x+1,y, width, height)
    elif action == direction.LEFT:
        # input("action = left x-1")
        new_pos = get_index(x-1,y, width, height)
    else:
        print("ERR: this action did not move position",action)
        return
    
    new_state = tuple([new_pos]) + keepStuff
    parent = node
    new_action = action
    f = node._f
    g = node._g

    child = Node(new_state,parent,new_action,f,g)
    child.calculateG(new_action, parent, new_state) 
    child.calculateF(new_state, goal)
    return child

def main():
    # rooms= 6 #2, 4
    # room_size = 6 #4, 5 
    grid = BestPriceSearch(1, False)#, rooms, room_size)
    grid.episode(model_search_actions, model_search_result)
    grid.printScore()


if __name__ == "__main__":
    main()
    

