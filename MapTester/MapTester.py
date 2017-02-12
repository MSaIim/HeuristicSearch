import xlwt, sys, subprocess, os, platform
import MapTester.ExcelLists as ExcelLists
from MapTester.AlgoRunner import AlgoRunner


class MapTester(object):
  def __init__(self, mapList, excelSheet, weight1, weight2):
    self.book = xlwt.Workbook()
    self.avgSheet = self.book.add_sheet("Averages")
    self.mapSheet = self.book.add_sheet("Benchmarks")

    # Save info
    self.excelSheet = excelSheet

    # Make the grid
    self.algos = AlgoRunner(mapList, weight1, weight2)

    # Print message if list bigger than 5
    if(len(mapList) > 5):
      print("Only up to five maps may be tested at a time. Testing only the first five given.\n")
      sys.stdout.flush()


  # Open the map and run the algorithms
  def run(self):
    print("Please wait, this may take a couple of minutes...")
    sys.stdout.flush()

    for i in range(len(self.algos.mapList)):
      print("> ", end="")
      sys.stdout.flush()

      # Load map and run algorithms
      self.algos.loadMap(i)
      self.algos.runAll()

      # Write to Excel sheet
      self.writeMapData(i)

      # Clear lists for next map
      self.algos.clearDataLists()

      # Map done
      print(''.join([" [Map", str(i+1), " Done]"]))

    # Writes total averages and save excel sheet
    self.writeAvgData()
    self.book.save(self.excelSheet)


  # Open the workbook to see results
  def results(self):
    if platform.system() == "Windows":
      os.startfile(os.path.realpath(self.excelSheet))
    elif platform.system() == "Darwin":
      subprocess.Popen(["open", os.path.realpath(self.excelSheet)])
    else:
      subprocess.Popen(["xdg-open", os.path.realpath(self.excelSheet)])


  # Write data to excel sheet
  def writeMapData(self, row):
    # Cell properties
    map_cell = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;' 'font: colour white, bold True;')
    algo_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white, bold True; align: horiz center;')
    head_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white; align: horiz right;')
    sng_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white;')

    # Print the map number above start write_merge(top_row, bottom_row, left_column, right_column)
    self.mapSheet.write_merge(ExcelLists.dataRows[row]-2, ExcelLists.dataRows[row]-2, 0, 1, ''.join(["Map", str(row+1)]), map_cell)

    # Print the headers
    isWeight1 = True
    for i in range(len(ExcelLists.headers)):
      # Print the heuristics
      if(ExcelLists.headers[i][1] == 0):
        # Default heuristic
        heuristic = ExcelLists.headers[i][0]

        # Get the different weights
        if(ExcelLists.headers[i][2] >= 13 and isWeight1):
          isWeight1 = False
          heuristic = ''.join([ExcelLists.headers[i][0], "(w=", str(self.algos.weight1), ")"])
        elif(ExcelLists.headers[i][2] >= 13 and isWeight1 == False):
          isWeight1 = True
          heuristic = ''.join([ExcelLists.headers[i][0], "(w=", str(self.algos.weight2), ")"])

        # Write the heuristic (top_row, bottom_row, left_column, right_column)
        self.mapSheet.write_merge(ExcelLists.dataRows[row]-2, ExcelLists.dataRows[row]-2, ExcelLists.headers[i][2], ExcelLists.headers[i][2]+3, heuristic, algo_cell)

      # Print the data headers (Check if column is "Path Length", "Nodes Expanded", or "Memory (KB)" for width)
      elif(ExcelLists.headers[i][1] == 1):
        if(ExcelLists.headers[i][2] >= 3 and ExcelLists.headers[i][0] != "Time (ms)"):
          self.mapSheet.col(ExcelLists.headers[i][2]).width = 4500
          self.mapSheet.write(ExcelLists.dataRows[row]-1, ExcelLists.headers[i][2], ExcelLists.headers[i][0], head_cell)
        else:
          self.mapSheet.write(ExcelLists.dataRows[row]-1, ExcelLists.headers[i][2], ExcelLists.headers[i][0], sng_cell)

      # Everything else ("Average")
      else: # (top_row, bottom_row, left_column, right_column)
        self.mapSheet.write_merge(ExcelLists.avgHeader[row][1], ExcelLists.avgHeader[row][1], ExcelLists.avgHeader[row][2], ExcelLists.avgHeader[row][2]+1, ExcelLists.avgHeader[row][0])

    # Write start/goal locations
    for i in range(0, 10):
      self.mapSheet.write(ExcelLists.dataRows[row]+i, 0, "".join(["(", str(self.algos.grid.startLocations[i].X), ",", str(self.algos.grid.startLocations[i].Y), ")"]))
      self.mapSheet.write(ExcelLists.dataRows[row]+i, 1, "".join(["(", str(self.algos.grid.goalLocations[i].X), ",", str(self.algos.grid.goalLocations[i].Y), ")"]))

    # Get the data from the algorithms
    for col in range(len(ExcelLists.dataCols)):
      num = 0
      avgIndex = ExcelLists.dataAvgs[row][0] + col  # Go to next heuristic

      # Go through the algorithm and get the 10 numbers for each column
      for i in range(ExcelLists.dataAvgs[col][0], ExcelLists.dataAvgs[col][1]):
        self.mapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.dataCols[col], self.algos.time[i])
        self.mapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.dataCols[col]+1, self.algos.pathlength[i])
        self.mapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.dataCols[col]+2, self.algos.nodeexpanded[i])
        self.mapSheet.write(ExcelLists.dataRows[row]+num, ExcelLists.dataCols[col]+3, self.algos.memreqs[i])

        # Go to next row
        num += 1

      # Get average of column
      self.mapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col], self.algos.avgTime[avgIndex])
      self.mapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col]+1, self.algos.avgPath[avgIndex])
      self.mapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col]+2, self.algos.avgNode[avgIndex])
      self.mapSheet.write(ExcelLists.dataRows[row]+11, ExcelLists.dataCols[col]+3, self.algos.avgMem[avgIndex])


  # Write averages to excel sheet
  def writeAvgData(self):
    # Cell properties
    detail_cell = xlwt.easyxf('pattern: pattern solid, fore_colour black;' 'font: colour white, bold True; align: horiz center')
    heu_cell = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;' 'font: colour black, bold True;')
    avg_cell = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;' 'font: colour black, bold True; align: horiz right')

    # Write details (top_row, bottom_row, left_column, right_column)
    self.avgSheet.write_merge(1, 1, 1, 5, "Averages across all 5 maps. [Note: (*) means no heuristic.]", detail_cell)

    # Write the headers (Keep "Heuristics" on the left side)
    for i in range(len(ExcelLists.avgHeaders)):
      if(i == 0):
        self.avgSheet.write(ExcelLists.avgHeaders[i][1], ExcelLists.avgHeaders[i][2], ExcelLists.avgHeaders[i][0], heu_cell)
      else:
        self.avgSheet.write(ExcelLists.avgHeaders[i][1], ExcelLists.avgHeaders[i][2], ExcelLists.avgHeaders[i][0], avg_cell)

      # Set the width of the columns
      self.avgSheet.col(ExcelLists.avgHeaders[i][2]).width = 6000


    # Write the heuristics
    isWeight1 = True
    for i in range(len(ExcelLists.heuristics)):
       #Default heuristic
      heuristic = ExcelLists.heuristics[i][0]

      # Get the different weights
      if(ExcelLists.heuristics[i][1] >= 5 and isWeight1):
        isWeight1 = False
        heuristic = ''.join([ExcelLists.heuristics[i][0], "(w=", str(self.algos.weight1), ")"])
      elif(ExcelLists.heuristics[i][1] >= 5 and isWeight1 == False):
        isWeight1 = True
        heuristic = ''.join([ExcelLists.heuristics[i][0], "(w=", str(self.algos.weight2), ")"])

      self.avgSheet.write(ExcelLists.heuristics[i][1], ExcelLists.heuristics[i][2], heuristic)


    # Write the data
    for i in range(len(ExcelLists.heuristics)):
      self.algos.totalAverage(i)
      self.avgSheet.write(ExcelLists.heuristics[i][1], ExcelLists.heuristics[i][2]+1, self.algos.avgAllTime)
      self.avgSheet.write(ExcelLists.heuristics[i][1], ExcelLists.heuristics[i][2]+2, self.algos.avgAllPath)
      self.avgSheet.write(ExcelLists.heuristics[i][1], ExcelLists.heuristics[i][2]+3, self.algos.avgAllNode)
      self.avgSheet.write(ExcelLists.heuristics[i][1], ExcelLists.heuristics[i][2]+4, self.algos.avgAllMem)

