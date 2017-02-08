import subprocess, os, platform, sys
from Tests.MapTester import MapTester

# Map list to run tests on and the excel workbook file path
mapList = ["Resources/maps/Map01.map", "Resources/maps/Map02.map"]
filename = "Resources/maps/Trials0.xls"

# Run the tests
test = MapTester(mapList, filename)
test.run()

# Open the workbook
if platform.system() == "Windows":
	os.startfile(os.path.realpath(filename))
elif platform.system() == "Darwin":
	subprocess.Popen(["open", os.path.realpath(filename)])
else:
	subprocess.Popen(["xdg-open", os.path.realpath(filename)])
