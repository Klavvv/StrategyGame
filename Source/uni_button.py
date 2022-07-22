import pygame

SCREEN_RESOLUTION = (1920,1080)
COLOR_PRIMARY = (238,33,33)
COLOR_SECONDARY = (197,197,197)
# COLOR_SECONDARY = (197,172,75)
COLOR_BACKGROUND = (7,7,7)

class ButtonA:
	def __init__(self, text, size, fontsize, displacement):
		self.button = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',fontsize).render(text , True , COLOR_SECONDARY)
		self.buttonHover = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',fontsize+3).render(text, True , COLOR_PRIMARY)
		self.size = size
		self.textLocation = (1920/2 - self.button.get_rect()[2]/2, 1080/2 - self.button.get_rect()[3]/2 + displacement)
		self.hoverTextLocation = (1920/2 - self.buttonHover.get_rect()[2]/2, 1080/2 - self.buttonHover.get_rect()[3]/2 + displacement)
		self.rectShape = (1920/2 - self.size[0]/2, 1080/2 - self.size[1]/2 + displacement, self.size[0], self.size[1])

	def draw(self, screen, mouse):
		rect = pygame.draw.rect(screen,COLOR_BACKGROUND, self.rectShape)
		if rect.collidepoint(mouse):
			screen.blit(self.buttonHover , self.hoverTextLocation)
		else:
			screen.blit(self.button , self.textLocation)

	def cursorIn(self, mouse):
		if mouse[0] > self.rectShape[0] and mouse[0] < self.rectShape[0] + self.rectShape[2] and mouse[1] > self.rectShape[1] and mouse[1] < self.rectShape[1] + self.rectShape[3]:
			return True


class ButtonB:
	def __init__(self, text, size, fontsize, location):
		self.button = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',fontsize).render(text , True , COLOR_SECONDARY)
		self.buttonHover = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',fontsize+2).render(text, True , COLOR_PRIMARY)
		self.size = size
		self.textLocation = ( location[0]+size[0]/2 - self.button.get_rect()[2]/2, location[1]+size[1]/2 - self.button.get_rect()[3]/2 )
		self.hoverTextLocation = ( location[0]+size[0]/2 - self.buttonHover.get_rect()[2]/2, location[1]+size[1]/2 - self.buttonHover.get_rect()[3]/2 )
		self.rectShape = (location[0], location[1],size[0], size[1])
		self.secret_number = None
		self.forceHover = False

	def draw(self, screen, mouse):
		rect = pygame.draw.rect(screen,COLOR_BACKGROUND, self.rectShape)
		if rect.collidepoint(mouse) or self.forceHover:
			screen.blit(self.buttonHover , self.hoverTextLocation)
		else:
			screen.blit(self.button , self.textLocation)

	def cursorIn(self, mouse):
		if mouse[0] > self.rectShape[0] and mouse[0] < self.rectShape[0] + self.rectShape[2] and mouse[1] > self.rectShape[1] and mouse[1] < self.rectShape[1] + self.rectShape[3]:
			return True
	
	def moveUpDown(self, disp):
		self.textLocation = ( self.textLocation[0], self.textLocation[1]+disp )
		self.hoverTextLocation = ( self.hoverTextLocation[0], self.hoverTextLocation[1]+disp )
		self.rectShape = (self.rectShape[0] , self.rectShape[1] + disp, self.rectShape[2], self.rectShape[3])

	def setSecretNumber(self, number):
		self.secret_number = number

	def forceHoverF(self, bo):
		self.forceHover = bo

class ButtonI:
	def __init__(self, size, nImage, hImage, location):
		self.button = pygame.image.load(nImage)#.convert()
		self.buttonHover = pygame.image.load(hImage)#.convert()
		self.size = size
		self.imgLocation = ( location[0]+size[0]/2 - self.button.get_rect()[2]/2, location[1]+size[1]/2 - self.button.get_rect()[3]/2 )
		self.hoverImgLocation = ( location[0]+size[0]/2 - self.buttonHover.get_rect()[2]/2, location[1]+size[1]/2 - self.buttonHover.get_rect()[3]/2 )
		self.rectShape = (location[0], location[1],size[0], size[1])
		self.forceHover = False

	def draw(self, screen, mouse):
		rect = pygame.draw.rect(screen,COLOR_BACKGROUND, self.rectShape)
		if rect.collidepoint(mouse) or self.forceHover:
			screen.blit(self.buttonHover , self.hoverImgLocation)
		else:
			screen.blit(self.button , self.imgLocation)
	
	def forceHoverF(self, bo):
		self.forceHover = bo

	def cursorIn(self, mouse):
		if mouse[0] > self.rectShape[0] and mouse[0] < self.rectShape[0] + self.rectShape[2] and mouse[1] > self.rectShape[1] and mouse[1] < self.rectShape[1] + self.rectShape[3]:
			return True

class SmartText:
	def __init__(self, text, size, fontsize, location):
		self.button = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',fontsize).render(text , True , (COLOR_SECONDARY))
		self.size = size
		self.textLocation = ( location[0]+size[0]/2 - self.button.get_rect()[2]/2, location[1]+size[1]/2 - self.button.get_rect()[3]/2 )
		self.rectShape = (location[0], location[1],size[0], size[1])
		self.fontsize = fontsize
		self.text = text

	def draw(self, screen, mouse):
		pygame.draw.rect(screen,(COLOR_BACKGROUND), self.rectShape)
		# rect = pygame.draw.rect(screen,(255,0,0), self.rectShape)
		screen.blit(self.button , self.textLocation)
		
class SmartText2:
	def __init__(self, text, size, fontsize, location):
		self.button = pygame.font.Font('content/menu/consolab.ttf',fontsize).render(text , True , COLOR_SECONDARY)
		self.size = size
		self.textLocation = ( location[0]+size[0]/2 - self.button.get_rect()[2]/2, location[1]+size[1]/2 - self.button.get_rect()[3]/2 )
		self.rectShape = (location[0], location[1],size[0], size[1])
		self.fontsize = fontsize
		self.text = text

	def draw(self, screen, mouse):
		pygame.draw.rect(screen,COLOR_BACKGROUND, self.rectShape)
		# rect = pygame.draw.rect(screen,(255,0,0), self.rectShape)
		screen.blit(self.button , self.textLocation)

class SmartText2Left:
	def __init__(self, text, size, fontsize, location):
		self.button = pygame.font.Font('content/menu/consolab.ttf',fontsize).render(text , True , COLOR_SECONDARY)
		self.size = size
		self.textLocation = (location[0]+ size[0] - self.button.get_width(), location[1]+size[1]/2 - self.button.get_rect()[3]/2 )
		self.rectShape = (location[0], location[1],size[0], size[1])
		self.fontsize = fontsize
		self.text = text

	def draw(self, screen, mouse):
		pygame.draw.rect(screen,COLOR_BACKGROUND, self.rectShape)
		# rect = pygame.draw.rect(screen,(255,0,0), self.rectShape)
		screen.blit(self.button , self.textLocation)