# Headers (String,, startRow, startColumn)
headers = [
  ("Start", 1, 0), ("Goal", 1, 1), ("Average", 13, 0),
  ("AStar (Given Heuristic)", 0, 3),  ("Time (ms)", 1, 3),  ("Path Length (cost)", 1, 4),  ("Nodes Expanded", 1, 5),  ("Memory (KB)", 1, 6),
  ("Uniform Cost Search",     0, 8),  ("Time (ms)", 1, 8),  ("Path Length (cost)", 1, 9),  ("Nodes Expanded", 1, 10), ("Memory (KB)", 1, 11),
  ("Manhattan ",              0, 13), ("Time (ms)", 1, 13), ("Path Length (cost)", 1, 14), ("Nodes Expanded", 1, 15), ("Memory (KB)", 1, 16),
  ("Manhattan ",              0, 18), ("Time (ms)", 1, 18), ("Path Length (cost)", 1, 19), ("Nodes Expanded", 1, 20), ("Memory (KB)", 1, 21),
  ("Euclidean ",              0, 23), ("Time (ms)", 1, 23), ("Path Length (cost)", 1, 24), ("Nodes Expanded", 1, 25), ("Memory (KB)", 1, 26),
  ("Euclidean ",              0, 28), ("Time (ms)", 1, 28), ("Path Length (cost)", 1, 29), ("Nodes Expanded", 1, 30), ("Memory (KB)", 1, 31),
  ("Diagonal ",               0, 33), ("Time (ms)", 1, 33), ("Path Length (cost)", 1, 34), ("Nodes Expanded", 1, 35), ("Memory (KB)", 1, 36),
  ("Diagonal ",               0, 38), ("Time (ms)", 1, 38), ("Path Length (cost)", 1, 39), ("Nodes Expanded", 1, 40), ("Memory (KB)", 1, 41),
  ("Chebyshev ",              0, 43), ("Time (ms)", 1, 43), ("Path Length (cost)", 1, 44), ("Nodes Expanded", 1, 45), ("Memory (KB)", 1, 46),
  ("Chebyshev ",              0, 48), ("Time (ms)", 1, 48), ("Path Length (cost)", 1, 49), ("Nodes Expanded", 1, 50), ("Memory (KB)", 1, 51)
]
avgHeader = [("Average", 13, 0), ("Average", 28, 0), ("Average", 43, 0), ("Average", 58, 0), ("Average", 73, 0)]

# Averages Headers and Heuristics
avgHeaders = [("Heuristics", 2, 1), ("Time (ms)", 2, 2), ("Path Length (cost)", 2, 3), ("Nodes Expanded", 2, 4), ("Memory (KB)", 2, 5)]

heuristics = [
  ("AStar (Given Heuristic)", 3, 1),  ("Uniform Cost Search (*)", 4, 1), 
  ("Manhattan ",              5, 1),  ("Manhattan ",              6, 1), 
  ("Euclidean ",              7, 1),  ("Euclidean ",              8, 1), 
  ("Diagonal ",               9, 1),  ("Diagonal ",              10, 1), 
  ("Chebyshev ",             11, 1),  ("Chebyshev ",             12, 1), 
]

# Rows and columns where the data begins printing
dataRows = [2, 17, 32, 47, 62]
dataCols = [3, 8, 13, 18, 23, 28, 33, 38, 43, 48]
dataAvgs = [(0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90), (90, 100)]
