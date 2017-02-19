from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize([
    	"Algorithms/Base/Formulas.pyx", "Algorithms/Base/Heap.pyx", "Algorithms/Base/ManySearch.pyx", "Algorithms/Base/SingleSearch.pyx", 
    	"Algorithms/AStar.pyx", "Algorithms/IntegratedAStar.pyx", "Algorithms/SequentialAStar.pyx", "Algorithms/UniformCost.pyx", "Algorithms/WeightedAStar.pyx",
    	"Grid/Cell.pyx", "Grid/Grid.pyx", 
    	"Utilities/Button.pyx", "Utilities/Constants.pyx", "Utilities/Form.pyx", "Utilities/Selectors.pyx"
    	"Main.pyx"
    ]),
)
