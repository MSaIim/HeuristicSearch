from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["Algorithms/Heap.pyx", "Algorithms/Formulas.pyx", "Algorithms/Search.pyx", 
    	"Algorithms/AStar.pyx", "Algorithms/WeightedAStar.pyx", "Algorithms/UniformCost.pyx"]),
)