from Algorithms.Heap import *
from Grid.Cell import *

heap = PriorityQueue()

cell1 = Cell(100, 1)
cell2 = Cell(4, 77)
cell3 = Cell(88, 1)
cell4 = Cell(12, 822)
cell5 = Cell(16, 55)

heap.push(cell1, 6)
heap.push(cell2, 2)
heap.push(cell3, 4)
heap.push(cell4, 0)
heap.push(cell5, 5)

print(heap.pop())		# Returns cell4
heap.remove(cell2)		# Deletes cell2
print(heap.pop())		# Would have returned cell2, but now returns cell3
