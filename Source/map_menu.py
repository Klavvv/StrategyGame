import os
import pygame
import sys
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
from province import *
from country import *
from readMaps import *
import math
from uni_button import *
from game import *
import random


SCREEN_RESOLUTION = (1920,1080)
COLOR_PRIMARY = (238,33,33)
COLOR_SECONDARY = (197,197,197)
# COLOR_SECONDARY = (197,172,75)
COLOR_BACKGROUND = (7,7,7)
COLOR_BACKGROUND_SECOND = (14,14,14)

clock = pygame.time.Clock()

def map_menu(screen):
	ON = True
	BACKGROUND_IMAGE = pygame.image.load("content/menu/menu_map.png").convert()
	BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE,SCREEN_RESOLUTION)
	screen.blit(BACKGROUND_IMAGE,(0,0))


	quit_button = ButtonB("← WYJDŹ", (120,40), 20, (10,screen.get_size()[1]-42))
	play_button = ButtonB("GRAJ", (120,40), 35, (screen.get_size()[0]-130,screen.get_size()[1]-50))
	maps_up_button =  ButtonI((40,40), "content/menu/arrow_up_normal.png", "content/menu/arrow_up_hover.png", (460,300))
	maps_down_button =  ButtonI((40,40), "content/menu/arrow_down_normal.png", "content/menu/arrow_down_hover.png", (460,890))
	factions_up_button =  ButtonI((40,40), "content/menu/arrow_up_normal.png", "content/menu/arrow_up_hover.png", (1420,300))
	factions_down_button =  ButtonI((40,40), "content/menu/arrow_down_normal.png", "content/menu/arrow_down_hover.png", (1420,890))

	MAPS = readMapsFromFolder()
	# print(MAPS)
	MAPS_BUTTONS = []
	space = 0
	for map_elements in MAPS:
		temp_name = map_elements[0]
		temp = ButtonB( temp_name, (600,50), 15 ,(180,340+space*50) )
		temp.setSecretNumber(space)
		MAPS_BUTTONS.append(temp)
		space += 1

	FACTION_BUTTONS = []

	MAPS_INDEX=0
	FACT_INDEX=0
	SHOW_MAPS = MAPS_BUTTONS[MAPS_INDEX:MAPS_INDEX+11]
	SHOW_FACT = []

	text_chosed_map = SmartText("Wybrana mapa: ", (700,50), 20, (130,950))
	text_chosed_faction = SmartText("Wybrana frakcja: ", (700,50), 20, (1090,950))

	CHOSED_MAP = None
	CHOSED_FACTION = None
	CHOSED_FACTION_REAL = None
	while ON:
		realmouse = pygame.mouse.get_pos()
		pygame.draw.rect(screen,COLOR_BACKGROUND, (150,300, 660, 600 ))
		pygame.draw.rect(screen,COLOR_BACKGROUND, (1110,300, 660, 600 ))

		quit_button.draw(screen,realmouse)
		play_button.draw(screen,realmouse)
		maps_up_button.draw(screen,realmouse)
		maps_down_button.draw(screen,realmouse)
		factions_up_button.draw(screen,realmouse)
		factions_down_button.draw(screen,realmouse)
		text_chosed_map.draw(screen,realmouse)
		text_chosed_faction.draw(screen,realmouse)

		for x in SHOW_MAPS:
			x.draw(screen, realmouse)
		for x in SHOW_FACT:
			x.draw(screen, realmouse)

		







		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:

				if play_button.cursorIn(realmouse):
					game(screen, MAPS[CHOSED_MAP],CHOSED_FACTION_REAL)
					screen.blit(BACKGROUND_IMAGE,(0,0))
				
				elif quit_button.cursorIn(realmouse):
					ON = False

				elif maps_up_button.cursorIn(realmouse):
					if MAPS_INDEX > 0:
						MAPS_INDEX -= 1
						SHOW_MAPS = MAPS_BUTTONS[MAPS_INDEX:MAPS_INDEX+11]
						for every in MAPS_BUTTONS:
							every.moveUpDown(50)

				elif maps_down_button.cursorIn(realmouse):
					if MAPS_INDEX+11 < len(MAPS_BUTTONS):
						MAPS_INDEX += 1
						SHOW_MAPS = MAPS_BUTTONS[MAPS_INDEX:MAPS_INDEX+11]
						for every in MAPS_BUTTONS:
							every.moveUpDown(-50)

				elif factions_up_button.cursorIn(realmouse):
					if FACT_INDEX > 0:
						FACT_INDEX -= 1
						SHOW_FACT = FACTION_BUTTONS[FACT_INDEX:FACT_INDEX+11]
						for every in FACTION_BUTTONS:
							every.moveUpDown(50)

				elif factions_down_button.cursorIn(realmouse):
					if FACT_INDEX+11 < len(FACTION_BUTTONS):
						FACT_INDEX += 1
						SHOW_FACT = FACTION_BUTTONS[FACT_INDEX:FACT_INDEX+11]
						for every in FACTION_BUTTONS:
							every.moveUpDown(-50)

				for map_elem in SHOW_MAPS:
					if map_elem.cursorIn(realmouse):
						text_chosed_map = SmartText("Wybrana mapa: "+str(  MAPS[ map_elem.secret_number ][0]  ), (600,50), 20, (180,950))
						CHOSED_MAP = map_elem.secret_number
						for aaa in MAPS_BUTTONS:
							aaa.forceHoverF(False)
						map_elem.forceHoverF(True)
						CHOSED_FACTION = None
						text_chosed_faction = SmartText("Wybrana frakcja:", (600,50), 20, (1140,950))
						FACTION_BUTTONS = []
						fact_space = 0
						faction_list = MAPS[CHOSED_MAP]
						# print(faction_list)
						for fact in faction_list[1]:
							fact_name = fact[0]
							temp5 = ButtonB( str(fact_name), (600,50), 15 ,(1140,340+fact_space*50) )
							temp5.setSecretNumber(fact_space)
							fact_space+=1
							FACTION_BUTTONS.append(temp5)
						FACT_INDEX=0
						SHOW_FACT = FACTION_BUTTONS[FACT_INDEX:FACT_INDEX+11]

				for fact_elem in SHOW_FACT:
					if fact_elem.cursorIn(realmouse):
						text_chosed_faction = SmartText("Wybrana frakcja: "+str( MAPS[CHOSED_MAP][1][fact_elem.secret_number][0] ), (600,50), 20, (1140,950))
						CHOSED_FACTION = fact_elem.secret_number
						CHOSED_FACTION_REAL = MAPS[CHOSED_MAP][1][fact_elem.secret_number][1]
						for aaa in FACTION_BUTTONS:
							aaa.forceHoverF(False)
						fact_elem.forceHoverF(True)




		pygame.display.update()
		clock.tick(120)


# map()