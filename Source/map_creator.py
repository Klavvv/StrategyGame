import os
import pygame
import sys
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
from province import *
from country import *
import math
from uni_button import *
from saveNewMap import *
import random

SCREEN_RESOLUTION = (1920,1080)
COLOR_PRIMARY = (238,33,33)
COLOR_SECONDARY = (197,197,197)
# COLOR_SECONDARY = (197,172,75)
COLOR_BACKGROUND = (7,7,7)
COLOR_BACKGROUND_SECOND = (14,14,14)
ZOOM = 1
DISPLACEMENT = 50

clock = pygame.time.Clock()
# pygame.init()
# pygame.display.set_caption("MAP")
# display = pygame.display.set_mode(SCREEN_RESOLUTION,0,32)
# pygame.mouse.set_cursor(*pygame.cursors.arrow)

def map(screen):
	ON = True
	display = pygame.Surface( (screen.get_size()[0], screen.get_size()[1] - 2*DISPLACEMENT ) )
	CIRCLE_RADIUS = 10
	SAVE_TIMER_XD = 0
	STATES_LIST = readCountries()
	STATE_NOW = 0

	PROVINCE_NAMES = readProvinceNames()
	PROVINCE_NAMES_LEN = len(PROVINCE_NAMES)

	img_list = os.listdir('content\\creator_backgrounds')
	N_IMAGES = len(img_list)
	N_NOW = 0

	temp = []
	T = []
	points = []

	quit_button = ButtonB("← WYJDŹ", (120,40), 20, (10,screen.get_size()[1]-DISPLACEMENT+8))
	saveButton = ButtonI((40,40), "content/menu/creator_save.png", "content/menu/creator_save_h.png", (screen.get_size()[0]-50,2))
	undoButton = ButtonI((40,40), "content/menu/creator_undo.png", "content/menu/creator_undo_h.png", (screen.get_size()[0]-100,2))
	rBgButton = ButtonI((30,40), "content/menu/arrow_right_normal.png", "content/menu/arrow_right_hover.png", (screen.get_size()[0]-50,screen.get_size()[1]-DISPLACEMENT+8))
	lBgButton = ButtonI((30,40), "content/menu/arrow_left_normal.png", "content/menu/arrow_left_hover.png", (screen.get_size()[0]-111,screen.get_size()[1]-DISPLACEMENT+8))
	sizePlusButton = ButtonI((30,40), "content/menu/arrow_plus.png", "content/menu/arrow_plus_hover.png", (screen.get_size()[0]-151,screen.get_size()[1]-DISPLACEMENT+8))
	sizeMinusButton = ButtonI((30,40), "content/menu/arrow_minus.png", "content/menu/arrow_minus_hover.png", (screen.get_size()[0]-212,screen.get_size()[1]-DISPLACEMENT+8))
	circleRadiusUp = ButtonI((30,40), "content/menu/arrow_plus.png", "content/menu/arrow_plus_hover.png", (screen.get_size()[0]-252,screen.get_size()[1]-DISPLACEMENT+8))
	circleRadiusDown = ButtonI((30,40), "content/menu/arrow_minus.png", "content/menu/arrow_minus_hover.png", (screen.get_size()[0]-313,screen.get_size()[1]-DISPLACEMENT+8))
	factionLeft = ButtonI((34,35), "content/menu/arrow_faction_left.png", "content/menu/arrow_faction_left_h.png", (666, 5))
	factionRight = ButtonI((34,35), "content/menu/arrow_faction_rightl.png", "content/menu/arrow_faction_right_h.png", (1200 ,5))


	top_rect = pygame.draw.rect(screen,COLOR_BACKGROUND, (0,0,screen.get_size()[0],DISPLACEMENT))
	bottom_rect = pygame.draw.rect(screen,COLOR_BACKGROUND, (0,screen.get_size()[1]-DISPLACEMENT,screen.get_size()[0],DISPLACEMENT))
	pygame.draw.rect(screen,COLOR_SECONDARY, (0,DISPLACEMENT-5,screen.get_size()[0],DISPLACEMENT))
	pygame.draw.rect(screen,COLOR_SECONDARY, (0,screen.get_size()[1] - DISPLACEMENT,screen.get_size()[0],5))
	main_text = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',30).render("KREATOR MAP" , True , COLOR_PRIMARY)
	bg_text = pygame.image.load("content/menu/chBgImg.png").convert()
	size_text = pygame.image.load("content/menu/chSizeBtn.png").convert()
	circle_text = pygame.image.load("content/menu/chCircleImg.png").convert()
	creator_icon = pygame.image.load("content/menu/creator_icon.png").convert()
	creator_tutorial = pygame.image.load("content/menu/creator_tutorial.png").convert()
	save_display = pygame.image.load("content/menu/save_display.png").convert()
	

	# screen.blit(state_text1,(550,3))
	# screen.blit(state_text2,(700,8))
	STATES_LIST[STATE_NOW].drawCreator(screen, STATE_NOW)
	screen.blit(creator_icon,(10,8))
	screen.blit(creator_tutorial,(screen.get_size()[0]/2 - creator_tutorial.get_width()/2 ,screen.get_size()[1] - DISPLACEMENT + 8))
	screen.blit(main_text,(50,0))
	screen.blit(bg_text,(screen.get_size()[0]-80,screen.get_size()[1]-DISPLACEMENT+15))
	screen.blit(size_text,(screen.get_size()[0]-181,screen.get_size()[1]-DISPLACEMENT+15))
	screen.blit(circle_text,(screen.get_size()[0]-282,screen.get_size()[1]-DISPLACEMENT+15))

	creator_background = pygame.image.load("content/creator_backgrounds/"+str(img_list[N_NOW])).convert()
	X_DISP = screen.get_size()[0]/2 - creator_background.get_width()/2
	Y_DISP = screen.get_size()[1]/2 - creator_background.get_height()/2
	XY_DISP_SPEED = 100

	dt = 0
	speed = 300

	while ON:
		display.fill(COLOR_BACKGROUND_SECOND)
		display.blit(creator_background,(0+X_DISP,0+Y_DISP))
		realmouse = pygame.mouse.get_pos()
		mouse = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]-DISPLACEMENT) 
		pygame.draw.circle(display, (255,0,0) , mouse ,CIRCLE_RADIUS, width=1)

		quit_button.draw(screen,realmouse)
		rBgButton.draw(screen,realmouse)
		lBgButton.draw(screen,realmouse)
		saveButton.draw(screen,realmouse)
		undoButton.draw(screen,realmouse)
		sizePlusButton.draw(screen,realmouse)
		sizeMinusButton.draw(screen,realmouse)
		circleRadiusUp.draw(screen,realmouse)
		circleRadiusDown.draw(screen,realmouse)
		factionLeft.draw(screen,realmouse)
		factionRight.draw(screen,realmouse)


		# R Y S O W A N I E   I S T N I E J Ą C Y C H   R Z E C Z Y
		for poly in T:
			ppp = []
			# st_num = poly[1]
			st_col = poly[2]
			for elem in poly[0]:
				temp1 = elem[0] + X_DISP
				temp2 = elem[1] + Y_DISP
				ppp.append((temp1,temp2))
			pygame.gfxdraw.filled_polygon(display,ppp,st_col)
			pygame.gfxdraw.polygon(display,ppp,  (255,0,0) )
			# pygame.draw.polygon(display, st_col ,ppp)
			# pygame.draw.polygon(display, (255,0,0) ,ppp, width=2)
			# display.blit(poly[5] , (poly[4][0]+X_DISP - poly[5].get_width()/2, poly[4][1]+Y_DISP- poly[5].get_height()/2) )

		for point in points:
			pygame.draw.circle(display, (255,0,0) , (point[0]+1+X_DISP, point[1]+Y_DISP) ,5)

		for poly in T:		
			display.blit(poly[5] , (poly[4][0]+X_DISP - poly[5].get_width()/2, poly[4][1]+Y_DISP- poly[5].get_height()/2) )

		pygame.draw.circle(display, (255,0,0) , mouse ,CIRCLE_RADIUS, width=1)


		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if not top_rect.collidepoint(pygame.mouse.get_pos()) and not bottom_rect.collidepoint(pygame.mouse.get_pos()):
					k = True
					for p in points:
						if math.sqrt((mouse[0]-p[0]-X_DISP)*(mouse[0]-p[0]-X_DISP)+(mouse[1]-p[1]-Y_DISP)*(mouse[1]-p[1]-Y_DISP)) <=  CIRCLE_RADIUS:
							temp.append(p)
							points.append(p)
							k = False
							break
					if k:
						temp.append((mouse[0]-X_DISP,mouse[1]-Y_DISP))
						points.append((mouse[0]-X_DISP,mouse[1]-Y_DISP))
					# print(temp)
				if quit_button.cursorIn(realmouse):
					ON = False
				if saveButton.cursorIn(realmouse):
					saveMap(T,STATES_LIST,(X_DISP,Y_DISP))
					SAVE_TIMER_XD = 180
				if rBgButton.cursorIn(realmouse):
					if N_NOW+2 > len(img_list):
						N_NOW = 0
					else:
						N_NOW += 1
					creator_background = pygame.image.load("content/creator_backgrounds/"+str(img_list[N_NOW])).convert()
					X_DISP = screen.get_size()[0]/2 - creator_background.get_width()/2
					Y_DISP = screen.get_size()[1]/2 - creator_background.get_height()/2
					display.blit(creator_background,(0+X_DISP,0+Y_DISP))
				if lBgButton.cursorIn(realmouse):
					if N_NOW-1 < 0:
						N_NOW = N_IMAGES-1
					else:
						N_NOW -= 1
					creator_background = pygame.image.load("content/creator_backgrounds/"+str(img_list[N_NOW])).convert()
					X_DISP = screen.get_size()[0]/2 - creator_background.get_width()/2
					Y_DISP = screen.get_size()[1]/2 - creator_background.get_height()/2
					display.blit(creator_background,(0+X_DISP,0+Y_DISP))
				if undoButton.cursorIn(realmouse):
					if len(T) > 0 and len(temp) == 0:
						points = points[:-len(T[-1][0])]
						T = T[:-1]
				if circleRadiusUp.cursorIn(realmouse):
					if CIRCLE_RADIUS < 60:
						CIRCLE_RADIUS+=5
				if circleRadiusDown.cursorIn(realmouse):
					if CIRCLE_RADIUS > 10:
						CIRCLE_RADIUS-=5
				if factionRight.cursorIn(realmouse):
					if STATE_NOW+2 > len(STATES_LIST):
						STATE_NOW = 0
					else:
						STATE_NOW += 1
					STATES_LIST[STATE_NOW].drawCreator(screen, STATE_NOW)
				if factionLeft.cursorIn(realmouse):
					if STATE_NOW-1 < 0:
						STATE_NOW = len(STATES_LIST) - 1
					else:
						STATE_NOW -= 1
					STATES_LIST[STATE_NOW].drawCreator(screen, STATE_NOW)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and len(temp) > 2:
					prov_name = PROVINCE_NAMES[ random.randint(0, PROVINCE_NAMES_LEN-1) ]
					# print(STATE_NOW)
					# print(prov_name)
					# print(temp)
					x_avg = 0
					y_avg = 0
					for x in temp:
						x_avg += x[0]
						y_avg += x[1]
					x_avg //= len(temp)
					y_avg //= len(temp)
					font = pygame.font.Font('content/menu/LEMONMILK-Regular.otf',12)
					# print(prov_name)
					province_rend = font.render(prov_name, True , COLOR_BACKGROUND)
					# newProvince = Province(prov_name, temp)
					# newProvince.setOwnerCreator(STATES_LIST, STATE_NOW)
					T.append([temp, STATES_LIST[STATE_NOW].id, STATES_LIST[STATE_NOW].color1,prov_name,(x_avg,y_avg),province_rend])
					# T.append(newProvince)
					temp = []
				# if event.key == pygame.K_w:
				# 	Y_DISP += XY_DISP_SPEED
				# elif event.key == pygame.K_s:
				# 	Y_DISP -= XY_DISP_SPEED
				# elif event.key == pygame.K_a:
				# 	X_DISP += XY_DISP_SPEED
				# elif event.key == pygame.K_d:
				# 	X_DISP -= XY_DISP_SPEED
		keys = pygame.key.get_pressed()
		if keys[K_w]:
			Y_DISP += speed*dt
		elif keys[K_s]:
			Y_DISP -= speed*dt
		if keys[K_a]:
			X_DISP += speed*dt
		elif keys[K_d]:
			X_DISP -= speed*dt


		if SAVE_TIMER_XD > 0:
			display.blit(save_display,(0,0))
			SAVE_TIMER_XD -= 1


		screen.blit(display,(0,DISPLACEMENT))

		# print("Kreator | "+str(clock.get_fps()))
		pygame.display.update()
		dt = clock.tick(60) / 1000


# map()