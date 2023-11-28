## PEAS ASSESSMENT

> Performance: 
    The performance measure of this project, would be cost effective. Finding the 
    optimal path that has the least amount of cost is the goal. To be more specific
    to get every item that is on the *shopping list* into the *bag* and return to
    start positon with each step costing *gas* money.

> Enviorment: 
    The enviorment is a area rectangle *X width and Y height* also it has *N stores*
    with range of *1 to 100 $* per each item they sale that is on your *shopping list*.
    Each step cost is the *gas* price unless buying, which will be the cost of the item.

The defaults is as follows:
- width = 7
- height = 5
- stores = 4
- gas = 1
- shopping list = [ apples, oranges, bannanas ]
- starting place will always be the same top left corner = 0

    **Observability** Fully observable. All information is given.
  
    **Uncertanty** Deterministic, all things are given to you, though the stores go to random places each restart
  
    **Duration** Sequential, best strategies come from optimal search algorythmns
  
    **Stability** Static, nothing moves until finished.
  
    **Grandularity** Discreet. All values are given.
  
    **Particpants** Single agent will be the only player.
  
    **Knowledge** Known, all nessary physics are known.
  

> Actuators: 
    The actuators are all about moving the player, and buying the items to put in
    the bag.

Actions go as follows:  

**movement actions**:  
    
- up = 0
- down = 1
- left = 2
- right = 3  
    
**buy actions**:  
    
- buy apple = 4
- buy orange = 5
- buy bannana = 6  
    

> Sensors: 
    The locations of each store, the positon of the player, 
    bag / objects holding, shopping list / things needed, 
    and the prices of each item at each store.


## Search Strategy

```
While not at the GOAL_STATE:
    Find the shortest path of each store:
        For each item in each store:
            add path cost to each item
            find cheapest item that you dont have
    go to it and buy it
```

#### shortest path strategies

- Random 

- Astar

<!-- - Iteritive Deepening -->

<!-- - BFS -->

## Statistical Results 

| agent | adverage_score |
|:-----:| -------------- |
| Random|                |
| Astar |                |



