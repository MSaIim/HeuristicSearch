# Headers (String,, startRow, startColumn)
headers = [
  ("Start", 1, 0), ("Goal", 1, 1), ("Average", 13, 0),
  ("Uniform Cost Search",     0, 3),  ("Time (ms)", 1, 3),  ("Path Length (cost)", 1, 4),  ("Nodes Expanded", 1, 5),  ("Memory (KB)", 1, 6),
  ("AStar (Given Heuristic)", 0, 8),  ("Time (ms)", 1, 8),  ("Path Length (cost)", 1, 9),  ("Nodes Expanded", 1, 10), ("Memory (KB)", 1, 11),
  ("AStar Manhattan",         0, 13), ("Time (ms)", 1, 13), ("Path Length (cost)", 1, 14), ("Nodes Expanded", 1, 15), ("Memory (KB)", 1, 16),
  ("AStar Euclidean",         0, 18), ("Time (ms)", 1, 18), ("Path Length (cost)", 1, 19), ("Nodes Expanded", 1, 20), ("Memory (KB)", 1, 21),
  ("AStar Diagonal",          0, 23), ("Time (ms)", 1, 23), ("Path Length (cost)", 1, 24), ("Nodes Expanded", 1, 25), ("Memory (KB)", 1, 26),
  ("AStar Chebyshev",         0, 28), ("Time (ms)", 1, 28), ("Path Length (cost)", 1, 29), ("Nodes Expanded", 1, 30), ("Memory (KB)", 1, 31),
  ("Weighted Manhattan ",     0, 33), ("Time (ms)", 1, 33), ("Path Length (cost)", 1, 34), ("Nodes Expanded", 1, 35), ("Memory (KB)", 1, 36),
  ("Weighted Manhattan ",     0, 38), ("Time (ms)", 1, 38), ("Path Length (cost)", 1, 39), ("Nodes Expanded", 1, 40), ("Memory (KB)", 1, 41),
  ("Weighted Euclidean ",     0, 43), ("Time (ms)", 1, 43), ("Path Length (cost)", 1, 44), ("Nodes Expanded", 1, 45), ("Memory (KB)", 1, 46),
  ("Weighted Euclidean ",     0, 48), ("Time (ms)", 1, 48), ("Path Length (cost)", 1, 49), ("Nodes Expanded", 1, 50), ("Memory (KB)", 1, 51),
  ("Weighted Diagonal ",      0, 53), ("Time (ms)", 1, 53), ("Path Length (cost)", 1, 54), ("Nodes Expanded", 1, 55), ("Memory (KB)", 1, 56),
  ("Weighted Diagonal ",      0, 58), ("Time (ms)", 1, 58), ("Path Length (cost)", 1, 59), ("Nodes Expanded", 1, 60), ("Memory (KB)", 1, 61),
  ("Weighted Chebyshev ",     0, 63), ("Time (ms)", 1, 63), ("Path Length (cost)", 1, 64), ("Nodes Expanded", 1, 65), ("Memory (KB)", 1, 66),
  ("Weighted Chebyshev ",     0, 68), ("Time (ms)", 1, 68), ("Path Length (cost)", 1, 69), ("Nodes Expanded", 1, 70), ("Memory (KB)", 1, 71),
  ("Weighted AStar Given ",   0, 73), ("Time (ms)", 1, 73), ("Path Length (cost)", 1, 74), ("Nodes Expanded", 1, 75), ("Memory (KB)", 1, 76),
  ("Weighted AStar Given ",   0, 78), ("Time (ms)", 1, 78), ("Path Length (cost)", 1, 79), ("Nodes Expanded", 1, 80), ("Memory (KB)", 1, 81)
]

# Averages Headers (MapSheet and AverageSheet)
avgHeader = [("Average", 13, 0), ("Average", 28, 0), ("Average", 43, 0), ("Average", 58, 0), ("Average", 73, 0)]
avgHeaders = [("Heuristics", 2, 1), ("Time (ms)", 2, 2), ("Path Length (cost)", 2, 3), ("Nodes Expanded", 2, 4), ("Memory (KB)", 2, 5)]

# Average sheet row headers
heuristics = [
  ("Uniform Cost Search (*)", 3, 1), ("AStar (Given Heuristic)", 4, 1), ("AStar Manhattan", 5, 1), ("AStar Euclidean", 6, 1), ("AStar Diagonal", 7, 1), 
  ("AStar Chebyshev", 8, 1), ("Weighted Manhattan ", 9, 1),  ("Weighted Manhattan ", 10, 1), ("Weighted Euclidean ", 11, 1), ("Weighted Euclidean ", 12, 1), 
  ("Weighted Diagonal ", 13, 1), ("Weighted Diagonal ", 14, 1), ("Weighted Chebyshev ", 15, 1), ("Weighted Chebyshev ", 16, 1), ("Weighted AStar Given ", 17, 1),
  ("Weighted AStar Given ", 18, 1)
]

# Rows and columns where the data begins printing
dataRows = [2, 17, 32, 47, 62]
dataCols = [3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58, 63, 68, 73, 78]
dataAvgs = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90), (90, 100), (100, 110), (110, 120), (120, 130), (130, 140), (140, 150), (150, 160)]

# For printing averages (Will need to change if adding/removing tests)
dataAvgIndex = [0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224]


# /*\ ======================================================================================================
# |*|   PHASE 2 - Includes Sequential A* and Integrated A*
# \*/ ======================================================================================================

# Headers for sequential and integrated A*
setIntHeaders = [
  ("Start", 1, 0), ("Goal", 1, 1), ("Average", 13, 0),
  ("Sequential A* (Anchor=M, Hueristics=A,E,D,C, Weights=", 0, 3),  ("Time (ms)", 1, 3),  ("Path Length (cost)", 1, 4),  ("Nodes Expanded", 1, 5),  ("Memory (KB)", 1, 6),
  ("Sequential A* (Anchor=E, Hueristics=A,M,D,C, Weights=", 0, 8),  ("Time (ms)", 1, 8),  ("Path Length (cost)", 1, 9),  ("Nodes Expanded", 1, 10), ("Memory (KB)", 1, 11),
  ("Sequential A* (Anchor=M, Hueristics=A,E,D,C, Weights=", 0, 13), ("Time (ms)", 1, 13), ("Path Length (cost)", 1, 14), ("Nodes Expanded", 1, 15), ("Memory (KB)", 1, 16),
  ("Sequential A* (Anchor=E, Hueristics=A,M,D,C, Weights=", 0, 18), ("Time (ms)", 1, 18), ("Path Length (cost)", 1, 19), ("Nodes Expanded", 1, 20), ("Memory (KB)", 1, 21),
  ("Integrated A* (Anchor=M, Hueristics=A,E,D,C, Weights=", 0, 23), ("Time (ms)", 1, 23), ("Path Length (cost)", 1, 24), ("Nodes Expanded", 1, 25), ("Memory (KB)", 1, 26),
  ("Integrated A* (Anchor=E, Hueristics=A,M,D,C, Weights=", 0, 28), ("Time (ms)", 1, 28), ("Path Length (cost)", 1, 29), ("Nodes Expanded", 1, 30), ("Memory (KB)", 1, 31),
  ("Integrated A* (Anchor=M, Hueristics=A,E,D,C, Weights=", 0, 33), ("Time (ms)", 1, 33), ("Path Length (cost)", 1, 34), ("Nodes Expanded", 1, 35), ("Memory (KB)", 1, 36),
  ("Integrated A* (Anchor=E, Hueristics=A,M,D,C, Weights=", 0, 38), ("Time (ms)", 1, 38), ("Path Length (cost)", 1, 39), ("Nodes Expanded", 1, 40), ("Memory (KB)", 1, 41),
]

p2Heuristics = [(20, 1), (21, 1), (22, 1), (23, 1), (24, 1), (25, 1), (26, 1), (27, 1)]
p2DataCols = [3, 8, 13, 18, 23, 28, 33, 38]
p2DataAvgIndex = [0, 8, 16, 24, 32, 40, 48, 56]
