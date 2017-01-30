import heapq
from functools import total_ordering
from enum import Enum
from Utilities import Constants

# Enum class to know the Cell's type
class Type(Enum):
	REGULAR = 1
	HARD = 2
	BLOCKED = 3

# The individual Cell
class Cell(object):
	def __init__(self, x, y):
		self.isHighway = False
		self.isStart = False
		self.isGoal = False
		self.type = Type.REGULAR

		# For algorithms
		self.X = int(x)
		self.Y = int(y)
		self.G = float("inf")
		self.parent = None

	def __lt__(self, other):
		return (self.X, self.Y) < (other.X, other.Y)

	# Equals method for use with lists (in, not in)
	def __eq__(self, other):
		return int(self.X) == int(other.X) and int(self.Y) == int(other.Y)

	# Python's toString() method
	def __str__(self):
		return "".join([str(self.X), ",", str(self.Y)])


class PriorityQueue(object):
	def __init__(self):
		self.heap = []


	def push(self, item, priority):
		heapq.heappush(self.heap, (priority, item))


	def pop(self):
		item = heapq.heappop(self.heap)
		#print("".join([str(item[1].X), ",", str(item[1].Y)]))
		return item[1]


	def contains(self, item):
		return item in [x[1] for x in self.heap]


	def isEmpty(self):
		return len(self.heap) == 0


	def remove(self, item):
		index = 0

		for i in range(len(self.heap)):
			if(self.heap[i][1] == item):
				index = i

		# Move slot to be removed to top of heap
		while index > 0:
			up = int((index + 1) / 2 - 1)
			self.heap[index] = self.heap[up]
			index = up

		# Remove top of heap and restore heap property
		heapq.heappop(self.heap)
