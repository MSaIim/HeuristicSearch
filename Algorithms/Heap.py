import heapq
from Utilities import Constants

class PriorityQueue(object):
	def __init__(self):
		self.heap = []


	def push(self, item, priority):
		heapq.heappush(self.heap, (priority, item))


	def pop(self):
		return heapq.heappop(self.heap)[1]


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
