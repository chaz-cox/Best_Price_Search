import numpy as np
import copy
import enum
import random

class Items(enum.IntEnum):
    APPLES = 0
    ORANGES = 1
    BANNANAS = 2

class ActionIndex(enum.IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    BUYAPPLE = 4
    BUYORANGE = 5
    BUYBANNANA = 6


class BestPriceState:
    def __init__(self, height=5, width=7, stores=4, shoppinglist=None, gas=1):
        #default shoppinglist is a list 0,1,2 where each
        #item a number 0-2 has a enum
        if shoppinglist  == None:
            shoppinglist = np.array([Items.APPLES, Items.ORANGES, Items.BANNANAS], dtype=np.int32)

        #there can only be a certain amount of stores for the grid
        #this the number of stores in the game 
        stores = stores % (height)
        if stores == 0:
            stores = 1

        #calculating prices for each store where the stores price is the index
        prices = []
        for i in range(stores):
            apples = random.randint(1,100)
            oranges = random.randint(1,100)
            bannana = random.randint(1,100)
            prices.append(np.array([apples,oranges,bannana]))

        #calculate grid width * hieght. grid:
        # user = -1
        # store = k where k is a number [1, stores]
        # travling_block (nothing) = 0
        self._grid = np.zeros(width*height, dtype=np.int8)

        self._width = width
        self._height = height

        self._shoppinglist = shoppinglist 

        self._position = 0
        #this is location on the grid the user is at
        self._grid[0] = -1 

        self._moneyspent = 0
        self._prices = prices

        self._gasprice = gas

        #items holding is the bag then increments on what you buy
        self._bag = np.zeros(len(shoppinglist), dtype=np.int8)
        self._amounttobuy = [1] * len(shoppinglist) 

        #init store locations
        self._stores = []
        for i in range(stores):
            #Pick a random location every row
            #x pos = random
            #y pos = each row from top going down  
            x = random.randint(0,width-1)
            y = height-1-i
            index = self.get_index(x,y) 
            self._stores.append(index)
            self._grid[index] = i+1 #store number 1-stores

        self._STUFF= {
                "grid": self._grid,
                "position":self._position,
                "bag":self._bag,
                "stores":self._stores,
                "shoppinglist":self._shoppinglist,
                "prices":self._prices,
                "gasprice":self._gasprice,
                "moneyspent":self._moneyspent,
                }
                
            
        return
#############################################
#getters
    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def shoppinglist(self):
        return self._shoppinglist

    @property
    def position(self):
        return self._position

    @property
    def moneyspent(self):
        return self._moneyspent

    @property
    def prices(self):
        return self._prices

    @property
    def bag(self):
        return self._bag

    @property
    def stores(self):
        return self._stores

    @property
    def amounttobuy(self):
        return self._amounttobuy

###########################################

#random stuff kinda happens in init so probs dont need this, but if I do, copy and paste stuff form init
    
    #def randomize(self, seed=None):
    #    if seed is not None:
    #        np.random.seed(seed)
    #        #idk randomize location or prices or items to buy??
    #    self._shoppinglist = np.random.randint(21, 3, dtype=np.int8)
    #    return self._grid

    def turn(self, action):
        #get x and y of your location
        x,y = self.get_coordinates(self._position)

        if action == ActionIndex.UP:
            new_pos = self.get_index(x,y-1)
            if new_pos:
                self._position = new_pos
            self._moneyspent += self._gasprice

        elif action == ActionIndex.DOWN:
            new_pos = self.get_index(x,y+1)
            if new_pos:
                self._position = new_pos
            self._moneyspent += self._gasprice

        elif action == ActionIndex.LEFT:
            new_pos = self.get_index(x-1,y)
            if new_pos:
                self._position = new_pos
            self._moneyspent += self._gasprice

        elif action == ActionIndex.RIGHT:
            new_pos = self.get_index(x+1,y)
            if new_pos:
                self._position = new_pos
            self._moneyspent += self._gasprice

        elif action == ActionIndex.BUYAPPLE:
            store = self.find_store(self._position)
            if store:
                price = self._prices[store][Items.APPLES]
                self._moneyspent += price
                self._bag[Items.APPLES] += 1
            else:
                self._moneyspent += self._gasprice

        elif action == ActionIndex.BUYORANGE:
            store = self.find_store(self._position)
            if store:
                price = self._prices[store][Items.ORANGES]
                self._moneyspent += price
                self._bag[Items.ORANGES] += 1
            else:
                self._moneyspent += self._gasprice

        elif action == ActionIndex.BUYBANNANA:
            store = self.find_store(self._position)
            if store:
                price = self._prices[store][Items.BANNANAS]
                self._moneyspent += price
                self._bag[Items.BANNANAS] += 1
            else:
                self._moneyspent += self._gasprice

        else:
            print(action, "is invalid action")
            return
        self.update()

    def update(self):
        #update stores then position
        self._grid = np.zeros(self._width*self._height, dtype=np.int8)
        for i in range(len(self._stores)):
            location = self._stores[i]
            self._grid[location] = i+1
        self._grid[self._position] = -1
        self.update_stuff()
        return

    @property
    def observation(self):
        return self._grid

    @observation.setter
    def observation(self, value):
        self._STUFF= {
                "grid": self._grid,
                "position":self._position,
                "bag":self._bag,
                "stores":self._stores,
                "shoppinglist":self._shoppinglist,
                "prices":self._prices,
                "gasprice":self._gasprice,
                "moneyspent":self._moneyspent,
        }

        self._STUFF = value
        self._grid = value["grid"]
        self._position = value["position"]
        self._bag = value["bag"]
        self._stores= value["stores"]
        self._prices= value["prices"]
        self._gasprice = value["gasprice"]
        self._moneyspent = value["moneyspent"]
        # self._height = value["grid"].shape[0]
        # self._width = value["grid"].shape[1]
        return #not sure what this does but yeah cool

    def update_stuff(self):
        self._STUFF= {
            "grid": self._grid,
            "position":self._position,
            "bag":self._bag,
            "stores":self._stores,
            "shoppinglist":self._shoppinglist,
            "prices":self._prices,
            "gasprice":self._gasprice,
            "moneyspent":self._moneyspent,
            }
        return
 
    def get_index(self,x, y):
        if x >= self._width or x < 0 or y >= self._height or y < 0:
            #invalid coordinates return none
            return None
        return y*self._width+ x 

    def get_coordinates(self,pos):
        x = pos % self._width
        y = pos // self._width
        return x,y

    def find_store(self,index):
        for s in range(len(self._stores)):
            # print(self._stores[s],index,s, "check")
            if index == self._stores[s]:
                return s
        return None

    def __str__(self):
        s = ""
        #go through the grid and add it out size-1 \n
        for y in range(self._height):
            for x in range(self._width):
                index = self.get_index(x,y)
                if self._grid[index] == 0:
                    s+= "|.|"
                elif self._grid[index] == -1:
                    s += "!u!"
                else:
                    s += "["+str(self._grid[index])+"]"
            s += '\n'

        bag = ""
        slist = ""
        for i in range(len(self._shoppinglist)):
            if self._shoppinglist[i] == Items.APPLES:
                bag+= "  apple: " + str(self._bag[i]) + '\n'
                slist+= "apple "
            elif self._shoppinglist[i] == Items.ORANGES:
                bag+= "  orange: " + str(self._bag[i]) +'\n'
                slist += "orange "
            elif self._shoppinglist[i] == Items.BANNANAS:
                bag+= "  bannana: " + str(self._bag[i]) +'\n'
                slist += "bannana "
            else:
                print("ERR: I dont understand this item in my shoppinglist:",self._shoppinglist[i])

        prices = ""
        items_cost = ["apples","oranges","bannanas"]
        for store in range(len(self._prices)):
            prices +="Store #"+str(store+1) + '\n'
            for item in range(3):
                prices += items_cost[item]+": $"+str(self._prices[store][item]) + '\n'

        s += "Shoppinglist: " +slist + '\n'
        s += "Bag: "+'\n' + bag 
        s+= "Prices: "+ '\n' +  prices
        s+= "Amount So far: " + str(self._moneyspent) +'\n'
        return s


class BestPriceModel:

    def ACTIONS(state):
        actions = [0,1,2,3,4,5,6]
        return actions

    def RESULT(state, action):
        state1 = copy.deepcopy(state)
        state1.turn(action)
        return state1

    def GOAL_TEST(state):
        #if amount to buy == bag and position == 0
        for item in range(len(state.bag)):
            if state.bag[item] < state.amounttobuy[item]:
                return False
        return state.position == 0 

    def STEP_COST(state, action, state1): 
        # this will be the money spent
        cost = state1.moneyspent - state.moneyspent
        return cost 

    def HEURISTIC(state):
        estimated_cost = 0.0
        return estimated_cost

if __name__ == "__main__":
    state = BestPriceState()
    print(state)
    state1 = BestPriceModel.RESULT(state, 1)
    print(state1)
    state2 = BestPriceModel.RESULT(state1,1)
    print(state2)
    state3 = BestPriceModel.RESULT(state2,3)
    print(state3)
    state4 = BestPriceModel.RESULT(state3,3)
    print(state4)
    state5 = BestPriceModel.RESULT(state4,3)
    print(state5)

    state6 = BestPriceModel.RESULT(state5,4)
    print(state6)
    state7 = BestPriceModel.RESULT(state6,5)
    print(state7)
    state8 = BestPriceModel.RESULT(state7,6)
    print(state8)
    # print()
    # state = BestPriceState()
    # print(BestPriceModel.GOAL_TEST(state))
    # state.randomize()
    # print(BestPriceModel.GOAL_TEST(state))
    
    # print()
    # state = BestPriceState()
    # state.randomize()
    # print(state)
    # action = 2
    # state1 = BestPriceModel.RESULT(state, action)
    # print(BestPriceModel.STEP_COST(state, action, state1))

    # def __init__(self, height=5, width=5, stores=3, shoppinglist=None, gas=1):
    tate = BestPriceState(2,2,1,None,1)
    print(tate)
