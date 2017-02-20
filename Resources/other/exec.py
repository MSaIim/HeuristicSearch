import cx_Freeze
import os, sys

os.environ['TCL_LIBRARY'] = "D:\\Code\\Python\\3.5.2\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "D:\\Code\\Python\\3.5.2\\tcl\\tk8.6"

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("Main.pyw", base=base)]
includes      = ["tkinter"]
include_files = [r"D:\Code\Python\3.5.2\tcl\DLLs\tcl86t.dll", \
                 r"D:\Code\Python\3.5.2\tcl\DLLs\tk86t.dll"]

cx_Freeze.setup(
    name="AStar Algorithm", 
    version = "1.0",
    options={"AStar.exe": {"packages":["pygame", "numpy", "pympler", "cython"], "includes": includes, "include_files": include_files}}, 
    executables = executables)
