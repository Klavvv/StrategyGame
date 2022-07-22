import os
import json
from province import *
from country import *

def readMapsFromFolder():
	listdir = os.listdir('content/maps')
	SAVE_DATA = []
	for save in listdir:
		# try:
		with open("content/maps/"+save, "r") as saveData:
			temporary = json.load(saveData)
			game_name = temporary['name']
			# print(game_name)
			game_countries = []
			for element in temporary['countries']:
				game_countries.append( [   element['name']  , element['country_id'] , element['color2']  ] )
			SAVE_DATA.append( [game_name, game_countries, save]  )
		# except:
		# 	pass
	return SAVE_DATA


def readGameData(mapName):
	with open("content/maps/"+mapName, "r") as saveData:

		temporary = json.load(saveData)

		return temporary

def provJ2provT(game_data, countries):
	provinces = []
	for province in game_data["provinces"]:
		temp = Province(province["name"],province["points"])
		owner = None
		for country in countries:
			if country.id == province["owner"]:
				owner = country
		temp.setOwner( owner )
		provinces.append( temp )
	return provinces

def counJ2counT(game_data):
	countries = []
	for country in game_data["countries"]:
		countries.append(Country( country["country_id"], country["name"], country["color1"], country["color2"], country["color3"]) )
	return countries