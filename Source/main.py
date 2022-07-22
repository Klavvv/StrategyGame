from json.tool import main
import pygame
import sys
from pygame.locals import *
from pygame import gfxdraw
from uni_button import *
import map_creator
import map_menu

SCREEN_RESOLUTION = (1920,1080)
COLOR_PRIMARY = (238,33,33)
COLOR_SECONDARY = (197,197,197)
# COLOR_SECONDARY = (197,172,75)
COLOR_BACKGROUND = (7,7,7)
COLOR_BACKGROUND_SECOND = (14,14,14)

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Test")
flags = FULLSCREEN | DOUBLEBUF
screen = pygame.display.set_mode(SCREEN_RESOLUTION,flags,32)
pygame.mouse.set_cursor(*pygame.cursors.arrow)

def main_menu():
    BACKGROUND_IMAGE = pygame.image.load("content/menu/menu_background.png").convert()
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE,SCREEN_RESOLUTION)
    # OV = pygame.image.load("content/menu/overlay.png").convert_alpha()

    screen.blit(BACKGROUND_IMAGE,(0,0))
    space = 85
    menu_button1 = ButtonA("NOWA GRA", (350,60), 45, space*1)
    # menu_button2 = ButtonA("WCZYTAJ GRĘ", (350,60), 30, space*2)
    menu_button3 = ButtonA("KREATOR MAP", (350,60), 30, space*2)
    # menu_button4 = ButtonA("O GRZE", (350,60), 30, space*4)
    menu_button5 = ButtonA("WYJDŹ", (350,60), 30, space*5)
    
    while True:
        mousePosition = pygame.mouse.get_pos()
        menu_button1.draw(screen,mousePosition)
        # menu_button2.draw(screen,mousePosition)
        menu_button3.draw(screen,mousePosition)
        # menu_button4.draw(screen,mousePosition)
        menu_button5.draw(screen,mousePosition)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if menu_button1.cursorIn(mousePosition):
                    map_menu.map_menu(screen)
                    screen.blit(BACKGROUND_IMAGE,(0,0))
                # elif menu_button2.cursorIn(mousePosition):
                #     pygame.quit()
                elif menu_button3.cursorIn(mousePosition):
                    map_creator.map(screen)
                    screen.blit(BACKGROUND_IMAGE,(0,0))
                # elif menu_button4.cursorIn(mousePosition):
                #     pygame.quit()
                elif menu_button5.cursorIn(mousePosition):
                    pygame.quit()

       
        # print("Menu | "+str(clock.get_fps()))
        pygame.display.update()
        clock.tick(120)


main_menu()