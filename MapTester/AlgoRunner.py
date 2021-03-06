import sys
import Algorithms.Base.Formulas as Formulas
import MapTester.ExcelLists as ExcelLists
from pympler.asizeof import asizeof
from Grid.Grid import Grid
from Algorithms.AStar import AStar
from Algorithms.WeightedAStar import WeightedAStar
from Algorithms.UniformCost import UniformCost
from Algorithms.SequentialAStar import SequentialAStar
from Algorithms.IntegratedAStar import IntegratedAStar


class AlgoRunner(object):
  def __init__(self, mapList, weights):
    self.grid = Grid()
    self.weights = weights
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


  # Clear the data lists
  def clearDataLists(self):
    self.time.clear()
    self.pathlength.clear()
    self.nodeexpanded.clear()
    self.memreqs.clear()
    

  # Clear the average lists
  def clearAvgLists(self):
    self.avgTime.clear()
    self.avgPath.clear()
    self.avgNode.clear()
    self.avgMem.clear()


  # Run all phase 1 tests
  def runPhase1Tests(self):
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
    self.weightedAStarGiven1()
    self.weightedAStarGiven2()


  # Run all phase 1 tests
  def runPhase2Tests(self):
    self.sequentialAStar1()
    self.sequentialAStar2()
    self.sequentialAStar3()
    self.sequentialAStar4()
    self.integratedAStar1()
    self.integratedAStar2()
    self.integratedAStar3()
    self.integratedAStar4()


  # Average the list up
  def calculateAverage(self, index):
    self.avgTime.append(sum(self.time[ExcelLists.dataAvgs[index][0]:ExcelLists.dataAvgs[index][1]]) / 10)
    self.avgPath.append(sum(self.pathlength[ExcelLists.dataAvgs[index][0]:ExcelLists.dataAvgs[index][1]]) / 10)
    self.avgNode.append(sum(self.nodeexpanded[ExcelLists.dataAvgs[index][0]:ExcelLists.dataAvgs[index][1]]) / 10)
    self.avgMem.append(sum(self.memreqs[ExcelLists.dataAvgs[index][0]:ExcelLists.dataAvgs[index][1]]) / 10)


  # Calculate average across all maps
  def p1TotalAverage(self, index):
    # Get the first values from map 1
    timeAvgTotal = [self.avgTime[index]]
    pathAvgTotal = [self.avgPath[index]]
    nodeAvgTotal = [self.avgNode[index]]
    memAvgTotal  = [self.avgMem[index]]

    # Get values from other maps, if any
    for num in range(1, len(self.mapList)):
      timeAvgTotal.append(self.avgTime[index+16*num])
      pathAvgTotal.append(self.avgPath[index+16*num])
      nodeAvgTotal.append(self.avgNode[index+16*num])
      memAvgTotal.append(self.avgMem[index+16*num])

    # Average them
    self.avgAllTime = sum(timeAvgTotal) / len(timeAvgTotal)
    self.avgAllPath = sum(pathAvgTotal) / len(pathAvgTotal)
    self.avgAllNode = sum(nodeAvgTotal) / len(nodeAvgTotal)
    self.avgAllMem = sum(memAvgTotal) / len(memAvgTotal)


  # Calculate average across all maps
  def p2TotalAverage(self, index):
    # Get the first values from map 1
    timeAvgTotal = [self.avgTime[index]]
    pathAvgTotal = [self.avgPath[index]]
    nodeAvgTotal = [self.avgNode[index]]
    memAvgTotal  = [self.avgMem[index]]

    # Get values from other maps, if any
    for num in range(1, len(self.mapList)):
      timeAvgTotal.append(self.avgTime[index+8*num])
      pathAvgTotal.append(self.avgPath[index+8*num])
      nodeAvgTotal.append(self.avgNode[index+8*num])
      memAvgTotal.append(self.avgMem[index+8*num])

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
      with WeightedAStar(self.grid, Formulas.ManhattanDistance, self.weights[0], i) as weightedAStar:
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
      with WeightedAStar(self.grid, Formulas.ManhattanDistance, self.weights[1], i) as weightedAStar:
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
      with WeightedAStar(self.grid, Formulas.EuclideanDistance, self.weights[0], i) as weightedAStar:
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
      with WeightedAStar(self.grid, Formulas.EuclideanDistance, self.weights[1], i) as weightedAStar:
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
      with WeightedAStar(self.grid, Formulas.DiagonalDistance, self.weights[0], i) as weightedAStar:
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
      with WeightedAStar(self.grid, Formulas.DiagonalDistance, self.weights[1], i) as weightedAStar:
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
      with WeightedAStar(self.grid, Formulas.ChebyshevDistance, self.weights[0], i) as weightedAStar:
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
      with WeightedAStar(self.grid, Formulas.ChebyshevDistance, self.weights[1], i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(13)
    self.printDot()


  # Weighted AStar algorithm using Manhattan heuristic with a weight of 2.0
  def weightedAStarGiven1(self):
    for i in range(10):
      with WeightedAStar(self.grid, Formulas.AStarHeuristic, self.weights[0], i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(14)
    self.printDot()


  # Weighted AStar algorithm using Manhattan heuristic with a weight of 2.0
  def weightedAStarGiven2(self):
    for i in range(10):
      with WeightedAStar(self.grid, Formulas.AStarHeuristic, self.weights[1], i) as weightedAStar:
        found = weightedAStar.search()
        if(found):
          self.time.append(weightedAStar.time)
          self.pathlength.append(weightedAStar.pathlength)
          self.nodeexpanded.append(weightedAStar.nodeexpanded)
          self.memreqs.append(asizeof(weightedAStar) / 1000)

    self.calculateAverage(15)
    self.printDot()


  # Sequential AStar algorithm using Manhattan Anchor
  def sequentialAStar1(self):
    for i in range(10):
      heuristics = [Formulas.ManhattanDistance, Formulas.AStarHeuristic, Formulas.EuclideanDistance, Formulas.DiagonalDistance, Formulas.ChebyshevDistance]
      n = len(heuristics)

      with SequentialAStar(self.grid, n, self.weights[0], self.weights[1], heuristics, i) as seqAStar:
        found = seqAStar.search()
        if(found):
          self.time.append(seqAStar.time)
          self.pathlength.append(seqAStar.pathlength)
          self.nodeexpanded.append(seqAStar.nodeexpanded)
          self.memreqs.append(asizeof(seqAStar) / 1000)

    self.calculateAverage(0)
    self.printDot()


  # Sequential AStar algorithm using Euclidean Anchor
  def sequentialAStar2(self):
    for i in range(10):
      heuristics = [Formulas.EuclideanDistance, Formulas.AStarHeuristic, Formulas.ManhattanDistance, Formulas.DiagonalDistance, Formulas.ChebyshevDistance]
      n = len(heuristics)

      with SequentialAStar(self.grid, n, self.weights[0], self.weights[1], heuristics, i) as seqAStar:
        found = seqAStar.search()
        if(found):
          self.time.append(seqAStar.time)
          self.pathlength.append(seqAStar.pathlength)
          self.nodeexpanded.append(seqAStar.nodeexpanded)
          self.memreqs.append(asizeof(seqAStar) / 1000)

    self.calculateAverage(1)
    self.printDot()


  # Sequential AStar algorithm using Manhattan Anchor
  def sequentialAStar3(self):
    for i in range(10):
      heuristics = [Formulas.ManhattanDistance, Formulas.AStarHeuristic, Formulas.EuclideanDistance, Formulas.DiagonalDistance, Formulas.ChebyshevDistance]
      n = len(heuristics)

      with SequentialAStar(self.grid, n, self.weights[2], self.weights[3], heuristics, i) as seqAStar:
        found = seqAStar.search()
        if(found):
          self.time.append(seqAStar.time)
          self.pathlength.append(seqAStar.pathlength)
          self.nodeexpanded.append(seqAStar.nodeexpanded)
          self.memreqs.append(asizeof(seqAStar) / 1000)

    self.calculateAverage(2)
    self.printDot()


  # Sequential AStar algorithm using Euclidean Anchor
  def sequentialAStar4(self):
    for i in range(10):
      heuristics = [Formulas.EuclideanDistance, Formulas.AStarHeuristic, Formulas.ManhattanDistance, Formulas.DiagonalDistance, Formulas.ChebyshevDistance]
      n = len(heuristics)

      with SequentialAStar(self.grid, n, self.weights[2], self.weights[3], heuristics, i) as seqAStar:
        found = seqAStar.search()
        if(found):
          self.time.append(seqAStar.time)
          self.pathlength.append(seqAStar.pathlength)
          self.nodeexpanded.append(seqAStar.nodeexpanded)
          self.memreqs.append(asizeof(seqAStar) / 1000)

    self.calculateAverage(3)
    self.printDot()


  # Integrated AStar algorithm using Manhattan Anchor
  def integratedAStar1(self):
    for i in range(10):
      heuristics = [Formulas.ManhattanDistance, Formulas.AStarHeuristic, Formulas.EuclideanDistance, Formulas.DiagonalDistance, Formulas.ChebyshevDistance]
      n = len(heuristics)

      with IntegratedAStar(self.grid, n, self.weights[0], self.weights[1], heuristics, i) as intAStar:
        found = intAStar.search()
        if(found):
          self.time.append(intAStar.time)
          self.pathlength.append(intAStar.pathlength)
          self.nodeexpanded.append(intAStar.nodeexpanded)
          self.memreqs.append(asizeof(intAStar) / 1000)

    self.calculateAverage(4)
    self.printDot()


  # Integrated AStar algorithm using Euclidean Anchor
  def integratedAStar2(self):
    for i in range(10):
      heuristics = [Formulas.EuclideanDistance, Formulas.AStarHeuristic, Formulas.ManhattanDistance, Formulas.DiagonalDistance, Formulas.ChebyshevDistance]
      n = len(heuristics)

      with IntegratedAStar(self.grid, n, self.weights[0], self.weights[1], heuristics, i) as intAStar:
        found = intAStar.search()
        if(found):
          self.time.append(intAStar.time)
          self.pathlength.append(intAStar.pathlength)
          self.nodeexpanded.append(intAStar.nodeexpanded)
          self.memreqs.append(asizeof(intAStar) / 1000)

    self.calculateAverage(5)
    self.printDot()


  # Integrated AStar algorithm using Manhattan Anchor
  def integratedAStar3(self):
    for i in range(10):
      heuristics = [Formulas.ManhattanDistance, Formulas.AStarHeuristic, Formulas.EuclideanDistance, Formulas.DiagonalDistance, Formulas.ChebyshevDistance]
      n = len(heuristics)

      with IntegratedAStar(self.grid, n, self.weights[2], self.weights[3], heuristics, i) as intAStar:
        found = intAStar.search()
        if(found):
          self.time.append(intAStar.time)
          self.pathlength.append(intAStar.pathlength)
          self.nodeexpanded.append(intAStar.nodeexpanded)
          self.memreqs.append(asizeof(intAStar) / 1000)

    self.calculateAverage(6)
    self.printDot()


  # Integrated AStar algorithm using Euclidean Anchor
  def integratedAStar4(self):
    for i in range(10):
      heuristics = [Formulas.EuclideanDistance, Formulas.AStarHeuristic, Formulas.ManhattanDistance, Formulas.DiagonalDistance, Formulas.ChebyshevDistance]
      n = len(heuristics)

      with IntegratedAStar(self.grid, n, self.weights[2], self.weights[3], heuristics, i) as intAStar:
        found = intAStar.search()
        if(found):
          self.time.append(intAStar.time)
          self.pathlength.append(intAStar.pathlength)
          self.nodeexpanded.append(intAStar.nodeexpanded)
          self.memreqs.append(asizeof(intAStar) / 1000)

    self.calculateAverage(7)
    self.printDot()
