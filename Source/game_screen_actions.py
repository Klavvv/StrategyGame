import datetime
import pygame
from uni_button import *
from ejaj import *

SCREEN_RESOLUTION = (1920,1080)
COLOR_PRIMARY = (238,33,33)
COLOR_SECONDARY = (197,197,197)
# COLOR_SECONDARY = (197,172,75)
COLOR_BACKGROUND = (7,7,7)
COLOR_BACKGROUND_SECOND = (14,14,14)

class GameClock:
	def __init__(self, date):
		self.currentTime  =  date
		self.timeRender = None
		self.position = (1820, 0)
	
	def tickClock(self):
		self.currentTime += datetime.timedelta(days=1)
		self.timeRender = SmartText2( self.currentTime.strftime("%m-%d-%Y"), (100,45), 15, self.position  )
		
class PlayerData:
	def __init__(self, money, TOP_BAR_AFTER_NAME_LOC):
		self.money = money
		self.dailyMoneyCurr = 0
		self.dailyMoneyOld = 0

		self.moneyRender = None
		self.dailyMoneyRender = None

		self.position = (TOP_BAR_AFTER_NAME_LOC, 0)
	
	def moneyChange(self):
		self.moneyRender = SmartText2Left( "piniondze:"+str(round(self.money,2)).rjust(11,' ')+" zł    +"+str(round(self.dailyMoneyCurr,2))+" zł/doba" , (370,45), 15, self.position  )

	# def dailyMoneyChange(self):
	# 	if self.dailyMoneyCurr != self.dailyMoneyOld:
	# 		self.dailyMoneyOld = self.dailyMoneyCurr
	# 		self.dailyMoneyRender =  SmartText2Left( str(self.dailyMoneyCurr).rjust(8,'-')+" zł" , (100,45), 15, (self.position[0]+140, self.position[1])  )

def sort_by_second(table):
	table.sort(key = lambda x: x[1])
	return table

	
def screen_actions(screen, display, GAME_CLOCK, PROVINCES, COUNTRIES, PLAYER_DATA, TRANSPORT, chosedFaction):
	GAME_CLOCK.tickClock()
	GAME_CLOCK.timeRender.draw(screen,(0,0))

	PLAYER_DATA.moneyChange()
	PLAYER_DATA.moneyRender.draw(screen,(0,0))





	# print(TRANSPORT)
	NEW_TRANSPORT = []
	for transport in TRANSPORT:
		# print(transport.time)
		for province in PROVINCES:
			if transport.province1_id == province.province_id:
				if transport.state1 != province.state:
					transport.state1 = province.state
			if transport.province2_id == province.province_id:
				if transport.state2 != province.state:
					transport.state2 = province.state
				# if transport.state2 != province.state:
				# 	transport.state2 = province.state

		transport.time -= 1
		if transport.time >= 0:
			transport.visual_1 = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',13).render(">"*(6-transport.time), True , COLOR_PRIMARY)
			NEW_TRANSPORT.append(transport)
		else:
			for x in PROVINCES:
				if x.province_id == transport.province2_id:
					if (transport.state1 == transport.state2 or x.state == transport.state1) and x.state == transport.inicjator :
						x.army += transport.army
						x.updateArmy()
					else:
						x.army -= transport.army
						if x.army < 0:
							for country in COUNTRIES:
								if country.id == transport.state1:
									x.army = abs(x.army)
									x.setOwner(country)
						x.updateArmy()
			for country in COUNTRIES:
				if country.id == transport.state1 or country.id == transport.state2:
					country.renderName(PROVINCES)
				country.updateDailyMoney(PROVINCES)
	

	STATS = []
	CO_STAT = []
	for country in COUNTRIES:
		CO_STAT.append( [country.name, round(country.dailyMoney,3), country.agression] )
	CO_STAT = sort_by_second(CO_STAT)
	for country in CO_STAT:
		STATS.append( pygame.font.Font('content/menu/consola.ttf',12).render( country[0] +"  "+str( country[1] )+"  "+str( country[2] ), True , COLOR_SECONDARY) )
	STATS.append( pygame.font.Font('content/menu/consola.ttf',12).render( "FRAKCJA  PKB  A", True , COLOR_PRIMARY) )
	STATS = STATS[::-1]


	AI_DATA = ai_actions2(chosedFaction, COUNTRIES, PROVINCES, NEW_TRANSPORT)
	NEW_TRANSPORT = AI_DATA["transport"]
	PROVINCES = AI_DATA["provinces"]
	COUNTRIES = AI_DATA["countries"]



	
	return {"transport":NEW_TRANSPORT, "provinces":PROVINCES, "countries":COUNTRIES, "stats":STATS }


	# PLAYER_DATA.dailyMoneyChange()
	# PLAYER_DATA.dailyMoneyRender.draw(screen,(0,0))