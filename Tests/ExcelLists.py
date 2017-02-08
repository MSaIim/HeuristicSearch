# Headers (String,, startRow, startColumn)
headers = [
	("Start", 1, 0), ("Goal", 1, 1), ("Average", 13, 0),
	("AStar",          0, 3),  ("Time", 1, 3),  ("Path Length", 1, 4),  ("Nodes Expanded", 1, 5),
	("Uniform Cost",   0, 7),  ("Time", 1, 7),  ("Path Length", 1, 8),  ("Nodes Expanded", 1, 9),
	("Manhattan 1.25", 0, 11), ("Time", 1, 11), ("Path Length", 1, 12), ("Nodes Expanded", 1, 13),
	("Manhattan 2.00", 0, 15), ("Time", 1, 15), ("Path Length", 1, 16), ("Nodes Expanded", 1, 17),
	("Euclidean 1.25", 0, 19), ("Time", 1, 19), ("Path Length", 1, 20), ("Nodes Expanded", 1, 21),
	("Euclidean 2.00", 0, 23), ("Time", 1, 23), ("Path Length", 1, 24), ("Nodes Expanded", 1, 25),
	("Diagonal 1.25",  0, 27), ("Time", 1, 27), ("Path Length", 1, 28), ("Nodes Expanded", 1, 29),
	("Diagonal 2.00",  0, 31), ("Time", 1, 31), ("Path Length", 1, 32), ("Nodes Expanded", 1, 33),
	("Chebyshev 1.25", 0, 35), ("Time", 1, 35), ("Path Length", 1, 36), ("Nodes Expanded", 1, 37),
	("Chebyshev 2.00", 0, 39), ("Time", 1, 39), ("Path Length", 1, 40), ("Nodes Expanded", 1, 41)
]

avgHeader = [("Average", 13, 0), ("Average", 28, 0), ("Average", 43, 0), ("Average", 58, 0), ("Average", 73, 0)]


# Rows and columns where the data begins printing
dataRows = [2, 17, 32, 47, 62]
dataCols = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39]
dataAvgs = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90), (90, 100)]
