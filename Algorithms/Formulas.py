import math
from copy import deepcopy

from Utilities import Constants
from Grid.Cell import Type, Cell, Point


class Formulas(object):
	@staticmethod
	def AStarHeuristic(s, goal):
		a = math.sqrt(2)
		min_XY = min(abs(s.X - goal.X), abs(s.Y - goal.Y))
		max_XY = max(abs(s.X - goal.X), abs(s.Y - goal.Y))

		return (a * min_XY) + max_XY - min_XY


	@staticmethod
	def Successors(s, grid):
		cells = []

		for row in range(s.X-1, s.X+2):
			for col in range(s.Y-1, s.Y+2):
				if(row == s.X and col == s.Y):
					continue

				if(row < 0 or row > Constants.ROWS-1 or col < 0 or col > Constants.COLUMNS-1):
					continue

				if(grid[row][col].type != Type.BLOCKED):
					cells.append(grid[row][col])

		return cells


	@staticmethod
	def PathCost(s, sprime):
		cost = 0
		sType = s.type
		sprimeType = sprime.type

		if(s.X != sprime.X and s.Y != sprime.Y):
			if(sType == Type.REGULAR and sprimeType == Type.REGULAR):
				cost = math.sqrt(2)
			elif(sType == Type.HARD and sprimeType == Type.HARD):
				cost = math.sqrt(8)
			elif((sType == Type.REGULAR and sprimeType == Type.HARD) or (sType == Type.HARD and sprimeType == Type.REGULAR)):
				cost = (math.sqrt(2) + math.sqrt(8)) / 2
		else:
			if(sType == Type.REGULAR and sprimeType == Type.REGULAR):
				cost = 0.25 if s.isHighway and sprime.isHighway else 1
			elif(sType == Type.HARD and sprimeType == Type.HARD):
				cost = 0.50 if s.isHighway and sprime.isHighway else 2
			elif((sType == Type.REGULAR and sprimeType == Type.HARD) or (sType == Type.HARD and sprimeType == Type.REGULAR)):
				cost = 0.375 if s.isHighway and sprime.isHighway else 1.5

		return cost
