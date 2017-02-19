import xlwt, sys, subprocess, os, platform
import MapTester.ExcelLists as ExcelLists
from MapTester.AlgoRunner import AlgoRunner


class MapTester(object):
  def __init__(self, excelSheet, mapList, weights):
    self.book = xlwt.Workbook()
    self.avgSheet = self.book.add_sheet("Averages")
    self.p1MapSheet = self.book.add_sheet("Phase1 Benchmarks")
    self.p2MapSheet = self.book.add_sheet("Phase2 Benchmarks")

    # Save info
    self.excelSheet = excelSheet

    # Make the grid
    self.algos = AlgoRunner(mapList, weights)

    # Print message if list bigger than 5
    if(len(mapList) > 5):
      print("Only up to five maps may be tested at a time. Testing only the first five given.\n")
      sys.stdout.flush()


  # Open the map and run the algorithms
  def run(self):
    print("Please wait, this may take a couple of minutes.")
    sys.stdout.flush()

    # Run phase 1 and 2 tests
    self.testPhase1()
    self.testPhase2()

    # Save excel workbook
    self.book.save(self.excelSheet)


  # Run Phase1 Tests
  def testPhase1(self):
    print("\nRunning Phase1 Tests:")
    sys.stdout.flush()

    for i in range(len(self.algos.mapList)):
      print("> ", end="")
      sys.stdout.flush()

      # Load map and run algorithms
      self.algos.loadMap(i)
      self.algos.runPhase1Tests()

      # Write to Excel sheet
      self.writeMapDataPhase1(i)

      # Clear lists for next map
      self.algos.clearDataLists()

      # Map done
      print(''.join([" [Map", str(i+1), " Done]"]))

    # Writes total averages
    self.writeAvgDataPhase1()


  # Run Phase2 Tests
  def testPhase2(self):
    print("\nRunning Phase2 Tests:")
    sys.stdout.flush()

    # Clear lists
    self.algos.clearDataLists()
    self.algos.clearAvgLists()

    for i in range(len(self.algos.mapList)):
      print("> ", end="")
      sys.stdout.flush()

      # Load map and run algorithms
      self.algos.loadMap(i)
      self.algos.runPhase2Tests()

      # Write to Excel sheet
      self.writeMapDataPhase2(i)

      # Clear lists for next map
      self.algos.clearDataLists()

      # Map done
      print(''.join([" [Map", str(i+1), " Done]"]))

    # Writes total averages
    self.writeAvgDataPhase2()


  # Open the workbook to see results
  def results(self):
    if platform.system() == "Windows":
      os.startfile(os.path.realpath(self.excelSheet))
    elif platform.system() == "Darwin":
      subprocess.Popen(["open", os.path.realpath(self.excelSheet)])
    else:
      subprocess.Popen(["xdg-open", os.path.realpath(self.excelSheet)])


  # Write data to excel sheet
  def writeMapDataPhase1(self, row):
    # Cell properties
    map_cell = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;' 'font: colour white, bold True;')
    algo_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white, bold True; align: horiz center;')
    head_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white; align: horiz right;')
    sng_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white;')

    # Print the map number above start write_merge(top_row, bottom_row, left_column, right_column)
    self.p1MapSheet.write_merge(ExcelLists.dataRows[row]-2, ExcelLists.dataRows[row]-2, 0, 1, ''.join(["Map", str(row+1)]), map_cell)

    # Print the headers
    isWeight1 = True
    for i in range(len(ExcelLists.headers)):
      # Print the heuristics
      if(ExcelLists.headers[i][1] == 0):
        # Default heuristic
        heuristic = ExcelLists.headers[i][0]

        # Get the different weights
        if(ExcelLists.headers[i][2] >= 33 and isWeight1):
          isWeight1 = False
          heuristic = ''.join([ExcelLists.headers[i][0], "(w=", str(self.algos.weights[0]), ")"])
        elif(ExcelLists.headers[i][2] >= 33 and isWeight1 == False):
          isWeight1 = True
          heuristic = ''.join([ExcelLists.headers[i][0], "(w=", str(self.algos.weights[1]), ")"])

        # Write the heuristic (top_row, bottom_row, left_column, right_column)
        self.p1MapSheet.write_merge(ExcelLists.dataRows[row]-2, ExcelLists.dataRows[row]-2, ExcelLists.headers[i][2], ExcelLists.headers[i][2]+3, heuristic, algo_cell)

      # Print the data headers (Check if column is "Path Length", "Nodes Expanded", or "Memory (KB)" for width)
      elif(ExcelLists.headers[i][1] == 1):
        if(ExcelLists.headers[i][2] >= 3 and ExcelLists.headers[i][0] != "Time (ms)"):
          self.p1MapSheet.col(ExcelLists.headers[i][2]).width = 4500
          self.p1MapSheet.write(ExcelLists.dataRows[row]-1, ExcelLists.headers[i][2], ExcelLists.headers[i][0], head_cell)
        else:
          self.p1MapSheet.write(ExcelLists.dataRows[row]-1, ExcelLists.headers[i][2], ExcelLists.headers[i][0], sng_cell)

      # Everything else ("Average")
      else: # (top_row, bottom_row, left_column, right_column)
        self.p1MapSheet.write_merge(ExcelLists.avgHeader[row][1], ExcelLists.avgHeader[row][1], ExcelLists.avgHeader[row][2], ExcelLists.avgHeader[row][2]+1, ExcelLists.avgHeader[row][0])

    # Write start/goal locations
    for i in range(0, 10):
      self.p1MapSheet.write(ExcelLists.dataRows[row]+i, 0, "".join(["(", str(self.algos.grid.startLocations[i].X), ",", str(self.algos.grid.startLocations[i].Y), ")"]))
      self.p1MapSheet.write(ExcelLists.dataRows[row]+i, 1, "".join(["(", str(self.algos.grid.goalLocations[i].X), ",", str(self.algos.grid.goalLocations[i].Y), ")"]))

    # Get the data from the algorithms
    for col in range(len(ExcelLists.dataCols)):
      num = 0
      avgIndex = ExcelLists.dataAvgIndex[row] + col  # Go to next heuristic

      # Go through the algorithm and get the 10 numbers for each column
      for i in range(ExcelLists.dataAvgs[col][0], ExcelLists.dataAvgs[col][1]):
        self.p1MapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.dataCols[col]+0, self.algos.time[i])
        self.p1MapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.dataCols[col]+1, self.algos.pathlength[i])
        self.p1MapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.dataCols[col]+2, self.algos.nodeexpanded[i])
        self.p1MapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.dataCols[col]+3, self.algos.memreqs[i])

        # Go to next row
        num += 1

      # Get average of column
      self.p1MapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col]+0, self.algos.avgTime[avgIndex])
      self.p1MapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col]+1, self.algos.avgPath[avgIndex])
      self.p1MapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col]+2, self.algos.avgNode[avgIndex])
      self.p1MapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col]+3, self.algos.avgMem[avgIndex])


  # Write averages to excel sheet
  def writeAvgDataPhase1(self):
    # Cell properties
    det_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white, bold True; align: horiz center')
    heu_cell = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;' 'font: colour black, bold True;')
    avg_cell = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;' 'font: colour black, bold True; align: horiz right')

    # Write details (top_row, bottom_row, left_column, right_column)
    self.avgSheet.write_merge(1, 1, 1, 5, "Averages across all 5 maps. [Note: (*) means no heuristic.]", det_cell)

    # Write the headers (Keep "Heuristics" on the left side)
    for i in range(len(ExcelLists.avgHeaders)):
      if(i == 0):
        self.avgSheet.write(ExcelLists.avgHeaders[i][1], ExcelLists.avgHeaders[i][2], ExcelLists.avgHeaders[i][0], heu_cell)
        self.avgSheet.col(ExcelLists.avgHeaders[i][2]).width = 16000
      else:
        self.avgSheet.write(ExcelLists.avgHeaders[i][1], ExcelLists.avgHeaders[i][2], ExcelLists.avgHeaders[i][0], avg_cell)
        self.avgSheet.col(ExcelLists.avgHeaders[i][2]).width = 6700

    # Write the heuristics
    isWeight1 = True
    for i in range(len(ExcelLists.heuristics)):
       #Default heuristic
      heuristic = ExcelLists.heuristics[i][0]

      # Get the different weights
      if(ExcelLists.heuristics[i][1] >= 9 and isWeight1):
        isWeight1 = False
        heuristic = ''.join([ExcelLists.heuristics[i][0], "(w=", str(self.algos.weights[0]), ")"])
      elif(ExcelLists.heuristics[i][1] >= 9 and isWeight1 == False):
        isWeight1 = True
        heuristic = ''.join([ExcelLists.heuristics[i][0], "(w=", str(self.algos.weights[1]), ")"])

      self.avgSheet.write(ExcelLists.heuristics[i][1], ExcelLists.heuristics[i][2], heuristic)


    # Write the data
    for i in range(len(ExcelLists.heuristics)):
      self.algos.p1TotalAverage(i)
      self.avgSheet.write(ExcelLists.heuristics[i][1], ExcelLists.heuristics[i][2]+1, self.algos.avgAllTime)
      self.avgSheet.write(ExcelLists.heuristics[i][1], ExcelLists.heuristics[i][2]+2, self.algos.avgAllPath)
      self.avgSheet.write(ExcelLists.heuristics[i][1], ExcelLists.heuristics[i][2]+3, self.algos.avgAllNode)
      self.avgSheet.write(ExcelLists.heuristics[i][1], ExcelLists.heuristics[i][2]+4, self.algos.avgAllMem)


  # Write data to excel sheet
  def writeMapDataPhase2(self, row):
    # Cell properties
    map_cell = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;' 'font: colour white, bold True;')
    algo_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white, bold True; align: horiz center;')
    head_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white; align: horiz right;')
    sng_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white;')

    # Print the map number above start write_merge(top_row, bottom_row, left_column, right_column)
    self.p2MapSheet.write_merge(ExcelLists.dataRows[row]-2, ExcelLists.dataRows[row]-2, 0, 1, ''.join(["Map", str(row+1)]), map_cell)

    # Print the headers
    for i in range(len(ExcelLists.setIntHeaders)):
      # Print the heuristics
      if(ExcelLists.setIntHeaders[i][1] == 0):
        # Concatenate weights to heuristic
        if(ExcelLists.setIntHeaders[i][2] == 3 or ExcelLists.setIntHeaders[i][2] == 8 or ExcelLists.setIntHeaders[i][2] == 23 or ExcelLists.setIntHeaders[i][2] == 28):
          heuristic = ''.join([ExcelLists.setIntHeaders[i][0], str(self.algos.weights[0]), ", ", str(self.algos.weights[1]), ")"])
        else:
          heuristic = ''.join([ExcelLists.setIntHeaders[i][0], str(self.algos.weights[2]), ", ", str(self.algos.weights[3]), ")"])

        # Write (top_row, bottom_row, left_column, right_column)
        self.p2MapSheet.write_merge(ExcelLists.dataRows[row]-2, ExcelLists.dataRows[row]-2, ExcelLists.setIntHeaders[i][2], ExcelLists.setIntHeaders[i][2]+3, heuristic, algo_cell)

      # Print the data headers (Check if column is "Path Length", "Nodes Expanded", or "Memory (KB)" for width)
      elif(ExcelLists.setIntHeaders[i][1] == 1):
        if(ExcelLists.setIntHeaders[i][2] >= 3 and ExcelLists.setIntHeaders[i][0] != "Time (ms)"):
          self.p2MapSheet.col(ExcelLists.setIntHeaders[i][2]).width = 4700
          self.p2MapSheet.write(ExcelLists.dataRows[row]-1, ExcelLists.setIntHeaders[i][2], ExcelLists.setIntHeaders[i][0], head_cell)
        else:
          self.p2MapSheet.write(ExcelLists.dataRows[row]-1, ExcelLists.setIntHeaders[i][2], ExcelLists.setIntHeaders[i][0], sng_cell)

      # Everything else ("Average")
      else: # (top_row, bottom_row, left_column, right_column)
        self.p2MapSheet.write_merge(ExcelLists.avgHeader[row][1], ExcelLists.avgHeader[row][1], ExcelLists.avgHeader[row][2], ExcelLists.avgHeader[row][2]+1, ExcelLists.avgHeader[row][0])

    # Write start/goal locations
    for i in range(0, 10):
      self.p2MapSheet.write(ExcelLists.dataRows[row]+i, 0, "".join(["(", str(self.algos.grid.startLocations[i].X), ",", str(self.algos.grid.startLocations[i].Y), ")"]))
      self.p2MapSheet.write(ExcelLists.dataRows[row]+i, 1, "".join(["(", str(self.algos.grid.goalLocations[i].X), ",", str(self.algos.grid.goalLocations[i].Y), ")"]))

    # Get the data from the algorithms
    for col in range(len(ExcelLists.p2DataCols)):
      num = 0
      avgIndex = ExcelLists.p2DataAvgIndex[row] + col  # Go to next heuristic

      # Go through the algorithm and get the 10 numbers for each column
      for i in range(ExcelLists.dataAvgs[col][0], ExcelLists.dataAvgs[col][1]):
        self.p2MapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.p2DataCols[col]+0, self.algos.time[i])
        self.p2MapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.p2DataCols[col]+1, self.algos.pathlength[i])
        self.p2MapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.p2DataCols[col]+2, self.algos.nodeexpanded[i])
        self.p2MapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.p2DataCols[col]+3, self.algos.memreqs[i])

        # Go to next row
        num += 1

      # Get average of column
      self.p2MapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.p2DataCols[col]+0, self.algos.avgTime[avgIndex])
      self.p2MapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.p2DataCols[col]+1, self.algos.avgPath[avgIndex])
      self.p2MapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.p2DataCols[col]+2, self.algos.avgNode[avgIndex])
      self.p2MapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.p2DataCols[col]+3, self.algos.avgMem[avgIndex])


  # Write averages to excel sheet
  def writeAvgDataPhase2(self):
    # Cell properties
    det_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white, bold True; align: horiz center')
    heu_cell = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;' 'font: colour black, bold True;')
    avg_cell = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;' 'font: colour black, bold True; align: horiz right')

    # Write the heuristics (top_row, bottom_row, left_column, right_column)
    heuristic1 = ''.join([ExcelLists.setIntHeaders[3][0], str(self.algos.weights[0]), ", ", str(self.algos.weights[1]), ")"])
    heuristic2 = ''.join([ExcelLists.setIntHeaders[8][0], str(self.algos.weights[0]), ", ", str(self.algos.weights[1]), ")"])
    heuristic3 = ''.join([ExcelLists.setIntHeaders[13][0], str(self.algos.weights[2]), ", ", str(self.algos.weights[3]), ")"])
    heuristic4 = ''.join([ExcelLists.setIntHeaders[18][0], str(self.algos.weights[2]), ", ", str(self.algos.weights[3]), ")"])
    heuristic5 = ''.join([ExcelLists.setIntHeaders[23][0], str(self.algos.weights[0]), ", ", str(self.algos.weights[1]), ")"])
    heuristic6 = ''.join([ExcelLists.setIntHeaders[28][0], str(self.algos.weights[0]), ", ", str(self.algos.weights[1]), ")"])
    heuristic7 = ''.join([ExcelLists.setIntHeaders[33][0], str(self.algos.weights[2]), ", ", str(self.algos.weights[3]), ")"])
    heuristic8 = ''.join([ExcelLists.setIntHeaders[38][0], str(self.algos.weights[2]), ", ", str(self.algos.weights[3]), ")"])

    self.avgSheet.write(ExcelLists.p2Heuristics[0][0], ExcelLists.p2Heuristics[0][1], heuristic1)
    self.avgSheet.write(ExcelLists.p2Heuristics[1][0], ExcelLists.p2Heuristics[0][1], heuristic2)
    self.avgSheet.write(ExcelLists.p2Heuristics[2][0], ExcelLists.p2Heuristics[0][1], heuristic3)
    self.avgSheet.write(ExcelLists.p2Heuristics[3][0], ExcelLists.p2Heuristics[0][1], heuristic4)
    self.avgSheet.write(ExcelLists.p2Heuristics[4][0], ExcelLists.p2Heuristics[0][1], heuristic5)
    self.avgSheet.write(ExcelLists.p2Heuristics[5][0], ExcelLists.p2Heuristics[0][1], heuristic6)
    self.avgSheet.write(ExcelLists.p2Heuristics[6][0], ExcelLists.p2Heuristics[0][1], heuristic7)
    self.avgSheet.write(ExcelLists.p2Heuristics[7][0], ExcelLists.p2Heuristics[0][1], heuristic8)

    # Write the data
    for i in range(len(ExcelLists.p2Heuristics)):
      self.algos.p2TotalAverage(i)
      self.avgSheet.write(ExcelLists.p2Heuristics[i][0], ExcelLists.p2Heuristics[i][1]+1, self.algos.avgAllTime)
      self.avgSheet.write(ExcelLists.p2Heuristics[i][0], ExcelLists.p2Heuristics[i][1]+2, self.algos.avgAllPath)
      self.avgSheet.write(ExcelLists.p2Heuristics[i][0], ExcelLists.p2Heuristics[i][1]+3, self.algos.avgAllNode)
      self.avgSheet.write(ExcelLists.p2Heuristics[i][0], ExcelLists.p2Heuristics[i][1]+4, self.algos.avgAllMem)
