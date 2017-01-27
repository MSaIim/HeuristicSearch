import pygame, os
from Buttons import Button
from Grid import Grid
from Cell import Type

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
BLUE = (66, 134, 244)
GREEN = (129, 226, 140)
PINK = (183, 62, 137)


# Width and Height of a Cell along with the margin between them
WIDTH = 4
HEIGHT = 4
MARGIN = 1

# Initialize the Grid and center the screen
grid = Grid()
button = Button()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize pygame
pygame.init()
WINDOW_SIZE = [801, 701]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Heuristic Search")
pygame.display.set_icon(pygame.image.load('images/icon.png'))

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Get the position from mouse click
			pos = pygame.mouse.get_pos()

			# Change the x/y screen coordinates to grid coordinates
			column = pos[0] // (WIDTH + MARGIN)
			row = pos[1] // (HEIGHT + MARGIN)

			# Print out the coordinates
			print("Grid coordinates: (", row, ",", column, ")")

	# Set the screen background
	screen.fill(BLACK)
	#                    surface.  color.      x.   y. length.  height. width
	button.create_button(screen, (183,62,137), 20, 611, 200,    75,    0,        "Reload", (255,255,255))


	# Draw the grid
	for row in range(120):
		for column in range(160):
			color = WHITE
			if grid.cells[row][column].type == Type.HARD:
				color = GREY
			if grid.cells[row][column].isHighway == True:
				color = BLUE
			if grid.cells[row][column].type == Type.BLOCKED:
				color = BLACK
			if grid.cells[row][column].isStart == True:
				color = GREEN
			if grid.cells[row][column].isGoal == True:
				color = PINK

			pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

	# Limit to 60 frames per second
	clock.tick(60)
	
	# Update the screen
	pygame.display.flip()



# Prevent hang if idle
pygame.quit()