import pygame, os
from Utilities import Constants
from Utilities.Controls import Control
from Grid.Grid import Grid
from Grid.Cell import Type
from Algorithms.Search import Search
from Algorithms.AStar import AStar


class GUI(object):
	def __init__(self):
		self.grid = Grid()							# Setup the grid

		self.optionsText = Control()				# Options text
		self.reloadButton = Control()				# Reload button
		self.saveButton = Control()					# Reload button
		self.loadButton = Control()					# Reload button
		self.astarButton = Control()				# AStar button
		os.environ['SDL_VIDEO_CENTERED'] = '1'		# Center the window

		# Set the screen size, title, and icon
		self.grid_image = pygame.Surface((160.2 * (Constants.WIDTH + Constants.MARGIN), 120.2 * (Constants.HEIGHT + Constants.MARGIN)))
		self.screen = pygame.display.set_mode(Constants.WINDOW_SIZE)
		pygame.display.set_caption("Heuristic Search")
		pygame.display.set_icon(pygame.image.load('Resources/icon.png'))

		# Initialize pygame
		pygame.init()

		# Used to manage how fast the screen updates (60 FPS)
		clock = pygame.time.Clock()
		clock.tick(60)

	# Any updates to be made while the program is running
	def update(self):
		done = False

		while not done:
			self.grid_image.fill(Constants.GREEN)
			self.screen.fill(Constants.WHITE)


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				elif event.type == pygame.MOUSEBUTTONDOWN:
					# Get the position from mouse click
					pos = pygame.mouse.get_pos()	

					# RELOAD BUTTON CLICKED
					if self.reloadButton.pressed(pos):
						self.grid = Grid()
					# LOAD BUTTON CLICKED
					elif self.loadButton.pressed(pos):
						self.grid.load()
					# SAVE BUTTON CLICKED
					elif self.saveButton.pressed(pos):
						self.grid.save()
					elif self.astarButton.pressed(pos):
						astarAlgo = AStar(self.grid.cells, self.grid.startLocation, self.grid.goalLocation)
						self.grid.setPath(astarAlgo.search())
					
					# Convert x/y screen coordinates to grid coordinates				 
					column = pos[0] // (Constants.WIDTH + Constants.MARGIN)	- 4	 # Change the x screen coordinate to grid coordinate
					row = pos[1] // (Constants.HEIGHT + Constants.MARGIN) - 4	 # Change the y screen coordinate to grid coordinate

					# Print out the coordinates if clicked inside grid
					if(row > -1 and row < Constants.ROWS and column > -1 and column < Constants.COLUMNS):
						print("Grid coordinates: (", row, ",", column, ")")
					

			# Draw the grid
			self.draw()

			# Update the screen
			pygame.display.flip()

		# Prevent hang if idle
		pygame.quit()


	# All the draw calls for the screen
	def draw(self):
		# Draw boxes (surface, color, rectangle[x, y, width, height], width)
		pygame.draw.rect(self.screen, Constants.BLACK, [18, 18, 805, 605], 1)			# Border around grid
		pygame.draw.rect(self.screen, Constants.DARK_BLUE, [850, 18, 230, 400], 1)		# Box on right

		# Button (surface, color, x, y, length, height, width, text, text_color)
		self.loadButton.create_button(self.screen, Constants.DARK_BLUE, 850, 527, 110, 40, 0, "Load Map", (255,255,255))
		self.saveButton.create_button(self.screen, Constants.DARK_BLUE, 970, 527, 110, 40, 0, "Save Map", (255,255,255))
		self.reloadButton.create_button(self.screen, Constants.PINK, 850, 577, 230, 45, 0, "Regenerate Map", (255,255,255))
		self.astarButton.create_button(self.screen, Constants.DARK_BLUE, 850, 430, 90, 40, 0, "AStar", (255,255,255))

		# Draw text (surface, text, text_color, length, height, x, y)
		self.optionsText.write_text(self.screen, "Options", Constants.BLACK, 150, 100, 890, 450)

		# Draw the grid
		full_width, full_height = Constants.MARGIN + Constants.WIDTH, Constants.MARGIN + Constants.HEIGHT

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
				pygame.draw.rect(self.grid_image, color, [full_width * column + Constants.MARGIN, full_height * row + Constants.MARGIN, Constants.WIDTH, Constants.HEIGHT])

		# Draw grid area onto the screen with given offset
		self.screen.blit(self.grid_image, (Constants.X_OFFSET, Constants.Y_OFFSET))


# Check if this script is being run directly (if it is, then __name__ becomes __main__)
if __name__ == '__main__':
    gui = GUI()
    gui.update()
