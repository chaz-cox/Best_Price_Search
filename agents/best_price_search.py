import gymnasium as gym
import best_price 
from Queue import PriorityQueue

class Node():
    def __init__(self, state, parent, action, f, g):
        self._state = state
        self._parent = parent
        self._depth = self.getParentDepth(parent) + 1
        self._action = action 
        self._f = f #node cost -> f = g + h  
        self._g = g #total weights path from start node

    def getParentDepth(self, parent):
        if parent:
            return parent.getDepth()
        else:
            return -1 

    def getDepth(self):
        return self._depth

    def goalState(self):
        return #TRUE OR FALSE 

    def setF(self, f):
        self._f = f
    
    def setG(self, g):
        self._g = g

    def calculateG(self,a,node,state):
        self._g += self.stepCost(a,node,state)

    def calculateF(self, state,goal):
        self._f = self._g + self.getHeuristic(state, goal)

    def getHeuristic(self, state, goal): #better state
        #calculate Manhattin distance once you get it working
        return 0
    
    def stepCost(self, a, node, state):#action,other_node,better state
        return 1 

    def __lt__(self,other):
        return self._f < other._f

################################################################################

class BestPriceSearch():
    def __init__(self, play_times, human,n,s):
        self._playTimes = play_times
        self._adverageScore = 0
        self._env = self.create(human)

    def create(self, human,n,s):
          # return gym.make("MiniGrid-MultiRoom-N6-S6-v0", render_mode = "human",)
        if human:
            return gym.make("best_price/BestPrice-v0", render_mode = "human",)
        else:
            return gym.make("best_price/BestPrice-v0",)

    def episode(self, actionsFunc, resultFunc, backup):
        for i in range(self._playTimes):
            observation , info = self._env.reset()
            totalReward = 0
            self._adverageScore += self.run(observation, totalReward, actionsFunc, resultFunc, backup)
        self._adverageScore = self._adverageScore / self._playTimes
        self._env.close()

                
    def run(self, observation, totalReward, actionsFunc, resultFunc, backup):
        g = 0
        f = 0
        prev = None
        action = -1

        node = Node(observation, prev, action, f, g)

        s = self.aStar(node,getf,actionsFunc, resultFunc)
        if not s:
            print("NO RESULT FOUND")
            return 0 
        actions = []
        while s._parent != None:
            actions.append(s._action)
            s =s._parent


        terminated = truncated = False
        while not (terminated or truncated):
            observation, reward, terminated, truncated, info = self._env.step(actions.pop())
            totalReward += reward
        return totalReward

    def printScore(self):
        print("Adverage Score:",self._adverageScore)

    def findGoalLocation(self, obs):
        for y in range(obs.shape[1]):
            for x in range(obs.shape[0]):
                index,color,state = obs[x][y]
                obj = constants.IDX_TO_OBJECT[index] 
                colour = constants.IDX_TO_COLOR[color]
                if obj == "goal":
                    return x,y
        print("ERROR COULDNT FIND goal")

    def findAgentLocation(self,obs):
        for y in range(obs.shape[1]):
            for x in range(obs.shape[0]):
                index,color,state = obs[x][y]
                obj = constants.IDX_TO_OBJECT[index] 
                colour = constants.IDX_TO_COLOR[color]
                if obj == "agent":
                    return x,y
        print("ERROR COULDNT FIND agent")
    
    def findDoors(self, obs):
        doors = []
        for y in range(obs.shape[1]):
            for x in range(obs.shape[0]):
                index,color,state = obs[x][y]
                obj = constants.IDX_TO_OBJECT[index] 
                colour = constants.IDX_TO_COLOR[color]
                if obj == "door":
                    doors.append((x,y,state))
        if len(doors)== 0:
            print("ERROR COULDNT FIND a door")
        return doors

    def findWalls(self,obs):
        walls = []
        for y in range(obs.shape[1]):
            for x in range(obs.shape[0]):
                index, color, state = obs[x][y]
                obj = constants.IDX_TO_OBJECT[index]
                if obj == "wall":
                    walls.append((x,y))
        if len(walls) == 0:
            print("ERROR COULDNT FIND a wall")
        return walls
                    

    def encode(self, state):
        x, y = self.findAgentLocation(state["image"])
        direction = state["image"][x][y][2]
        doors = self.findDoors(state["image"])
        return (x, y, direction) + tuple(doors)



    def aStar(self, node, getNodef, actionsFunc, resultFunc, backup):
        # state = self.encode(node._state)
        walls = self.findWalls(node._state["image"])
        goal = self.findGoalLocation(node._state["image"])
        node._state = self.encode(node._state)
        node.calculateF(node._state,goal) #just to be safe
        reached = {}
        if backup:
            Q = PriorityQueueBackup()
        else:
            Q = PriorityQueue(getNodef)
        Q.push(node)
        reached[node._state] = node
        while (not backup and Q.length() > 0) or (backup and not Q.empty()):
            # print(Q.length())
            s = Q.pop()
            if s.goalState(goal):
                return s 
            for a in actionsFunc(s,walls,goal):
                S = resultFunc(s,a,goal)
                if (S._state not in reached) or (S._g < reached[S._state]._g):
                    Q.push(S)
                    reached[S._state] = S



