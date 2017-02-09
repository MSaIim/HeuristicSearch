# Headers (String,, startRow, startColumn)
headers = [
	("Start", 1, 0), ("Goal", 1, 1), ("Average", 13, 0),
	("AStar (From PDF)",    0, 3),  ("Time (ms)", 1, 3),  ("Path Length (cost)", 1, 4),  ("Nodes Expanded", 1, 5),
	("Uniform Cost Search", 0, 7),  ("Time (ms)", 1, 7),  ("Path Length (cost)", 1, 8),  ("Nodes Expanded", 1, 9),
	("Manhattan ",          0, 11), ("Time (ms)", 1, 11), ("Path Length (cost)", 1, 12), ("Nodes Expanded", 1, 13),
	("Manhattan ",          0, 15), ("Time (ms)", 1, 15), ("Path Length (cost)", 1, 16), ("Nodes Expanded", 1, 17),
	("Euclidean ",   	    0, 19), ("Time (ms)", 1, 19), ("Path Length (cost)", 1, 20), ("Nodes Expanded", 1, 21),
	("Euclidean ",   		0, 23), ("Time (ms)", 1, 23), ("Path Length (cost)", 1, 24), ("Nodes Expanded", 1, 25),
	("Diagonal ",    		0, 27), ("Time (ms)", 1, 27), ("Path Length (cost)", 1, 28), ("Nodes Expanded", 1, 29),
	("Diagonal ",    		0, 31), ("Time (ms)", 1, 31), ("Path Length (cost)", 1, 32), ("Nodes Expanded", 1, 33),
	("Chebyshev ",   		0, 35), ("Time (ms)", 1, 35), ("Path Length (cost)", 1, 36), ("Nodes Expanded", 1, 37),
	("Chebyshev ",   		0, 39), ("Time (ms)", 1, 39), ("Path Length (cost)", 1, 40), ("Nodes Expanded", 1, 41)
]
avgHeader = [("Average", 13, 0), ("Average", 28, 0), ("Average", 43, 0), ("Average", 58, 0), ("Average", 73, 0)]

# Averages Headers and Heuristics
avgHeaders = [("Heuristics", 2, 1), ("Time (ms)", 2, 2), ("Path Length (cost)", 2, 3), ("Nodes Expanded", 2, 4)]

heuristics = [
	("AStar (From PDF)", 3, 1),  ("Uniform Cost Search (*)", 4, 1), 
	("Manhattan ",       5, 1),  ("Manhattan ",              6, 1), 
	("Euclidean ",       7, 1),  ("Euclidean ",              8, 1), 
	("Diagonal ",        9, 1),  ("Diagonal ",              10, 1), 
	("Chebyshev ",       11, 1), ("Chebyshev ",             12, 1), 
]

# Rows and columns where the data begins printing
dataRows = [2, 17, 32, 47, 62]
dataCols = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39]
dataAvgs = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90), (90, 100)]

