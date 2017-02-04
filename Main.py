import pygame, os
import Algorithms.Formulas as Formulas
import Utilities.Constants as Constants
from tkinter import messagebox
from Grid.Grid import Grid
from Utilities.Button import Button
from Algorithms.AStar import AStar
from Algorithms.WeightedAStar import WeightedAStar
from Algorithms.UniformCost import UniformCost


class GUI(object):
	def __init__(self):
		# Setup the grid
		self.grid = Grid()

		# For ui elements
		self.buttons = []

		# For algorithms
		self.time = 0
		self.heuristic = Formulas.ManhattanDistance

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
		self.setup_dynamic()
		self.setup_static()


	# /*\ =======================================================================
	# |*|	MAIN GAME LOOP
	# |*|		- run() Handles any updates (input)
	# |*|		- draw() Draws everything on the screen
	# \*/ =======================================================================

	# Run the loop to handle input and draw calls
	def run(self):
		done = False

		while not done:
			self.gridSurface.fill(Constants.GREEN)

			# Handle any input
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				else:
					self.handleInput(event)
		
			# Draw the grid and update screen
			self.draw()
			pygame.display.flip()

		# Prevent hang if idle
		pygame.quit()


	# Draw the different elements on screen
	def draw(self):
		# Get mouse position
		mouse = pygame.mouse.get_pos()

		# Draw the buttons
		for button in self.buttons:
			button.draw(self.screen, mouse)

		# Draw grid and selection square
		self.grid.draw(self.gridSurface, mouse)
		pygame.draw.rect(self.gridSurface, Constants.RED, [mouse[0]-22, mouse[1]-22, 8, 8], 1)

		# Draw grid area onto the screen with given offset
		self.screen.blit(self.gridSurface, (Constants.X_OFFSET, Constants.Y_OFFSET))


	# Handle any input
	def handleInput(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Get the position from mouse click
			pos = pygame.mouse.get_pos()	

			# RELOAD BUTTON CLICKED
			if self.reloadButton.pressed(pos):
				del self.grid
				self.grid = Grid()
				self.write_info(self.grid.startLocation.X, self.grid.startLocation.Y)

			# LOAD BUTTON CLICKED
			elif self.loadButton.pressed(pos):
				self.grid.load()
				self.write_info(self.grid.startLocation.X, self.grid.startLocation.Y)

			# SAVE BUTTON CLICKED
			elif self.saveButton.pressed(pos):
				self.grid.save()

			# ASTAR BUTTON CLICKED
			elif self.astarButton.pressed(pos):
				self.heuristic = Formulas.AStarHeuristic
				with AStar(self.grid.cells, self.grid.startLocation, self.grid.goalLocation) as astar:
					self.grid.resetAlgoCells()
					found = astar.search()
					if(found):
						self.grid.setPath(astar.getPath())
					else:
						messagebox.showinfo("AStar Results", "No path could be found to the goal.")

					self.time = astar.time
					self.write_info(self.cell.X, self.cell.Y)

			# WEIGHTED ASTAR BUTTON CLICKED
			elif self.weightedAStarButton.pressed(pos):
				self.heuristic = Formulas.ManhattanDistance
				with WeightedAStar(self.grid.cells, self.grid.startLocation, self.grid.goalLocation, self.heuristic, 2) as weightedAStar:
					self.grid.resetAlgoCells()
					found = weightedAStar.search()
					if(found):
						self.grid.setPath(weightedAStar.getPath())
					else:
						messagebox.showinfo("Weighted AStar Results", "No path could be found to the goal.")

					self.time = weightedAStar.time
					self.write_info(self.cell.X, self.cell.Y)

			# UNIFORM COST BUTTON CLICKED
			elif self.uniformCostButton.pressed(pos):
				self.heuristic = Formulas.NoHeuristic
				with UniformCost(self.grid.cells, self.grid.startLocation, self.grid.goalLocation) as uniformCost:
					self.grid.resetAlgoCells()
					found = uniformCost.search()
					if(found):
						self.grid.setPath(uniformCost.getPath())
					else:
						messagebox.showinfo("Uniform Cost Results", "No path could be found to the goal.")

					self.time = uniformCost.time
					self.write_info(self.cell.X, self.cell.Y)
					
			# Convert x/y screen coordinates to grid coordinates				 
			column = pos[0] // (Constants.WIDTH + Constants.MARGIN) - 3
			row = pos[1] // (Constants.HEIGHT + Constants.MARGIN) - 3

			# Print out the cell information when clicked
			if(row > -1 and row < Constants.ROWS and column > -1 and column < Constants.COLUMNS):
				self.write_info(row, column)


	# /*\ =======================================================================
	# |*|	SETUP UI ELEMENTS
	# |*|		- setup_dynamic() Sets up the elements that change due to 
	# |*|		  screen refresh
	# |*|		- setup_static() Sets up elements that don't get effected
	# \*/ =======================================================================

	# Setup the interface with buttons and text
	def setup_dynamic(self):
		self.screen.fill(Constants.WHITE)

		# Draw boxes (surface, color, rectangle[x, y, width, height], width)
		pygame.draw.rect(self.screen, Constants.BLACK, [18, 18, 965, 725], 1)				# Border around grid
		pygame.draw.rect(self.screen, Constants.DARK_BLUE, [1030, 28, 230, 200], 1)			# Information box
		pygame.draw.rect(self.screen, Constants.DARK_BLUE, [1030, 260, 230, 200], 1)		# Algoirthms box
		pygame.draw.rect(self.screen, Constants.WHITE, [1080, 10, 125, 100])				# White box (information)
		pygame.draw.rect(self.screen, Constants.WHITE, [1090, 230, 115, 100])				# White box (algorithms)

		# Draw text (surface, text, text_color, text_size, x, y)
		self.write_text("Information", Constants.BLACK, 20, 1085, 20)
		self.write_text("Algorithms", Constants.BLACK, 20, 1095, 250)
		self.write_text("Options", Constants.BLACK, 20, 1105, 610)
		self.write_text("Cell:", Constants.BLACK, 18, 1070, 65)
		self.write_text("f(n):", Constants.BLACK, 18, 1070, 95)
		self.write_text("g(n):", Constants.BLACK, 18, 1070, 125)
		self.write_text("h(n):", Constants.BLACK, 18, 1070, 155)
		self.write_text("Time:", Constants.BLACK, 18, 1070, 185)


	# Setup the static elements
	def setup_static(self):
		# Reset info box
		self.heuristic = Formulas.NoHeuristic
		self.write_info(self.grid.startLocation.X, self.grid.startLocation.Y)

		# Buttons (text, text_color, length, height, x_pos, y_pos, btn_color, hover_color)
		self.reloadButton = Button("Regenerate Map", Constants.WHITE, 230, 45, 1030, 695, Constants.PINK, Constants.DARK_PINK)					# Reload button
		self.saveButton = Button("Save Map", Constants.WHITE, 110, 40, 1150, 650, Constants.LIGHT_BLUE, Constants.DARK_BLUE)					# Save button
		self.loadButton = Button("Load Map", Constants.WHITE, 110, 40, 1030, 650, Constants.LIGHT_BLUE, Constants.DARK_BLUE)					# Load button
		self.astarButton = Button("   AStar   ", Constants.WHITE, 180, 40, 1055, 295, Constants.LIGHT_BLUE, Constants.DARK_BLUE)				# AStar button
		self.weightedAStarButton = Button("Weighted A*", Constants.WHITE, 180, 40, 1055, 345, Constants.LIGHT_BLUE, Constants.DARK_BLUE)		# Weighted A* button
		self.uniformCostButton = Button("Uniform Cost", Constants.WHITE, 180, 40, 1055, 395, Constants.LIGHT_BLUE, Constants.DARK_BLUE)		# Unifor Cost button

		# Add buttons to list
		buttonAppend = self.buttons.append
		buttonAppend(self.reloadButton)
		buttonAppend(self.saveButton)
		buttonAppend(self.loadButton)
		buttonAppend(self.astarButton)
		buttonAppend(self.weightedAStarButton)
		buttonAppend(self.uniformCostButton)


	# /*\ =======================================================================
	# |*|	HELPER FUNCTIONS
	# |*|		- write_text() Displays text on the screen
	# |*|		- write_info() Writes inside the information box
	# |*|		- resetInformation() - Resets the text in info box
	# \*/ =======================================================================

	# Write text on the screen
	def write_text(self, text, text_color, text_size, x, y):
		myFont = pygame.font.SysFont("Calibri", text_size)
		myFont.set_bold(True)
		myText = myFont.render(text, 1, text_color)
		self.screen.blit(myText, (x, y))


	# Fill in the information box on the right
	def write_info(self, row, col):
		# Reset screen
		self.setup_dynamic()
		
		# Update the cell info
		self.cell = self.grid.cells[row, col]
		hn = self.heuristic(self.cell, self.grid.goalLocation, self.grid.cells)
		fn = self.cell.G + hn
		gn = self.cell.G

		# Draw text (surface, text, text_color, text_size, x, y)
		if(self.cell is not None):
			self.write_text("".join(["(", str(self.cell.X), ", ", str(self.cell.Y), ")"]), Constants.BLACK, 16, 1130, 65)
			self.write_text(f'{fn:.6f}', Constants.BLACK, 16, 1130, 97)
			self.write_text(f'{gn:.6f}', Constants.BLACK, 16, 1130, 127)
			self.write_text(f'{hn:.2f}', Constants.BLACK, 16, 1130, 157)

		# Print the time it took to find path
		self.write_text("".join([str(self.time), " ms"]), Constants.BLACK, 16, 1130, 187)


# Check if this script is being run directly (if it is, then __name__ becomes __main__)
if __name__ == '__main__':
	gui = GUI()
	gui.run()
