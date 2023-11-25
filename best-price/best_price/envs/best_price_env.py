import gymnasium
import numpy as np
from gymnasium import spaces
from best_price.envs.best_price_model import BestPriceModel
from best_price.envs.best_price_model import BestPriceState
from best_price.envs.best_price_model import Items, ActionIndex  

try:
    import pygame
except ImportError as e:
    raise DependencyNotInstalled(
        "pygame is not installed, `pip install` must have failed."
    ) from e

class BestPriceEnv(gymnasium.Env):

    metadata = {
        "render_modes": ["human", "rgb_array", "ansi"],
        "render_fps": 1,
    }

    def __init__(self, render_mode=None, render_fps=None, height=5, width=7, stores=4, shoppinglist=None, gas=1):
        self.render_mode = render_mode
        self.render_fps = render_fps
        self.action_space = spaces.Discrete(7)
        self.height = height
        self.width = width
        self.stores = stores
        self.shoppinglist = shoppinglist
        self.gas = gas
        self.observation_space = spaces.Dict({
            "grid": spaces.Box(low=0, high=6,shape=(height,width),dtype=np.int32),
            "position": spaces.Discrete(height*width),
            "bag": spaces.Box(low=0,high=3,shape=(3,),dtype=np.int32),
            "stores":spaces.Box(low=0,high=3,shape=(3,),dtype=np.int32),
            "shoppinglist": spaces.Box(low=0, high=3, shape=(3,), dtype=np.int32),
            "prices":spaces.Box(low=0, high=3, shape=(3,), dtype=np.int32),
            "gasprice":spaces.Discrete(gas),
            "moneyspent":spaces.Discrete(1),
            })#Ill have to come back to this.. add stores??

        # display support
        # self.cell_size = (800//items_count, 60)
        # self.window_size = (
        #     self.coin_count * self.cell_size[0],
        #     1 * self.cell_size[1],
        # )
        # self.window_surface = None
        # self.clock = None
        # self.head_color = (255, 0, 0)
        # self.tail_color = (0, 0, 255)
        # self.background_color = (170, 170, 170)
        return

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = BestPriceState(self.height,self.width,self.stores,self.shoppinglist,self.gas)
        observation = self.state._STUFF
        info = {}
        return observation, info

    def step(self, action):
        state = self.state
        # print(state)
        state1 = BestPriceModel.RESULT(state, action)
        # print(state1)
        self.state = state1

        # print(state._STUFF)
        # print(state1._STUFF)
        
        observation = state1._STUFF
        reward = BestPriceModel.STEP_COST(state, action, state1)
        terminated = BestPriceModel.GOAL_TEST(state1)
        info = {}

        # display support
        # if self.render_mode == "human":
        #     self.render()
        return observation, reward, terminated, False, info

    # def render(self):
    #     if self.render_mode is None:
    #         assert self.spec is not None
    #         gym.logger.warn(
    #             "You are calling render method without specifying any render mode. "
    #             "You can specify the render_mode at initialization, "
    #             f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
    #         )
    #         return

    #     if self.render_mode == "ansi":
    #         return self._render_text()
    #     else:
    #         return self._render_gui(self.render_mode)

    def _render_text(self):
        return str(self.state)

    # def _render_gui(self, mode):
    #     if self.window_surface is None:
    #         pygame.init()

    #         if mode == "human":
    #             pygame.display.init()
    #             pygame.display.set_caption("Best Price Search")
    #             self.window_surface = pygame.display.set_mode(self.window_size)
    #         else:  # rgb_array
    #             self.window_surface = pygame.Surface(self.window_size)
    #     if self.clock is None:
    #         self.clock = pygame.time.Clock()

    #     rect = pygame.Rect((0,0), self.window_size)
    #     pygame.draw.rect(self.window_surface, self.background_color, rect)
    #     for item in range(self.items_count):
    #         x = (item+0.5)*self.cell_size[0]
    #         y = 0.5*self.cell_size[1]
    #         r = 0.4*min(self.items_count)
    #         if self.state.item(item):
    #             color = self.tail_color
    #         else:
    #             color = self.head_color
    #         pygame.draw.circle(self.window_surface, color, (x,y), r)

    #     if mode == "human":
    #         pygame.event.pump()
    #         pygame.display.update()
    #         self.clock.tick(self.metadata["render_fps"])
    #     else:  # rgb_array
    #         return np.transpose(
    #             np.array(pygame.surfarray.pixels3d(self.window_surface)), axes=(1, 0, 2)
    #         )
    
    # def close(self):
    #     if self.window_surface is not None:
    #         pygame.display.quit()
    #         pygame.quit()
    #     return
    


    
