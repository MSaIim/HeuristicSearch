import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import Utilities.Constants as Constants
from tkinter import messagebox
from Grid.Grid import Grid
from Utilities.Button import Button
from Algorithms.AStar import AStar
from Algorithms.WeightedAStar import WeightedAStar
from Algorithms.UniformCost import UniformCost
from Algorithms.SequentialAStar import SequentialAStar
from Algorithms.IntegratedAStar import IntegratedAStar
from Utilities.Selectors import AStarSelector, WeightedSelector, StartGoalSelector, SeqIntSelector


class GUI(object):
  def __init__(self):
    # Setup the screen
    self.grid = Grid()
    self.buttons = []

    # For algorithms
    self.time = 0

    # Set the screen size, position, title, and icon
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    self.screen = pygame.display.set_mode(Constants.WINDOW_SIZE)
    self.gridSurface = pygame.Surface((Constants.COLUMNS * (Constants.WIDTH + Constants.MARGIN), Constants.ROWS * (Constants.HEIGHT + Constants.MARGIN)))
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
  # |*| MAIN GAME LOOP
  # |*|   - run() Handles any updates (input)
  # |*|   - draw() Draws everything on the screen
  # \*/ =======================================================================

  # Run the loop to handle input and draw calls
  def run(self):
    done = False

    while not done:
      self.gridSurface.fill(Constants.LIGHT_GREEN)

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
        self.write_info(self.grid.currentStart.X, self.grid.currentStart.Y)

      # LOAD BUTTON CLICKED
      elif self.loadButton.pressed(pos):
        self.grid.load()
        self.write_info(self.grid.currentStart.X, self.grid.currentStart.Y)

      # SAVE BUTTON CLICKED
      elif self.saveButton.pressed(pos):
        self.grid.save()

      # START-GOAL PAIR CLICKED
      elif self.startGoalButton.pressed(pos):
        sgForm = StartGoalSelector(self.grid.startLocations, self.grid.goalLocations)
        if(sgForm.index >= 0):
          self.grid.resetAlgoCells()
          self.grid.setNewStartGoalPair(sgForm.index)
          self.write_info(self.grid.currentStart.X, self.grid.currentStart.Y)
        del sgForm

      # ASTAR BUTTON CLICKED
      elif self.astarButton.pressed(pos):
        # Ask for heuristic
        astarForm = AStarSelector()

        if(astarForm.heuristic != None):
          with AStar(self.grid, astarForm.heuristic) as astar:
            found = astar.search()
            if(found):
              self.grid.setPath(astar.getPath())
            else:
              messagebox.showinfo("AStar Results", "No path could be found to the goal.")

            self.time = astar.time
            self.write_info(self.clickedCell.X, self.clickedCell.Y)

      # WEIGHTED ASTAR BUTTON CLICKED
      elif self.weightedAStarButton.pressed(pos):
        # Ask for heuristic and weight
        heuForm = WeightedSelector()

        # Run with the given weight and heuristic
        if(heuForm.weight >= 1):
          with WeightedAStar(self.grid, heuForm.heuristic, heuForm.weight) as weightedAStar:
            found = weightedAStar.search()
            if(found):
              self.grid.setPath(weightedAStar.getPath())
            else:
              messagebox.showinfo("Weighted AStar Results", "No path could be found to the goal.")

            self.time = weightedAStar.time
            self.write_info(self.clickedCell.X, self.clickedCell.Y)

        # Remove from memory
        del heuForm

      # UNIFORM COST BUTTON CLICKED
      elif self.uniformCostButton.pressed(pos):
        with UniformCost(self.grid) as uniformCost:
          found = uniformCost.search()
          if(found):
            self.grid.setPath(uniformCost.getPath())
          else:
            messagebox.showinfo("Uniform Cost Results", "No path could be found to the goal.")

          self.time = uniformCost.time
          self.write_info(self.clickedCell.X, self.clickedCell.Y)

      # SEQUENTIAL ASTAR BUTTON CLICKED
      elif self.seqAStarButton.pressed(pos):
        # Ask for anchor, heuristics, and weight
        seqForm = SeqIntSelector()

        # Run with the given weights and heuristics
        if(seqForm.weight1 >= 1 and seqForm.weight2 >= 1):
          heuristics = seqForm.heuristicFunctions
          n = len(heuristics)

          with SequentialAStar(self.grid, n, seqForm.weight1, seqForm.weight2, heuristics) as seqAStar:
            found = seqAStar.search()
            if(found):
              self.grid.setPath(seqAStar.getPath())
            else:
              messagebox.showinfo("Sequential AStar Results", "No path could be found to the goal.")

            self.time = seqAStar.time
            self.write_info(self.clickedCell.X, self.clickedCell.Y)

        # Remove from memory
        del seqForm

       # INTEGRATED ASTAR BUTTON CLICKED
      elif self.intAStarButton.pressed(pos):
        # Ask for anchor, heuristics, and weight
        intForm = SeqIntSelector()

        # Run with the given weights and heuristics
        if(intForm.weight1 >= 1 and intForm.weight2 >= 1):
          heuristics = intForm.heuristicFunctions
          n = len(heuristics)

          with IntegratedAStar(self.grid, n, intForm.weight1, intForm.weight2, heuristics) as intAStar:
            found = intAStar.search()
            if(found):
              self.grid.setPath(intAStar.getPath())
            else:
              messagebox.showinfo("Integrated AStar Results", "No path could be found to the goal.")

            self.time = intAStar.time
            self.write_info(self.clickedCell.X, self.clickedCell.Y)

        # Remove from memory
        del intForm


      # Convert x/y screen coordinates to grid coordinates
      column = pos[0] // (Constants.WIDTH + Constants.MARGIN) - 3
      row = pos[1] // (Constants.HEIGHT + Constants.MARGIN) - 3

      # Print out the cell information when clicked
      if(row > -1 and row < Constants.ROWS and column > -1 and column < Constants.COLUMNS):
        self.write_info(row, column)


  # /*\ =======================================================================
  # |*| SETUP UI ELEMENTS
  # |*|   - setup_dynamic() Sets up the elements that change due to
  # |*|     screen refresh
  # |*|   - setup_static() Sets up elements that don't get effected
  # \*/ =======================================================================

  # Setup the interface with buttons and text
  def setup_dynamic(self):
    self.screen.fill(Constants.WHITE)

    # Draw boxes (surface, color, rectangle[x, y, width, height], width)
    pygame.draw.rect(self.screen, Constants.BLACK, [18, 18, 965, 725], 1)               # Border around grid
    pygame.draw.rect(self.screen, Constants.DARK_BLUE, [1030, 28, 230, 200], 1)         # Information box
    pygame.draw.rect(self.screen, Constants.DARK_BLUE, [1030, 260, 230, 310], 1)        # Algoirthms box
    pygame.draw.rect(self.screen, Constants.WHITE, [1080, 10, 125, 100])                # White box (information)
    pygame.draw.rect(self.screen, Constants.WHITE, [1090, 230, 115, 100])               # White box (algorithms)
    pygame.draw.rect(self.screen, Constants.DARK_BLUE, [1055, 500, 180, 1], 1)          # Horizontal line

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
    self.write_info(self.grid.currentStart.X, self.grid.currentStart.Y)

    # Buttons (text, text_color, length, height, x_pos, y_pos, btn_color, hover_color)
    self.reloadButton = Button("Regenerate Map", 14, Constants.WHITE, 230, 45, 1030, 695, Constants.PINK, Constants.DARK_PINK)                  # Reload button
    self.saveButton = Button("Save Map", 7, Constants.WHITE, 110, 40, 1150, 650, Constants.LIGHT_BLUE, Constants.DARK_BLUE)                     # Save button
    self.loadButton = Button("Load Map", 7, Constants.WHITE, 110, 40, 1030, 650, Constants.LIGHT_BLUE, Constants.DARK_BLUE)                     # Load button
    self.astarButton = Button("AStar", 12, Constants.WHITE, 180, 35, 1055, 285, Constants.LIGHT_BLUE, Constants.DARK_BLUE)                      # AStar button
    self.weightedAStarButton = Button("Weighted A*", 12, Constants.WHITE, 180, 35, 1055, 325, Constants.LIGHT_BLUE, Constants.DARK_BLUE)        # Weighted A* button
    self.uniformCostButton = Button("Uniform Cost", 12, Constants.WHITE, 180, 35, 1055, 365, Constants.LIGHT_BLUE, Constants.DARK_BLUE)         # Uniform Cost button
    self.seqAStarButton = Button("Sequential A*", 12, Constants.WHITE, 180, 35, 1055, 405, Constants.LIGHT_BLUE, Constants.DARK_BLUE)           # Sequential A* button
    self.intAStarButton = Button("Integrated A*", 12, Constants.WHITE, 180, 35, 1055, 445, Constants.LIGHT_BLUE, Constants.DARK_BLUE)           # Integrated A* button
    self.startGoalButton = Button("Start-Goal Pair", 12, Constants.WHITE, 180, 35, 1055, 520, Constants.PINK, Constants.DARK_PINK)              # Start-Goal Pair button

    # Add buttons to list
    buttonAppend = self.buttons.append
    buttonAppend(self.reloadButton)
    buttonAppend(self.saveButton)
    buttonAppend(self.loadButton)
    buttonAppend(self.astarButton)
    buttonAppend(self.weightedAStarButton)
    buttonAppend(self.uniformCostButton)
    buttonAppend(self.seqAStarButton)
    buttonAppend(self.intAStarButton)
    buttonAppend(self.startGoalButton)


  # /*\ =======================================================================
  # |*| HELPER FUNCTIONS
  # |*|   - write_text() Displays text on the screen
  # |*|   - write_info() Writes inside the information box
  # |*|   - resetInformation() - Resets the text in info box
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
    self.clickedCell = self.grid.cells[row, col]

    # Draw text (surface, text, text_color, text_size, x, y)
    if(self.clickedCell is not None):
      self.write_text("".join(["(", str(self.clickedCell.X), ", ", str(self.clickedCell.Y), ")"]), Constants.BLACK, 16, 1130, 65)
      self.write_text("{:.6f}".format(self.clickedCell.F), Constants.BLACK, 16, 1130, 97)
      self.write_text("{:.6f}".format(self.clickedCell.G), Constants.BLACK, 16, 1130, 127)
      self.write_text("{:.2f}".format(self.clickedCell.H), Constants.BLACK, 16, 1130, 157)

    # Print the time it took to find path
    self.write_text("".join([str(self.time), " ms"]), Constants.BLACK, 16, 1130, 187)


# Check if this script is being run directly (if it is, then __name__ becomes __main__)
if __name__ == '__main__':
  gui = GUI()
  gui.run()
