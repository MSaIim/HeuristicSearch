# ![](http://i.imgur.com/0ScJMnq.png) HeuristicSearch

In this project, the AStar family of algorithms were implemented. To better understand the performance and how a heuristic guides the algorithm, there are five different ones to choose from (All the heuristic formulas can be found under `Algorithms/Formulas.py`), which are:

+ AStar Given
+ Manhattan Distance
+ Euclidean Distance
+ Chebyshev Distance
+ Diagonal Distance

In addition, there is also the Uniform Cost Search algorithm which does not use any heuristic; resulting in the shortest path cost to the goal (Manhattan and Euclidean come really close if their weight is set to one).

## ![](http://i.imgur.com/6M9J6Rh.png1) Implementation
Grid Layout:

+ Eight regions that are hard to traverse (Grey cells)
+ Four highways set which only move horizontal and vertical (Blue lines).
+ 20% of the cells are blocked (Black cells)
+ Everything else is a regular cell (Green cells)
+ A random start (White cell) and goal (Red cell) location are set

Algorithms:

A minimum heap was used to store the nodes that will be expanded in a structure called the fringe (open list). This way the node with the higest priority (cost of traversing + the heuristic) will be expanded next. Using two 2D boolean arrays to check if a node was in the closed or open list drastically improved the time complexity from `O(n)` to `O(1)`.

## ![](http://i.imgur.com/QsYSAfQ.png?1) Screenshots
This shows the path from start to goal (in yellow) using the AStar algorithm with the given heuristic.
<p align="center">
<img src="http://i.imgur.com/zVWLYp0.png" />
</p>

## ![] (http://i.imgur.com/O7Vcbty.png?1) Setup
You must have `Python 3.6` installed with `pygame` and `numpy`. If you have Python2 installed alongside Pythong3, then run the following commands using `pip3`.

Install [pygame](http://www.pygame.org/download.shtml) and [numpy](http://www.pygame.org/download.shtml)

    pip install pygame
    pip install numpy
    
Once those are installed, just double click `Main.pyw` and everything should work. Please note: clicking on "Weighted AStar", "Start-Goal Pair", "Load Map", or "Save Map" buttons can bring up their pop up diaglog windows behind the main window sometimes.
