import gymnasium as gym
import best_price 
from queue import PriorityQueue
import enum
import copy

class stateIndex(enum.IntEnum):
    POSITION = 0
    BAG = 1
    STORES = 2
    SHOPPINGLIST = 3
    PRICES = 4

class Node():
    def __init__(self, state, parent, action, f, g,starting=False):
        self._state = self.encode(state,starting)
        # print(self._state)
        self._parent = parent
        self._depth = self.getParentDepth(parent) + 1
        self._action = action 
        self._f = f #node cost -> f = g + h  
        self._g = g #total weights path from start node

    def encode(self,state,starting):
        if not starting:
            return state
        position = tuple([state["position"]])
        bag = tuple([tuple(state["bag"])])
        stores = tuple([tuple(state["stores"])])
        # grid = state["grid"]
        shoppinglist = tuple([tuple(state["shoppinglist"])])
        prices = tuple([tuple(map(tuple,state["prices"]))])
        return(position + bag + stores + shoppinglist +prices)
        


    def addToBag(self, item):
        # (9, (0, 0, 0), (30, 23, 20, 9), (0, 1, 2), ((24, 91, 24), (69, 58, 63), (25, 20, 93), (38, 11, 59)))
        bag = self._state[stateIndex.BAG]
        item_tuple = (bag[item]+1,) #increment
        new_bag = bag[:item]+ item_tuple + bag[item+1:]
        new_state = self._state[:stateIndex.BAG] + tuple([new_bag]) + self._state[stateIndex.BAG+1:]
        self._state = new_state
        return 
        

    def getParentDepth(self, parent):
        if parent:
            return parent.getDepth()
        else:
            return -1 

    def getDepth(self):
        return self._depth

    def goalState(self):
        for item in self._state[stateIndex.BAG]:
            if item == 0:
                return False
        return self._state[stateIndex.POSITION] == 0
    
    def pathGoal(self,goal):
        return self._state[stateIndex.POSITION] == goal

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
    def __init__(self, play_times, human):#,n,s):
        self._playTimes = play_times
        self._adverageScore = 0
        self._env = self.create(human)

    def create(self, human):#,n,s):
          # return gym.make("MiniGrid-MultiRoom-N6-S6-v0", render_mode = "human",)
        if human:
            return gym.make("best_price/BestPrice-v0", render_mode = "human",)
        else:
            return gym.make("best_price/BestPrice-v0",)

    def episode(self, actionsFunc, resultFunc):
        for i in range(self._playTimes):
            observation , info = self._env.reset()
            totalReward = 0
            self._adverageScore += self.run(observation, totalReward, actionsFunc, resultFunc)
        self._adverageScore = self._adverageScore / self._playTimes
        self._env.close()

                
    def run(self, observation, totalReward, actionsFunc, resultFunc):
        g = 0
        f = 0
        prev = None
        action = -1

        node = Node(observation, prev, action, f, g, True)

        actions = self.wrapper(node,actionsFunc, resultFunc)
        if not actions:
            print("NO RESULT FOUND")
            return 0 

        state = best_price.BestPriceState()
        state.observation = observation
        terminated = truncated = False
        while not (terminated or truncated):
            action = actions.pop(0)
            print(state)
            print("action",action)
            input()
            observation, reward, terminated, truncated, info = self._env.step(action)
            state.observation = observation
            totalReward += reward
        return totalReward

    def printScore(self):
        print("Adverage Score:",self._adverageScore)

    def findPath(self, node):
        path = []
        if not node:
            print("ERR finding path. node == None")
            return path
        while node._parent != None:
            path.append(node._action)
            node =node._parent
        return path

#checks the bag if the item is still needed
    def stillNeed(self,node, product):
        print("still need",product)
        if node._state[stateIndex.BAG][product] > 0:
            return False
        return True

    #best deal with the cheapest item
    def findBestDeal(self, prices,cheapest_items):
        if len(cheapest_items) == 0:
            print("ERR: there is no cheap items")
            return 
        price = min(cheapest_items)
        for store in range(len(prices)):
            for product in range(len(prices[store])):
                if prices[store][product] == price:
                    return store, product 
        print("ERR: there was no product for a price of",price)
        return

    def buy(self,dealItem,parent):
        if not parent:
            print("ERR node == None cannot Buy")
            return
        action = dealItem + 4
        f = parent._f
        g = parent._g
        child = Node(parent._state,parent, action, f, g)
        # child.calculateG(action,parent,parent._state)
        # child.calculateF(parent._state,)
        child._state[stateIndex.BAG][dealItem]+=1
        return child

    def haveAllItems(self,node):
        if not node:
            print("ERR node == none dont know if you havve items")
            return True
        for item in node._state[stateIndex.BAG]:
            if item <= 0:
                return False
        return True


#runs my search strategy 
    def wrapper(self, node,actionsFunc, resultFunc):
        all_actions = []
        while not node.goalState():
            prices = []
            cheapest_items = []
            for store in range(len(node._state[stateIndex.STORES])):
                path_node = self.aStar(node,node._state[stateIndex.STORES][store],actionsFunc, resultFunc)
                path = self.findPath(path_node)
                # input("pos"+str(node._state[stateIndex.POSITION])+" store:"+str(store)+str(path))
                cost = len(path) #*gas which is 1 rn
                store_price = []
                cheapest = float("inf")
                for item in range(len(node._state[stateIndex.PRICES][store])):
                    product = node._state[stateIndex.SHOPPINGLIST][item] 
                    # finds the cheapest item needed
                    if float(cheapest) > float(node._state[stateIndex.PRICES][store][item]+cost) and self.stillNeed(node,product):
                        cheapest = int(node._state[stateIndex.PRICES][store][item]+cost)
                    store_price.append(node._state[stateIndex.PRICES][store][item]+cost)
                cheapest_items.append(cheapest)
                prices.append(store_price)
            # print(prices, cheapest_items)
            dealStore, dealItem = self.findBestDeal(prices, cheapest_items)
            # print("GOAL store",dealStore+1)
            node = self.aStar(node, node._state[stateIndex.STORES][dealStore], actionsFunc, resultFunc)
            path_node = copy.deepcopy(node)
            # print(self.findPath(path_node))
            all_actions += self.findPath(path_node)
            all_actions.append(dealItem+4) #buy item 
            node.addToBag(dealItem)
            # input("pos"+str(node._state[stateIndex.POSITION])+" store:"+str(store)+"actions"+str(all_actions)+"bag"+str(node._state[stateIndex.BAG]))
            new_state = node._state
            node = Node(new_state,None,-1,0,0) #kill node parent
            # node = self.buy(dealItem,node)
            if self.haveAllItems(node):
                home= 0 
                node= self.aStar(node,home,actionsFunc, resultFunc)
                print(node._state[stateIndex.POSITION])
                all_actions += self.findPath(node)
                print("GOING HOME", all_actions)
                return all_actions 
        return None


    def aStar(self, node, goal, actionsFunc, resultFunc ):
        node.calculateF(node._state,goal) #just to be safe
        reached = {}
        Q = PriorityQueue()
        Q.put(node)
        reached[node._state] = node
        while not Q.empty():
            s = Q.get()
            if s.pathGoal(goal):
                return s 
            for a in actionsFunc(s,goal):
                S = resultFunc(s,a,goal)
                if (S._state not in reached) or (S._g < reached[S._state]._g):
                    Q.put(S)
                    reached[S._state] = S



