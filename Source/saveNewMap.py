from datetime import datetime
from country import *
import json


def saveMap(provincesList, stateList, displacement):
	# print(stateList)
	i = 0
	while os.path.exists("content/maps/map_%s.json" % i):
		i += 1
	MAP_NAME = "map_"+str(i)
	COUNTRIES = []
	PROVINCES = []
	OWN = []
	for province in provincesList:
		temp = {
			'name': province[3],
			'owner': province[1],
			'points': province[0]
		}
		if province[1] not in OWN:
			OWN.append(province[1])
		PROVINCES.append(temp)

	# index = 0
	for country in stateList:
		if country.id in OWN:
			temp = {
				'name': country.name,
				'country_id':country.id,
				'color1': country.color1,
				'color2': country.color2,
				'color3': country.color3
			}
			COUNTRIES.append(temp)
			# index+=1
	# print(OWN)
	newMap = {
		'name': MAP_NAME,
		'center': displacement,
		'countries': COUNTRIES,
		'provinces': PROVINCES
	}

	with open("content/maps/"+MAP_NAME+".json", "w") as outfile:
		json.dump(newMap, outfile)
	# with open(MAP_NAME+".json", "r") as fff:
	# 	print(json.load(fff))

