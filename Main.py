import pygame, os, math
import Utilities.Constants as Constants
import Algorithms.Formulas as Formulas
from Utilities.Controls import Control
from Grid.Grid import Grid
from Grid.Cell import Type
from Algorithms.Search import Search
from Algorithms.AStar import AStar
from Algorithms.AStarWeighted import AStarWeighted


class GUI(object):
	def __init__(self):
		self.grid = Grid()							# Setup the grid

		self.reloadButton = Control()				# Reload button
		self.saveButton = Control()					# Reload button
		self.loadButton = Control()					# Reload button
		self.astarButton = Control()				# AStar button
		self.astarWeightedButton = Control()		# AStarWeighted button
		self.uniformCostButton = Control()			# Uniform Cost button

		# For information


		# Set the screen size, position, title, and icon
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		self.screen = pygame.display.set_mode(Constants.WINDOW_SIZE)
		self.gridSurface = pygame.Surface((160.2 * (Constants.WIDTH + Constants.MARGIN), 120.2 * (Constants.HEIGHT + Constants.MARGIN)))
		pygame.display.set_caption("Heuristic Search")
		pygame.display.set_icon(pygame.image.load('Resources/icon.png'))

		# Initialize pygame
		pygame.init()

		# Used to manage how fast the screen updates (60 FPS)
		clock = pygame.time.Clock()
		clock.tick(60)

		# Setup the interface
		self.setup()

	# Setup the interface with buttons and text
	def setup(self):
		self.screen.fill(Constants.WHITE)

		# Draw boxes (surface, color, rectangle[x, y, width, height], width)
		pygame.draw.rect(self.screen, Constants.BLACK, [18, 18, 965, 725], 1)			# Border around grid
		pygame.draw.rect(self.screen, Constants.DARK_BLUE, [1030, 28, 230, 200], 1)		# Information box
		pygame.draw.rect(self.screen, Constants.DARK_BLUE, [1030, 260, 230, 200], 1)		# Algoirthms box
		pygame.draw.rect(self.screen, Constants.WHITE, [1080, 10, 125, 100])				# White box (information)
		pygame.draw.rect(self.screen, Constants.WHITE, [1090, 230, 115, 100])			# White box (algorithms)

		# Draw text (surface, text, text_color, text_size, x, y)
		self.write_text("Information", Constants.BLACK, 20, 1085, 20)
		self.write_text("Algorithms", Constants.BLACK, 20, 1095, 250)
		self.write_text("Options", Constants.BLACK, 20, 1105, 610)
		self.write_text("Cell:", Constants.BLACK, 18, 1070, 65)
		self.write_text("f(n):", Constants.BLACK, 18, 1070, 95)
		self.write_text("g(n):", Constants.BLACK, 18, 1070, 125)
		self.write_text("h(n):", Constants.BLACK, 18, 1070, 155)
		self.write_text("Time:", Constants.BLACK, 18, 1070, 185)

		# Button (surface, color, x, y, length, height, width, text, text_color)
		self.loadButton.create_button(self.screen, Constants.DARK_BLUE, 1030, 650, 110, 40, 0, "Load Map", (255,255,255))
		self.saveButton.create_button(self.screen, Constants.DARK_BLUE, 1150, 650, 110, 40, 0, "Save Map", (255,255,255))
		self.reloadButton.create_button(self.screen, Constants.PINK, 1030, 695, 230, 45, 0, "Regenerate Map", (255,255,255))
		self.astarButton.create_button(self.screen, Constants.DARK_BLUE, 1055, 295, 180, 40, 0, "   AStar   ", (255,255,255))
		self.astarWeightedButton.create_button(self.screen, Constants.DARK_BLUE, 1055, 345, 180, 40, 0, "Weighted A*", (255,255,255))
		self.uniformCostButton.create_button(self.screen, Constants.DARK_BLUE, 1055, 395, 180, 40, 0, "Uniform Cost", (255,255,255))


	# Run the loop to handle input and draw calls
	def run(self):
		done = False

		while not done:
			self.gridSurface.fill(Constants.GREEN)		# Reset the grid area

			# Handle any input
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				else:
					self.handleInput(event)
		
			# Draw the grid
			self.drawGrid()

			# Mouse over cell
			x, y = pygame.mouse.get_pos()
			pygame.draw.rect(self.gridSurface, Constants.NEON_GREEN, [x-22, y-22, 8, 8], 1)

			# Draw grid area onto the screen with given offset
			self.screen.blit(self.gridSurface, (Constants.X_OFFSET, Constants.Y_OFFSET))

			# Update the screen
			pygame.display.flip()

		# Prevent hang if idle
		pygame.quit()


	# Handle any input
	def handleInput(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Get the position from mouse click
			pos = pygame.mouse.get_pos()	

			# RELOAD BUTTON CLICKED
			if self.reloadButton.pressed(pos):
				self.grid = Grid()
				self.setup()
			# LOAD BUTTON CLICKED
			elif self.loadButton.pressed(pos):
				self.grid.load()
				self.setup()
			# SAVE BUTTON CLICKED
			elif self.saveButton.pressed(pos):
				self.grid.save()
			elif self.astarButton.pressed(pos):
				astarAlgo = AStar(self.grid.cells, self.grid.startLocation, self.grid.goalLocation)
				self.grid.setPath(astarAlgo.search())
			elif self.astarWeightedButton.pressed(pos):
				astarWeightedAlgo = AStarWeighted(self.grid.cells, self.grid.startLocation, self.grid.goalLocation, 2.5)
				self.grid.setPath(astarWeightedAlgo.search())
					
			# Convert x/y screen coordinates to grid coordinates				 
			column = pos[0] // (Constants.WIDTH + Constants.MARGIN)	- 3	 # Change the x screen coordinate to grid coordinate
			row = pos[1] // (Constants.HEIGHT + Constants.MARGIN) - 3	 # Change the y screen coordinate to grid coordinate

			# Print out the coordinates if clicked inside grid
			if(row > -1 and row < Constants.ROWS and column > -1 and column < Constants.COLUMNS):
				self.setup()

				# Get cell at position
				cell = self.grid.cells[row, column]
				hn = Formulas.AStarHeuristic(cell, self.grid.goalLocation)
				fn = cell.G + hn

				# Draw text (surface, text, text_color, text_size, x, y)
				self.write_text("".join(["(", str(row), ", ", str(column), ")"]), Constants.BLACK, 16, 1130, 65)
				self.write_text(f'{fn:.6f}', Constants.BLACK, 16, 1130, 95)
				self.write_text(f'{cell.G:.6f}', Constants.BLACK, 16, 1130, 125)
				self.write_text(f'{hn:.6f}', Constants.BLACK, 16, 1130, 155)


	# Draw the grid
	def drawGrid(self):
		full_width, full_height = Constants.MARGIN + Constants.WIDTH, Constants.MARGIN + Constants.HEIGHT

		# Draw the grid
		for row in range(Constants.ROWS):
			for column in range(Constants.COLUMNS):
				cell = self.grid.cells[row, column]
				color = Constants.GREEN

				if cell.type == Type.HARD: 		
					color = Constants.GREY				# Hard to traverse
				if cell.type == Type.BLOCKED:
					color = Constants.BLACK				# Blocked path

				if cell.isHighway and cell.type == Type.HARD:
					color = Constants.DARK_BLUE			# Highway and hard to traverse
				if cell.isHighway and cell.type == Type.REGULAR:
					color = Constants.LIGHT_BLUE		# Highway and regular
					
				if cell.isStart == True:			
					color = Constants.WHITE				# Start vertex
				if cell.isGoal == True:			
					color = Constants.RED				# Goal vertex

				if cell.isPath == True:
					color = Constants.YELLOW
					if cell.type == Type.HARD:
						color = Constants.DARK_YELLOW

				# Draw the cell
				pygame.draw.rect(self.gridSurface, color, [full_width * column + Constants.MARGIN, full_height * row + Constants.MARGIN, Constants.WIDTH, Constants.HEIGHT])


	def write_text(self, text, text_color, text_size, x, y):
		myFont = pygame.font.SysFont("Calibri", text_size)
		myFont.set_bold(True)
		myText = myFont.render(text, 1, text_color)
		self.screen.blit(myText, (x, y))

# Check if this script is being run directly (if it is, then __name__ becomes __main__)
if __name__ == '__main__':
    gui = GUI()
    gui.run()
