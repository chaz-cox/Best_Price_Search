## PEAS ASSESSMENT

> **Performance:**
> 
>   The performance measure of this project is to be cost-effective. Finding the optimal path with the minimum cost is the goal. To be more specific, the objective is to get every item on the *shopping list* into the *bag* and return to the starting position, with each step incurring a cost in *gas* money.
>
> The performance measure goes as follows: each step is either the gas amount or the amount of an item at a store if the player is at a store.

> **Environment:**
> 
>    The environment is a rectangular area with a width of *X* and height of *Y*. It contains *N stores* offering items on your *shopping list*, each priced between *$1 to $100*. Each step's cost is the *gas* price, unless buying, in which case it's the cost of the item.

    The defaults are as follows:
    - width = 7
    - height = 5
    - stores = 4
    - gas = 1
    - shopping list = [Apples, Oranges, Bananas]
    - the starting place is always the top left corner (0, 0).
    
**Observability:** Fully observable. All information is given.
  
**Uncertainty:** Deterministic; all relevant information is provided, although store locations change randomly with each restart.
  
**Duration:** Sequential; optimal search algorithms are best suited for the task.
  
**Stability:** Static; nothing moves until the task is finished.
  
**Granularity:** Discrete; all values are given.
  
**Participants:** A single agent will be the only player.
  
**Knowledge:** Known; all necessary physics are understood.

> **Actuators:**
> 
>  The actuators are responsible for moving the player and buying items to put in the bag.

Actions are as follows:  

**Movement Actions:**  
    
- up = 0
- down = 1
- left = 2
- right = 3  
    
**Buy Actions:**  
    
- buy apple = 4
- buy orange = 5
- buy banana = 6  

> **Sensors:**
> 
>    The sensors provide information on store locations, player position, bag/objects held, shopping list/things needed, and the prices of each item at each store.

## Search Strategy

```
While not at the GOAL_STATE*:
    Find the shortest path for each store:
        For each item in each store:
            Add path cost to each item
        Find the cheapest item that you don't have
Go to it and buy it
```
*The goal state is to have every item on the shopping list in the bag, and to return to the starting position. 
#### Shortest Path Strategies

- **Random:**
  - *Description:* A random strategy without a specific pathfinding approach.

- **Astar:**
  - *Description:* A* is an optimal and efficient pathfinding algorithm that prioritizes paths with lower estimated costs, guaranteeing completeness and optimality under suitable conditions.

- **Iterative Deepening:**
  - *Description:* IDS is a memory-efficient and adaptable search algorithm that explores increasing depths, making it suitable for problems with unknown depths and offering a balance between memory efficiency and optimality.


## Statistical Results 

Heuristic = 0 

| Agent     | Average Score | Time   |
|:-----:    | ------------- | ------ |
| Astar     | $43            | 0.010  |

Heuristic = Manhattan

| Agent     | Average Score | Time   |
|:-----:    | ------------- | ------ |
| Random    | NO solution    | N/A    |
| Astar     | $94            | 0.005  |
| Iterative | $84            | 0.015  |
