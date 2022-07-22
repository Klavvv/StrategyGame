import pygame
import matplotlib.path as mplPath
import random

SCREEN_RESOLUTION = (1920,1080)
COLOR_PRIMARY = (238,33,33)
COLOR_SECONDARY = (197,197,197)
# COLOR_SECONDARY = (197,172,75)
COLOR_BACKGROUND = (7,7,7)
COLOR_BACKGROUND_SECOND = (14,14,14)
DISPLACEMENT = 50

def returnDevelopmentImage(num):
	if num > 0 and num <=8:
		return pygame.image.load("content/menu/m"+str(num)+".png").convert_alpha()
	else:
		return pygame.font.Font('content/menu/LEMONMILK-Regular.otf',11).render(" ", True , COLOR_SECONDARY)

class Province:
	def __init__(self, name, points):
		self.points = points
		self.realPoints = None
		self.state = None
		self.name = name
		self.province_id = None

		self.neighbourhood = None

		self.min_flags = None

		self.defence = 0
		self.development = 0 #random.randint(0,8)
		self.population = 1.0
		self.army = 100

		self.color_main = (255,255,255)
		self.color_border = (255,255,255)
		self.color_text = (255,255,255)

		self.province_name = None
		self.province_def = None
		self.province_dev = None
		self.province_pop = None
		self.province_arm = None

		self.prov_dev_disp = None
		self.prov_arm_disp = None

		# self.big_province_name = None
		# self.big_province_arm = None
		# self.big_province_dev = None
		self.big_province_name = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',14).render(str(self.name), True , COLOR_PRIMARY)
		self.big_province_dev = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',11).render("Rozwój: "+str(self.development)+"/8", True , COLOR_PRIMARY)
		self.big_province_arm = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',11).render("Armia:  "+str(self.army), True , COLOR_PRIMARY)

		self.averagePoint = None

		
	def draw(self,screen):
		pygame.gfxdraw.filled_polygon(screen,self.realPoints,self.color_main)

	def cursorIn(self, mouse):
		if self.min_flags[0] < mouse[0] < self.min_flags[2] and self.min_flags[1] < mouse[1] < self.min_flags[3]:
			poli_path = mplPath.Path(self.realPoints)
			if poli_path.contains_point(mouse):
				return True

	def deleteArmy(self):
		self.army = 0
		font2 = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',7)
		self.province_arm = font2.render("armia:  "+str(self.army), True , self.color_border)
		self.big_province_arm = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',11).render("Armia:  "+str(self.army), True , COLOR_PRIMARY)
		self.prov_arm_disp = self.province_name.get_width()/2 - self.province_arm.get_width()/2

	def updateArmy(self):
		font2 = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',7)
		self.province_arm = font2.render("armia:  "+str(self.army), True , self.color_border)
		self.big_province_arm = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',11).render("Armia:  "+str(self.army), True , COLOR_PRIMARY)
		self.prov_arm_disp = self.province_name.get_width()/2 - self.province_arm.get_width()/2

	def upgradeProvince(self):
		self.development+=1
		self.big_province_dev = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',11).render("Rozwój: "+str(self.development)+"/8", True , COLOR_PRIMARY)
		self.province_dev = returnDevelopmentImage(self.development)
		self.prov_dev_disp = self.province_name.get_width()/2 - self.province_dev.get_width()/2

	def buyArmy(self):
		self.army += 50
		self.big_province_arm = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',11).render("Armia:  "+str(self.army), True , COLOR_PRIMARY)
		self.province_arm = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',7).render("armia:  "+str(self.army), True , self.color_border)
		self.prov_arm_disp = self.province_name.get_width()/2 - self.province_arm.get_width()/2

	def setId(self,province_id):
		self.province_id = province_id

	def drawDetails(self,screen):
		pygame.gfxdraw.polygon(screen,self.realPoints,  self.color_border )

	def drawBorder(self,screen, mouse):
		if self.min_flags[0] < mouse[0] < self.min_flags[2] and self.min_flags[1] < mouse[1] < self.min_flags[3]:
			poli_path = mplPath.Path(self.realPoints)
			if poli_path.contains_point(mouse):
				pygame.draw.polygon(screen,  self.color_border,self.realPoints, width=5)


	def drawData(self,screen, displacement):
		x_avg = self.averagePoint[0] + displacement[0] - self.province_name.get_rect()[2]/2
		y_avg = self.averagePoint[1] + displacement[1] - self.province_name.get_rect()[3]/2
		screen.blit(self.province_name , (x_avg, y_avg-15))
		screen.blit(self.province_dev , (x_avg + self.prov_dev_disp , y_avg-2))
		screen.blit(self.province_arm , (x_avg + self.prov_arm_disp, y_avg+10))


	def setOwner(self, country):
		self.state = country.id
		self.color_main = country.color1
		self.color_border = country.color2
		self.color_text = country.color3
		font = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',8)
		font2 = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',7)
		self.province_name = font.render(self.name, True , self.color_text)
		self.province_def = font2.render("o: "+str(self.defence), True , self.color_border)

		self.province_dev = returnDevelopmentImage(self.development)
		self.province_arm = font2.render("armia:  "+str(self.army), True , self.color_border)

		self.prov_dev_disp = self.province_name.get_width()/2 - self.province_dev.get_width()/2
		self.prov_arm_disp = self.province_name.get_width()/2 - self.province_arm.get_width()/2
		# self.province_name.set_alpha(170)
		# self.province_name.convert_alpha()
		# self.province_def.convert_alpha()
		# self.province_dev.convert_alpha()
		# self.province_arm.convert_alpha()


	def setOwnerCreator(self, STATES, state):
		self.state = STATES[state].name
		self.color_main = STATES[state].color1
		self.color_border = STATES[state].color2
		self.color_text = STATES[state].color3
		font = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',11)
		font2 = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',10)
		self.province_name = font.render(self.name, True , self.color_text)
		self.province_def = font2.render("o: "+str(self.defence), True , self.color_border)
		self.province_dev = font2.render("r: "+str(self.development), True , self.color_border)
		self.province_pop = font2.render("p:  "+str(self.population) + "M", True , self.color_border)

	def setMiddlePoint(self):
		x_avg = 0
		y_avg = 0
		for x in self.points:
			x_avg += x[0]
			y_avg += x[1]
		x_avg //= len(self.points)
		y_avg //= len(self.points)
		self.averagePoint = (x_avg, y_avg)
	
	def setRealPoints(self, displacement):
		min_flags = [100000000, 100000000, -100000000, -100000000]
		real_points = []
		for point in self.points:
			a = point[0] + displacement[0]
			b = point[1] + displacement[1]
			real_points.append( (a, b) )

			if a <= min_flags[0]:
				min_flags[0] = a
			if a > min_flags[2]:
				min_flags[2] = a

			if b <= min_flags[1]:
				min_flags[1] = b
			if b > min_flags[3]:
				min_flags[3] = b

		self.realPoints = real_points
		self.min_flags = min_flags
    	
