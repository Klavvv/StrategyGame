import os
import pygame
import sys
from pygame.locals import *
# from pygame import gfxdraw
# import numpy as np
from province import *
from country import *
from readMaps import *
from uni_button import *
from game_screen_actions import *
from warThings import *
from datetime import datetime


SCREEN_RESOLUTION = (1920,1080)
COLOR_PRIMARY = (238,33,33)
COLOR_SECONDARY = (197,197,197)
# COLOR_SECONDARY = (197,172,75)
COLOR_BACKGROUND = (7,7,7)
COLOR_BACKGROUND_SECOND = (14,14,14)
DISPLACEMENT = 50

clock = pygame.time.Clock()

def game(screen, chosenMap, chosedFaction):
	print(chosedFaction)
	display = pygame.Surface( (screen.get_size()[0], screen.get_size()[1] - 2*DISPLACEMENT ) )

	GAME_DATA = readGameData(chosenMap[2])
	COUNTRIES = counJ2counT(GAME_DATA)
	PROVINCES = provJ2provT(GAME_DATA, COUNTRIES)
	CENTER_OF_MAP = GAME_DATA["center"]
	X_DISP = CENTER_OF_MAP[0]
	Y_DISP = CENTER_OF_MAP[1]
	GAME_CLOCK = GameClock( datetime.now() )
	GAME_ACTION_EVENT = pygame.USEREVENT+1
	GAME_ACTION_EVENT_INTERVAL = 2000
	GAME_CLOCK_SPEED = 1
	pygame.time.set_timer(GAME_ACTION_EVENT, int(GAME_ACTION_EVENT_INTERVAL * ( 1/GAME_CLOCK_SPEED)))
	TOP_BAR_AFTER_NAME_LOC = 0


	player_flag = None
	player_name = None
	for country in COUNTRIES:
		country.renderName(PROVINCES)
		country.setMoney(200)
		if country.id == chosedFaction:
			country.player = True
			player_name = country.name
			if country.flag != None:
				player_flag = country.flag

	prov_id = 0
	for province in PROVINCES:
		province.setRealPoints(CENTER_OF_MAP)
		province.setMiddlePoint()
		province.setId(prov_id)
		prov_id += 1
	
	for country in COUNTRIES:
		country.updateDailyMoney(PROVINCES)

	for province in PROVINCES:
		temp = []
		for other_province in PROVINCES:
			if other_province.province_id != province.province_id:
				counter = 0
				for point in other_province.points:
					if point in province.points:
						counter += 1
				if counter > 1:
					temp.append(other_province.province_id)
		province.neighbour = temp
	print( PROVINCES[0].name )
	print( PROVINCES[0].neighbour )

	top_rect = pygame.draw.rect(screen,COLOR_BACKGROUND, (0,0,screen.get_size()[0],DISPLACEMENT))
	bottom_rect = pygame.draw.rect(screen,COLOR_BACKGROUND, (0,screen.get_size()[1]-DISPLACEMENT,screen.get_size()[0],DISPLACEMENT))
	pygame.draw.rect(screen,COLOR_SECONDARY, (0,DISPLACEMENT-5,screen.get_size()[0],DISPLACEMENT))
	pygame.draw.rect(screen,COLOR_SECONDARY, (0,screen.get_size()[1] - DISPLACEMENT,screen.get_size()[0],5))
	static_image_clock = pygame.image.load("content/game/clock.png").convert_alpha()
	static_time_speed = SmartText2( str(float(GAME_CLOCK_SPEED)) + " X ", (50,45), 15, (1740, 0)  )

	screen.blit(static_image_clock, (1795,10))
	static_time_speed.draw(screen,(0,0))

	quit_button = ButtonB("← WYJDŹ", (120,40), 20, (10,screen.get_size()[1]-42))
	button_clock_speed_up = ButtonI((30,45), "content/menu/arrow_plus.png", "content/menu/arrow_plus_hover.png", (1705,0))
	button_clock_speed_pause = ButtonI((30,45), "content/menu/pause.png", "content/menu/pause_hover.png", (1675,0))
	button_clock_speed_down = ButtonI((30,45), "content/menu/arrow_minus.png", "content/menu/arrow_minus_hover.png", (1645,0))
	button_buy = ButtonI((45,45), "content/game/buy_normal.png", "content/game/buy_hover.png", (1870, 1035))
	button_army = ButtonI((45,45), "content/game/army_normal.png", "content/game/army_hover.png", (1825, 1035))

	if player_flag != None:
		screen.blit(player_flag, (7,7))
		player_name_text = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',15).render(player_name , True , COLOR_SECONDARY)
		screen.blit(player_name_text , (55, 22 - player_name_text.get_height()/2  ))
		TOP_BAR_AFTER_NAME_LOC = 55 + player_name_text.get_width()
		# screen.blit(pygame.image.load("content/menu/money.png").convert_alpha(), (TOP_BAR_AFTER_NAME_LOC+30,12))
		# TOP_BAR_AFTER_NAME_LOC += 50
	else:
		player_name_text = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',15).render(player_name , True , COLOR_SECONDARY)
		screen.blit(player_name_text , (7, 22 - player_name_text.get_height()/2  ))
		TOP_BAR_AFTER_NAME_LOC = player_name_text.get_width() + 7
		# screen.blit(pygame.image.load("content/menu/money.png").convert_alpha(), (TOP_BAR_AFTER_NAME_LOC+30,12))
		# TOP_BAR_AFTER_NAME_LOC += 50

	
	PLAYER_DATA = PlayerData(0, TOP_BAR_AFTER_NAME_LOC+10)


	dt = 0
	speed = 300

	isPause = True
	tempSpeed = 1

	FIRST_CHOSED = None
	SECOND_CHOSED = None
	TRANSPORT = []

	BUY_DEV_CLICK = False
	BUY_MODE = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',40).render("TRYB ULEPSZANIA PROWINCJI" , True , COLOR_PRIMARY)
	BUY_MODE_POINT = (960 - BUY_MODE.get_width()/2, 10 )
	BUY_DEV_COST = 100

	BUY_ARMY_CLICK = False
	ARMY_MODE = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',40).render("TRYB REKRUTACJI ARMII" , True , COLOR_PRIMARY)
	ARMY_MODE_POINT = (960 - ARMY_MODE.get_width()/2, 10 )
	BUY_ARMY_COST = 100

	STATS = []

	GAMEON = True
	while GAMEON:
		display.fill((44,44,50))
		realmouse = pygame.mouse.get_pos()
		mouse = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]-DISPLACEMENT) 

		button_clock_speed_up.draw(screen,realmouse)
		button_clock_speed_down.draw(screen,realmouse)
		button_clock_speed_pause.draw(screen,realmouse)
		button_buy.draw(screen,realmouse)
		button_army.draw(screen,realmouse)
		quit_button.draw(screen,realmouse)




		for province in PROVINCES:
			province.setRealPoints((X_DISP,Y_DISP))
			province.draw(display)
			province.drawDetails(display)
		#LAG
		for province in PROVINCES:
			province.drawBorder(display, mouse)
			province.drawData(display, (X_DISP, Y_DISP))
		#LAG
		for province in PROVINCES:
			if province.cursorIn(mouse):
				display.blit(province.big_province_name , (10, 10))
				display.blit(province.big_province_dev , (10, 30))
				display.blit(province.big_province_arm , (10, 45))
				break
		for country in COUNTRIES:
			country.drawName(display, mouse,(X_DISP, Y_DISP))

		for transport in TRANSPORT:
			transport.draw(display,(X_DISP, Y_DISP))

		# STATS
		st_index = 0
		for stats in STATS:
			display.blit(stats, (1920 - stats.get_width() - 5,10 + st_index*14))
			st_index += 1
		
		

		if BUY_DEV_CLICK:
			display.blit(BUY_MODE,BUY_MODE_POINT)
		elif BUY_ARMY_CLICK:
			display.blit(ARMY_MODE,ARMY_MODE_POINT)





		# if MOUSE_OVER_FACTION != None:


		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == GAME_ACTION_EVENT and isPause:
				# print("Game | "+str(clock.get_fps()))
				for country in COUNTRIES:
					country.updateMoney()
					if country.player:
						PLAYER_DATA.money = country.money
						PLAYER_DATA.dailyMoneyCurr = country.dailyMoney

				RET_DATA = screen_actions(screen, display, GAME_CLOCK, PROVINCES, COUNTRIES, PLAYER_DATA, TRANSPORT, chosedFaction)
				TRANSPORT = RET_DATA["transport"]
				PROVINCES = RET_DATA["provinces"]
				COUNTRIES = RET_DATA["countries"]
				STATS = RET_DATA["stats"]







			if event.type == pygame.MOUSEBUTTONDOWN:
				if quit_button.cursorIn(realmouse):
					GAMEON = False
				elif button_buy.cursorIn(realmouse):
					BUY_ARMY_CLICK = False
					button_army.forceHoverF(False)
					if BUY_DEV_CLICK:
						button_buy.forceHoverF(False)
						BUY_DEV_CLICK = False
					else:
						button_buy.forceHoverF(True)
						BUY_DEV_CLICK = True
				elif button_army.cursorIn(realmouse):
					BUY_DEV_CLICK = False
					button_buy.forceHoverF(False)
					if BUY_ARMY_CLICK:
						button_army.forceHoverF(False)
						BUY_ARMY_CLICK = False
					else:
						button_army.forceHoverF(True)
						BUY_ARMY_CLICK = True

				elif button_clock_speed_up.cursorIn(realmouse):
					if isPause:
						if GAME_CLOCK_SPEED < 3:
							GAME_CLOCK_SPEED += 0.5
							pygame.time.set_timer(GAME_ACTION_EVENT, int(GAME_ACTION_EVENT_INTERVAL * ( 1/GAME_CLOCK_SPEED)))
							static_time_speed = SmartText2( str(float(GAME_CLOCK_SPEED)) + " X ", (50,45), 15, (1740, 0)  )
							static_time_speed.draw(screen,(0,0))
							isPause = True
					else:
						GAME_CLOCK_SPEED = tempSpeed
						pygame.time.set_timer(GAME_ACTION_EVENT, int(GAME_ACTION_EVENT_INTERVAL * ( 1/GAME_CLOCK_SPEED)))
						static_time_speed = SmartText2( str(float(GAME_CLOCK_SPEED)) + " X ", (50,45), 15, (1740, 0)  )
						static_time_speed.draw(screen,(0,0))
						isPause = True
				elif button_clock_speed_down.cursorIn(realmouse):
					if isPause:
						if GAME_CLOCK_SPEED > 0.5:
							GAME_CLOCK_SPEED -= 0.5
							pygame.time.set_timer(GAME_ACTION_EVENT, int(GAME_ACTION_EVENT_INTERVAL * ( 1/GAME_CLOCK_SPEED)))
							static_time_speed = SmartText2( str(float(GAME_CLOCK_SPEED)) + " X ", (50,45), 15, (1740, 0)  )
							static_time_speed.draw(screen,(0,0))
							isPause = True
					else:
						GAME_CLOCK_SPEED = tempSpeed
						pygame.time.set_timer(GAME_ACTION_EVENT, int(GAME_ACTION_EVENT_INTERVAL * ( 1/GAME_CLOCK_SPEED)))
						static_time_speed = SmartText2( str(float(GAME_CLOCK_SPEED)) + " X ", (50,45), 15, (1740, 0)  )
						static_time_speed.draw(screen,(0,0))
						isPause = True
				elif button_clock_speed_pause.cursorIn(realmouse):
					tempSpeed = GAME_CLOCK_SPEED
					static_time_speed = SmartText2( str(float(0.0)) + " X ", (50,45), 15, (1740, 0)  )
					static_time_speed.draw(screen,(0,0))
					isPause = False
		
				# print(event.button)
				if event.button == 3 and not BUY_DEV_CLICK and not BUY_ARMY_CLICK:
					for province in PROVINCES:
						if province.cursorIn(mouse):
							if province.state == chosedFaction:
								FIRST_CHOSED = province
							# print(province.name)
				elif event.button == 1:
					if BUY_DEV_CLICK:
						for province in PROVINCES:
							if province.cursorIn(mouse):
								if province.state == chosedFaction and province.development <8:
									if PLAYER_DATA.money >= BUY_DEV_COST:
										for country in COUNTRIES:
											if country.player:
												country.money -= BUY_DEV_COST
												province.upgradeProvince()
												country.updateDailyMoney(PROVINCES)
												PLAYER_DATA.money -= BUY_DEV_COST
												PLAYER_DATA.moneyChange()
												PLAYER_DATA.moneyRender.draw(screen,(0,0))
					elif BUY_ARMY_CLICK:
						for province in PROVINCES:
							if province.cursorIn(mouse):
								if province.state == chosedFaction:
									if PLAYER_DATA.money >= BUY_ARMY_COST:
										for country in COUNTRIES:
											if country.player:
												country.money -= BUY_ARMY_COST
												province.buyArmy()
												# country.updateDailyMoney(PROVINCES)
												PLAYER_DATA.money -= BUY_ARMY_COST
												PLAYER_DATA.moneyChange()
												PLAYER_DATA.moneyRender.draw(screen,(0,0))
					else:
						for province in PROVINCES:
							if province.cursorIn(mouse):
								if FIRST_CHOSED != None and FIRST_CHOSED.province_id != province.province_id:
									SECOND_CHOSED = province
									counter = 0
									for point in SECOND_CHOSED.points:
										if point in FIRST_CHOSED.points:
											counter += 1
									if counter > 1:
										# for aaa in PROVINCES:
										# 	if aaa.province_id == FIRST_CHOSED.province_id:
										# 		# aaa.deleteArmy()
										# 		print("XD")
										TRANSPORT.append(  Transport(FIRST_CHOSED , SECOND_CHOSED, FIRST_CHOSED.state )   )
										FIRST_CHOSED.deleteArmy()
						FIRST_CHOSED = None
						SECOND_CHOSED = None





		keys = pygame.key.get_pressed()
		if keys[K_w]:
			Y_DISP += speed*dt
		elif keys[K_s]:
			Y_DISP -= speed*dt
		if keys[K_a]:
			X_DISP += speed*dt
		elif keys[K_d]:
			X_DISP -= speed*dt

		# print("Game | "+str(clock.get_fps()))
		screen.blit(display,(0,DISPLACEMENT))
		pygame.display.update()
		dt = clock.tick(120) / 1000


# map()