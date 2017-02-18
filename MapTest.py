from MapTester.MapTester import MapTester

# The weights to test
weight1, weight2 = 1.25, 2.0

# Excel workbook file path and Map list to run tests on
workbook = "Resources/benchmarks/TestTrial.xls"
mapList  = ["Resources/maps/Map1.map", "Resources/maps/Map2.map", "Resources/maps/Map3.map", "Resources/maps/Map4.map", "Resources/maps/Map5.map"]

# Run the tests
maptest = MapTester(workbook, mapList, weight1, weight2)
maptest.run()
maptest.results()
