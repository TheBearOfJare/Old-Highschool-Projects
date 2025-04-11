import requests
from keep_alive import keep_alive
import discord
import pnwkit
import requests
import random
import datetime
import math
import time
from replit import db

minscore = 10000000
maxscore = 0
ids = []
person = ''
key = '51f2058772e1cb'
client = discord.Client()
pnwkit.set_key(key)
update = True
alert = False
awaitwar = False
awaittargets = False
quotecount = 0
type = ''
enemy = ''
who = ''
db['most nuked'] = 0
db['nuke award'] = 'nobody'
db['most damage'] = 0
db['damage award'] = 'nobody'
db['most loot'] = 0
db['loot award'] = 'nobody'

awardlist = []


quotes = [
		'“When the people fear the government there is tyranny, when the government fears the people there is liberty.” - John Basil Barnhill',
		'“They who can give up essential liberty to obtain a little temporary safety deserve neither liberty nor safety.” - Benjamin Franklin',
		'“Those who deny freedom to others deserve it not for themselves.” - Abraham Lincoln.',
		'“If liberty means anything at all, it means the right to tell people what they do not want to hear.” - George Orwell.',
		"“For to be free is not merely to cast off one's chains, but to live in a way that respects and enhances the freedom of others.” - Nelson Mandela",
		'“Whoever would overthrow the liberty of a nation must begin by subduing the freeness of speech.” - Benjamin Franklin',
		"“Liberty means responsibility. That is why most men dread it.” - George Bernard Shaw",
		"Give me liberty, or give me death! - Patrick Henry"
]

soldiers = [
		"Corcerina", "EZIC Star", "Grepera", "Azrael",
		"Classical Christian Alliance", "Empire of Texas", "Andonia",
		"Federated People of Texas", "Hussaria", "Borneo Republic", "Eanraig",
		"Hogwarts Empire", "Marius Meritocracy", "Newer Orleans", "Nopolia",
		"Evolin", "Spork", "Filuji", "Williamsbourg", "Floridian Republic",
		"The Kingdom of Fearless", "Noctustein", "Conservative States", "Borbland",
		"Afrikanerland", "The land of the pharaohs", "Grand Bunger Empire",
		"New Livonia", "Libertariaia", "Lupus Dominion", "Texas 2", "iggloo Mk2",
		"The New United States"
]

newawards = []
async def acheivements():
		global awardlist
		global newawards
		global wheretosend
		citizens = requests.get(
				f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{
		nations(alliance_id: 6215 first:500) {{ 
		data {{
				alliance_position
				last_active
				nation_name
				num_cities
				nukes
				wars {{
				attacks {{
						att_id
						infra_destroyed_value
						money_stolen
				}}
				}}
				gross_national_income
				soldier_kills
				tank_kills
				aircraft_kills
				ship_kills
				nuke_kills
				discord
		}}
		}}
}}''').json()['data']['nations']['data']
		nukemax = db['nukemax']

		for nation in citizens:
				if nation['alliance_position'] == 'APPLICANT':
						continue

				wars = nation['wars']
				nuked = nation['nuke_kills']
				loot = 0
				gni = (nation['gross_national_income'] / 365) / 1000000
				damage = 0
				aluminum = 0
				steel = 0

				for war in wars:
						for attack in war['attacks']:
								if attack['att_id'] == nation['id']:
										damage += attack['infra_destroyed_value']
										loot += attack['money_stolen']

				if nuked > 1 and nuked < 5 and f"{nation['discord']} First taste of radiation" not in awardlist:
						awardlist.append(f"{nation['discord']} First taste of radiation")
						newawards.append(f"{nation['discord']} First taste of radiation")

				if nuked >= 5 and nuked < 10:
						awardlist.append(f"{nation['discord']} Irradiated")

				if nuked > nukemax:
						db['most nuked'] = nuked
						db['resident biohazard'] = nation['discord']

				if gni > 1 and gni < 5 and f"{nation['discord']} $ Washington $" not in awardlist:
						awardlist.append(f"{nation['discord']} $ Washington $")

				if gni > 5 and gni < 10 and f"{nation['discord']} $ Lincoln $" not in awardlist:
						awardlist.append(f"{nation['discord']} $ Lincoln $")

				if gni > 10 and gni < 20 and f"{nation['discord']} $ Hamilton $" not in awardlist:
						awardlist.append(f"{nation['discord']} $ Hamilton $")

				if gni > 20 and f"{nation['discord']} $ Tubman $" not in awardlist:
						awardlist.append(f"{nation['discord']} $ Tubman $")

				troops = nation['soldier_kills'] - [
						f"{nation['nation_name']} troops old"
				]
				troops = troops * 5

				tanks = nation['tank_kills'] - [f"{nation['nation_name']} tanks old"]
				steel += (0.5 * tanks)
				tanks = tanks * 60

				planes = nation['aircraft_kills'] - [
						f"{nation['nation_name']} planes old"
				]
				aluminum += (5 * planes)
				planes = planes * 4000

				ships = nation['ship_kills'] - [f"{nation['nation_name']} ships old"]
				steel += (ships * 30)
				ships = ships * 50000

				prices = requests.get(
						'''https://api.politicsandwar.com/graphql?api_key={key}&query={{
		tradeprices(first: 1) {{
		data {{
				steel
				aluminum
		}}
		}}
}}''').json()['data']['tradeprices']['data']
				steel = steel * prices[0]
				aluminum = aluminum * prices[1]

				db[f"{nation['nation_name']}"] = round(
						(damage + troops + tanks + planes + ships + steel + aluminum) / 1000000, 3)

				db[f"{nation['nation_name']} loot"] = round((loot/1000000, 3))


async def leaderboard(message):
		global wheretosend
		nations = requests.get(
				'''https://api.politicsandwar.com/graphql?api_key={key}&query={{
		nations(alliance_id: 6215 color: "blue") ""{
		data {{
				nation_name
				discord
		}}
		}}
}}''').json()['data']['nations']['data']
		highscores = [0] * 20
		best = ['none'] * 20
		for nation in nations:
				count = 0
				for i in highscores:
						score = db[f"{nation['nation_name']}"]
						if score < i:
								count += 1
								continue
						else:
								highscores[count] = score
								best[count] = f"{nation['nation name']}, aka {nation['discord']}"
								break
		
		Message = '```'
		count = 0
		for i in range(11):
				Message = Message + f'\n{count}. {best[count]}: destroyed ${highscores[count]} million.  --  {count+10}. {best[count+10]}: destroyed ${highscores[count]+10} million.'

		Message = Message+'\n```'
		await wheretosend.send(f'**Masters of Destruction**')
		await wheretosend.send(Message)

	
async def warcosts(message, id, who):
		global wheretosend
		stats = [
				'infrastructure', 'casualties', 'resources', 'money stolen', 'total'
		]
		stats = [0, 0, 0, 0, 0]
		loot = 0
		money = 0
		gas = 0
		munitions = 0
		steel = 0
		aluminum = 0
		uranium = 0
		cas = 0
		if who == 'all':
				person = requests.get(
						f'https://api.politicsandwar.com/graphql?api_key={key}&query={{tradeprices{{data {{aluminum steel munitions gasoline uranium}}}} nations(alliance_id: 6215 color: "blue" first: 500){{data{{nation_name, id, wars{{attacks {{att_id type def_mun_used att_mun_used def_gas_used att_gas_used money_stolen aircraft_killed_by_tanks infra_destroyed_value attcas1 attcas2 defcas1 defcas2 money_stolen}}}}}}}}}}'
				).json()['data']
		else:
				person = requests.get(
						f'https://api.politicsandwar.com/graphql?api_key={key}&query={{tradeprices{{data {{aluminum steel munitions gasoline uranium}}}} nations(id: {id} first: 1){{data{{nation_name, id, wars{{attacks {{att_id type def_mun_used att_mun_used def_gas_used att_gas_used money_stolen aircraft_killed_by_tanks infra_destroyed_value attcas1 attcas2 defcas1 defcas2 money_stolen}}}}}}}}}}'
				).json()['data']

		prices = person['tradeprices']['data'][0]
		prices = [
				prices['steel'], prices['aluminum'], prices['gasoline'],
				prices['munitions'], prices['uranium']
		]

		print(len(person['nations']['data']))
		if who == 'all':
				for nation in person['nations']['data']:
						wars = nation['wars']
						for war in wars:
								for attack in war['attacks']:
										if attack['att_id'] == id:

												if attack['type'] == 'GROUND':
														cas += (attack['attcas1'] * 5)
														cas += (attack['attcas2'] * 60)
														steel += (0.5 * attack['attcas2'])
														gas += attack['att_gas_used']
														munitions += attack['att_mun_used']
														money += attack['money_stolen']

												if attack['type'][0:2] == 'AIR':
														cas += (attack['attcas1'] * 4000)
														aluminum += (5 * attack['attcas1'])
														gas += attack['att_gas_used']
														munitions += attack['att_mun_used']

												if attack['type'] == 'NAVAL':
														cas += (attack['attcas1'] * 50000)
														steel += (30 * attack['attcas1'])
														gas += attack['att_gas_used']
														munitions += attack['att_mun_used']

												if attack['type'][0:7] == 'MISSILE':
														cas += 150000
														aluminum += 100
														gas += 75
														munitions += 75

												if attack['type'][0:4] == 'NUKE':
														cas += 1750000
														aluminum += 750
														gas += 500
														uranium += 250

										else:
												stats[0] += attack['infra_destroyed_value']

												if attack['type'] == 'GROUND':
														cas += (attack['defcas1'] * 5)
														cas += (attack['defcas2'] * 60)
														steel += (0.5 * attack['defcas2'])
														if str(attack['aircraft_killed_by_tanks']
																		) != 'None':
																aluminum += (
																		5 * attack['aircraft_killed_by_tanks'])
																cas += (4000 *
																				attack['aircraft_killed_by_tanks'])
														gas += attack['att_gas_used']
														munitions += attack['att_mun_used']
														money -= attack['money_stolen']
														loot += attack['money_stolen']

												if attack['type'][0:3] == 'AIR':
														cas += (attack['defcas1'] * 4000)
														aluminum += (5 * attack['defcas1'])
														gas += attack['att_gas_used']
														munitions += attack['att_mun_used']

														if attack['type'] == 'AIRVSHIPS':
																cas += (attack['defcas2'] * 50000)
																steel += (30 * attack['defcas2'])

														if attack['type'] == 'AIRVTANKS':
																cas += (attack['defcas2'] * 60)
																steel += (0.5 * attack['defcas2'])

														if attack['type'] == 'AIRVSOLDIERS':
																cas += (attack['defcas2'] * 5)

														if attack['type'] == 'AIRVMONEY':
																cas += (attack['defcas2'])

												if attack['type'] == 'NAVAL':
														steel += (30 * attack['defcas1'])
														gas += attack['att_gas_used']
														munitions += attack['att_mun_used']
				resource = (steel * prices[0]) + (aluminum * prices[1]) + (
						gas * prices[2]) + (munitions * prices[3]) + (uranium * prices[4])

				stats[1] = resource
				stats[2] = cas
				stats[3] = money

				stats[4] = stats[0] + stats[1] + stats[2] + loot

				await wheretosend.send(
						f'**Deficit:**\n```Infrastructure losses: ${round(stats[0]/1000000,3)}M\nResource expenditure: ${round(stats[1]/1000000,3)}M\nMilitary losses: ${round(stats[2]/1000000,3)}M\nNet monetary loot: {stats[3]}\nTOTAL: ${round(stats[4]/1000000,3)}M```'
				)
				return

		wars = person['nations']['data'][0]['wars']
		for war in wars:
				for attack in war['attacks']:
						if attack['att_id'] == id:

								if attack['type'] == 'GROUND':
										cas += (attack['attcas1'] * 5)
										cas += (attack['attcas2'] * 60)
										steel += (0.5 * attack['attcas2'])
										gas += attack['att_gas_used']
										munitions += attack['att_mun_used']
										money += attack['money_stolen']

								if attack['type'][0:2] == 'AIR':
										cas += (attack['attcas1'] * 4000)
										aluminum += (5 * attack['attcas1'])
										gas += attack['att_gas_used']
										munitions += attack['att_mun_used']

								if attack['type'] == 'NAVAL':
										cas += (attack['attcas1'] * 50000)
										steel += (30 * attack['attcas1'])
										gas += attack['att_gas_used']
										munitions += attack['att_mun_used']

								if attack['type'][0:7] == 'MISSILE':
										cas += 150000
										aluminum += 100
										gas += 75
										munitions += 75

								if attack['type'][0:4] == 'NUKE':
										cas += 1750000
										aluminum += 750
										gas += 500
										uranium += 250

						else:
								stats[0] += attack['infra_destroyed_value']

								if attack['type'] == 'GROUND':
										cas += (attack['defcas1'] * 5)
										cas += (attack['defcas2'] * 60)
										steel += (0.5 * attack['defcas2'])
										if str(attack['aircraft_killed_by_tanks']) != 'None':
												aluminum += (5 * attack['aircraft_killed_by_tanks'])
												cas += (4000 * attack['aircraft_killed_by_tanks'])
										gas += attack['att_gas_used']
										munitions += attack['att_mun_used']
										money -= attack['money_stolen']
										loot += attack['money_stolen']

								if attack['type'][0:3] == 'AIR':
										cas += (attack['defcas1'] * 4000)
										aluminum += (5 * attack['defcas1'])
										gas += attack['att_gas_used']
										munitions += attack['att_mun_used']

										if attack['type'] == 'AIRVSHIPS':
												cas += (attack['defcas2'] * 50000)
												steel += (30 * attack['defcas2'])

										if attack['type'] == 'AIRVTANKS':
												cas += (attack['defcas2'] * 60)
												steel += (0.5 * attack['defcas2'])

										if attack['type'] == 'AIRVSOLDIERS':
												cas += (attack['defcas2'] * 5)

										if attack['type'] == 'AIRVMONEY':
												cas += (attack['defcas2'])

								if attack['type'] == 'NAVAL':
										steel += (30 * attack['defcas1'])
										gas += attack['att_gas_used']
										munitions += attack['att_mun_used']

		resource = (steel * prices[0]) + (aluminum * prices[1]) + (
				gas * prices[2]) + (munitions * prices[3]) + (uranium * prices[4])

		stats[1] = resource
		stats[2] = cas
		stats[3] = money

		stats[4] = stats[0] + stats[1] + stats[2] + loot

		await wheretosend.send(
				f'**Deficit:**\n```Infrastructure losses: ${round(stats[0]/1000000,3)}M\nResource expenditure: ${round(stats[1]/1000000,3)}M\nMilitary losses: ${round(stats[2]/1000000,3)}M\nNet monetary loot: {stats[3]}\nTOTAL: ${round(stats[4]/1000000,3)}M```'
		)


async def stats(message, who, user):
		global wheretosend
		person = requests.get(
				f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id: {who} first: 1){{data{{id, leader_name, cities{{barracks factory hangar drydock}}}}}}}}'''
		).json()['data']['nations']['data'][0]
		barracks = 0
		factories = 0
		hangars = 0
		drydocks = 0

		x = 0
		while x < len(person['cities']):
				barracks += person['cities'][x]['barracks']
				factories += person['cities'][x]['factory']
				x += 1

		x = 0
		while x < len(person['cities']):
				hangars += person['cities'][x]['hangar']
				x += 1

		x = 0
		while x < len(person['cities']):
				drydocks += person['cities'][x]['drydock']
				x += 1
		cities = len(person['cities'])
		await wheretosend.send(
				f'{user} has:\n{barracks} barracks,\n{factories} factories,\n{hangars} hangars, and\n{drydocks} drydocks.\n\nThis classifies {user} at a {round(barracks/cities,1)}, {round(factories/cities,1)}, {round(hangars/cities,1)}, {round(drydocks/cities,1)} build.'
		)


async def MMR(message, who):
		global wheretosend
		global alert
		fail = 0
		good = 0
		succsess = 0
		key = '2dae66a36f73b1'
		if who == 'all':
				citizens = requests.get(
						f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(alliance_id: 6215 color: "Blue" first: 500){{data{{id, leader_name, cities{{barracks factory hangar drydock}}}}}}}}'''
				).json()['data']['nations']['data']

		else:
				citizens = requests.get(
						f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id: {who} first: 1){{data{{id, leader_name, cities{{barracks factory hangar drydock}}}}}}}}'''
				).json()['data']['nations']['data']

		i = 0
		while i < len(citizens):
				groundforces = 0
				aircraft = 0
				ships = 0
				missing = []

				x = 0
				while x < len(citizens[i]['cities']):
						groundforces += citizens[i]['cities'][x]['barracks']
						groundforces += citizens[i]['cities'][x]['factory'] * 2.5
						x += 1

				if groundforces < 5 * len(citizens[i]['cities']):
						missing.append(
								f"\nGround Forces: you need either {math.ceil((5*len(citizens[i]['cities'])-groundforces))} more barracks or {math.ceil((5*len(citizens[i]['cities'])-groundforces)/2.5)} more factories"
						)

				x = 0
				while x < len(citizens[i]['cities']):
						aircraft += citizens[i]['cities'][x]['hangar']
						x += 1

				if aircraft < 5 * len(citizens[i]['cities']):
						missing.append(
								f"\nAircraft: you need {5*len(citizens[i]['cities'])-aircraft} more hangars"
						)

				x = 0
				while x < len(citizens[i]['cities']):
						ships += citizens[i]['cities'][x]['drydock']
						x += 1

				if ships < len(citizens[i]['cities']):
						missing.append(
								f"\nShips: you need {len(citizens[i]['cities'])-ships} more drydocks"
						)

				x = 0
				Message = ''
				while x < len(missing):
						Message = Message + missing[x]
						x += 1
				print(Message)
				print(groundforces / (5 * len(citizens[i]['cities'])))
				print(aircraft / (5 * len(citizens[i]['cities'])))
				print(ships / len(citizens[i]['cities']))
				print(len(citizens[i]['cities']))
				if Message != '':
						if alert == True:
								requests.post(
										"https://politicsandwar.com/api/send-message/",
										data={
												"to": citizens[i]['id'],
												"subject": f'Minimum Military',
												"message":
												f"Hey {citizens[i]['leader_name']},\nIt appears that you do not yet meet the minimum military requirements for citizens. This is an automated reminder; please let me know if there has been a mistake. Our current requirements are either 5 barracks or 2 factories per city, plus 5 hangars per city and 1 drydock per city. You need to increase your military capacity in the following areas:\n{Message}\n\nAgain, if this was a mistake please let me know. Otherwise please work to quickly meet these requirements. If you need financial assitance in meeting them, contact @The Decendant in discord or message Eonia (Nation: Corcerina) and ask for help in meeting the minimum military requirements.",
												"key": {key}
										})
						succsess += (groundforces / 5 * len(citizens[i]['cities'])) + (
								aircraft / 5 * len(citizens[i]['cities'])) + (
										ships / len(citizens[i]['cities']))
						fail += 1
						i += 1
				else:
						succsess += ((groundforces / (5 * len(citizens[i]['cities']))) +
														(aircraft / (5 * len(citizens[i]['cities']))) +
														(ships / len(citizens[i]['cities']))) / 3
						good += 1
						i += 1

		succsess = succsess / len(citizens)

		if who == 'all':
				await wheretosend.send(
						f'```\nFail: {fail}\nPass: {good}\nOverall Pass Rate: {round(100*(good/(fail+good)),2)}%\nMilitary Readyness: {round(succsess,2)}%```'
				)
		else:
				if Message != '':
						await wheretosend.send(Message)
				else:
						await wheretosend.send(
								f"Looks like you're all good! You passed MMR with a overall percentage of {round(succsess*100,2)}%"
						)


async def soldierMMR(message, who):
		global wheretosend
		Messagelist = []
		faillist = []
		fail = 0
		good = 0
		succsess = 0
		key = '2dae66a36f73b1'
		if who == 'all':
				people = soldiers

		else:
				people = [1]

		i = 0
		while i < len(people):
				if who == 'all':
						citizens = requests.get(
								f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(nation_name: "{soldiers[i]}" first: 1){{data{{id, leader_name, cities{{barracks factory hangar drydock}}}}}}}}'''
						).json()['data']['nations']['data']
				else:
						citizens = requests.get(
								f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id: {who} first: 1){{data{{id, leader_name, cities{{barracks factory hangar drydock}}}}}}}}'''
						).json()['data']['nations']['data']
				groundforces = 0
				aircraft = 0
				ships = 0
				missing = []

				try:
						print(citizens[0]['cities'])
				except Exception:
						print(citizens)
						print(soldiers[i])
						i += 1
						continue
				x = 0
				while x < len(citizens[0]['cities']):
						groundforces += citizens[0]['cities'][x]['barracks']
						groundforces += citizens[0]['cities'][x]['factory'] * 2.5
						x += 1

				if groundforces < 10 * len(citizens[0]['cities']):
						missing.append(
								f"\nGround Forces: you need either {math.ceil((10*len(citizens[0]['cities'])-groundforces))} more barracks or {math.ceil((10*len(citizens[0]['cities'])-groundforces)/2.5)} more factories"
						)

				x = 0
				while x < len(citizens[0]['cities']):
						aircraft += citizens[0]['cities'][x]['hangar']
						x += 1

				if aircraft < 5 * len(citizens[0]['cities']):
						missing.append(
								f"\nAircraft: you need {5*len(citizens[0]['cities'])-aircraft} more hangars"
						)

				x = 0
				while x < len(citizens[0]['cities']):
						ships += citizens[0]['cities'][x]['drydock']
						x += 1

				if ships < len(citizens[0]['cities']):
						missing.append(
								f"\nShips: you need {len(citizens[0]['cities'])-ships} more drydocks"
						)

				x = 0
				Message = ''
				while x < len(missing):
						Message = Message + missing[x]
						x += 1
				print(Message)
				print(groundforces / (10 * len(citizens[0]['cities'])))
				print(aircraft / (5 * len(citizens[0]['cities'])))
				print(ships / len(citizens[0]['cities']))
				print(len(citizens[0]['cities']))

				if Message != '':
						succsess += ((groundforces / 10 * len(citizens[0]['cities'])) +
														(aircraft / 5 * len(citizens[0]['cities'])) +
														(ships / len(citizens[0]['cities']))) / 3
						faillist.append(
								f'https://politicsandwar.com/nation/id={citizens[0]["id"]}')
						Messagelist.append(Message)
						fail += 1
						i += 1
				else:
						succsess += ((groundforces / (10 * len(citizens[0]['cities']))) +
														(aircraft / (5 * len(citizens[0]['cities']))) +
														(ships / len(citizens[0]['cities']))) / 3
						good += 1
						i += 1

		succsess = succsess / len(citizens)

		if who == 'all':
				global person
				user = await client.fetch_user(person)
				await user.send(
						f'```\nFail: {fail}\nPass: {good}\nOverall Pass Rate: {round(100*(good/(fail+good)),2)}%\nMilitary Readyness: {round(succsess,2)}%```'
				)
				x = 0
				for i in faillist:
						await user.send(i)
						await user.send(Messagelist[x])
						x += 1
		else:
				if Message != '':
						await wheretosend.send(Message)
				else:
						await wheretosend.send(
								f"Looks like you're all good! You passed MMR with a overall percentage of {round(succsess*100,2)}%"
						)


async def alliancewar(message):
		global wheretosend
		global enemy
		global type
		global Message
		global awaitwar
		Message = f"{type}\nFind a target in {enemy} and declare war IMMEDIATELY./nTHIS IS NOT A DRILL. THIS IS A REAL WAR."
		await wheretosend.send(
				f'Your message reads:\n{Message}\n\nReady to send it? (y/n)')
		awaitwar = True


async def wartargets(message):
		global targets
		global Message
		global awaittargets
		global minscore
		global maxscore

		if len(targets) == 1:
				length = 1
				target = targets[0]
				skip = True
				nation = []
				for i in target:
						if skip == True and i != '=':
								continue
						if i == '=':
								skip = False
								continue
						nation.append(i)

				nation = ''.join(nation)
				nation = requests.get(f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id: {nation}){{data{{score}}}}}}''').json()['data']['nations']['data'][0]['score']
				minscore = nation*0.57142857142
				maxscore = nation*1.33333333
						
		else:
				for target in targets:
						skip = True
						for i in target:
								if skip == True and i != '=':
										continue
								if i == '=':
										skip = False
										continue
								nation.append(i)

						nation = ''.join(nation)
						nation = requests.get(f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id: {nation}){{data{{score}}}}}}''').json()['data']['nations']['data'][0]['score']
						if nation*0.57142857142 < minscore:
								minscore = nation*0.57142857142
						if nation*1.33333333 > maxscore:
								maxscore = nation*1.33333333
						
				length = 0
				
		targets = str(targets).replace('[', '')
		targets = targets.replace(']', '')
		targets = targets.replace("'", "")

		if length == 1:
				Message = f"You are called to assist in fighting against this nation: {targets}.\n\nIf you are confident in your ability to fight this nation, declare war. If you are otherwise incapable of fighting this nation, or unequiped to do so, by all means do not declare war."
		else:
				Message = f"You are called to assist in fighting against any of these targets: {targets}.\n\nFind one or more of these which you are confident in your ability to fight against and declare war. If you are otherwise incapable of fighting these, or unequiped to do so, by all means do not declare war."
		
		await wheretosend.send(
				f'Your message reads:\n{Message}\n\nReady to send it? (y/n)')
		awaittargets = True
		return

@client.event
async def on_ready():
		print('Ready...')
		global quotecount
		quotecount = random.randint(0, len(quotes) - 1)

acount = 0
@client.event
async def on_message(message):
		global wheretosend
		global minscore
		global maxscore
		global ids
		global alert
		global who
		global update
		global enemy
		global type
		global awaitwar
		global awaittargets
		global person
		global quotecount
		global acount	
		quote = quotes[quotecount]
		
		if message.author == client.user:
				return

		wheretosend = message.channel
		content = message.content

		if content.startswith('&verify'):
			person = message.author.id
			try:
				user = await client.fetch_user(person)
				db[f'{user} key'] = content[8:]
				await wheretosend.send('Success')
			except Exception:
				return
			
		
		if acount > 5:
				#await activity()
				acount = 0
		
		else:
				acount+=1

		for award in awardlist:
				count = 0
				for i in award:
						if i == ' ':
								who = award[0:count]
								award = award[count+1:]
								break
						count+=1
						if award == 'First taste of radiation':
								reason = 'get nuked at least once'
						if award == 'Irradiated':
								reason = 'get nuked at least 5 times'
						if award == 'Resident Biohazard':
								reason = 'get hit by more nukes than anybody else in the alliance'
						if award == '$ Washingtons $':
								reason == 'make more than $1M per day'
						if award == '$ Lincolns $':
								reason == 'make more than $5M per day'
						
				#await wheretosend.send(f'Congrats, <@{who}>!\nAcheivment Unlocked: "{award}" ({reason}).')

		

		if awaitwar == True:
				recipients = requests.get(
						f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(alliance_id: 6215 min_score: {who[0]} max_score: {who[1]} first: 500){{data{{id}}}}}}'''
				).json()['data']['nations']['data']

				response = content
				if response == "y":
						for i in recipients:
								print(
										requests.post(
												"https://politicsandwar.com/api/send-message/",
												data={
														"to": i['id'],
														"subject": f'War with {enemy}',
														"message": Message,
														"key": {key}
												}))

						await wheretosend.send('Sent!')
						awaitwar = False

				elif response == 'n':
						await wheretosend.send('Ok, Canceled.')
						awaitwar = False
				return

		if awaittargets == True:

				response = content
				if response == "y":
						recipients = requests.get(f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(alliance_id: 6215 first: 500 vmode: false min_score: {minscore} max_score: {maxscore}){{data{{id,discord}}}}}}''').json()['data']['nations']['data']
						for i in recipients:
								if i['discord'] != '':
										
										continue
								print(
										requests.post(
												"https://politicsandwar.com/api/send-message/",
												data={
														"to": i['id'],
														"subject": f'War Targets',
														"message": Message,
														"key": {'32b01c4ce92661'}
												}))
						await wheretosend.send('Sent!')
						awaittargets = False

				elif response == 'n':
						await wheretosend.send('Ok, Canceled.')
						awaittargets = False
				return

		if content == ('&warcosts'):
				person = message.author.id
				try:
						user = await client.fetch_user(person)
				except Exception:
						return
				try:
						player = pnwkit.nation_query({"discord": str(user)}, "id")[0]

				except Exception:
						await wheretosend.send(
								f"You don't seem to have discord attached to your nation.\nGo to https://politicsandwar.com/nation/edit/  and add your actual discord profile: {user}"
						)
						return

				player = list(str(player))
				del player[:9]
				player = ''.join(player)
				await warcosts(message, player, 'null')
				return

		if content == ('&warcosts all'):
				person = message.author.id
				try:
						user = await client.fetch_user(person)
				except Exception:
						return

				if str(user) != 'NightSoldat#9332' and str(
								user) != 'TheBearOfJare#2866' and str(
										user) != 'The Descendant#6672' and str(
												user) != 'Azrael#5827' and str(
														user) != 'Indigo#9882' and str(
																user) != 'Luke S#3588' and str(
																		user) != 'LeiaHair#0925':
						await wheretosend.send(
								"You don't have permission to use this command.")
						return
				await warcosts(message, 'null', 'all')
				return

		if content.startswith('&war targets'):
				global targets
				targets = []
				person = message.author.id
				try:
						user = await client.fetch_user(person)
				except Exception:
						return

				if str(user) != 'NightSoldat#9332' and str(
								user) != 'TheBearOfJare#2866' and str(
										user) != 'The Descendant#6672' and str(
												user) != 'Azrael#5827' and str(
														user) != 'Indigo#9882' and str(
																user) != 'Luke S#3588' and str(
																		user) != 'LeiaHair#0925' and str(
																				user) != 'MariusEmber#0832':
						await wheretosend.send(
								"You don't have permission to use this command.")
						return

				data = content
				data = list(data)
				del data[:13]

				while len(data) > 0:
						count = 0
						for i in data:
								print(targets)
								if i == ",":
										target = data[0:count]
										target = ''.join(target)
										targets.append(target)
										del data[0:count + 1]
								count += 1
								
						if count >= len(data):
								target = ''.join(data)
								targets.append(target)
								break

				print(targets)

				await wartargets(message)
				return

		if content.startswith('&alliance war'):
				person = message.author.id
				try:
						user = await client.fetch_user(person)
				except Exception:
						return

				if str(user) != 'NightSoldat#9332' and str(
								user) != 'TheBearOfJare#2866' and str(
										user) != 'The Descendant#6672' and str(
												user) != 'Azrael#5827' and str(
														user) != 'Indigo#9882' and str(
																user) != 'Luke S#3588' and str(
																		user) != 'LeiaHair#0925' and str:
						await wheretosend.send(
								"You don't have permission to use this command.")
						return

				data = content
				data = list(data)
				del data[:15]

				i = 0
				while i < len(data):
						if data[i] == ",":
								enemy = data[:i]
								break
						i += 1

				enemy = ''.join(enemy)
				del data[:i + 2]
				i = 0
				while i < len(data):
						if data[i] == ',':
								who = data[:i]
								break
						i += 1

				del data[:i + 2]
				type = ''.join(data)
				if type == 'defensive':
						type = f'ALERT: We are currently under attack by the alliance, {enemy}.'
				elif type == 'offensive':
						type = f'ALERT: We have declared war on, and are therefore at war with the alliance, {enemy}.'

				if ''.join(who) == 'all':
						who = [0, 10000]
						await alliancewar(message)
				else:
						i = 0
						while i < len(who):
								if who[i] == '-':
										who = [int(''.join(who[:i])), int(''.join(who[i + 1:]))]
										break
								i += 1

						await alliancewar(message)
				return

		if content == ('&liberty'):
				await wheretosend.send(quote)
				quotecount += 1
				if quotecount == len(quotes):
						quotecount = 0
				return

		if content == ('&MMR') or content == ('&MMR all'):
				await MMR(message, 'all')

		if content == ('&MMR me'):
				name = message.author.id
				try:
						user = await client.fetch_user(name)
				except Exception:
						return
				try:
						player = pnwkit.nation_query({"discord": str(user)}, "id")[0]
				except Exception:
						await wheretosend.send(
								f"You don't seem to have discord attached to your nation.\nGo to https://politicsandwar.com/nation/edit/  and add your actual discord profile: {user}"
						)
						return

				player = list(str(player))
				del player[:9]
				player = ''.join(player)
				await MMR(message, player)
				return

		if content.startswith('&stats'):
				user = ''.join(list(content)[7:])
				print(user)
				try:
						player = pnwkit.nation_query({"discord": str(user)}, "id")[0]
				except Exception:
						await wheretosend.send(
								f"{user} doesn't seem to have discord attached to their nation."
						)
						return

				player = list(str(player))
				del player[:9]
				player = ''.join(player)
				await stats(message, player, user)
				return

		if content == ('&MMR soldier all'):
				person = message.author.id
				try:
						user = await client.fetch_user(person)
				except Exception:
						return

				if str(user) != 'NightSoldat#9332' and str(
								user) != 'TheBearOfJare#2866' and str(
										user) != 'The Descendant#6672' and str(
												user) != 'Azrael#5827' and str(
														user) != 'Indigo#9882' and str(
																user) != 'Luke S#3588' and str(
																		user) != 'LeiaHair#0925':
						await wheretosend.send(
								"You don't have permission to use this command.")
						return
				await soldierMMR(message, 'all')

		if content == ('&MMR soldier'):
				name = message.author.id
				try:
						user = await client.fetch_user(name)
				except Exception:
						return
				try:
						player = pnwkit.nation_query({"discord": str(user)}, "id")[0]
				except Exception:
						await wheretosend.send(
								f"You don't seem to have discord attached to your nation.\nGo to https://politicsandwar.com/nation/edit/  and add your actual discord profile: {user}"
						)
						return

				player = list(str(player))
				del player[:9]
				player = ''.join(player)
				await soldierMMR(message, player)
				return

		if content == ('&alert MMR'):
				person = message.author.id
				try:
						user = await client.fetch_user(person)
				except Exception:
						return

				if str(user) != 'NightSoldat#9332' and str(
								user) != 'TheBearOfJare#2866' and str(
										user) != 'The Descendant#6672' and str(
												user) != 'Azrael#5827' and str(
														user) != 'Indigo#9882' and str(
																user) != 'Luke S#3588' and str(
																		user) != 'LeiaHair#0925':
						await wheretosend.send("You don't have permission to use this command.")
						return
				
				alert = True
				await MMR(message, 'all')
				return

		if content == ('&def wars'):
				nations = requests.get(
				f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{
		nations(alliance_id: 6215 first:500) {{
						data {{
								color
								id
								alliance_position
								wars {{
										reason
										def_id
										att_id
								turns_left
								def_resistance
										att_resistance
										def_peace
										att_peace
								}}
						}}
				}}
		}}''').json()['data']['nations']['data']
				
				for nation in nations:
						for war in nation['wars']:
								reason = war['reason'].lower()
								if war['def_id'] != nation['id'] or war['def_peace'] == True or war['att_peace'] == True or war['def_resistance'] <= 0 or war['att_resistance'] <= 0 or war['turns_left'] <= 0 or nation['alliance_position'] == 'APPLICANT' or 'counter' in reason:
										continue
								else:
										await wheretosend.send(f"SoL member https://politicsandwar.com/nation/id={nation['id']} is under attack by https://politicsandwar.com/nation/id={war['att_id']}.")
										
				return
				
		if content == ('&embassy'):
				name = message.author.id
				try:
						user = await client.fetch_user(name)
				except Exception:
						return
				try:
						player = pnwkit.nation_query({"discord": str(user)}, "id")[0]
				except Exception:
						await wheretosend.send(
								f"You don't seem to have discord attached to your nation.\nGo to https://politicsandwar.com/nation/edit/  and add your actual discord profile: {user}"
						)
						return

				player = list(str(player))
				del player[:9]
				player = ''.join(player)

				player = requests.get(f'''https://api.politicsandwar.com/graphql?api_key={key}&query={{nations(id: {player}){{data{{alliance{{name}}}}}}}}''').json()['data']['nations']['data'][0]['alliance']['name']
				server = message.guild
				
				#await client.create_channel(server, f'{player}', type=discord.ChannelType.text)
				#az = await client.fetch_user("Azrael#5827")
				over = {user: discord.PermissionOverwrite(read_messages=True),
								#az: discord.PermissionOverwrite(read_messages=True),
								server.default_role: discord.PermissionOverwrite(read_messages=False)
								}
				cat = discord.utils.get(server.categories, name="EMBASSIES")
				channel = await server.create_text_channel(f'{player}', overwrites = over, catagory = cat)
				
				role = discord.utils.get(server.roles, name="Foreign Diplomat")
				await message.author.add_roles(role)
				
				await wheretosend.send(f'Created the Embassy "{player}". REMINDER: inactive embassies may be deleted after extended periods of neglect.')

		if content.startswith('&warchest'):
				name = message.author.id
				try:
						user = await client.fetch_user(name)
				except Exception:
						return
				try:
						player = pnwkit.nation_query({"discord": str(user)}, "id")[0]
				except Exception:
						await wheretosend.send(
								f"You don't seem to have discord attached to your nation.\nGo to https://politicsandwar.com/nation/edit/  and add your actual discord profile: {user}"
						)
						return

				player = list(str(player))
				del player[:9]
				player = ''.join(player)
				
				if content == '&warchest':
						nation = requests.get(f'''https://api.politicsandwar.com/graphql?api_key=32b01c4ce92661&query={{
														nations(id: {player}){{
																data{{
																		nation_name
																		num_cities
																		steel
																aluminum
																		gasoline
																		munitions
																		food
																		uranium}}
														}}
}}''').json()['data']['nations']['data'][0]
						steel = nation['steel']
						aluminum = nation['aluminum']
						gasoline = nation['gasoline']
						munitions = nation['munitions']
						food = nation['food']
						uranium = nation['uranium']
						
						cities = nation['num_cities']
						
						try:
							await wheretosend.send(f"{nation['nation_name']} has:\n```{steel} steel - {round(steel/(cities*15),2)}% of required\n{aluminum} aluminum - {round(aluminum/(cities*15),2)}% of required\n{gasoline} gas - {round(gasoline/(cities*20),2)}% of required\n{munitions} munitions - {round(munitions/(cities*20),2)}% of required\n{food} food - {round(food/(cities*100),2)}% of required\n{uranium} uranium - {round(uranium/(cities*2),2)}% of required\n```")
						except Exception:
							await wheretosend.send('HmmMmMMm... something went **very** wrong.')
				else:
						user = ''.join(list(content)[10:])
						print(user)
						try:
								player = pnwkit.nation_query({"discord": str(user)}, "id")[0]
						except Exception:
								await wheretosend.send(
										f"{user} doesn't seem to have discord attached to their nation."
								)
								return
		
						player = list(str(player))
						del player[:9]
						player = ''.join(player)
						
						nation = requests.get(f'''https://api.politicsandwar.com/graphql?api_key=32b01c4ce92661&query={{
														nations(id: {player}){{
																data{{
																		nation_name
																		num_cities
																		steel
																aluminum
																		gasoline
																		munitions
																		food
																		uranium}}
														}}
}}''').json()['data']['nations']['data'][0]
						steel = nation['steel']
						aluminum = nation['aluminum']
						gasoline = nation['gasoline']
						munitions = nation['munitions']
						food = nation['food']
						uranium = nation['uranium']
						
						cities = nation['num_cities']

						try:
							await wheretosend.send(f"{nation['nation_name']} has:\n```{steel} steel - {round(steel/(cities*15),2)}% of required\n{aluminum} aluminum - {round(aluminum/(cities*15),2)}% of required\n{gasoline} gas - {round(gasoline/(cities*20),2)}% of required\n{munitions} munitions - {round(munitions/(cities*20),2)}% of required\n{food} food - {round(food/(cities*100),2)}% of required\n{uranium} uranium - {round(uranium/(cities*2),2)}% of required\n```")
						except Exception:
							await wheretosend.send('HmmMmMMm... something went **very** wrong.')


		if content.startswith('&deposit'):
			person = message.author.id
			try:
				user = await client.fetch_user(person)
			except Exception:
				return
			syntax = message.content[9:].split(' ')
			amount = syntax[0]
			resource = syntax[1]
			try:
				userkey = db[f'{user} key']
				failed = False
			except Exception:
				await wheretosend.send(f"You need to enable whitelisted acess to use this command. I sent you the instructions just now (unless you have DM's disabled)")
				await user.send("To use the deposit command you need to enable whitelisted acess, found in the api section of the account page in politics in war. You also need to verify you api key, which enables liberty bot to make the deposit in your name. Deposits can only be made with the API to your alliance bank so don't worry about others being able to steel your stuff, and you can check your bank recs to see that its legit.\nuse `&verify apikey123456` to verify your key (do this in this DM, NOT in a public server). Whitelisted access must be done manualy in-game.")
				failed = True
			if failed == True:
				return

			try:
				print(requests.get(f'''https://api.politicsandwar.com/graphql?api_key={'51f2058772e1cb'}&query=mutation{{bankDeposit({resource}:{amount}) {{date}}}}''', headers = {"X-Bot-Key": "2553f9d9a60208e2", "X-Api-Key": f"{userkey}"}).json()['data']['bankDeposit']['date'])
				await wheretosend.send(f'Sucessfully deposited {amount} {resource}.\n<@!710965782640721982>')
			except Exception:
				await wheretosend.send('Syntax error: a correct usage of &deposit would look like\n`&deposit 20 food`')
	
		if content == ('?liberty'):
				await wheretosend.send(
						'```\nCommands:\n&liberty - generates a nice quote about liberty and freedom\n```'
				)
keep_alive()
client.run('OTU4NDAzMzg3NTI1ODUzMzA0.GF9QZk.Fc0LDGdmQH6d1SWtIQBANTvQA-xffFIBbYWvXA')
