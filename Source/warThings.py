import pygame

SCREEN_RESOLUTION = (1920,1080)
COLOR_PRIMARY = (238,33,33)
COLOR_SECONDARY = (197,197,197)
# COLOR_SECONDARY = (197,172,75)
COLOR_BACKGROUND = (7,7,7)
COLOR_BACKGROUND_SECOND = (14,14,14)

class Transport:
	def __init__(self, province1, province2,inicjator):
		self.province1_id = province1.province_id
		self.province2_id = province2.province_id
		self.state1 = province1.state
		self.state2 = province2.state
		self.inicjator = inicjator

		self.color = province1.color_main
		self.army = province1.army
		self.loc1 = province1.averagePoint
		self.loc2 = province2.averagePoint
		self.avgPoint = ( (province1.averagePoint[0]+province2.averagePoint[0])/2, (province1.averagePoint[1]+province2.averagePoint[1])/2   )
		self.size = (50,30)
		self.time = 6
		self.visual_1 = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',13).render(" ", True , COLOR_PRIMARY)
		self.visual_2 = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',13).render(str(province1.army), True , COLOR_PRIMARY)
	
	def draw(self, screen, disp):
		point = (self.avgPoint[0]-self.size[0]/2+disp[0], self.avgPoint[1]-self.size[1]/2+disp[1], self.size[0], self.size[1] )
		pygame.draw.rect(screen,self.color, point)
		pygame.draw.rect(screen,COLOR_PRIMARY, point,width=2)
		# visual_1 = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',13).render(">"*(6-self.time), True , COLOR_PRIMARY)
		
		screen.blit(self.visual_1,point)
		screen.blit(self.visual_2,(point[0]+5, point[1]+10))