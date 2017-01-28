import pygame
from pygame.locals import *

class Control(object):
	def create_button(self, surface, color, x, y, length, height, width, text, text_color):
		surface = self.draw_button(surface, color, length, height, x, y, width)
		surface = self.write_text(surface, text, text_color, length, height, x, y)
		self.rect = pygame.Rect(x,y, length, height)
		return surface

	def write_text(self, surface, text, text_color, length, height, x, y):
		font_size = int(length//len(text))
		myFont = pygame.font.SysFont("Calibri", font_size)
		myFont.set_bold(True)
		myText = myFont.render(text, 1, text_color)
		surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
		return surface

	def draw_button(self, surface, color, length, height, x, y, width):
		s = pygame.Surface((length, height))
		s.fill(color)
		surface.blit(s, (x,y))
		pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)  
		return surface

	def pressed(self, mouse):
		if mouse[0] > self.rect.topleft[0]:
			if mouse[1] > self.rect.topleft[1]:
				if mouse[0] < self.rect.bottomright[0]:
					if mouse[1] < self.rect.bottomright[1]:
						return True

		return False
