import heapq

class PriorityQueue(object):
  def __init__(self):
    self.heap = []


  # Push an item onto the heap with the given priority
  def push(self, priority, item):
    heapq.heappush(self.heap, (priority, item))


  # Pop the item that has the highest priority (lowest number)
  def pop(self):
    return heapq.heappop(self.heap)


  # Look at the root element
  def peek(self):
    return self.heap[0];


  # Check if and item is inside the heap
  def contains(self, item):
    return item in [x[1] for x in self.heap]


  # Check if the heap is empty
  def isEmpty(self):
    return len(self.heap) == 0


  # Remove item from the heap if it exists
  def remove(self, item):
    # TODO: Make this not O(n)
    if (item in self.heap):
      self.heap.remove(item)
      heapq.heapify(self.heap)
