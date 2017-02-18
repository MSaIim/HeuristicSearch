import sys
import Algorithms.Base.Formulas as Formulas
import MapTester.ExcelLists as ExcelLists
from pympler.asizeof import asizeof
from Grid.Grid import Grid
from Algorithms.AStar import AStar
from Algorithms.WeightedAStar import WeightedAStar
from Algorithms.UniformCost import UniformCost


class AlgoRunner(object):
  def __init__(self, mapList, weight1, weight2):
    self.grid = Grid()
    self.weight1 = weight1
    self.weight2 = weight2
    self.mapList = mapList[:5]

    # Lists to keep the data
    self.time = []
    self.pathlength = []
    self.nodeexpanded = []
    self.memreqs = []

    # Averages
    self.avgTime = []
    self.avgPath = []
    self.avgNode = []
    self.avgMem = []


  # Load the given map
  def loadMap(self, index):
    self.grid.load(self.mapList[index])


  # Save the given map
  def saveMap(self, filepath):
    self.grid.save(filepath)


  # Print dot and flush
  def printDot(self):
    print(".", end="")
    sys.stdout.flush()


  # Clear the average and data cells
  def clearDataLists(self):
    self.time.clear()
    self.pathlength.clear()
    self.nodeexpanded.clear()
    

  # Run all the tests
  def runAll(self):
    self.uniformcost()
    self.astarGiven()
    self.astarManhattan()
    self.astarEuclidean()
    self.astarDiagonal()
    self.astarChebyshev()
    self.weightedAStarManhattan1()
    self.weightedAStarManhattan2()
    self.weightedAStarEuclidean1()
    self.weightedAStarEuclidean2()
    self.weightedAStarDiagonal1()
    self.weightedAStarDiagonal2()
    self.weightedAStarChebyshev1()
    self.weightedAStarChebyshev2()


  # Average the list up
  def calculateAverage(self, index):
    self.avgTime.append(sum(self.time[ExcelLists.dataAvgs[index][0]:ExcelLists.dataAvgs[index][1]]) / 10)
    self.avgPath.append(sum(self.pathlength[ExcelLists.dataAvgs[index][0]:ExcelLists.dataAvgs[index][1]]) / 10)
    self.avgNode.append(sum(self.nodeexpanded[ExcelLists.dataAvgs[index][0]:ExcelLists.dataAvgs[index][1]]) / 10)
    self.avgMem.append(sum(self.memreqs[ExcelLists.dataAvgs[index][0]:ExcelLists.dataAvgs[index][1]]) / 10)


  # Calculate average across all maps
  def totalAverage(self, index):
    # Get the first values from map 1
    timeAvgTotal = [self.avgTime[index]]
    pathAvgTotal = [self.avgPath[index]]
    nodeAvgTotal = [self.avgNode[index]]
    memAvgTotal  = [self.avgMem[index]]

    # Get values from other maps, if any
    for num in range(1, len(self.mapList)):
      timeAvgTotal.append(self.avgTime[index+14*num])
      pathAvgTotal.append(self.avgPath[index+14*num])
      nodeAvgTotal.append(self.avgNode[index+14*num])
      memAvgTotal.append(self.avgMem[index+14*num])

    # Average them
    self.avgAllTime = sum(timeAvgTotal) / len(timeAvgTotal)
    self.avgAllPath = sum(pathAvgTotal) / len(pathAvgTotal)
    self.avgAllNode = sum(nodeAvgTotal) / len(nodeAvgTotal)
    self.avgAllMem = sum(memAvgTotal) / len(memAvgTotal)


  # Uniform Cost Search algorithm
  def uniformcost(self):
    for i in range(10):
      with UniformCost(self.grid, i) as uniformCost:
        found = uniformCost.search()
        if(found):
          self.time.append(uniformCost.time)
          self.pathlength.append(uniformCost.pathlength)
          self.nodeexpanded.append(uniformCost.nodeexpanded)
          self.memreqs.append(asizeof(uniformCost) / 1000)

    self.calculateAverage(0)
    self.printDot()


  # AStar algorithm with given heuristic
  def astarGiven(self):
    for i in range(10):
      with AStar(self.grid, Formulas.AStarHeuristic, i) as astar:
        found = astar.search()
        if(found):
          self.time.append(astar.time)
          self.pathlength.append(astar.pathlength)
          self.nodeexpanded.append(astar.nodeexpanded)
          self.memreqs.append(asizeof(astar) / 1000)

    self.calculateAverage(1)
    self.printDot()


  # AStar algorithm with manhattan heuristic
  def astarManhattan(self):
    for i in range(10):
      with AStar(self.grid, Formulas.ManhattanDistance, i) as astar:
        found = astar.search()
        if(found):
          self.time.append(astar.time)
          self.pathlength.append(astar.pathlength)
          self.nodeexpanded.append(astar.nodeexpanded)
          self.memreqs.append(asizeof(astar) / 1000)

    self.calculateAverage(2)
    self.printDot()


  # AStar algorithm with euclidean heuristic
  def astarEuclidean(self):
    for i in range(10):
      with AStar(self.grid, Formulas.EuclideanDistance, i) as astar:
        found = astar.search()
        if(found):
          self.time.append(astar.time)
          self.pathlength.append(astar.pathlength)
          self.nodeexpanded.append(astar.nodeexpanded)
          self.memreqs.append(asizeof(astar) / 1000)

    self.calculateAverage(3)
    self.printDot()


  # AStar algorithm with diagonal heuristic
  def astarDiagonal(self):
    for i in range(10):
      with AStar(self.grid, Formulas.DiagonalDistance, i) as astar:
        found = astar.search()
        if(found):
          self.time.append(astar.time)
          self.pathlength.append(astar.pathlength)
          self.nodeexpanded.append(astar.nodeexpanded)
          self.memreqs.append(asizeof(astar) / 1000)

    self.calculateAverage(4)
    self.printDot()


  # AStar algorithm with diagonal heuristic
  def astarChebyshev(self):
    for i in range(10):
      with AStar(self.grid, Formulas.ChebyshevDistance, i) as astar:
        found = astar.search()
        if(found):
          self.time.append(astar.time)
          self.pathlength.append(astar.pathlength)
          self.nodeexpanded.append(astar.nodeexpanded)
          self.memreqs.append(asizeof(astar) / 1000)

    self.calculateAverage(5)
    self.printDot()


  # Weighted AStar algorithm using Manhattan heuristic with a weight of 1.25
  def weightedAStarManhattan1(self):
    for i in range(10):
      with WeightedAStar(self.grid, Formulas.ManhattanDistance, self.weight1, i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(6)
    self.printDot()


  # Weighted AStar algorithm using Manhattan heuristic with a weight of 2.0
  def weightedAStarManhattan2(self):
    for i in range(10):
      with WeightedAStar(self.grid, Formulas.ManhattanDistance, self.weight2, i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(7)
    self.printDot()


  # Weighted AStar algorithm using Euclidean heuristic with a weight of 1.25
  def weightedAStarEuclidean1(self):
    for i in range(10):
      with WeightedAStar(self.grid, Formulas.EuclideanDistance, self.weight1, i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(8)
    self.printDot()


  # Weighted AStar algorithm using Euclidean heuristic with a weight of 2.0
  def weightedAStarEuclidean2(self):
    for i in range(10):
      with WeightedAStar(self.grid, Formulas.EuclideanDistance, self.weight2, i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(9)
    self.printDot()


  # Weighted AStar algorithm using Diagonal heuristic with a weight of 1.25
  def weightedAStarDiagonal1(self):
    for i in range(10):
      with WeightedAStar(self.grid, Formulas.DiagonalDistance, self.weight1, i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(10)
    self.printDot()


  # Weighted AStar algorithm using Diagonal heuristic with a weight of 2.0
  def weightedAStarDiagonal2(self):
    for i in range(10):
      with WeightedAStar(self.grid, Formulas.DiagonalDistance, self.weight2, i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(11)
    self.printDot()


  # Weighted AStar algorithm using Chebyshev heuristic with a weight of 1.25
  def weightedAStarChebyshev1(self):
    for i in range(10):
      with WeightedAStar(self.grid, Formulas.ChebyshevDistance, self.weight1, i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(12)
    self.printDot()


  # Weighted AStar algorithm using Chebyshev heuristic with a weight of 2.0
  def weightedAStarChebyshev2(self):
    for i in range(10):
      with WeightedAStar(self.grid, Formulas.ChebyshevDistance, self.weight2, i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(13)
    self.printDot()
