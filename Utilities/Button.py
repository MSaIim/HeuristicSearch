import pygame

class Button(object):
  def __init__(self, text, text_size, text_color, length, height, x_pos, y_pos, btn_color, hover_color):
    # Setup the button
    self.btnSurface = pygame.Surface((length, height))
    self.rect = pygame.Rect(x_pos, y_pos, length, height)

    # Setup font
    btnfont = pygame.font.SysFont("Calibri", int(length//text_size), True)
    self.text = btnfont.render(text, 1, text_color)
    self.x_offset = (x_pos+length/2) - self.text.get_width()/2
    self.y_offset = (y_pos+height/2) - self.text.get_height()/2

    # Save member vars
    self.length = length
    self.height = height
    self.x_pos = x_pos
    self.y_pos = y_pos
    self.btn_color = btn_color
    self.hover_color = hover_color
    

  # Draw the button on the given surface
  def draw(self, surface, mouse):
    # Check if mouse is hovering button
    if(self.rect.collidepoint(mouse)):
      self.btnSurface.fill(self.hover_color)
    else:
      self.btnSurface.fill(self.btn_color)

    # Draw button and outline
    surface.blit(self.btnSurface, (self.x_pos, self.y_pos))
    pygame.draw.rect(surface, (190,190,190), (self.x_pos, self.y_pos, self.length, self.height), 1)

    # Draw text
    surface.blit(self.text, (self.x_offset, self.y_offset))


  # Detect when the mouse is pressed on this button
  def pressed(self, mouse):
    if mouse[0] > self.rect.topleft[0]:
      if mouse[1] > self.rect.topleft[1]:
        if mouse[0] < self.rect.bottomright[0]:
          if mouse[1] < self.rect.bottomright[1]:
            return True

    return False
