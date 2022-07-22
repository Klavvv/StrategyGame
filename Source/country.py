import json
import os
import pygame
import random

SCREEN_RESOLUTION = (1920,1080)
COLOR_PRIMARY = (238,33,33)
COLOR_SECONDARY = (197,197,197)
# COLOR_SECONDARY = (197,172,75)
COLOR_BACKGROUND = (7,7,7)
COLOR_BACKGROUND_SECOND = (14,14,14)

class Country:
	def __init__(self, country_id, name, color1, color2, color3):
		self.player = False
		self.id = country_id
		self.name = name
		self.provinces = []

		self.money = 0
		self.dailyMoney = 0

		self.agression = random.randint(2,7)

		self.color1 = color1
		self.color2 = color2
		self.color3 = color3

		self.center = None
		self.nameRender = None
		self.nameRenderHover = None
		self.nameRenderPos = None

		self.flag = None
		self.flagPos = None

		self.stillExist = True

	def drawCreator(self, screen, state_now):
		state_text2 = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',20, bold=True, italic=True).render( self.name + " ("+str(state_now)+")", True , COLOR_BACKGROUND)
		pos = screen.get_size()[0]/2 - (state_text2.get_width())/2
		pygame.draw.rect(screen,COLOR_SECONDARY, (700, 5, 500, 35 ))
		screen.blit(state_text2,(pos,8))

	def renderName(self, provinces):
		avg_x = 0
		avg_y = 0
		num = 0
		min_x = 1000000000
		max_x = -1000000000
		for province in provinces:
			if province.state == self.id:
				for x in province.points:
					if x[0] < min_x:
						min_x = x[0]
					if x[0] > max_x:
						max_x = x[0]
					avg_x += x[0]
					avg_y += x[1]
					num += 1
		if num!= 0:
			avg_x = (avg_x//num)
			avg_y = (avg_y//num)
			self.center = (avg_x, avg_y)
		else:
			self.stillExist = False


		name_size = max_x - min_x
		initial_text_size = 70
		color = (255,255,255)
		if (self.color1[0] + self.color1[1] + self.color1[2])/3 > 128:
			color = (0,0,0)
		self.nameRender = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',initial_text_size).render(self.name , True , color)
		while self.nameRender.get_width() > name_size - 50 and initial_text_size > 9:
			initial_text_size -= 1
			self.nameRender = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',initial_text_size).render(self.name , True , color)
		self.nameRender.set_alpha(220)
		self.nameRenderPos = ( self.center[0] - self.nameRender.get_width()/2 , self.center[1] - self.nameRender.get_height()/2   )
		try:
			self.flag = pygame.image.load("content/countries/"+str(self.name)+".png").convert_alpha()
			self.flagPos = ( self.center[0] - self.flag.get_width()/2 , self.center[1] - self.nameRender.get_height()/2 - self.flag.get_height()  )
		except:
			pass
		print(" ")

	def drawName(self,screen, mouse ,displacement):
		if self.stillExist:
			point = ( self.nameRenderPos[0]+displacement[0], self.nameRenderPos[1]+displacement[1]  )
			screen.blit(self.nameRender,point)
			if self.flag != None:
				point2 = ( self.flagPos[0]+displacement[0], self.flagPos[1]+displacement[1] )
				screen.blit(self.flag, point2)

	def setMoney(self,money):
		self.money = money
	
	def addMoney(self,money):
		self.money += money

	def substractMoney(self,money):
		self.money -= money
	
	def getMoney(self):
		return self.money
	
	def updateMoney(self):
		self.money += self.dailyMoney
	
	def updateDailyMoney(self, provinces):
		daily = 0
		for province in provinces:
			if province.state == self.id:
				daily += 0.1 + 0.2 * province.development
		self.dailyMoney = daily

		




def readCountries():
	countries = []
	listdir = os.listdir('content\\countries')
	# print(listdir)
	for x in range(len(listdir)):
		# try:
		if listdir[x][-4:] == "json":
			with open('content\\countries\\'+listdir[x] , 'r') as openfile:
				json_obj = json.load(openfile)
			temp = Country(json_obj["country_id"] ,json_obj["name"], json_obj["color1"], json_obj["color2"], json_obj["color3"])
			countries.append(temp)
		# except:
		# 	pass
	# print(countries)
	return countries

def readProvinceNames():
	file = open("content/game/polish_wies_database.txt", "r")
	file = file.read().split("\n")
	return file
	
