from gymnasium.envs.registration import register

from best_price.envs.best_price_env import BestPriceEnv
from best_price.envs.best_price_model import BestPriceModel
from best_price.envs.best_price_model import BestPriceState

register(
    # best_price is this folder name
    # -v0 is because this first version
    # BestPrice is the pretty name for gym.make
    id="best_price/BestPrice-v0",
    
    # best_price.envs is the path best_price/envs
    # BestPriceEnv is the class name
    entry_point="best_price.envs:BestPriceEnv",
    
    # configure the automatic wrapper to truncate after 50 steps
    max_episode_steps=50,
)
