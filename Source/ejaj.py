from warThings import *
import random

def ai_actions(chosedFaction, COUNTRIES, PROVINCES, TRANSPORT):
	for country in COUNTRIES:
		if country.player != True:
			country_provinces = []
			country_neighbourhood = []
			for province in PROVINCES:
				if province.state == country.id:
					country_provinces.append(province)
			for province in country_provinces:
				temp = [province,[]]
				for provvv in PROVINCES:
					if provvv.state != province.state and provvv not in temp[1]:
						counter = 0
						for point in provvv.points:
							if point in province.points:
								counter += 1
						if counter > 1:
							temp[1].append(provvv)
				country_neighbourhood.append(temp)

			for neighbour in country_neighbourhood:
				for place_to_attack in neighbour[1]:
					if place_to_attack.army < neighbour[0].army:
						_attack = True
						for trans in TRANSPORT:
							if trans.province1_id == place_to_attack.province_id and trans.province2_id == neighbour[0].province_id:
								_attack = False
						if _attack:
							TRANSPORT.append(  Transport(neighbour[0] , place_to_attack)   )
							for aaaa in PROVINCES:
								if aaaa.province_id == neighbour[0].province_id:
									aaaa.deleteArmy()
	return {"transport":TRANSPORT, "provinces":PROVINCES}

def ai_actions2(chosedFaction, COUNTRIES, PROVINCES, TRANSPORT):

	for province in PROVINCES:
		if province.state != chosedFaction:
			for neighbour in province.neighbour:
				for other_province in PROVINCES:
					if neighbour == other_province.province_id:
						if other_province.state != province.state:
							if other_province.army < province.army:
								chance = (1-(other_province.army / province.army)) * 100
								if random.randint(0,100) < chance:
									if random.randint(0,150) < 1: 
										_attack = True
										for trans in TRANSPORT:
											if trans.province1_id == other_province.province_id and trans.province2_id == province.province_id:
												_attack = False
										if _attack:
											TRANSPORT.append(  Transport(province , other_province, province.state)   )
											province.deleteArmy()
						break
	for country in COUNTRIES:
		if not country.player:
			if random.randint(0,10) < country.agression:
				if country.money >= 100:
					for province in PROVINCES:
						if province.state == country.id:
							if random.randint(0,100) < 5:
								if country.money >= 100:
									country.money -= 100
									province.buyArmy()
			else:
				if country.money >= 100:
					for province in PROVINCES:
						if province.state == country.id and province.development < 8:
							if random.randint(0,100) < 5:
								if country.money >= 100:
									country.money -= 100
									province.upgradeProvince()
									country.updateDailyMoney(PROVINCES)
			
				






	return {"transport":TRANSPORT, "provinces":PROVINCES, "countries":COUNTRIES}



			# print(country_neighborhood)