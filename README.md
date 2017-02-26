# ![](http://i.imgur.com/0ScJMnq.png) HeuristicSearch

In this project, the AStar family of algorithms were implemented to show how a computer can find its own optimal path. To better understand the performance and how a heuristic guides the algorithm, there are five different heuristic implementations (All the heuristic formulas can be found under `Algorithms/Formulas.py`):

+ AStar Given
+ Manhattan Distance
+ Euclidean Distance
+ Chebyshev Distance
+ Diagonal Distance

In addition, there is also the Uniform Cost Search algorithm which does not use any heuristic; resulting in the shortest path cost to the goal (Manhattan and Euclidean give the same path length cost if their weight is set to one).

## ![](http://i.imgur.com/O7Vcbty.png?1) Setup
You must have Python 3+ installed with `pygame` and `numpy`. If you want to run `MapTest.py`, you will need `xlwt` and `pympler` as well. If you have Python2 installed alongside Python3, then run the following commands using `pip3`.

Install [pygame](http://www.pygame.org/download.shtml) and [numpy](http://www.numpy.org) for the main program. Install [xlwt](https://pypi.python.org/pypi/xlwt) and [pympler](https://pypi.python.org/pypi/Pympler) for the `MapTest.py`program.

    pip install pygame numpy
    pip install xlwt pympler

If you have Cython installed, you can gain some performace speed by renaming every `.py` file to `.pyx` and running the `setup.py` file inside the "Resources/other" folder.

Once those are installed, just double click `Main.pyw` and everything should work. Please note: pop up dialog windows from clicking certain buttons (AStar, Weighted A\*, Sequential A\*, and Integrated A\*) may appear behind the main window sometimes.

## ![](http://i.imgur.com/6M9J6Rh.png1) Implementation
Grid Layout:

+ Eight regions that are hard to traverse (Grey cells)
+ Four highway sets which only move horizontal and vertical (Blue lines).
+ 20% of the cells are blocked (Black cells)
+ Everything else is a regular cell (Green cells)
+ A random start (White cell) and goal (Red cell) location are set

Algorithms:

A minimum heap was used to store the nodes that will be expanded in a structure called the fringe (open list). This way the node with the higest priority (cost of traversing + the heuristic) will be expanded next. To reduce the time complexity of checking if a node is in the fringe or closed list from `O(n)` to `O(1)`, 2D boolean arrays were used for each list.

## ![](http://i.imgur.com/QsYSAfQ.png?1) Screenshots
This shows the path from start to goal (in yellow) using the AStar algorithm with the given heuristic.
<p align="center">
<img src="http://i.imgur.com/rGeUY52.png" />
</p>

You may also run the `MapTest.py` program to run tests on the different implementations of the algorithms using the different heuristics. The results will be saved in an Excel workbook with three sheets. Please edit `MapTest.py` to test any maps you want with any given weights. Please note that the tests may take up to 15 minutes to complete (Progress can be viewed in the console window that opens up) and each time you run the `MapTest.py` program, you must give it a new Excel workbook name or rename the one it created in a previous run through. The workbook should look similar to the picture below when done:
<p align="center">
<img src="http://i.imgur.com/creFNQ0.png" />
</p>
